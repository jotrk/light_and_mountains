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
w_dir = argv[1]

# img dir
i_dir = argv[2]

# web thumb dir
t_dir = argv[3]

# img suffix, .e.g. png
suffix = argv[4]

images = argv[5:]

img_data = []

idx = 0

for image in images:
    i = basename(image)
    t = i.replace('.' + suffix, '_b.' + suffix)

    metadata = GExiv2.Metadata(i_dir + sep + i)

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

    img = Image.open(i_dir + sep + i)

    i_width = img.size[0]
    i_height = img.size[1]

    img.close()

    img = Image.open(t_dir + sep + t)

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
            , 'w_dir': w_dir
            , 't_dir': t_dir
            , 'i_width': i_width
            , 'i_height': i_height
            , 't_width': t_width
            , 't_height': t_height
            , 'exif': exif
            }
        )

    idx = idx + 1

print(dumps(img_data))