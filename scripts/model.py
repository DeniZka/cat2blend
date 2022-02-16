'''
#HEADER ----------------
h_tmd0 = '' # 0x00 hader
h_p1 = '' #0x04 bytesX12
h_floats = [] # 0x10 floatsX6
h_size = 0  #0x28 header size from 'tdm0' 0xe0 and larger
#ADDRESSES -----------------
            #UNKNOWN zeros
a_OPs = 0   #0x40 uint64 address of .`.@ pattern
a_CSB = 0   #0x48 uint64 address of CSB0 pattern
a_flx2 = 0  #0x50 uint64 address of .....? double floats
a_u0 = 0    #0x58 UNKNOWN
a_u1 = 0    #0x60 UNKNOWN cursor.cat got!
a_vgrps = 0 #0x68 uint64 address of vertex groups
a_faces = 0 #0x70 uint64 address of faces 
a_RRpat = 0 #0x78 uint64 address of RR pattern
a_u2    = 0 #0x80 UNKNOWN
a_FFpat = 0 #0x88 uint64 address of 0xFF pattern
a_verts = 0 #0x90 uint64 address of vertices and their stuff
            #0x98 UNKNOWN
            #0xA0 UNKNOWN
#COUNTERS
c_andU = 0  #0xa8 xxxx&U. (repeat of starts min 0x5e0 or 0x610 (len 0x38) then trunk
            #0xac unknown
            #0xb0 unknown
c_OPs = 0   #0xb4 (byteX2 length .`.0.. pattern) trunk
c_CSB0 = 0  #0xb8 or BGS0 (len 0x14) trunk
c_flx2 = 0  #0xbc pairs of floats 0x00000000 0x00000000 trunk
c_btxt = 0  #0xc0 bytes count INF BRK and other
c_uin2 = 0  #0xc4 8xbyte data count
c_vgrps = 0 #0xc8 vertex groups count aka d807 pattern
c_faces = 0 #0xCC trinagle count  uint32
c_RRpat = 0 #0xD0 count of pattern with RR        (FIXME: could be swapped with FF)
c_u1 = 0    #0xD4 (only zeros found) RESERVED???
c_FFpat = 0 #0xD8 count of pattern with 0xFF at    (FIXME: could be swapped with RR)
c_verts = 0 #0xDC vertex count  uint32
# EXTRA DATA
# unknown additional info
a_bl1s = 0  #0xe0 start address of CSB0 data pattern
a_bl1f = 0  #0xe8 finish assress of CSB0 data
a_bl2s = 0  #0xf0 start address unt64?
a_bl2f = 0  #0xf8 stop address of block
            #0xd0 block size???
c_tnsx = 0  #0x100 count of 0x10 bytes (data is after variable c_uin2)
c_btsx = 0  #0x104 (if applicable by size) array of bytes before d807 trunk

#END HEADER


d807 = 2008 #pre tri counting pattern uint32,D8,07,XX XX XX XX XX XX XX XX XX XX
# pattern xxx&U.. size 0x38
pat1 = 0 #patternt .`.0.. size 0x6
# read 8 byte (zeros)
# patternt xxxxBGS0...    size 0x14
# pattern  xxxxxxA...?...?    size 0x28
c_string = 1 #FIXME somewhere in header string count may be 2
'''


from struct import unpack

#Model header class
class Modelh:
    def __init__(self, f, offset):
        self.f = f
        self.offset = offset
        self.valid = False
        self.len = 0
        self.have_bones = False
        
        #move to offset
        if self.f.tell() != self.offset:
            self.f.seek(self.offset, 0)
            
        #check valid
        h_tmd0 = f.read(4).decode('ascii')        
        if h_tmd0 == 'tmd0':
            self.valid = True
            
        #skip 2 byte
        f.seek(2, 1)
        #check ability
        self.type1 = unpack('<B', self.f.read(1))[0]
        self.type2 = unpack('<B', self.f.read(1))[0]
        print("HEADER TYPE: ", hex(self.type1), hex(self.type2))
        self.check_ability()
        if self.vblk_len == 0:
            self.valid = False
            print("ERROR: UNSUPPORTED HEADER")    
            return
        
        
        #check self size
        self.f.seek(self.offset + 0x28, 0)
        self.len = unpack('<I', self.f.read(4))[0]
        print("HEADER SIZE", hex(self.len))
        if self.len < 0xE0:
            self.valid = False
            print("ERROR: UNSUPPORTED (SMALLER) HEADER")
            return
        
        #read known part
        self.f.seek(self.offset + 0x68, 0)
        self.vgrp_adr, self.face_adr = unpack('<QQ', self.f.read(8*2))
        self.f.seek(self.offset + 0x90, 0)
        self.vert_adr = unpack('<Q', self.f.read(8*1))[0]
                
        #read face (vertex) goups and face count
        self.f.seek(self.offset + 0xc8, 0)
        self.vgrp_cnt, self.face_cnt = unpack('<II', self.f.read(4*2))
        #read vertex count
        self.f.seek(self.offset + 0xdc, 0)
        self.vert_cnt = unpack('<I', self.f.read(4*1))[0]
        
        
        if self.have_bones:
            self.f.seek(self.offset + 0xE0, 0)
            self.rig_adr, self.rigb_adr, self.bones_adr, self.bonesh_adr = unpack('<QQQQ', self.f.read(8*4))
            self.rig_cnt, self.rigb_cnt, self.bones_cnt, self.bonesh_cnt = unpack('<IIII', self.f.read(4*4))
    

    
    def check_ability(self):
        #FIXME: find the different - smaller then 0x18 (header E0) !!!
        self.vblk_len = 0
        if (self.type2 & 0b0101_0000) == 0b0101_0000:  #0x5X
            self.vblk_len = 0x18 #0x97 0x50
                    
        if (self.type2 & 0b0111_0100) == 0b0111_0100: #0x74:
            print("seems there are weights and bones")
            self.vblk_len += 0x8 #0x97 0x74
            self.have_bones = True

        self.face_len = 2            
        if (self.type2 & 0b0000_1000) == 0b0000_1000: #0xX8 mask of face index size
            self.face_len = 4

        if (self.type1 & 0b0000_1111) == 0b0000_1111: #0xXF
            self.vblk_len += 0x8
        
        self.uv_cnt = 1 #FIXME: COULD BE DIFFERENT IN SMALLER HEADERS
        if (self.type1 & 0b0010_0000) == 0b0010_0000: #0xBX
            self.vblk_len += 0x4 #additional uvs
            self.uv_cnt += 1
        
        if (self.type1 & 0b0100_0000) == 0b0100_0000: #0xFX
            self.vblk_len += 0x4 #additional uvs
            self.uv_cnt += 1
            


