# eps-mazes
Program to generate maze figures

## I/O & Example Execution
The input is taken from stdin, and the output is pushed to stdout. To input and output to files, redirect.\
Example execution:
`python3 maze-to-eps.py < SampleMazes/maze1.txt > maze1.eps`

## Flags
| Flag | Syntax | Description |
| --- | --- | --- |
| Cell Size | `-c` | Specifies cell size, takes integer for value.<br />Default: `10` |
| Line Weight | `-w`| Specifies line wall weight, takes float for value<br />Default: `1` |
| Wall Mode | `-m` | Specifies line or cell mode, takes `line` or `cell` for value.<br />Default: `line` |
| Spaced Input  | `-s` | Enables spaced input, meaning the input file has spaces between each cell. |
| Grid Coloring | `-g` | Enables grid coloring to distinguish cells. |
| Numbering | `-n` | Enables cell numbering.<br />Note that the input file must contain cell numbers. |
| Labels | `-l` | Enables axis labels |

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
