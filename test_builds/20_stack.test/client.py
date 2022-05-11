import socket
import struct

server_addr = ('192.168.11.1',5555)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    a = int(input('a (uint32_t)> '))
    aa = int(input('aa (uint32_t)> '))

    s.sendto(struct.Struct('!II').pack(a,aa),server_addr)
    r,_ = s.recvfrom(256)
    r1 = struct.Struct('!II').unpack(r)[0]
    r2 = struct.Struct('!II').unpack(r)[1]
    print('Result1:',r1)
    print('Result2:',r2)
    print()
