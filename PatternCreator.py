#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 18:53:37 2019

@author: zoekahana
"""

from PIL import Image
from ColorKdTree import ColorKdTree
from Color import Color
import numpy as np
from scipy.cluster.vq import kmeans,vq

# Class for manipulating images to create patterns.
class PatternCreator:
    
    ''' Creates a new image handler.
    Constructor arguments:
    :param filepath: the filepath where the image is located.
    '''
    def __init__(self, filepath):
        
        # The image filepath.
        self.filepath = filepath
        
        # The original image.
        self.orig_im = Image.open(filepath).convert("RGB")
    
    ''' Creates a cross-stitch pattern from the original image.
    Method arguments:
    :param width: the desired width in number of stitches
    :param brand: the brand of thread colors to use.
    :param max_colors: the maximum number of colors to be used in the result.
    Returns the image converted into a pattern.
    '''
    def create_pattern(self, width, brand, max_colors = 200):

        # Resize the image to the desired width.
        resized = self.resize_image(self.orig_im, width)
        resized.show()
        
        # Reduce the number of colors to no more than the specified maximum.
        reduced = self.reduce_colors(resized, max_colors)
        
        reduced.show()
        
        # Recolor the reduced image with the available colors from the brand.
        recolored = self.recolor_image(reduced, "DMC")
        
        print("colors used:", len(recolored.getcolors()))
        
        recolored.show()
        # Return the recolored image.
        return recolored
        
        
    ''' Resizes an image.
    Method arguments:
    :param img: the image to be resized.
    :param width: the width to resize to.
    Returns the resized image.
    '''
    def resize_image(self, img, width):
        
        # Get the current height-to-width ratio.
        curr_width, curr_height = img.size
        ratio = curr_height / curr_width
        
        # Find the resizing height based on the ratio.
        height = int(width * ratio)
        
        # Return the resized image.
        return img.resize((width, height))
    
    ''' Reduces the number of colors in an image.
    Method arguments:
    :param img: the image to be color-reduced.
    :param max_colors: the maximum number of colors allowed in the result.
    Returns the image with no more than max_colors colors.
    '''
    def reduce_colors(self, img, max_colors):
        
        # Convert the image into a pixel array and normalize values to [0, 1].
        img = np.array(img) / 255
        
        # Obtain the width and height of the image.
        width = img.shape[0]
        height = img.shape[1]

        # Reshape the array of pixels.
        pixels = np.reshape(img, (width * height, 3)).astype(float)

        # Perform the clustering and quantization using k-means.
        centroids, _ = kmeans(pixels, max_colors)
        quant, _ = vq(pixels, centroids)

        # Reshape the result of the quantization to a 2D array.
        centers_idx = np.reshape(quant, (width, height))

        # Create a pixel array from the centroids.        
        clustered = centroids[centers_idx]

        # Create an image from the clustered pixel array.
        reduced = Image.fromarray((clustered * 255).astype(np.uint8), "RGB")
        
        # Return the reduced image.
        return reduced
    
    ''' Recolors an image using thread colors from a given brand.
    Method arguments:
    :param img: the image to be recolored.
    :param thread_brand: the brand of thread colors to use.
    Returns the recolored image.
    '''
    def recolor_image(self, img, thread_brand):
        
        # A mapping of colors seen in the image to their nearest neighbor.
        colors_seen = {}
        
        # A list of the colors used in the final image.
        colors_used = []
        
        # Construct a KD-tree of colors based on the thread brand.
        if thread_brand == "DMC":
            color_tree = ColorKdTree("DMC.txt")
        elif thread_brand == "test":
            color_tree = ColorKdTree("test.txt")
        
        # Obtain the width and height of the image.
        width = img.width
        height = img.height
        
        # Create a new image to fill with the new colors.
        new_image = Image.new("RGB", (width, height))
        
        # Load the old and new images as pixel arrays.
        old_pixels = img.load()
        new_pixels = new_image.load()

        # Loop through the pixels in the old image.
        for col in range(width):
            for row in range(height):
                
                # Obtain the RGB values of the old image.
                r, g, b  = old_pixels[col, row]
                color = Color(r, g, b)
                
                # Obtain new color if color has been seen before.
                if color.rgb in colors_seen:
                    new_color = colors_seen[color.rgb]
                    
                # If color hasn't been seen before, find nearest neighbor and
                # add it to the mapping.
                else:
                    new_color = color_tree.nearest_neighbor(color).color
                    colors_seen[color.rgb] = new_color
                    
                    # If new color has not been used before, add to list.
                    if new_color.rgb not in colors_used:
                        colors_used.append(new_color.rgb)
                    
                # Color the correct pixel in the new image with the new color.
                new_r, new_g, new_b = new_color.rgb
                new_pixels[col, row] = (new_r, new_g, new_b)
      
        # Return the recolored image.
        return new_image
        
# Main method.
if __name__ == '__main__':
    test = PatternCreator("/Users/zoekahana/Downloads/dsotm.png")
    test.create_pattern(175, "DMC", 100)
