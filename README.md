# eps-mazes
Program to generate maze figures

## I/O & Example Execution
The input is taken from stdin, and the output is pushed to stdout. To input and output to files, redirect.\
Example execution:
`python3 maze-to-eps.py < SampleMazes/maze1.txt > maze1.eps`

## Flags
| Flag | Syntax | Description |
| --- | --- | --- |
| Length | `-l` | Specifies cell length, takes integer for value.<br />Default: `10` |
| Wall Mode | `-m` | Specifies line or cell mode, takes `line` or `cell` for value.<br />Default: `line` |
| Spaced Input  | `-s` | Specifies if input contains spaces between each cell or not, takes `t` or `f` for value.<br />Default: `t`|
| Grid Coloring | `-g` | Toggles grid coloring to distinguish cells, takes `t` or `f` for value.<br />Default: `t`|
| Numbered | `-n` | Specifies if the cells are numbered, takes `t` or `f` for value.<br />Default: `t`|
| Line Weight | `-w`| Specifies line wall weight, takes float for value<br />Default: `1` |
| Labels | `-c` | Toggles grid labels, takes `t` or `f` for value.<br />Default: `f` |

## Line Mode
A maze displayed in line mode has lines for walls (as opposed to cells):\
![Error loading line mode image](/ReadmeAssets/line-mode.jpg)

To convert mazes like the above to plain text,
you must turn each line segment into a full sized cell.\
This is modelled in the image below:
![Error Loading Image](/ReadmeAssets/wall-to-cell.jpg)
When you run the program in line mode, it will properly convert the cell equivalent text to the line maze it represents

## Cell Mode
A maze displayed in cell mode has walls the same width as paths:\
![Error loading cell mode image](/ReadmeAssets/cell-mode.jpg)
