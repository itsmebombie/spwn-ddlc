# i wrote this code like 2 years ago and told chatgpt
# to rewrite it using opencv instead of pillow

import cv2
import colorsys
import os

# ACTUAL CODE

HEIGHT = 32

# allowed_files = ["class.png", "club.png", "corridor.png", "residential.png"]

# we exclude folders because spwn is slow as fuck with more than hundreds of kb in memory
excluded_folders = ["cg", "menu", "poem_special", "stab"]

dir = './ddlc-decompiled/images.rpa/images'
outDir = './output.txt'

width, height = 0, 0
frames = {}
frs = {}

for subdir, dirs, files in os.walk(dir):
    for file in files:
        # if file not in allowed_files: continue

        # rhat the hell, this is supposed to exclude folders
        continue_loop = False
        for i in excluded_folders:
            if i in subdir.replace(dir+os.sep, "").replace("\\", "/").split("/"): continue_loop = True; break 
        if continue_loop: continue

        img = cv2.imread(os.path.join(subdir, file), cv2.IMREAD_UNCHANGED)
        width, height, _ = img.shape
        ratio = height / width
        img = cv2.resize(img, (int(HEIGHT * ratio), HEIGHT), interpolation=cv2.INTER_AREA)
        width, height, _ = img.shape
        frames[subdir.replace(dir+os.sep, "").replace("\\", "/")+"/"+file] = img

for f in frames.keys():
    height, width, channels = frames[f].shape
    frs[f] = {"res": [height, width], "image": []}

    for x in range(height):
        frs[f]["image"].append([])
        for y in range(width):
            b, g, r, a = 0, 0, 0, 0

            # lmao good code
            if channels == 4: b, g, r, a = frames[f][x][y]
            elif channels == 3: 
                b, g, r = frames[f][x][y]
                a = 255
            
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            if a > 127:
                frs[f]["image"][x].append([int(h*360), int(round(s, 3)*999), int(round(v/255, 3)*999)])
            else:
                frs[f]["image"][x].append([])

    print(f, " objects:", width*height, " h:", height, " w:", width)


with open(outDir, 'w') as f:
    f.write(str(frs).replace("'", '"').replace(" ", ""))
