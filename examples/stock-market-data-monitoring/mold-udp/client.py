import socket
import struct
import threading

MCAST_IP = 'localhost'
MCAST_PORT = 5555

RETR_IP = 'localhost'
RETR_PORT = 7777

RETR_ADDR=(RETR_IP,RETR_PORT)

def unpack_messages(data):
    blocks = data
    messages = []
    
    while len(blocks)!=0:
        l = struct.unpack('!H',blocks[:2])[0]
        blocks = blocks[2:]
        messages.append(blocks[:l])
        blocks = blocks[l:]
    
    return messages



s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto(b'HELLO',RETR_ADDR)

next_id = 1
while True:
    print('NEXT SHOULD BE',next_id)
    data, addr = s.recvfrom(1024)
    _, seq_id, count = struct.unpack('!10sQH',data[:20])
    
    # ask retransmission if neccessaire
    if seq_id>next_id:
        s.sendto(struct.pack('!10sQH',b'testdata  ',next_id,seq_id-next_id),RETR_ADDR)

    # print received messages
    messages = unpack_messages(data[20:])
    for i,msg in enumerate(messages):
        print('#',seq_id+i,msg)

    # adjust expected next id
    if seq_id>=next_id:
        next_id = seq_id + count

    print()
