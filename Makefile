
all: hotplate.stl

spiral.scad: spiral.py make_spiral.py
	python2 make_spiral.py > spiral.scad

hotplate.stl: hotplate.scad paths.scad spiral.scad
	openscad -o hotplate.stl hotplate.scad

