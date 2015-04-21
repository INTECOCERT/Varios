#!/usr/bin/env python

import sys
from PIL import Image
import matplotlib.pyplot as plt
from scipy import stats

# Usage: ./imgchi2 <input>
if len(sys.argv) < 4:
	print("Usage: %s <input>" % sys.argv[0])
	print("\te.g.: %s lena.bmp" % sys.argv[0])
	sys.exit()

# If an element within the list is less than 4, merge it with the following one
def unify(l):
	
	ul = []
	m = 5
	for i in range(0, len(l)-1):
	
		if l[i] < 4:
			l[i+1] = l[i] + l[i+1]

		if l[i] >= 4:
			ul.append(l[i])
			if l[i] < m: m = len(ul)-1

	# If odd, delete the least frequent index
	if len(ul) % 2 != 0:
		del ul[m]

	return ul

def expected(l): 

	expected = []

	for i in range(0, len(l)-1, 2):
		expected.append((l[i]+l[i+1])/2)

	return expected

def chitest(l):

	ul = unify(l)

	# Prepare data for Chi square statistic
	ul_even = ul[::2]
	e = expected(ul)

	# Run Chi square test
	chi, p = stats.chisquare(ul_even, e, 0)

	return chi, p

# Open image
im = Image.open(sys.argv[1])
rgb_im = im.convert('RGB')

# Get the histogram
hist = rgb_im.histogram()

rchi, rp = chitest(hist[0:255])
gchi, gp = chitest(hist[256:511])
bchi, bp = chitest(hist[512:768])

print("R: %.6f" % rp)
print("G: %.6f" % gp)
print("B: %.6f" % bp)
