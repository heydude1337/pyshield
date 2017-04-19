# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 09:06:55 2015

Functions to find point of intersection and angle of intersection between
two lines
"""
import math
import random
import numpy as np
import matplotlib.pyplot as plt


#number of significant digits (rounding)
SIG_DIGITS = 6

def sci_round(x, sig=SIG_DIGITS):
    """Scientific rounding

       x:                 float to be rounded
       sig = SIG_DIGITS:  Number of significant digits """

    if x == 0:  # special case, prevent taking log of zero
        return x
    else:    # round
        return round(x, sig-int(math.floor(math.log10(abs(x))))-1)

def intersect_line(L0, L2):
    """ calculates the intersects of two lines

        L0 and L1: Lines specified by ((x0, y0), (x1, y1))

        - function returns the coordinataes of the intersection
          between both lines (px, py)
        - function returns an empty tuple if no intersection is found
        function returns (NaN, NaN) if lines are parallel
    """

    # unwrap lines
    x = [L0[0][0], L0[1][0], L2[0][0], L2[1][0]]
    y = [L0[0][1], L0[1][1], L2[0][1], L2[1][1]]


    #calculate denominator
    s1_x = x[1] - x[0]
    s1_y = y[1] - y[0]

    s2_x = x[3] - x[2]
    s2_y = y[3] - y[2]

    den = (-s2_x * s1_y + s1_x * s2_y)


    # if denominator is zero lines are parallel return NaN
    if sci_round(den) == 0:
        return (np.NAN, np.NAN)

    # parameterize line
    s = (-s1_y * (x[0] - x[2]) + s1_x * (y[0] - y[2])) / den
    t = (s2_x * (y[0] - y[2]) - s2_y * (x[0] - x[2])) / den

    # check if intersection lies on line pieces
    if (s >= 0) & (s <= 1) & (t >= 0) & (t <= 1):
        # calculate the intersection and return
        i_x = x[0] + (t * s1_x)
        i_y = y[0] + (t * s1_y)

        return (sci_round(i_x), sci_round(i_y))

    # lines not parallel but no intersection found on finite lines
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
    v0 = abs(L[1]-L[0])
    v1 = [0, 1]

    #normalize vectors
    n0 = v0/np.linalg.norm(v0)
    n1 = v1/np.linalg.norm(v1)

    #prevent rounding errors, acos returns an error for values > 1
    inprod = sci_round(np.inner(n0, n1))

    #calculate angles
    angle = math.acos(inprod)

    return sci_round(angle)

def intersect_lines(lines):
    """ Calculate all intersections of a  list of lines

        lines:  A list of lines. Each line is defined by two points
                line = ((x0, y0), (x1, y1))"""

    intersect = []
    for i in range(0, len(lines)):
        for j in range(i+1, len(lines)):
            p = intersect_line(lines[i], lines[j])
            if not None in p:
                if not np.any(np.isnan(p)):
                    intersect.append(p)

    return tuple(intersect)

def plot_lines(lines):
    """ Plot a list of lines with points of intersection

        lines:  A list of lines. Each line is defined by two points
                line = ((x0, y0), (x1, y1))"""

    for line in lines:
        plt.plot(line[:, 0], line[:, 1])

    intersects = intersect_lines(lines)
    for intersect in intersects:
        plt.plot(*intersect, ' ro')
    return

def rand_line(bounds=((0, 0), (1, 1))):
    """ Return a random line

         bounds: ((xmin, ymin), (xmax, ymax)) the line must be within these
                  bounds."""
    return np.array((rand_point(bounds), rand_point(bounds)))


def rand_point(bounds=((0, 0), (1, 1))):
    """ Return a random point.

        bounds:  ((xmin, ymin), (xmax, ymax)) the line point be within these
                  bounds."""
    xi = random.random() * (bounds[1][0]-bounds[0][0]) + bounds[0][0]
    yi = random.random() * (bounds[1][0]-bounds[0][0]) + bounds[0][0]
    return (xi, yi)


if __name__ == "__main__":
    # testing
    NLINES = 10
    BOX = ((-10, -10), (10, 10))

    random_lines = [rand_line(BOX) for i in range(0, NLINES)]



    plot_lines(random_lines)





