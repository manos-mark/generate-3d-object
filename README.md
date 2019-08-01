Execute the program from the command line like this:
	
	(Short arguments)
	blender cube.blend  --python cube.py -- -W 0.48 -H 0.9 -D 0.2 -P ~/Desktop/pictures/

	(Long arguments)
	blender cube.blend  --python cube.py -- --width 4.8 --height 9 --depth 2 --pictures-path ~/Desktop/pictures/

	(Work in background)
	blender --background cube.blend  --python cube.py -- -W 0.48 -H 0.9 -D 0.2 -P ~/Desktop/pictures/

After the -- you have to specify 4 arguments:

	-W, --width
	-H, --height
	-D, --depth
	-P, --pictures-path

The pictures folder must contain six pictures named:

	-"top.jpg"
	-"left.jpg"
	-"bottom.jpg"
	-"right.jpg"
	-"front.jpg"
	-"back.jpg"

The files cube.blend and cube.py must be in the same directory where you execute the script!

################## IMPORTANT ##################
# This script is only tested on Blender 2.79  #
################## IMPORTANT ##################
