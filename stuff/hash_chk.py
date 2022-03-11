#!/usr/bin/python3
import zlib
# clothes00_EE,
# clothes00_nml_EE,
# skin00_EE,
# skin00_nml_EE

# clothes00_outline_EE,
# cloth_fragment

dds_name = 'clothes00_outline_EE'

known_initial = {
    2:  0x65e3626d, # 00 02
    # no 3, 4 
    5:  0x0b840636, # obj12 obj13 obj44
    6:  0x50b362ef, # 00_spc 01_spc obj115
    7:  0xb979a551, # csl_nml non_add non_spc
    8:  0x101b2f58, # csl_body break_RR
    9:  0xce3f7ab5, # skin00_EE obj44_spc obj13_spc
    10: 0x51f4535b, # skirt00_EE
    11: 0x25391b1c, # height00_EE ef_scroll10
    12: 0x59a3c798, # wetbura00_EE bura00_00_EE clothes00_EE
    13: 0x1f90f357, # skin00_nml_EE pants00_00_EE
    14: 0x451a44fb, # skirt00_nml_EE
    15: 0xca72f004, # skirt00_brk0_EE skirt00_brk1_EE swim_blend00_EE
    16: 0xc758f1c7, # bura00_00_nml_EE clothes00_nml_EE clothes00_wet_EE pl11_weapon02_EE
    17: 0x8033134c, # acce_body03_00_EE clothes00_brk0_EE clothes00_brk1_EE pants00_00_nml_EE
    18: 0x90a7ddc8, # bg05_yuka_minasoko
    #no 19
    20: 0xd9cf5811, # pl11_weapon02_nml_EE
    21: 0x1668a9da, # richacce_head08_00_EE  acce_body03_00_nml_EE clothes00_brk1_wet_EE 
    22: 0x3eb8768a, # bg05_yuka_minasoko_spc
    #no 23, 24
    25: 0x5448a65f, # richacce_head08_00_nml_EE 
}
print("image name:", dds_name)
dl = len(dds_name)
print("Img name len:", dl)
seed = known_initial[dl]
print("Img seed:", hex(seed))
res = zlib.crc32(bytearray(dds_name.encode('ascii')), seed ) 
print("Your hash:", hex(res))






exit()

import sys
a = bytearray('zako01_00_EE'.encode('ascii'))
print(a)
crc = 0x04C11DB7
for x in a:
    crc ^= x << 24;
    for k in range(8):
        crc = (crc << 1) ^ 0x04c11db7 if crc & 0x80000000 else crc << 1
crc = ~crc
crc &= 0xffffffff
print(hex(crc))
exit()





sl = ['obj18', 'obj18,', "obj18,\r\n" ]
ss = [0x2fcb0d79, 0x790dcb2f]
for c in range(0xffffff):
    for s in sl:
        h = 0
        for c in s:
            h = h * c + ord(c)
#        if 

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

















