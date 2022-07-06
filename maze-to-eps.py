#!/usr/bin/env python

# convert square maze diagram to .eps file
# largely copied from Ryan Hayward's gopix
# https://github.com/ryanbhayward/gopix
#
# written by Luke Schultz
# created on July 5, 2022
# last edited on July 5, 2022


cell_radius = 10

def print_head(rows, cols):
    print("%!PS-Adobe-3.0 EPSF-3.0")
    print("%%BoundingBox: 0 0", cols*2*cell_radius, rows*2*cell_radius)


if __name__=="__main__":
    print_head(20, 20)
