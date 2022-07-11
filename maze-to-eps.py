#!/usr/bin/env python

# convert square maze diagram to .eps file
# largely copied from Ryan Hayward's gopix
# https://github.com/ryanbhayward/gopix
#
# written by Luke Schultz
# created on July 5, 2022
# last edited on July 11, 2022


import sys

cell_length = 10    # size of cell (in postscript units)
mode = "line"       # wall mode, either line or cell
spaced = True       # True if input has space between characters, false if not

def read_maze():
    jump = 1
    if spaced:
        jump = 2

    maze = []
    row = input()
    while row != "":
        maze.append([])
        for i in range(0, len(row), jump):
            maze[-1].append(row[i])
        try:
            row = input()
        except:
            break

    return maze

def print_head(rows, cols):
    print("%!PS-Adobe-3.0 EPSF-3.0")
    print("%%BoundingBox: 0 0", cols*cell_length, rows*cell_length)
    print("%%Pages: 0")
    print("%%EndComments")

def print_cell(row, col):
    print("newpath")
    print(col*cell_length, row*cell_length, "moveto")
    print((col+1)*cell_length, row*cell_length, "lineto")
    print((col+1)*cell_length, (row-1)*cell_length, "lineto")
    print(col*cell_length, (row-1)*cell_length, "lineto")
    print("closepath")
    print("fill")

def print_wall_vert(row, col):
    print("newpath")
    print(col*cell_length, row*cell_length, "moveto")
    print(col*cell_length, (row-1)*cell_length, "lineto")
    print("closepath")
    print("stroke")

def print_wall_hori(row, col):
    print("newpath")
    print(col*cell_length, row*cell_length, "moveto")
    print((col+1)*cell_length, row*cell_length, "lineto")
    print("closepath")
    print("stroke")

if __name__=="__main__":

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-l" or sys.argv[i] == "-length":
            try:
                cell_length = int(sys.argv[i+1])
            except:
                print("ERROR: unrecognized argument after length flag")
                print("Expected INTEGER")
                exit()
        if sys.argv[i] == "-m" or sys.argv[i] == "-mode":
            try:
                mode = sys.argv[i+1]
            except:
                print("Error: argument needed after mode flag")
                exit()

            if mode != "line" and mode != "cell":
                print("ERROR: mode argument must be either 'line' or 'wall'")
                exit()
        if sys.argv[i] == "-s" or sys.argv[i] == "-spaced":
            try:
                spaced = sys.argv[i+1]
                if spaced == "true" or spaced == "True" or spaced == "t" or spaced == "T":
                    spaced = True
                elif spaced == "false" or spaced == "False" or spaced == "f" or spaced == "F":
                    spaced = False
                else:
                    print("ERROR: unrecognized argument after spaced flag")
                    print("Expected BOOLEAN")
                    exit()
            except:
                print("ERROR: argument needed after spaced flag")
                exit()

    maze = read_maze()
    if mode == "line":
        print_head(len(maze)//2, len(maze[0])//2)
        total_rows = len(maze)//2
    else:
        print_head(len(maze), len(maze[0]))
        total_rows = len(maze)

    row = 0
    col = 0
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if mode == "line":
                row = i // 2
                col = j // 2
                if maze[i][j] == "x" or maze[i][j] == "X":
                    if i % 2 == 0 and j % 2 == 0:
                        continue
                    if i % 2 == 0:
                        print_wall_hori(total_rows-row, col)
                    elif j % 2 == 0:
                        print_wall_vert(total_rows-row, col)
            else:
                if maze[i][j] == "x" or maze[i][j] == "X":
                    print_cell(total_rows - i, j)

    print("showpage")

