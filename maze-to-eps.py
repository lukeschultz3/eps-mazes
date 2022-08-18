#!/usr/bin/env python3

# convert square maze diagram to .eps file
# built off of Ryan Hayward's gopix
# https://github.com/ryanbhayward/gopix
#
# written by Luke Schultz
# created on July 5, 2022
# last edited on August 15, 2022


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
    print("%%EndComments\n")
    print(line_width, "setlinewidth")
    print("1 setlinejoin\n")

    print("/NumRows", rows, "def")
    print("/NumCols", cols, "def")
    print("/Lightgray 0.95 def")
    print("/Darkgray 0.9 def")
    print("/CellSize", cell_length, "def")
    print("/FontSize CellSize 2 div def\n")

    print("% set font")
    print("/Sans-Serif findfont")
    print("FontSize scalefont")  # TODO: add flag to adjust
    print("setfont\n")

    with open("func_defs.eps", "r") as f:
        print(f.read())


def print_grid(rows, cols):
    print("""
% display grid with nested for loop
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
} for""")
    print("0 setgray\n")

def print_num(row, col, num, color=(0.8, 0, 0)):
    if 0 <= int(num) <= 9:
        print(int((col+0.07)*cell_length), int((row-0.7)*cell_length), "moveto")
    else:
        print(int((col-0.07)*cell_length), int((row-0.7)*cell_length), "moveto")
    print("(", num, ") true charpath")

def print_txt(row, col, txt, color=(0, 0, 0)):
    print("1 setlinewidth")
    print("newpath")
    print(int((col+0.07)*cell_length), int((row-0.7)*cell_length), "moveto")
    print("(", txt, ") true charpath")
    print("closepath")
    print(color[0], color[1], color[2], "setrgbcolor")
    print("stroke")
    print("0 setgray")
    print(line_width, "setlinewidth")

def print_labels(rows, cols):
    print("% display axis labels")
    print("0.8 0 0 setrgbcolor")
    print("1 setlinewidth")
    print("newpath")
    print("/a [ ", end="")
    for i in range(cols+1):
        print("(", end="")
        for j in range((i // 26) + 1):
            print(chr((i%26)+65), end="")
        print(") ", end="")
    print("] def", end="")
    print("""
0 1 NumCols {
    /Col exch def
    Col CellSize mul CellSize 0.35 mul add  NumRows CellSize mul CellSize 0.2 mul add moveto
    a Col get true charpath
} for
0 1 NumRows {
    /Row exch def
    CellSize 0.45 mul -1 mul NumRows Row sub 0.75 sub CellSize mul moveto
    Row 1 add 3 string cvs true charpath
} for""")
    print("closepath")
    print("stroke")
    print("0 setgray")
    print(line_width, "setlinewidth\n")

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

    # display white cells
    displayed = False
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
                if not displayed:
                    print("% display white cells")
                    print("newpath")
                    displayed = True

                print(col, total_rows-row-1, "Square")
    if displayed:
        print("closepath")
        print("1 setgray")
        print("fill\n")

    # display everything that isn't a wall or white cell
    displayed = False
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

            if not displayed and maze[i][j].lower() in ["s", "g"]:
                # only print header if necessary
                print("% display every non-wall and non-white cell")
                displayed = True

            if maze[i][j].lower() == "s":
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
    if displayed:
        print("\n")

    if numbered:
        print("% display cell numbers")
        print("1 setlinewidth")
        print("newpath")
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

                if not maze[i][j].lower() in ["w", "s", "g", "x", " "]:
                    try:
                        print_num(total_rows-row, col, int(maze[i][j]))
                    except:
                        try:
                            print_num(total_rows-row, col, float(maze[i][j]))
                        except:
                            # TODO: throw error
                            exit()

        print("closepath")
        #print(color[0], color[1], color[2], "setrgbcolor") #TODO
        print(0.8, 0, 0, "setrgbcolor") #TODO
        print("stroke")
        print("0 setgray")
        print(line_width, "setlinewidth\n")

    # display walls
    # note: display walls after everything else to improve visuals
    row = 0
    col = 0

    if mode == "cell":
        print("% display walls (cell mode)")
        print("newpath")
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j].lower() == "x":
                    print(j, total_rows-i-1, "Square")
        print("closepath")
        print("0 setgray")
        print("fill\n")
    else:
        print("% display walls (line mode)")
        print("newpath")
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j].lower() == "x":
                    # draw wall in line mode
                    if i % 2 == 0 and j % 2 == 0:
                        continue

                    row = i // 2
                    col = j // 2
                    if i % 2 == 0:
                        print(col, total_rows-row, "HoriWall")
                        #print_wall_hori(total_rows-row, col)
                    elif j % 2 == 0:
                        print(col, total_rows-row, "VertWall")
                        #print_wall_vert(total_rows-row, col)
        print("closepath")
        print("stroke\n")

    print("showpage")

