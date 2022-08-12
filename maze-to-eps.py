#!/usr/bin/env python3

# convert square maze diagram to .eps file
# built off of Ryan Hayward's gopix
# https://github.com/ryanbhayward/gopix
#
# written by Luke Schultz
# created on July 5, 2022
# last edited on August 12, 2022


import sys

ERROR_MSG = "ERROR: unrecognized argument after flag:"

cell_length = 20        # size of cell (in postscript units)
line_width  = 1         # line width
mode        = "line"    # wall mode, either line or cell
spaced      = False     # True if input has space between characters, False if not
grid        = False     # True if grid coloring is on, False if not
numbered    = False     # True if cell numbers are on, False if not
labels      = False     # True if grid labels on, False if not

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
    print("/NumRows", rows, "def")
    print("/NumCols", cols, "def")
    print("/Lightgray 0.95 def")
    print("/Darkgray 0.9 def")
    print("/CellSize 20 def")
    print("""
/Square         % col row Square
{ %def
    /Row exch def % Row and Col reversed on stack
    /Col exch def
    Col CellSize mul Row CellSize mul moveto
    Col 1 add CellSize mul Row CellSize mul lineto
    Col 1 add CellSize mul Row 1 add CellSize mul lineto
    Col CellSize mul Row 1 add CellSize mul lineto
} def
""")

def print_grid(rows, cols):
    print("""
% draw grid with nested for loop
0 1 NumRows {
    /i exch def
    0 1 NumCols {
        /j exch def
        newpath
        i j Square
        closepath
        i j add 2 mod 0 eq {
            Lightgray setgray
        } {
            Darkgray setgray
        } ifelse
        fill
    } for
} for
    """)
    print("0 setgray")

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

def print_num(row, col, num, color=(0.8, 0, 0)):
    print("1 setlinewidth")
    print("newpath")
    print("/Sans-Serif findfont")
    print(cell_length//2, "scalefont")  # TODO: add flag to adjust
    print("setfont")
    if 0 <= int(num) <= 9:
        print((col+0.07)*cell_length, (row-0.7)*cell_length, "moveto")
    else:
        print((col-0.07)*cell_length, (row-0.7)*cell_length, "moveto")
    print("(", num, ") true charpath")
    print("closepath")
    print(color[0], color[1], color[2], "setrgbcolor")
    print("stroke")
    print("0 setgray")
    print(line_width, "setlinewidth")

def print_txt(row, col, txt, color=(0, 0, 0)):
    print("1 setlinewidth")
    print("newpath")
    print("/Sans-Serif findfont")
    print(cell_length//2, "scalefont")  # TODO: add flag to adjust
    print("setfont")
    print((col+0.07)*cell_length, (row-0.7)*cell_length, "moveto")
    print("(", txt, ") true charpath")
    print("closepath")
    print(color[0], color[1], color[2], "setrgbcolor")
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
        if sys.argv[i].lower() == "-h" or sys.argv[i].lower() == "-help":
            with open("help.txt", "r") as f:
                print(f.read())
                exit()
        if sys.argv[i].lower() == "-c" or sys.argv[i].lower() == "-cell":
            try:
                cell_length = int(sys.argv[i+1])
            except IndexError:
                pass
            except ValueError:
                raise Exception(ERROR_MSG, "length. Expected INTEGER") from ValueError
        if sys.argv[i].lower() == "-m" or sys.argv[i].lower() == "-mode":
            try:
                mode = sys.argv[i+1]
            except IndexError:
                pass

            if mode != "line" and mode != "cell":
                raise Exception(ERROR_MSG, "mode. Expected 'line' or 'wall'") from ValueError
        if sys.argv[i].lower() == "-w" or sys.argv[i].lower() == "-weight":
            try:
                line_width = float(sys.argv[i+1])
            except ValueError:
                raise Exception(ERROR_MSG, "weight flag. Expected FLOAT") from ValueError
            except IndexError:
                pass
        if sys.argv[i].lower() == "-s" or sys.argv[i].lower() == "-spaced":
            spaced = True
        if sys.argv[i].lower() == "-g" or sys.argv[i].lower() == "-grid":
            grid = True
        if sys.argv[i].lower() == "-n" or sys.argv[i].lower() == "-numbered":
            numbered = True
            spaced = True  # input won't be read properly otherwise
        if sys.argv[i].lower() == "-l":
            labels = True

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
                print("newpath")
                print(col, total_rows-row-1, "Square")
                print("closepath")
                print(1, "setgray")
                print("fill")
            elif maze[i][j].lower() == "s":
                print("newpath")
                print(col, total_rows-row-1, "Square")
                print("closepath")
                print(0.8, 0, 0, "setrgbcolor")
                print("fill")
                print_txt(total_rows-row, col, "S", (1, 1, 1))
            elif maze[i][j].lower() == "g":
                print("newpath")
                print(col, total_rows-row-1, "Square")
                print("closepath")
                print(0, 0.8, 0, "setrgbcolor")
                print("fill")
                print_txt(total_rows-row, col, "G", (1, 1, 1))
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

    if mode == "cell":
        print("newpath")
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j].lower() == "x":
                    print(j, total_rows-i-1, "Square")
        print("closepath")
        print("0 setgray")
        print("fill")
    else:
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j].lower() == "x":
                    # draw wall in line mode
                    if i % 2 == 0 and j % 2 == 0:
                        continue

                    row = i // 2
                    col = j // 2
                    if i % 2 == 0:
                        print_wall_hori(total_rows-row, col)
                    elif j % 2 == 0:
                        print_wall_vert(total_rows-row, col)

    print("showpage")

