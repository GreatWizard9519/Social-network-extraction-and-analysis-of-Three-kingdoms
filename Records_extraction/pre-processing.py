#预处理

import re
import os
import pandas as pd
import numpy as np



#删除header 注释 断词
with open('sanguozhi1.txt','w+') as f_new:
    with open('sanguozhi.txt','r+') as f:

        for line in f.readlines():
            #删除headers
            if 'Records of the Three Kingdoms' in line:
                line = line.replace(line,'')
            #删除注释
            if re.match(r'[ ]*\d{0,4}[.]{1}[ ]{1}.*', line, re.I | re.M):
                line = line.replace(line,'')
            #连接断词
            if '- ' in line:
                line = line.replace('- ','')
            f_new.write(line)


