#! /bin/bash
TARGET_DIR="./template"

cp -r ../../../templates/p4_psa_ebpf_template/* ${TARGET_DIR}

python3 codegen.py

p4c-ebpf --arch psa -o main.c $TARGET_DIR/main.p4
clang -O2 -g -c -DBTF -emit-llvm -o main.bc main.c
llc -march=bpf -mcpu=generic -filetype=obj -o main.o main.bc