from PIL import ImageFont

import sys

picdir = sys.path[0] + '/pic/'

def generate_font_by(size) :
    return ImageFont.truetype(picdir + 'Font.ttc', size)

def font_size_58() :
    return generate_font_by(size=58)

def font_size_35() :
    return generate_font_by(size=35)

def font_size_32() :
    return generate_font_by(size=32)

def font_size_28() :
    return generate_font_by(size=28)

def font_size_22() :
    return generate_font_by(size=22)

def font_size_12() :
    return generate_font_by(size=12)
