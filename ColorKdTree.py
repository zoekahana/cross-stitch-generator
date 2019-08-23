#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 17:36:14 2019

@author: zoekahana
"""

import json
from Color import Color
from ColorNode import ColorNode

# Class for creating a KD-Tree of ColorNodes.
class ColorKdTree:
    
    ''' Dictionary mapping dimension number to RGB color. '''
    dim_to_rgb = {
            0: 'r',
            1: 'g',
            2: 'b'
            }
    
    ''' Creates a new Color Kd Tree from a JSON file of colors. 
    Constructor arguments:
    :param filepath: the filepath of a JSON file containing color objects.
    '''
    def __init__(self, filepath):
        
        # The dimension of the tree.
        self.max_dim = 3
        
        # Obtain list of colors from JSON file.
        with open(filepath) as json_file:
            colors = json.load(json_file)['colors']
            
        # Construct the tree from the list of colors and store the root.
        self.root = self.build_tree(colors, 0)
        
        
    ''' Constructs a tree from a list of colors.
    Method arguments:
    :param colors: a list of colors to be inserted.
    :param curr_dim: the current dimension being sorted by.
    Returns the root node of the tree.
    '''
    def build_tree(self, colors, curr_dim):
    
        # Return None if there are no more colors to insert.
        if len(colors) == 0:
            return None
        
        # Find the correct level to sort by.
        level = ColorKdTree.dim_to_rgb[curr_dim]
        
        # Sort the colors based on the correct color level.
        colors = sorted(colors, key = lambda c: c['rgb'][level])
        
        # Obtain the median color.
        mid = int(len(colors) / 2)
        median_color = colors[mid]
        
        # Set the current node to the median color.
        node = ColorNode(median_color)
        
        # Recurse through the left and right halves of the array.
        node.left = self.build_tree(colors[:mid], self.inc_dim(curr_dim))
        node.right = self.build_tree(colors[mid + 1:], self.inc_dim(curr_dim))
        
        # Return the node.
        return node
    
    ''' Increments dimension by one, wrapping back to 0 if needed.
    Method arguments:
    :param dim: the dimension to be incremented.
    Returns the incremented dimension.
    '''
    def inc_dim(self, dim):
        return (dim + 1) % self.max_dim
    
    ''' Finds the nearest neighbor to a given color.
    Method arguments:
    :param color: the color to find a nearest neighbor for.
    Returns the nearest neighbor as a color node.
    '''
    def nearest_neighbor(self, color):
        best_col, best_dis = self.nns(color, self.root, 0, float('inf'), None)
        return best_col
    
    ''' Recursive method for nearest neighbor search.
    Method arguments:
    :param color: the color to find a nearest neighbor for.
    :param curr_node: the node currently being evaluated as a neighbor.
    :param curr_dim: the current dimension.
    :param best_dis: the smallest distance found thus far.
    :param best_col: the closest neighbor thus far as a color node.
    Returns the nearest color neighbor as a color node and the distance.
    '''
    def nns(self, color, curr_node, curr_dim, best_dis, best_col):
        
        # Return the current best distance and color if node is None.
        if curr_node is None:
            return best_col, best_dis
     
        # Find the distance to the current color node.
        distance = color.sq_dist_to(curr_node.color)
        
        # Update the best distance and best color if necessary.
        if distance < best_dis:
            best_dis = distance
            best_col = curr_node
            
        # Determine whether to search left or right subtree first.
        curr_level = ColorKdTree.dim_to_rgb[curr_dim]
        if color.rgb[curr_level] < curr_node.color.rgb[curr_level]:
            search_first = curr_node.left
            search_second = curr_node.right
        else:
            search_first = curr_node.right
            search_second = curr_node.left
            
        # Check the branch closer to the query color.
        best_col, best_dis = self.nns(color, search_first, self.inc_dim(curr_dim), \
                            best_dis, best_col)
        
        # Check the branch further away from the query color if it could
        # contain a closer point.
        if (self.should_check_branch(color, curr_node, curr_dim, best_dis)):
            best_col, best_dis = self.nns(color, search_second, self.inc_dim(curr_dim), \
                            best_dis, best_col) 
        
        # Return the current closest color and current closest distance.
        return best_col, best_dis
    
    ''' Evaluates whether a branch could contain a closer neighbor.
    Method arguments:
    :param color: the color to find a nearest neighbor for.
    :param node: the parent node of the branch being checked.
    :param dim: the dimension to be checked on.
    :param best_dis: the current closest distance.
    Returns whether the tree branch should be checked for a neighbor.
    '''
    def should_check_branch(self, color, node, dim, best_dis):
        
        # Return false if the node is None.
        if node is None:
            return False
        
        # Find the color level corresponding to the dimension.
        level = ColorKdTree.dim_to_rgb[dim]
        
        # Only check branch if it could contain a closer point on that plane.
        return (color.rgb[level] - node.color.rgb[level]) ** 2 < best_dis
        
    ''' Prints color names in a tree in level-order for debugging. '''
    def iterate(self):
        
        # Queue for storing nodes throughout traversal.
        queue = []
        
        # Begin with the root.
        queue.append(self.root)
        
        # Add nodes in level order until there are none left.
        while (len(queue) != 0):
            currColor = queue.pop(0)
            print(currColor)
            
            # Add children to queue if they exist.
            if (currColor.left is not None):
                queue.append(currColor.left)
            if (currColor.right is not None):
                queue.append(currColor.right)
  
    
if __name__ == '__main__':
    tree = ColorKdTree("DMC.txt")
    tree.iterate()
    print()
    best_col = tree.nearest_neighbor(Color(0, 0, 100))
    print("nearest neighbor is", best_col)