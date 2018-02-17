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
#from scipy import ndimage

img=mpimg.imread('purple_flower.jpg')
# img: [height, width, RGB]

def pixelate(original, rows, columns, r_calc, c_calc):

    '''
    Function to pixelate the image using average RGB color of a block of pixels
    Pixel size of image must be divisible by the number of rows and columns
    i.e. size of original = (rows * r_calc, columns * c_calc)
    '''

    # reshape works as follows:
    # (final # rows, rows to calculate final rows, final # columns, 
    #                                      columns to calculate final columns)
    new = original.reshape(rows,r_calc,columns,c_calc)
    color_result = new.mean(axis=3).mean(axis=1)
    return color_result

def plt_image_components(full_color, reds, blues, greens, aspect_ratio):

    # Plot the original image and image broken up into RGB components
    fig = plt.figure()
    ax1 = fig.add_subplot(221)  # top left
    ax1 = plt.imshow(full_color, aspect=aspect_ratio, interpolation='nearest')
    ax2 = fig.add_subplot(222)  # top right
    ax2 = plt.imshow(reds, aspect=aspect_ratio, cmap='Reds', 
                     interpolation='nearest', vmin=0, vmax=256)
    plt.colorbar(ax2)
    ax3 = fig.add_subplot(223)  # bottom left
    ax3 = plt.imshow(greens, aspect=aspect_ratio, cmap='Greens', 
                     interpolation='nearest', vmin=0, vmax=256)
    plt.colorbar(ax3)
    ax4 = fig.add_subplot(224)  # bottom right
    ax4 = plt.imshow(blues, cmap='Blues', aspect=aspect_ratio, 
                     interpolation='nearest', vmin=0, vmax=256)
    plt.colorbar(ax4)
    
def unique_colors(array_to_test):
    
    long_dimension = np.shape(array_to_test)[0] * np.shape(array_to_test)[1]
    a = np.unique(array_to_test.reshape(long_dimension, 3), axis=0)
    uniques = np.size(a, axis=0)
    return uniques


# Get the aspect ratio of the original image
aspect_ratio = np.shape(img)[0] / np.shape(img)[1]
# Eventually this is read in from the user?
width = 80    # In mm
height = aspect_ratio * width   # mm

# Delicas size 11/0
bead_size_w = 1.6   # mm
bead_size_h = 1.3   # mm

# Calculate how many beads will be used in both dimensions
beads_w = int(width / bead_size_w)      # beads
beads_h = int(height / bead_size_h)     # beads
bead_aspect = beads_h/beads_w

# Actual dimensions of final product
final_width = beads_w * bead_size_w     # mm
final_height = beads_h * bead_size_h    # mm

# Calculate how many pixels will be averaged into each bead
pixels_w = int(np.shape(img)[1] / beads_w)
pixels_h = int(np.shape(img)[0] / beads_h)

# For now, just cutting pixels that aren't a multiple of the number of beads
o_reds = img[:,:,0]
small_reds = o_reds[0:pixels_h * beads_h, 0:pixels_w * beads_w]
o_greens = img[:,:,1]
small_greens = o_greens[0:pixels_h * beads_h, 0:pixels_w * beads_w]
o_blues = img[:,:,2]
small_blues = o_blues[0:pixels_h * beads_h, 0:pixels_w * beads_w]

r_result = pixelate(small_reds, beads_h, beads_w, pixels_h, pixels_w)
g_result = pixelate(small_greens, beads_h, beads_w, pixels_h, pixels_w)
b_result = pixelate(small_blues, beads_h, beads_w, pixels_h, pixels_w)

# Final result needs to be in uint8 type to plot correctly
final_result = np.stack([r_result, g_result, b_result], 
                        axis=2).astype(np.uint8)

#plt_image_components(img, img[:,:,0], img[:,:,1], img[:,:,2], 1)
#plt_image_components(final_result, r_result, g_result, b_result, bead_aspect)
#colors_original = unique_colors(img)
#colors_new = unique_colors(final_result)
#
#print("New number of unique colors:", colors_original)
#print("New number of unique colors:", colors_new)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Simple case to test out (4x4)
#test_reds = np.array([[82, 0, 82, 82],[82, 82, 82, 79],
#             [82, 82, 82, 47],[82, 90, 82, 82]])
#test_greens = np.array([[179, 0, 136, 136],[179, 39, 179,180],
#               [179, 179, 179, 229],[179, 200, 179, 179]])
#test_blues = np.array([[243, 0, 44, 44],[243, 243, 243, 52],
#              [243, 243, 102, 47],[243, 39, 243, 243]])
#test = np.stack([test_reds, test_greens, test_blues], axis=2).astype(np.uint8)
#
#r_test_result = pixelate(test_reds, 2, 2, 2, 2)      # Tested variations: 
#g_test_result = pixelate(test_greens, 2, 2, 2, 2)    # (2,2,2,2), (1,1,4,4), 
#b_test_result = pixelate(test_blues, 2, 2, 2, 2)     # (1,2,4,2)
#a_r = 2/2
#
#test_result = np.stack([r_test_result, g_test_result, b_test_result], 
#                       axis=2).astype(np.uint8)

#~~~~~~
# More complicated case (5x5)
test_reds = np.array([[82,79,79,0,82],[47,82,82,90,82],[79,82,82,0,79],
                      [82,79,79,79,90],[82,82,82,82,82]])
test_greens = np.array([[179,180,180,0,136],[229,39,179,200,136],
               [180,39,179,0,180],[136,180,180,180,200],[39,39,179,136,179]])
test_blues = np.array([[102,52,52,0,44],[47,243,102,39,44],
              [52,243,243,0,52],[44,52,52,52,39],[243,243,243,44,243]])
test = np.stack([test_reds, test_greens, test_blues], axis=2).astype(np.uint8)
a_r = (5/2)/(5/3)

one = np.array([82, 179, 243])
two = np.array([0, 0, 0])
three = np.array([82, 136, 44])
four = np.array([79, 180, 52])
five = np.array([82, 39, 243])
six = np.array([47, 229, 47])
seven = np.array([82, 179, 102])
eight = np.array([90, 200, 39])

# One way to calculate, using correct proportions of areas in average
#area = (1+2/3) * 2.5
#one_one = (seven + six + (2/3)*four + (2/3)*five + (1/2)*four + 
#           (2/3)*(1/2)*five) / area
#one_two = (seven + four + (1/3)*four + (1/3)*five + (1/2)*(1/3)*five + 
#           0.5*one + (1/3)*two + (1/3)*eight + (1/3)*(1/2)*two) / area
#one_three = (three + three + (2/3)*two + (2/3)*eight + (1/2)*four + 
#             (2/3)*(1/2)*two) / area
#two_one = (three + five + (1/2)*four + (1/2)*(2/3)*five + (2/3)*four + 
#           (2/3)*five) / area
#two_two = (four + one + (1/3)*five + (1/3)*four + (1/3)*three + (1/3)*four + 
#           (1/3)*(1/2)*five + (1/3)*(1/2)*two) /  area
#two_three = (eight + one + (2/3)*three + (2/3)*four + (1/2)*four + 
#             (2/3)*(1/2)*two) / area
#
#new = np.stack([one_one, one_two, one_three, two_one, two_two, two_three],
#                    axis=1)

# Another way to calculate, taking all pixels included in bead as equal average
# This should allow for not needing to drop any pixels
zero_zero = (seven + four + six + five + four + five) / 6
one_zero = (four + five + five + four + seven + one + two + eight + two) / 9
two_zero = (two + eight + two + three + three + four) / 6
zero_one = (four + three + five + five + four + five) / 6
one_one = (five + four + five + one + four + one + two + four + three) / 9
two_one = (two + four + three + four + eight + one) / 6
new = np.stack([zero_zero, one_zero, two_zero, zero_one, one_one, two_one],
               axis=1)

r_test_result = np.reshape(new[0],[2,3])
g_test_result = np.reshape(new[1],[2,3])
b_test_result = np.reshape(new[2],[2,3])

test_result = np.stack([r_test_result, g_test_result, b_test_result], 
                       axis=2).astype(np.uint8)

#~~~~~

plt_image_components(test, test_reds, test_greens, test_blues, 1)
plt_image_components(test_result, r_test_result, g_test_result, 
                     b_test_result, a_r)
    
test_colors_original = unique_colors(test)
test_colors_new = unique_colors(test_result)
print("New number of unique colors:", test_colors_original)
print("New number of unique colors:", test_colors_new)


