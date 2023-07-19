# i wrote this code like 2 years ago and told chatgpt
# to rewrite it using opencv instead of pillow

import cv2
import numpy as np
import colorsys
import os

# ACTUAL CODE

HEIGHT = 30

dir = './ddlc-decompiled/images.rpa/images/'
outDir = './output.txt'

frames = {}
frs = {}

for subdir, dirs, files in os.walk(dir):
    for file in files:
        img = cv2.imread(os.path.join(subdir, file))
        width, height, _ = img.shape
        ratio = height / width
        img = cv2.resize(img, (int(HEIGHT * ratio), HEIGHT), interpolation=cv2.INTER_AREA)
        width, height, _ = img.shape
        frames[file] = {
            "image": img,
            "width": width,
            "height": height,
        }

for f in frames.keys():
    print(f)
    frs[f] = []
    width, height = frames[f]["width"], frames[f]["height"]
    for x in range(width):
        frs[f].append([])
        for y in range(height):
            b, g, r = frames[f]["image"][x][y]
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            if v > 8:
                frs[f][x].append([int(h*360), int(round(s, 3)*1000), int(round(v/255, 3)*1000)])
            else:
                frs[f][x].append([])
    print(f, " objects:", width*height, " h:", width, " w:", height)

with open(outDir, 'w') as f:
    f.write(str(frs).replace("'", '"').replace(" ", ""))
