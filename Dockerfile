FROM osinstom/nikss:latest
USER root
RUN apt update
RUN apt upgrade -y
RUN apt install python3-pip tcpdump net-tools netcat -y
RUN pip3 install python-dotenv
RUN ulimit -l 1024
COPY requirements_dev.txt .
RUN pip3 install -r requirements_dev.txt
CMD /bin/bash -c "mount bpffs /sys/fs/bpf -t bpf"; /bin/bash

