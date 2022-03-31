#!/usr/bin/python3
import zlib

#print(hex(zlib.crc32(bytearray(0x1)) ))
#exit()


#known material name
#chr(0x4)
s = b'bg18_central_shop_window_1' #bg05_yuka_minasoko_add
print(s)
#known hash (little-endian readed)
req_res = 0xb4d09529  #

known_initial = [
#    (1, 0xb840207), #4
    (2,  0x65e3626d), # 00 02
    (3, 0x5cd1d97d),
    # no 3, 4 
    (5,  0x0b840636), # obj12 obj13 obj44
    (6,  0x50b362ef), # 00_spc 01_spc obj115
    (7,  0xb979a551), # csl_nml non_add non_spc
    (8,  0x101b2f58), # csl_body break_RR
    (9,  0xce3f7ab5), # skin00_EE obj44_spc obj13_spc
    (10, 0x51f4535b), # skirt00_EE
    (11, 0x25391b1c), # height00_EE ef_scroll10
    (12, 0x59a3c798), # wetbura00_EE bura00_00_EE clothes00_EE
    (13, 0x1f90f357), # skin00_nml_EE pants00_00_EE
    (14, 0x451a44fb), # skirt00_nml_EE
    (15, 0xca72f004), # skirt00_brk0_EE skirt00_brk1_EE swim_blend00_EE
    (16, 0xc758f1c7), # bura00_00_nml_EE clothes00_nml_EE clothes00_wet_EE pl11_weapon02_EE
    (17, 0x8033134c), # acce_body03_00_EE clothes00_brk0_EE clothes00_brk1_EE pants00_00_nml_EE
    (18, 0x591ee6a1), # pl34_eye_tensin_EE  0x90a7ddc8), # bg05_yuka_minasoko
    #no 19
    (20, 0xd9cf5811), # pl11_weapon02_nml_EE
    (21, 0x1668a9da), # richacce_head08_00_EE  acce_body03_00_nml_EE clothes00_brk1_wet_EE 
    (22, 0x0b0cfaef), # pl34_eye_tensin_nml_EE ###bg05_yuka_minasoko_spc
    (23, 0xd84fa8fe), # tex_brkct_obj37_snowman
    #no 23, 24
    (25, 0x5448a65f), # richacce_head08_00_nml_EE 
]

print('looking CRC32 initial for:', s, 'and', hex(req_res))

for tst in known_initial:
    res = zlib.crc32(s, tst[1]) 
    if res == req_res:
        print('found known len:"', tst[0], '" initial: ', hex(tst[1]))
        exit()
#exit()

print('not found, try to brute..')
#'''
def brute_range(start, finish):
    for i in range(start, finish):
        result = zlib.crc32(s, i)
        if result == req_res:
            print ('your initial is: ', hex(i) )
            return True    

for prc in range(0x100):
    print(hex(prc), '%')
    if brute_range(prc*0x1000000 , (prc+1)*0x1000000):
        print('success!!')
        break
    if prc == 0xff:
        print("failure")
print('done')


