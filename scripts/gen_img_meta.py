#!/usr/bin/env python3

from sys import argv
from os.path import basename, sep
from PIL import Image
from json import dumps
from jinja2 import Template

import gi
gi.require_version('GExiv2', '0.10')
from gi.repository import GExiv2

# web dir
W_DIR = argv[1]

# img dir
I_DIR = argv[2]

# web thumb dir
T_DIR = argv[3]

# img suffix, .e.g. png
SUFFIX = argv[4]

IMAGES = argv[5:]

img_data = []

idx = 0

for image in IMAGES:
    i = basename(image)
    t = i.replace('.' + SUFFIX, '_t.' + SUFFIX)

    metadata = GExiv2.Metadata(I_DIR + sep + i)

    try:
        title = metadata['Xmp.dc.title'].replace('lang="x-default" ', '')
    except:
        title = None

    try:
        caption = metadata['Exif.Image.ImageDescription']
    except:
        caption = None

    try:
        rating = metadata['Xmp.xmp.Rating']
    except:
        rating = None

    img = Image.open(I_DIR + sep + i)

    i_width = img.size[0]
    i_height = img.size[1]

    img.close()

    img = Image.open(T_DIR + sep + t)

    t_width = img.size[0]
    t_height = img.size[1]

    exif = { 'title': title
           , 'caption': caption
           , 'rating': rating
           }

    img_data.append(
            { 'idx': idx
            , 'i': i
            , 't': t
            , 'w_dir': W_DIR
            , 't_dir': T_DIR
            , 'i_width': i_width
            , 'i_height': i_height
            , 'i_aspect': i_width / i_height
            , 't_width': t_width
            , 't_height': t_height
            , 't_aspect': t_width / t_height
            , 'exif': exif
            }
        )

    idx = idx + 1

print(dumps(img_data))
