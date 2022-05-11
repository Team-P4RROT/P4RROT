import socket
import struct

server_addr = ('10.0.0.1',5555)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

for i in range(0, 1000, 2):
    s.sendto(struct.Struct('!BI').pack(ord('a'),i),server_addr)
    r,_ = s.recvfrom(256)
    r_res = struct.Struct('!??').unpack(r)[0]
    r_err = struct.Struct('!??').unpack(r)[1]
    print('added ' + str(i))

correct_positive = 0
correct_negative = 0
false_positive = 0
false_negative = 0

for i in range(0, 1000):
    s.sendto(struct.Struct('!BI').pack(ord('c'),i),server_addr)
    r,_ = s.recvfrom(256)
    r_res = struct.Struct('!??').unpack(r)[0]
    r_err = struct.Struct('!??').unpack(r)[1]
    print('checked ' + str(i))
    if (r_res == 1):
        if (i % 2 == 0):
            correct_positive += 1
        else:
            false_positive += 1
    else:
        if (i % 2 == 0):
            false_negative += 1
        else:
            correct_negative += 1

print('Identified as positive: ' + str(correct_positive + false_positive))
print('  Correct positive: ' + str(correct_positive))
print('  False positive: ' + str(false_positive))
print('Identified as negative: ' + str(correct_negative + false_negative))
print('  Correct negative: ' + str(correct_negative))
print('  False negative: ' + str(false_negative))
