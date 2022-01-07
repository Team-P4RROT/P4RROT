import socket
import struct
import sys

server_addr = (sys.argv[1],5555)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

print('Find x!')

while True:
    guess = int(input('guess (uint8_t)> '))

    s.sendto(struct.Struct('!B').pack(guess),server_addr)
    
    r,_ = s.recvfrom(256)
    r = struct.Struct('2s').unpack(r)[0].decode('utf-8')
    
    print('Result:',r)
    print()
