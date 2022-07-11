# eps-mazes
Program to generate maze figures

## Flags
| Flag | Syntax | Description |
| --- | --- | --- |
| length | -l | Specifies cell length, takes integer for value \ default: 10 |
| wall mode | -m | Specifies line or cell mode, takes "line" or "cell" for value \ default: line |
| space mode | -s | Specifies if input contains spaces between each cell or not, takes "t" or "f" for value \ default: True

## Line Mode
A maze displayed in line mode has lines for walls (as opposed to cells):\
![Error loading line mode image](/ReadmeAssets/line-mode.png)

To convert mazes like the above to plain text,
you must turn each line segment into a full sized cell.\
This is modelled in the image below:
![Error Loading Image](/ReadmeAssets/wall-to-cell.jpg)
When you run the program in line mode, it will properly convert the cell equivalent text to the line maze it represents

## Cell Mode
A maze displayed in cell mode has walls the same width as paths:\
![Error loading cell mode image](/ReadmeAssets/cell-mode.jpg)
