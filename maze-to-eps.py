#!/usr/bin/env python3

# convert square maze diagram to .eps file
# largely copied from Ryan Hayward's gopix
# https://github.com/ryanbhayward/gopix
#
# written by Luke Schultz
# created on July 5, 2022
# last edited on July 15, 2022


import sys

ERROR_MSG = "ERROR: unrecognized argument after flag:"

cell_length = 20    # size of cell (in postscript units)
mode = "line"       # wall mode, either line or cell
spaced = True       # True if input has space between characters, false if not
grid = True         # True if grid coloring is on, false if not
numbered = False    # True if cell numbers are on, false if not
line_width = 1      # line width
labels = False      # True if grid labels on, false if not

def read_maze():
    maze = []
    row = input()
    while row != "":
        maze.append([])
        last_index = 0
        for i in range(len(row)):
            if spaced and row[i] == " " and not last_index == i:
                maze[-1].append(row[last_index:i])
                last_index = i+1
            elif not spaced:
                # reading input with no spaces
                maze[-1].append(row[last_index])
                last_index += 1
        if last_index != len(row):
            maze[-1].append(row[last_index:])
        try:
            row = input()
        except:
            break

    return maze

def print_head(rows, cols):
    print("%!PS-Adobe-3.0 EPSF-3.0")
    if labels:
        print("%%BoundingBox:", -cell_length//2, -line_width,
              cols*cell_length+line_width, rows*cell_length+line_width+(cell_length//2))
    else:
        print("%%BoundingBox:", -line_width, -line_width,
              cols*cell_length+line_width, rows*cell_length+line_width)
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
    print(cell_length//4, "scalefont")  # TODO: add flag to adjust
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

def print_labels(rows, cols):
    print("0.8 0 0 setrgbcolor")
    print("1 setlinewidth")
    print("/Sans-Serif findfont")
    print(cell_length//2, "scalefont")
    print("setfont")

    for col in range(cols):
        print("newpath")
        print(col*cell_length, rows*cell_length+(cell_length*0.2), "moveto")
        print("(", chr((col%26)+65), ") true charpath")
        print("closepath")
        print("stroke")

    for row in range(rows):
        print("newpath")
        print(-(cell_length*0.75), (rows-row-0.75)*(cell_length), "moveto")
        print("(", row+1, ") true charpath")
        print("closepath")
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
                raise Exception(ERROR_MSG, "length. Expected INTEGER") from ValueError
        if sys.argv[i] == "-m" or sys.argv[i] == "-mode":
            try:
                mode = sys.argv[i+1]
            except IndexError:
                pass

            if mode != "line" and mode != "cell":
                raise Exception(ERROR_MSG, "mode. Expected 'line' or 'wall'") from ValueError
        if sys.argv[i] == "-s" or sys.argv[i] == "-spaced":
            try:
                spaced = sys.argv[i+1]
                if spaced.lower() == "true" or spaced.lower() == "t":
                    spaced = True
                elif spaced.lower() == "false" or spaced.lower() == "f":
                    spaced = False
                else:
                    raise Exception(ERROR_MSG, "spaced. Expected BOOLEAN") from ValueError
            except IndexError:
                pass
        if sys.argv[i] == "-g" or sys.argv[i] == "-grid":
            try:
                grid = sys.argv[i+1]
                if grid.lower() == "true" or grid.lower() == "t" or grid.lower() == "on":
                    grid = True
                elif grid.lower() == "false" or grid.lower() == "f" or grid.lower() == "off":
                    grid = False
                else:
                    raise Exception(ERROR_MSG, "grid. Expected BOOLEAN") from ValueError
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
                    raise Exception(ERROR_MSG, "numbered. Expected BOOLEAN") from ValueError
            except IndexError:
                pass
        if sys.argv[i] == "-w" or sys.argv[i] == "-weight":
            try:
                line_width = float(sys.argv[i+1])
            except ValueError:
                raise Exception(ERROR_MSG, "weight flag. Expected FLOAT") from ValueError
            except IndexError:
                pass
        if sys.argv[i] == "-c":
            try:
                labels = sys.argv[i+1]
                if labels.lower() == "true" or labels.lower() == "t":
                    labels = True
                elif labels.lower() == "false" or labels.lower() == "f":
                    labels = False
                else:
                    raise Exception(ERROR_MSG) from ValueError
            except IndexError:
                pass

    assert(not (spaced == False and numbered == True))  # TODO: change flags, avoid this

    maze = read_maze()

    if mode == "line":
        total_rows = len(maze) // 2
        total_cols = len(maze[0]) // 2
    else:
        total_rows = len(maze)
        total_cols = len(maze[0])

    print_head(total_rows, total_cols)

    # display grid
    if grid:
        print_grid(total_rows, total_cols)

    if labels:
        print_labels(total_rows, total_cols)

    # display everything that isn't a wall
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
                try:
                    print_num(total_rows-row, col, int(maze[i][j]))
                except:
                    try:
                        print_num(total_rows-row, col, float(maze[i][j]))
                    except:
                        exit()

    # display walls
    # note: display walls after everything else to improve visuals
    row = 0
    col = 0
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if mode == "line" and maze[i][j].lower() == "x":
                # draw wall in line mode
                if i % 2 == 0 and j % 2 == 0:
                    continue

                row = i // 2
                col = j // 2
                if i % 2 == 0:
                    print_wall_hori(total_rows-row, col)
                elif j % 2 == 0:
                    print_wall_vert(total_rows-row, col)

            elif maze[i][j].lower() == "x":
                # draw wall in cell mode
                print_cell(total_rows - i, j)

    print("showpage")

