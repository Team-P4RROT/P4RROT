import socket
import struct

server_addr = ('192.168.11.1',5555)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    op = input('operation (a(dd) / c(heck))> ')
    x = int(input('value (uint32_t)> '))

    s.sendto(struct.Struct('!BI').pack(ord(op[0]),x),server_addr)
    r,_ = s.recvfrom(256)
    r_res = struct.Struct('!??').unpack(r)[0]
    r_err = struct.Struct('!??').unpack(r)[1]
    print('Result:',r_res)
    print('Error:',r_err)
    print()
