# -*- coding:utf-8 -*-

import sys

from PIL import Image

images = ['01d','02d','03d','04d','09d','10d','11d','13d', '50d']

for name in images :
    im = Image.open(sys.path[0] + '/pic/' + name + '.png')
    x,y = im.size 
    try: 
        #  Use white to fill the background
        # (alpha band as paste mask). 
        p = Image.new('RGBA', im.size, (255,255,255))
        p.paste(im, (0, 0, x, y), im)
        p.save(sys.path[0] + '/pic/' + name + '.png')
        p.show()
    except:
        pass