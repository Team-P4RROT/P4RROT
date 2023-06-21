import pytest
import shutil
import os
import subprocess
import logging
import sys
from psa_ebpf_tools.ProjectSetupHelper import ProjectSetupHelper as PSH
from typing import Optional



# paths ##
PSA_TEST_DIR = os.path.join(os.path.dirname(__file__), "psa_ebpf")
PSA_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates", "p4_psa_ebpf_template")
##########




class TestPSACompilation:
    test_dirs = [os.path.join(PSA_TEST_DIR, cmd_dir_n) for cmd_dir_n in os.listdir(PSA_TEST_DIR)]

    logger = logging.getLogger(__name__)
    psh = PSH()

    def setup_test_dir(self, test_dir: str):
        test_subdir = os.path.join(test_dir, "template")
        os.makedirs(test_subdir, exist_ok=True)
        for fn in os.listdir(PSA_TEMPLATE_DIR):
            fp = os.path.join(PSA_TEMPLATE_DIR, fn)
            if os.path.isdir(fp):
                continue
            if not fp.endswith(".p4"):
                continue
            shutil.copy(fp, test_subdir)

    def build_template_in_test_build_dir(self, test_dir: str):
        prev_wd = os.getcwd()
        os.chdir(test_dir)
        res = subprocess.run(["python3", "codegen.py"])
        assert res.returncode == 0, res.stderr
        res = subprocess.run(["p4c-ebpf", "--arch", "psa", "-o", "main.c", "./template/main.p4"])
        assert res.returncode == 0, f"error msg: {res.stderr} normal output: {res.stdout}"
        res = subprocess.run(["clang", "-O2", "-g", "-c", "-DBTF", "-emit-llvm", "-o", "main.bc", "main.c"])
        assert res.returncode == 0
        res = subprocess.run(["llc", "-march=bpf", "-mcpu=generic", "-filetype=obj", "-o", "main.o", "main.bc"])
        assert res.returncode == 0
        os.chdir(prev_wd)

    def dynamic_test(self, test_dir: str):
        self.psh.setup_two_host_connection_template(os.path.join(test_dir, "main.o"))
        self.psh.start_nc_server()
        input("Server should be up now. press enter to kill it?")
        self.psh.stop_nc_server()



    @pytest.mark.parametrize("test_dir_path", test_dirs)
    def test_build_command(self, test_dir_path: str):
        try:
            self.psh.clean()
        except:
            pass
        self.logger.info("setting up the test dir")
        print(f"test_dir_path: {test_dir_path}")
        self.setup_test_dir(test_dir_path)
        self.logger.info("build...")
        self.build_template_in_test_build_dir(test_dir_path)
        self.dynamic_test(test_dir_path)
