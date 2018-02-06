#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 14:01:23 2018

Bead Pattern Maker

Imports an image with which to generate a pixelated version for beading 
different styles of seed bead stitches

"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy import ndimage

img=mpimg.imread('purple_flower.jpg')
# img: [height, width, RGB]
#imgplot = plt.imshow(img)

# Plot the original image and broken up into RGB components
fig = plt.figure()
ax1 = fig.add_subplot(221)  # top left
ax1 = plt.imshow(img)
ax2 = fig.add_subplot(222)  # top right
ax2 = plt.imshow(img[:,:,0],cmap='Reds')
plt.colorbar()
ax3 = fig.add_subplot(223)  # bottom left
ax3 = plt.imshow(img[:,:,1],cmap='Greens')
plt.colorbar()
ax4 = fig.add_subplot(224)  # bottom right
ax4 = plt.imshow(img[:,:,2],cmap='Blues')
plt.colorbar()

#https://matplotlib.org/examples/color/colormaps_reference.html

# Get the aspect ratio of the original image
aspect_ratio = np.shape(img)[0] / np.shape(img)[1]
# Eventually this is read in from the user?
width = 80    # In mm
height = aspect_ratio * width

#https://www.shipwreckbeads.com/support/docs/SeedBeadTable
# Delicas 11/0
bead_size_w = 1.6   # mm
bead_size_h = 1.3   # mm

# Calculate how many beads will be used in both dimensions
beads_w = int(width / bead_size_w)
beads_h = int(height / bead_size_h)
bead_aspect = beads_h/beads_w
# Actual dimensions of final product
final_width = beads_w * bead_size_w
final_height = beads_h * bead_size_h

# Calculate how many pixels will be averaged into each bead
pixels_w = int(np.shape(img)[1] / beads_w)
pixels_h = int(np.shape(img)[0] / beads_h)

#fig = plt.figure()
#plt.imshow(img, interpolation="nearest")

# For now, just cutting pixels that aren't a multiple of the number of beads
o_reds = img[:,:,0]
small_reds = o_reds[0:pixels_h * beads_h, 0:pixels_w * beads_w]
o_greens = img[:,:,1]
small_greens = o_greens[0:pixels_h * beads_h, 0:pixels_w * beads_w]
o_blues = img[:,:,2]
small_blues = o_blues[0:pixels_h * beads_h, 0:pixels_w * beads_w]
# Turn into a function
reds_view = small_reds.reshape(beads_h, pixels_h, beads_w, pixels_w)
r_result = reds_view.mean(axis=3).mean(axis=1)
greens_view = small_greens.reshape(beads_h, pixels_h, beads_w, pixels_w)
g_result = greens_view.mean(axis=3).mean(axis=1)
blues_view = small_blues.reshape(beads_h, pixels_h, beads_w, pixels_w)
b_result = blues_view.mean(axis=3).mean(axis=1)

# Final result needs to be in uint8 type to plot correctly
final_result = np.stack([r_result, g_result, b_result], 
                        axis=2).astype(np.uint8)

fig = plt.figure()
ax1 = fig.add_subplot(221)  # top left
ax1 = plt.imshow(r_result, cmap='Reds', interpolation='nearest', 
                 aspect=bead_aspect)
plt.colorbar()
ax2 = fig.add_subplot(222)  # top right
ax2 = plt.imshow(g_result, cmap='Greens', interpolation='nearest', 
                 aspect=bead_aspect)
plt.colorbar()
ax3 = fig.add_subplot(223)  # bottom left
ax3 = plt.imshow(b_result, cmap='Blues', interpolation='nearest', 
                 aspect=bead_aspect)
plt.colorbar()
ax4 = fig.add_subplot(224)  # bottom right
ax4 = plt.imshow(final_result, interpolation='nearest', aspect=bead_aspect)




# Simple case to test out
test_reds = np.array([[82, 0, 82, 82],[82, 82, 82, 79],
             [82, 82, 82, 47],[82, 90, 82, 82]])
test_greens = np.array([[179, 0, 136, 136],[179, 39, 179,180],
               [179, 179, 179, 229],[179, 200, 179, 179]])
test_blues = np.array([[243, 0, 44, 44],[243, 243, 243, 52],
              [243, 243, 102, 47],[243, 39, 243, 243]])

def pixelate(original, rows, columns, r_calc, c_calc):
    
    # reshape works as follows:
    # (final # rows, rows to calculate final rows, final # columns, 
    #                                      columns to calculate final columns)
    new = original.reshape(rows,r_calc,columns,c_calc)
    
    color_result = new.mean(axis=3).mean(axis=1)
    
    return color_result

r_result = pixelate(test_reds, 1, 2, 4, 2)      # Alternates: 
g_result = pixelate(test_greens, 1, 2, 4, 2)    # (2,2,2,2), (1,1,4,4)
b_result = pixelate(test_blues, 1, 2, 4, 2)

test_result = np.stack([r_result, g_result, b_result], axis=2).astype(np.uint8)

fig = plt.figure()
ax1 = fig.add_subplot(221)  # top left
ax1 = plt.imshow(test_reds,cmap='Reds',interpolation='nearest')
plt.colorbar()
ax2 = fig.add_subplot(222)  # top right
ax2 = plt.imshow(test_greens, cmap='Greens', interpolation="nearest")
plt.colorbar()
ax3 = fig.add_subplot(223)  # bottom left
ax3 = plt.imshow(test_blues, cmap='Blues', interpolation="nearest")
plt.colorbar()
ax4 = fig.add_subplot(224)  # bottom right
ax4 = plt.imshow(test_result, interpolation="nearest")
#plt.colorbar()
    

