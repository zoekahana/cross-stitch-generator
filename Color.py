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
        self.rgb = {'r': r, 'g': g, 'b': b}
        
    ''' Computes the squared distance between a color node and a given color.
    Method arguments:
    :param color: the comparative color.
    Returns the squared distance between the color and the given color.
    '''
    def sq_dist_to(self, color):
        return (self.rgb['r'] - color.rgb['r'])**2 + \
               (self.rgb['g'] - color.rgb['g'])**2 + \
               (self.rgb['b'] - color.rgb['b'])**2
               
    ''' Formats color for printing.
    '''
    def __str__(self):
        return '(' + str(self.rgb['r']) + ", " + str(self.rgb['g']) \
                                        + ", " + str(self.rgb['b']) + ")"