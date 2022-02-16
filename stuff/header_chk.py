from struct import unpack
import os
import os.path
from pathlib import Path

home = '/home/user/.local/share/Steam/steamapps/common/Senran Kagura Estival Versus/GameData/Model'
#home = '/home/denis/.steam/debian-installation/steamapps/common/Senran Kagura Estival Versus/GameData/Model'

RPT = {}

result = list(Path(home).rglob("*"))
for p in result:
    if os.path.isfile(p):
        with open(p, 'rb') as f:
            s = str(p).split('GameData/')
            #check header tmd0
            f.seek(0x500, 0)
            h = unpack('<I', f.read(4))[0]
            if h == 811887988:               
                f.seek(0x506, 0)
                key = unpack('H', f.read(2))[0]
                f.seek(0x506, 0)
                xx = unpack('BB', f.read(2))            
                if not key in RPT:
                    RPT[key] = (xx, [])
                RPT[key][1].append(s[1])
            
            
with open('report.txt', 'w') as f:
    for key in RPT:
        f.write(hex(RPT[key][0][0]))
        f.write(' ')
        f.write(hex(RPT[key][0][1]))
        f.write("\n")
        for path in RPT[key][1]:
            f.write("\t")
            f.write(str(path))
            f.write("\n")

            

            
#            print(hex(xx[0]), hex(xx[1]))
