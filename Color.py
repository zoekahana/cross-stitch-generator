#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 21:50:20 2019

@author: zoekahana
"""

# Class for storing colors as RGB values.
class Color:
    
    ''' Creates a new Color object.
    Constructor arguments:
    :param r: the color's red level.
    :param g: the color's green level.
    :param b: the color's blue level.
    '''
    def __init__(self, r, g, b):
        
        # A tuple holding the color's RGB values.
        self.rgb = (r, g, b)
        
    ''' Checks for equivalence between two colors.
    Method arguments:
    :param color: the color being checked for equivalence.
    Returns whether or not the colors have the same RGB values.
    '''
    def __eq__(self, color):
        return self.rgb == color.rgb
        
    def get_level(self, key):
        
        # Unpack the RGB values.
        r, g, b = self.rgb
        
        # Returnr the correct value depending on the key.
        if key == 'r':
            return r
        if key == 'g':
            return g
        if key == 'b':
            return b
    
    ''' Computes the squared distance between a color node and a given color.
    Method arguments:
    :param color: the comparative color.
    Returns the squared distance between the color and the given color.
    '''
    def sq_dist_to(self, color):
        
        # Unpack the RGB values.
        r1, g1, b1 = self.rgb
        r2, g2, b2 = color.rgb
        
        return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2
        
               
               
    ''' Formats color for printing.
    '''
    def __str__(self):
        r, g, b = self.rgb
        return '(' + str(r) + ", " + str(g) + ", " + str(b) + ")"