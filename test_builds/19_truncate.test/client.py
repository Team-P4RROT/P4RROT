import socket
import struct

server_addr = ('192.168.11.1',5555)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    a = int(input('a (uint32_t)> '))
    op = input('op ("+" or "-")> ')
    b = int(input('b (uint32_t)> '))

    s.sendto(struct.Struct('!IIB').pack(a,b,ord(op[0])),server_addr)
    r,_ = s.recvfrom(256)
    r = struct.Struct('!I').unpack(r)[0]
    print('Result:',r)
    print()
