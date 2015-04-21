#!/usr/bin/env python3

import sys
from PIL import Image
import matplotlib.pyplot as plt
import random
from itertools import product

# Usage: ./imgrand <input> <percentage> <output>
if len(sys.argv) < 4:
	print("Usage: %s <input> <percentage> <output>" % sys.argv[0])
	print("\te.g.: %s lena.bmp 95 lena_rand_95.bmp" % sys.argv[0])
	sys.exit()

random.seed()

# Open image
im = Image.open(sys.argv[1])

# Get pixels' RGB values
rgb_im = im.convert('RGB')
pixels = rgb_im.load()

total = float(sys.argv[2])/100 * rgb_im.size[0]*rgb_im.size[1]

# Go through all pixels until having modified 'total' pixels
for x, y in product(range(0,rgb_im.size[0]), range(0,rgb_im.size[1])):

	(r, g, b) = pixels[x,y]
			
	if random.randint(0,1) == 0: 
		r = r & 0xFE
		g = g & 0xFE
		b = b & 0xFE
	else:
		r = r | 0x01
		g = g | 0x01
		b = b | 0x01

	pixels[x, y] = (r, g, b)

	total = total - 1
	if total == 0: 
		break

rgb_im.save(sys.argv[3])	
