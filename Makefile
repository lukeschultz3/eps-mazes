maze1:
	python3 maze-to-eps.py < SampleMazes/maze1.txt > maze1.eps

maze2:
	python3 maze-to-eps.py < SampleMazes/maze2.txt > maze2.eps

maze3:
	python3 maze-to-eps.py < SampleMazes/maze3.txt > maze3.eps

maze3cell:
	python3 maze-to-eps.py -m cell < SampleMazes/maze3.txt > maze3cell.eps

maze3nospace:
	python3 maze-to-eps.py -s f < SampleMazes/maze3-no-space.txt > maze3nospace.eps

maze3doublesize:
	python3 maze-to-eps.py -l 20 < SampleMazes/maze3.txt > maze3double.eps

clean:
	rm *.eps
