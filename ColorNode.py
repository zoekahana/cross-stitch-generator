#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 18:09:08 2019

@author: zoekahana
"""

from Color import Color

# Class for storing a color as a node in a kd-tree.
class ColorNode:
    
    ''' Creates a new color node from a color object.
    Constructor arguments:
    :param color: information about a color read in from a JSON file.
    '''        
    def __init__(self, color):
        
        # The color, indicated by RGB values.
        self.color = Color(\
                           color['rgb']['r'], \
                           color['rgb']['g'], \
                           color['rgb']['b'] \
                           ) 
        
        # The color's name.
        self.name = color['name']
        
        # The color's brand.
        self.brand = color['brand']
        
        # The identifying code used by the color's brand.
        self.code = color['code']
        
        # The node's left and right children.
        self.left = None
        self.right = None
        
    ''' Formats node for printing.
    '''
    def __str__(self):
        return self.name + " " + self.color.__str__()