#!/usr/bin/env python3

# convert square maze diagram to .eps file
# largely copied from Ryan Hayward's gopix
# https://github.com/ryanbhayward/gopix
#
# written by Luke Schultz
# created on July 5, 2022
# last edited on July 13, 2022


import sys

cell_length = 10    # size of cell (in postscript units)
mode = "line"       # wall mode, either line or cell
spaced = True       # True if input has space between characters, false if not
grid = True         # True if grid coloring is on, false if not
numbered = False    # True if cell numbers are on, false if not
line_width = 1      # line width

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

def read_maze_numbered():
    maze = []
    row = input()
    while row != "":
        maze.append([])
        last_index = 0
        for i in range(len(row)):
            if row[i] == " " and not last_index == i:
                maze[-1].append(row[last_index:i])
                last_index = i+1
        if last_index != len(row):
            maze[-1].append(row[last_index:])
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
    print(line_width, "setlinewidth")
    print("1 setlinejoin")

def print_grid(rows, cols):
    for row in range(rows):
        for col in range(cols):
            print("newpath")
            print(col*cell_length, row*cell_length, "moveto")
            print((col+1)*cell_length, row*cell_length, "lineto")
            print((col+1)*cell_length, (row+1)*cell_length, "lineto")
            print(col*cell_length, (row+1)*cell_length, "lineto")
            print("closepath")
            if (row+col) % 2 == 0:
                print("0.95 setgray")
            else:
                print("0.9 setgray")
            print("fill")
    print("0 setgray")

def print_cell(row, col, color=(0,0,0)):
    print("newpath")
    print(col*cell_length, row*cell_length, "moveto")
    print((col+1)*cell_length, row*cell_length, "lineto")
    print((col+1)*cell_length, (row-1)*cell_length, "lineto")
    print(col*cell_length, (row-1)*cell_length, "lineto")
    print("closepath")
    print(color[0], color[1], color[2], "setrgbcolor")
    print("fill")
    print("0 0 0 setrgbcolor")

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

def print_num(row, col, num):
    print("1 setlinewidth")
    print("newpath")
    print("/Sans-Serif findfont")
    print(cell_length//2, "scalefont")
    print("setfont")
    if 0 <= int(num) <= 9:
        print((col+0.07)*cell_length, (row-0.7)*cell_length, "moveto")
    else:
        print((col-0.07)*cell_length, (row-0.7)*cell_length, "moveto")
    print("(", num, ") true charpath")
    print("closepath")
    print("0.8 0 0 setrgbcolor")
    print("stroke")
    print("0 setgray")
    print(line_width, "setlinewidth")


if __name__=="__main__":

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-l" or sys.argv[i] == "-length":
            try:
                cell_length = int(sys.argv[i+1])
            except IndexError:
                pass
            except ValueError:
                raise Exception("ERROR: unrecognized argument after length flag. Expected INTEGER") from ValueError
        if sys.argv[i] == "-m" or sys.argv[i] == "-mode":
            try:
                mode = sys.argv[i+1]
            except IndexError:
                pass

            if mode != "line" and mode != "cell":
                raise Exception("ERROR: unrecognized argument after mode flag. Expected 'line' or 'wall'") from ValueError
        if sys.argv[i] == "-s" or sys.argv[i] == "-spaced":
            try:
                spaced = sys.argv[i+1]
                if spaced == "true" or spaced == "True" or spaced == "t" or spaced == "T":
                    spaced = True
                elif spaced == "false" or spaced == "False" or spaced == "f" or spaced == "F":
                    spaced = False
                else:
                    raise Exception("ERROR: unrecognized argument after spaced flag. Expected BOOLEAN") from ValueError
            except IndexError:
                pass
        if sys.argv[i] == "-g" or sys.argv[i] == "-grid":
            try:
                grid = sys.argv[i+1]
                if grid == "true" or grid == "True" or grid == "t" or grid == "T" or grid == "on":
                    grid = True
                elif grid == "false" or grid == "False" or grid == "f" or grid == "F" or grid == "off":
                    grid = False
                else:
                    raise Exception("ERROR: unrecognized argument after grid flag. Expected BOOLEAN") from ValueError
            except IndexError:
                pass
        if sys.argv[i] == "-n" or sys.argv[i] == "-numbered":
            try:
                numbered = sys.argv[i+1]
                if numbered.lower() == "true" or numbered.lower() == "t":
                    numbered = True
                elif numbered.lower() == "false" or numbered.lower() == "f":
                    numbered = False
                else:
                    raise Exception("ERROR: unrecognized argument after numbered flag. Expected BOOLEAN") from ValueError
            except IndexError:
                pass
        if sys.argv[i] == "-w" or sys.argv[i] == "-weight":
            try:
                line_width = float(sys.argv[i+1])
            except ValueError:
                raise Exception("ERROR: unrecognized argument after weight flag. Expected FLOAT") from ValueError
            except IndexError:
                pass

    if numbered:
        maze = read_maze_numbered()
    else:
        maze = read_maze()

    if mode == "line":
        print_head(len(maze)//2, len(maze[0])//2)
        if grid:
            print_grid(len(maze)//2, len(maze[0])//2)
        total_rows = len(maze)//2
    else:
        print_head(len(maze), len(maze[0]))
        if grid:
            print_grid(len(maze), len(maze[0]))
        total_rows = len(maze)

    row = 0
    col = 0
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if mode == "line":
                row = i // 2
                col = j // 2
            elif mode == "cell":
                row = i
                col = j

            if maze[i][j].lower() == "w":
                print_cell(total_rows - row, col, (255, 255, 255))
            elif maze[i][j].lower() == "s":
                print_cell(total_rows - row, col, (0, 255, 0))
            elif maze[i][j].lower() == "g":
                print_cell(total_rows - row, col, (255, 0, 0))
            elif numbered and not maze[i][j] == " " and not maze[i][j].lower() == "x":
                print_num(total_rows-row, col, int(maze[i][j]))

    row = 0
    col = 0
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if mode == "line":
                row = i // 2
                col = j // 2
                if maze[i][j].lower() == "x":
                    if i % 2 == 0 and j % 2 == 0:
                        continue
                    if i % 2 == 0:
                        print_wall_hori(total_rows-row, col)
                    elif j % 2 == 0:
                        print_wall_vert(total_rows-row, col)
                elif numbered and not maze[i][j] == " ":
                    pass
                    #print_num(total_rows-row, col, int(maze[i][j]))
            else:
                if maze[i][j].lower() == "x":
                    print_cell(total_rows - i, j)
                elif numbered and not maze[i][j] == " ":
                    pass
                    #print_num(total_rows-i, j, int(maze[i][j]))

    print("showpage")

