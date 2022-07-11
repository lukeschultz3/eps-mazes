#!/usr/bin/env python

# convert square maze diagram to .eps file
# largely copied from Ryan Hayward's gopix
# https://github.com/ryanbhayward/gopix
#
# written by Luke Schultz
# created on July 5, 2022
# last edited on July 11, 2022


cell_length = 10


def read_maze():
    maze = []
    row = input()
    while row != "":
        maze.append([])
        for i in range(0, len(row), 2):
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

def print_wall(row, col):
    print("newpath")
    print(col*cell_length, row*cell_length, "moveto")
    print((col+1)*cell_length, row*cell_length, "lineto")
    print((col+1)*cell_length, (row+1)*cell_length, "lineto")
    print(col*cell_length, (row+1)*cell_length, "lineto")
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
    maze = read_maze()

    print_head(len(maze)//2, len(maze[0])//2)

    total_rows = len(maze)//2

    row = 0
    col = 0
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            row = i // 2
            col = j // 2
            if maze[i][j] == "x":
                if i % 2 == 0 and j % 2 == 0:
                    continue
                if i % 2 == 0:
                    print_wall_hori(total_rows-row, col)
                elif j % 2 == 0:
                    print_wall_vert(total_rows-row, col)

    print("showpage")

