# i wrote this code like 2 years ago and told chatgpt
# to rewrite it using opencv instead of pillow

import cv2
import colorsys
import os
import json

# ACTUAL CODE

HEIGHT = 38 # changing this will cause white lines where the images get cut off pls fix this

allowed_files = None
try:
    with open('./req_images.txt', 'r') as file:
        allowed_files = json.load(file)
except FileNotFoundError:
    print("req_images.txt doesnt exist, using all images instead.")


# we exclude folders because spwn is slow as fuck with more than hundreds of kb in memory
excluded_folders = ["cg", "menu", "poem_special", "stab", "bar", "button", "mouse", "overlay", "phone", "poemgame", "scrollbar", "slider"]

dir = './ddlc-decompiled/images.rpa'
outDir = './output.txt'

width, height = 0, 0
frames = {}
frs = {}

def read_img(subdir, file):
    global HEIGHT
    for i in excluded_folders:
        if i in subdir.replace(dir+os.sep, "").replace("\\", "/").split("/"): return
    
    dir_slash_file = subdir.replace(dir+os.sep, "").replace("\\", "/").replace("images/", "")+"/"+file

    if allowed_files != None and dir_slash_file not in allowed_files: return

    img = cv2.imread(os.path.join(subdir, file), cv2.IMREAD_UNCHANGED)
    width, height, _ = img.shape
    ratio = height / width
    img = cv2.resize(img, (int(HEIGHT * ratio), HEIGHT), interpolation=cv2.INTER_AREA)
    width, height, _ = img.shape

    if file == "splash.png": # make the splash text go bye-bye so we can replace it later in gd
        x_start, y_start = 460, 460
        x_end, y_end = 840, 590
        mask = img.copy()
        mask[y_start:y_end, x_start:x_end, 3] = 0
        img = cv2.copyTo(img, mask)

    frames[dir_slash_file] = img

print("reading images...")
for subdir, dirs, files in os.walk(dir):
    for file in files:
        read_img(subdir, file)



print("converting...")
for f in frames.keys():
    height, width, channels = frames[f].shape
    frs[f] = {"res": [height, width], "image": []}
    objects = 0

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
                objects += 1
                frs[f]["image"][x].append([int(h*360), int(round(s, 3)*999), int(round(v/255, 3)*999)])
            else:
                frs[f]["image"][x].append([])

    print(f, " objects:", objects, " h:", height, " w:", width)


with open(outDir, 'w') as f:
    f.write(str(frs).replace("'", '"').replace(" ", ""))
