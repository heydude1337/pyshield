# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 09:06:55 2015

Functions to find point of intersection and angle of intersection between
two lines
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import random

#number of significant digits (rounding)
SIG_DIGITS = 6

def sci_round(x, sig = SIG_DIGITS):
    """Scientific rounding
       
       x:                 float to be rounded
       sig = SIG_DIGITS:  Number of significant digits """
           
    if x==0:  # special case, prevent taking log of zero
        return x
    else:    # round
        return round(x, sig-int(math.floor(math.log10(abs(x))))-1)
        
def intersect_line(L0, L2):
  """ calculates the intersects of two lines
  
      L0 and L1: Lines specified by ((x0, y0), (x1, y1))
       
      function returns the coordinataes of the intersection between both lines (px, py)    
      function returns an empty tuple if no intersection is found
      function returns (NaN, NaN) if lines are parallel
  """

  # unwrap lines
  x1=L0[0][0]
  x2=L0[1][0]
  x3=L2[0][0]
  x4=L2[1][0]
  
  y1=L0[0][1]
  y2=L0[1][1]
  y3=L2[0][1]
  y4=L2[1][1]
  
  
  #calculate denominator
  s1_x = x2 - x1
  s1_y = y2 - y1
  
  s2_x = x4-x3
  s2_y = y4-y3

  den = (-s2_x * s1_y + s1_x * s2_y)
  
  
  # if denominator is zero lines are parallel return NaN
  if sci_round(den) == 0:
      return (np.NAN, np.NAN)
  
  # parameterize line 
  s = (-s1_y * (x1 - x3) + s1_x * (y1 - y3)) / den;
  t = ( s2_x * (y1 - y3) - s2_y * (x1 - x3)) / den;
 
  # check if intersection lies on line pieces
  if (s >= 0) & (s <= 1) & (t >= 0) & (t <= 1):
      # calculate the intersection and return        
      i_x = x1 + (t * s1_x);
      i_y = y1 + (t * s1_y);
      
      return (sci_round(i_x), sci_round(i_y))
    

  return (None, None)

def angle_between_lines(L0, L1):
    """ Angle in radians between two lines 
    
        L0 and L1: Lines specified by ((x0, y0), (x1, y1))
        
        Even if both lines don't intersect the angle is returned.
    """
    angle1 = line_angle(L0)
    angle2 = line_angle(L1)
    return sci_round(abs(angle2-angle1))
 
def line_angle(L):
    """ Angle in radians between a line and the x-axis
    
        L = ((x0, y0), (x1, y1)) is a line defined by two points
       
       """
        
    #define vector direction
    v0=abs(L[1]-L[0])
    v1=[0, 1]
    
    #normalize vectors
    n0=v0/np.linalg.norm(v0)
    n1=v1/np.linalg.norm(v1)
    
    #prevent rounding errors, acos returns an error for values > 1
    inprod = sci_round(np.inner(n0, n1))

    #calculate angles
    angle = math.acos(inprod)
    
    return sci_round(angle)
    
    
def intersect_lines(lines):
    """ Calculate all intersections of a  list of lines 
    
        lines:  A list of lines. Each line is defined by two points
                line = ((x0, y0), (x1, y1))"""
        
    intersect=[]    
    for i in range(0, len(lines)):
        for j in range(i+1, len(lines)):
            p=intersect_line(lines[i], lines[j])
            if not(None in p):
              if (not(np.any(np.isnan(p)))):
                intersect.append(p)
                
    return tuple(intersect)

def plot_lines(lines):  
    """ Plot a list of lines with points of intersection 
    
        lines:  A list of lines. Each line is defined by two points
                line = ((x0, y0), (x1, y1))"""    
                             
    for line in lines:
        plt.plot(line[:,0], line[:,1])
        
    intersects = intersect_lines(lines)
    for intersect in intersects:
        plt.plot(*intersect, ' ro' )
    return


#def point_distance(p, L):
#   """ Calculate all intersections of a  list of lines 
#    
#        lines:  A list of lines. Each line is defined by two points
#                line = ((x0, y0), (x1, y1))"""
#  x0=p[0]
#  y0=p[1]
#  x1=L[0][0]
#  x2=L[1][0]
# 
#  
#  y1=L[0][1]
#  y2=L[1][1]
# 
#  
#  d = abs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1) / math.sqrt((y2-y1)**2+(x2-x1)**2)
#  return d
#  

def rand_line(bounds=((0,0),(1,1))):
    """ Return a random line 
        
         bounds: ((xmin, ymin), (xmax, ymax)) the line must be within these
                  bounds."""
    return np.array((rand_point(bounds), rand_point(bounds)))
    
  
def rand_point(bounds=((0,0), (1,1))):
    """ Return a random point.
    
        bounds:  ((xmin, ymin), (xmax, ymax)) the line point be within these
                  bounds.""" 
    xi = random.random() * (bounds[1][0]-bounds[0][0]) + bounds[0][0]
    yi = random.random() * (bounds[1][0]-bounds[0][0]) + bounds[0][0]
    return (xi, yi)


if __name__ == "__main__":
    # testing
    nlines = 10
    bounds = ((-10, -10), (10, 10))

    lines=[rand_line(bounds) for i in range(0,nlines)]
    
    
    
    plot_lines(lines)





