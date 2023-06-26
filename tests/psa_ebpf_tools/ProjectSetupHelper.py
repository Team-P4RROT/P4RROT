import logging
import time
import os
from dotenv import load_dotenv
import subprocess
import argparse
from typing import Optional
import json

class ProjectSetupHelper:
    def __init__(self, env_file_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)

        self.module_root_dir = os.path.dirname(os.path.abspath(__file__))
        if env_file_path is None:
            self.env_file_path = os.path.join(self.module_root_dir, "network-config.env")
        else:
            self.env_file_path = env_file_path
        load_dotenv(dotenv_path=self.env_file_path)
        self.logger.warning(f"keys: {os.environ.keys()}")
        self.logger.warning(f"env_file_path: {self.env_file_path}")

        self.host_1_ip = os.getenv("HOST_1_IP")
        self.host_1_mac = os.getenv("HOST_1_MAC")
        self.host_1_inport = os.getenv("HOST_1_INPORT")

        self.host_2_ip = os.getenv("HOST_2_IP")
        self.host_2_mac = os.getenv("HOST_2_MAC")
        self.host_2_inport = os.getenv("HOST_2_INPORT")

        assert self.host_1_ip is not None
        assert self.host_1_mac is not None
        assert self.host_1_inport is not None

        assert self.host_2_ip is not None
        assert self.host_2_mac is not None
        assert self.host_2_inport is not None

        self.ingress_table = os.getenv("INGRESS_TABLE")
        self.action_forward_to = os.getenv("ACTION_FORWARD_TO_PORT")

        self.network_id = "/var/run/netns/switch"
        self.pipe_id = 1
        self.build_dir = os.getenv("P4RROTLET_BUILD_DIR")


        self.server_process: Optional[subprocess.Popen[bytes]] = None
        self.client_process: Optional[subprocess.Popen[bytes]] = None

    
    def log_process_failure(self, res: subprocess.CompletedProcess):
        self.logger.warning(f"The infrastructure setup script failed... (ret_code: {res.returncode})")
        self.logger.warning("output:")
        self.logger.warning("stdout")
        self.logger.warning(res.stdout)
        self.logger.warning("stderr")
        self.logger.warning(res.stderr)

    def setup_infrastructure(self):
        prv_wd = os.getcwd()
        os.chdir(self.module_root_dir)
        res = subprocess.run("./setup_infrastructure.sh")
        if res.returncode != 0:
            self.log_process_failure(res)
        os.chdir(prv_wd)

    def load_template(self, template_path):
        res = subprocess.run(["nsenter", f"--net={self.network_id}", "nikss-ctl",
                              "pipeline", "load", "id", str(self.pipe_id), template_path])
        if res.returncode != 0:
            self.log_process_failure(res)
            raise Exception

    def unload_pipe(self):
        res = subprocess.run(["nikss-ctl", "pipeline", "unload", "id", str(self.pipe_id)])
        if res.returncode != 0:
            self.log_process_failure(res)
            raise Exception

    def add_port(self, device_id):
        res = subprocess.run(["nsenter", f"--net={self.network_id}", "nikss-ctl",
                              "add-port", "pipe", str(self.pipe_id), "dev", device_id])
        if res.returncode != 0:
            self.log_process_failure(res)
            raise Exception

    def add_table_entry(self, table_name, action_name, key, data):
        res = subprocess.run(["nsenter", f"--net={self.network_id}",
                              "nikss-ctl", "table", "add",
                              "pipe", str(self.pipe_id), table_name,
                              "action", "name", action_name,
                              "key", key, "data", data])
        if res.returncode != 0:
            self.log_process_failure(res)
            raise Exception

    def setup_two_host_connection_template(self, template_path):
        self.setup_infrastructure()
        self.load_template(template_path)
        self.add_port("eth0")
        self.add_port("eth1")
        self.add_table_entry(self.ingress_table, self.action_forward_to, self.host_1_inport, self.host_2_inport)
        self.add_table_entry(self.ingress_table, self.action_forward_to, self.host_2_inport, self.host_1_inport)

    def shutdown(self):
        prv_wd = os.getcwd()
        os.chdir(self.module_root_dir)
        res = subprocess.run("./clean_infrastructure.sh")
        if res.returncode != 0:
            self.log_process_failure(res)
        os.chdir(prv_wd)

    def cleanup_build_files(self, fileendings=["o", "bc", "c"], dry_run: bool = True):
        for fn in os.listdir(self.build_dir):
            if fn.split(".")[-1] in fileendings:
                fp = os.path.join(self.build_dir, fn)
                command_args = ["rm", fp]
                self.logger.info(f"command: {' '.join(command_args)}")
                if not dry_run:
                    res = subprocess.run(command_args)
                    if res.returncode != 0:
                        self.log_process_failure(res)
                        raise Exception


    def read_io_json(self, json_path):
        try:
            with open(json_path,'r') as f:
                io = json.load(f)
        except FileNotFoundError as e:
            raise

        i = io["input"]

        o = io["output"] 

        # self.logger.info(io)
        # self.logger.info(i)
        # self.logger.info(o)
        return (i, o)



    def send_dynamic_payload(self, json_path):
        try:
            inputs, outputs = self.read_io_json(json_path)
        except FileNotFoundError as e:
            print(e)
            return

        for i in range(len(inputs)):
            self.client_process = subprocess.Popen(
                ["ip", "netns", "exec", "h2", "nc", "-u", self.host_1_ip, "5555"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
            self.logger.info(f"Testing {inputs[i]}")
            try:
                outs, errs = self.client_process.communicate(f"{inputs[i]}".encode(encoding="utf-8"), timeout=1)
            except subprocess.TimeoutExpired:
                self.client_process.kill()
                outs, errs = self.client_process.communicate()

            try: 
                assert outputs[i].encode('utf-8') ==outs
            except AssertionError:
                self.logger.error(f"Expected {outputs[i].encode('utf-8')}")
                self.logger.error(f"Got {outs}")
                raise


    def start_nc_servers(self):
        if self.server_process is not None:
            self.logger.info("server process is already running")
            return

        self.server_process = subprocess.Popen(
            ["ip", "netns", "exec", "h1", "nc", "-ul", "-k", "-p", "5555"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
            )
        self.logger.info("server processes started")


    def stop_nc_servers(self):
        if self.server_process is None:
            self.logger.info("server process is already shutdown")
            return

        self.server_process.terminate()
        self.client_process.terminate()

        while self.server_process.poll() is None:
            self.logger.info("waiting on the process to be terminated...")
            time.sleep(1)

        while self.client_process.poll() is None:
            self.logger.info("waiting on the process to be terminated...")
            time.sleep(1)

        self.server_process = None
        self.server_process = None


    def clean(self):
        self.cleanup_build_files()
        self.unload_pipe()
        self.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["setup", "load_template", "clean"])
    parser.add_argument("--template_path", "-tp", required=False, type=str)
    parser.add_argument("--build_dir", "-bd", default="./template")
    parser.add_argument("--env_file", "-ef", default="network-config.env")
    args = parser.parse_args()

    psh = ProjectSetupHelper(args.env_file)
    if args.cmd == "setup":
        psh.setup_infrastructure()
    elif args.cmd == "load_template":
        if args.template_path is None:
            raise Exception("load_template need a template (specified with --template_path / -tp)")
        psh.setup_two_host_connection_template(args.template_path)
    elif args.cmd == "clean":
        psh.clean()

