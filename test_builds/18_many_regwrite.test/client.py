import socket
import struct
import sys

server_addr = (sys.argv[1],5555)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

print('A simple accumulator...')

while True:
    cmd = input('method (put/get)> ')
    if cmd[0]=='g':
        index = int(input('index (0..5)> '))
        s.sendto(struct.Struct('!III').pack(value,index,1),server_addr)
    if cmd[0]=='p':
        index = int(input('index (0..5)> '))
        value = int(input('value (uint32_t)> '))
        s.sendto(struct.Struct('!III').pack(value,index,2),server_addr)
    
    r,_ = s.recvfrom(256)
    r = struct.Struct('!I').unpack(r)[0]
    
    print('Result:',r)
    print()
