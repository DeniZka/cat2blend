sl = ['obj18', 'obj18,', "obj18,\r\n" ]
ss = [0x2fcb0d79, 0x790dcb2f]
for c in range(0xffffff)
    for s in sl:
        h = 0
        for c in s:
            h = h * c + ord(c)
        print(hex(h))

exit()




import pyhash
sl = ['obj17', 'obj17,', "obj17,\r\n" ]
ss = [0x2fcb0d79, 0x790dcb2f]
hfl = []
hfl.append(pyhash.fnv1_32)
hfl.append(pyhash.fnv1a_32)
hfl.append(pyhash.fnv1a_32)
for h in hfl:
    for s in sl:
        print(hex(h(s)))
    print('')
print('ok')
'''
h = 0
for c in str:
    h = (h << 5) + h + ord(c)
print (hex(h))


h = 0
for c in str:
    h = ord(c) + (h << 6) + (h << 16) - h
print(hex(h))


h = 0
for c in str:
    h = h + ord(c)
print(hex(h))
'''

















