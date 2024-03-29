maze1:
	python3 maze-to-eps.py -s -g < SampleMazes/maze1.txt > maze1.eps

maze2:
	python3 maze-to-eps.py -s -g < SampleMazes/maze2.txt > maze2.eps

maze3:
	python3 maze-to-eps.py -s -g < SampleMazes/maze3.txt > maze3.eps

maze3cell:
	python3 maze-to-eps.py -s -g -m cell < SampleMazes/maze3.txt > maze3cell.eps

maze3nospace:
	python3 maze-to-eps.py -g < SampleMazes/maze3-no-space.txt > maze3nospace.eps

maze3doublesize:
	python3 maze-to-eps.py -c 20 -s -g < SampleMazes/maze3.txt > maze3double.eps

maze4:
	python3 maze-to-eps.py -c 30 -n -m cell < SampleMazes/maze4.txt > maze4.eps

maze5:
	python3 maze-to-eps.py -c 30 -n < SampleMazes/maze5.txt > maze5.eps

maze6:
	python3 maze-to-eps.py -s -g -m cell < SampleMazes/maze6.txt > maze6.eps

all:
	make maze1
	make maze2
	make maze3
	make maze3cell
	make maze3nospace
	make maze3doublesize
	make maze4
	make maze5
	make maze6

clean:
	find *.eps ! -name func_def_square.eps ! -name func_def_walls.eps -delete
