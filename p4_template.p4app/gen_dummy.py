
print('state dummy{')

parser = open('a_chains.p4').read()

for line in open('a_hdrlist.p4'):
    line = line.strip()
    if line == '':
        continue
    
    handle = line.split()[1].strip(';')
    if handle in parser:
        continue

    print('\tpkt.extract(hdr.{});'.format(handle))

print('\ttransition accept;')
print('}')
