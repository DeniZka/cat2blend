#this is main module

import bpy #, bpy.data, bpy.ops, bpy.props, bpy.types, bpy.context, bpy.utils, bgl, blf, mathutils
from mathutils import *; from math import *
from struct import unpack
import os
import os.path

#kinds of offset 0x14 byte in catalog
catlog = True
CTY_MSH = 0x01 #meshes
CTY_MTL = 0x08 #matireal and bin
CTY_MAP = 0x02 #maps in level 2
CTY_MOT = 0x04 #Motion
CTY_FX  = 0x05 #Effects

class Catfile:
    def __init__(self, f, name, pos, l, ftype, parent = None):
        global catlog
        self.level = parent.level + 1
        self.f = f
        self.name = name
        self.pos = pos
        self.l = l
        self.ftype = ftype        
        self.parent = parent
        print("LVL:", self.level, " FILE:", name, " Pos:", hex(pos))
        #ACHTUNG DO NOT READ FILE ON CREATION
    #save to file
    def save(self, fn):
        print('saving: ', self.name)
        self.f.seek(self.pos, 0)
        with open(fn, 'bw') as w:
            w.write(self.f.read(self.l))
        return None
    #get file data
    def get(self, fn):
        return None #mmap.mmap(f.fileno(), l, prot=mmap.PROT_READ, access=
        
class Catcat:
    def __init__(self, f, pos = 0, parent = None):
        global catlog
        self.log = True
        self.level = 0
        if parent != None:
            self.level = parent.level + 1
        print('LVL:', self.level, ' CATALOG pos:', hex(pos))#, " CAT :", self, 'parent:', parent)
        self.parent = parent
        self.items = []
        self.f = f
        self.pos = pos
        #parse catalog block
        self.f.seek(pos + 0xC, 0)
        #print("pos: ", hex(self.pos))
        self.iter_pos = self.pos + unpack( '<I', f.read(4) )[0]
        #print("iter: ", hex(self.iter_pos))
        self.length = unpack('<I', f.read(4) )[0]
        self.cty = unpack('<I', f.read(4) )[0] #content type inside
        print("Cont.type: ", hex(self.cty))
        self.raw_count = unpack('<I', f.read(4) )[0]
        print('sub count: ', hex(self.raw_count))
        
        #parse iterator block
        self.s_item_poses = []
        self.s_item_lens = []
        f.seek( self.iter_pos + 0x14, 0 )
        print(hex(self.iter_pos))
        for i in range(self.raw_count):
            self.s_item_poses.append(self.iter_pos + unpack('<I', f.read(4) )[0] )
        for i in range(self.raw_count):
            self.s_item_lens.append(unpack('<I', f.read(4) )[0] )
        
        #check parent was not defined some cty
        if self.cty == 0x0 and self.parent and self.parent.cty != 0x0:
            if self.parent.cty == CTY_MAP:
                print("THERE ARE MAPS")
                #read names
                lst = self.get_names(self.s_item_poses[0], self.s_item_lens[0])
                print(lst)
                #read and parse complex file contains DDS
                self.f.seek(self.s_item_poses[1], 0)
                hl = unpack('<I', f.read(4) )[0] #header len (incl. header)
                dc = unpack('<I', f.read(4) )[0] #map counter
                bl = unpack('<I', f.read(4) )[0] #block len (incl. header)
                # read only cause of file shift after file creation
                das = [] #dds data addresses 
                for i in range(dc): 
                    #DDS relative addresses after header
                    das.append( self.s_item_poses[1] + hl + unpack('<I', f.read(4) )[0] )
                #recalculate lengths
                dal = [] #dds data lengths                
                for i in range(dc):
                    if i < (dc - 1):
                        dal.append( das[i+1] - das[i] )
                    else:
                    
                        dal.append( self.s_item_poses[1] + bl - das[i] )
                #print ('das ', das)
                #print ('dal ', dal)
                #Create files        
                for i in range(dc):
                    self.items.append( Catfile(self.f, lst[i], das[i], dal[i], CTY_MAP, self) )
            else:
                print("SOME ANOTHER DATA")
        elif self.cty == CTY_MSH:
            print("MESH DATA")
            #read names
            lst = self.get_names(self.s_item_poses[0], self.s_item_lens[0])
            print(lst)
            #read files
            for i in range(len(lst)):
                self.f.seek(self.s_item_poses[i+1], 0)
                self.items.append( Catfile(self.f, lst[i], self.s_item_poses[i+1], self.s_item_lens[i+1], self.cty, self) )            
        elif self.cty == CTY_MOT:
            print("MOTION DATA")
            #TODO: FINISH MOTION DATA IMPORTING
        else:
            print("JUST DIR PARSE DEEPER")
            for i in range(self.raw_count):
                self.items.append( Catcat(f, self.s_item_poses[i], self ) )

    def get_names(self, pos, l):
        lst = []
        #get names
        self.f.seek(pos, 0) #turn back
        s = self.f.read(l).decode("ascii")
        lst = s.split(",\r\n")
        if lst[-1] == '': #remove last if empty
            lst.pop()
        return lst





    


    


        


