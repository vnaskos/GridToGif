#!/usr/bin/env python

# author Vasilis Naskos

import os, getopt, sys, subprocess
from PIL import Image

def usage():
	print "\nVersion: GridToGif 2012-01-13\n\
Description: produce animated gif files from grid pictures\n\
Usage: -i <inputfile> -c <columns> -r <rows> -d <delay> -o <outputfile>\n\n\
Parameters:\n\n\
	-h\t\thelp \n\
	-i --input\tinput file\n\
	-c --columns\tinput image's columns\n\
	-r --rows\tinput image's rows\n\
	-d --delay\tdelay between frames\n\
	-o --output\toutput file (.gif)\n\n\
Default Values:\n\n\
	columns = 4\n\
	rows = 4\n\
	delay = 15\n\
	output = anim.gif\n"

## check if imagemagick is installed
def check_packages():
	devnull = open(os.devnull,"w")
	retval = subprocess.call(["dpkg","-s","imagemagick"],stdout=devnull,stderr=subprocess.STDOUT)
	devnull.close()
	if retval != 0:
		sys.exit("To run this script you must install imagemagick package")

def generate_gif(input_file, delay, columns, rows, output):
	try:
		img = Image.open(input_file)
	except Exception:
		exit("Error loading image!\n"+input_file)
	
	width, height = img.size
	subwidth = width / columns
	subheight = height / rows

	images = ''
	index = 0

	os.system("mkdir gif_temp")
	sys.stdout.write("Cropping input image ...")
	for y in range(0, rows):
		top = subheight*y
		for x in range(0, columns):
			index += 1;
			left = subwidth*x
			box = (left, top, left+subwidth, top+subheight)
			area = img.crop(box)
			area.save("gif_temp/temp_image_"+str(index)+".jpg", 'jpeg')
			images += "gif_temp/temp_image_"+str(index)+".jpg "
	print " OK"

	## create gif using imagemagick
	sys.stdout.write("Generating Gif ...")
	os.system("convert -delay "+ str(delay) +" -loop 0 "+ images +" "+ output)
	print " OK"
	sys.stdout.write("Removing temporary files ...")
	os.system("rm -r "+"gif_temp")
	print " OK"

def main(argv):
	input_file = '';
	delay = '';
	columns = '';
	rows = '';
	output = '';

	check_packages();

	try:
		opts, args = getopt.getopt(argv, "hi:c:r:d:o:", ["help", "input=", "columns=", "rows=", "delay=", "output="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
		
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-i", "--input"):
			input_file = arg
		elif opt in ("-c", "--columns"):
			columns = arg
		elif opt in ("-r", "--rows"):
			rows = arg
		elif opt in ("-d", "--delay"):
			delay = arg
		elif opt in ("-o", "--output"):
			output = arg

	## check parameters
	if input_file == "":
		usage()
		sys.exit("Error no input image!");
		
	if columns == "":
		columns = 4
	else:
		try:
			columns = int(columns)
		except Exception:
			exit("Error at columns value!")
			
	if rows == "":
		rows = 4
	else:
		try:
			rows = int(rows)
		except Exception:
			exit("Error at rows value!")
	
	if delay == "":
		delay = 15
	
	if output == "":
		output = "anim.gif"

	generate_gif(input_file, delay, columns, rows, output)

if __name__ == "__main__":
   main(sys.argv[1:])
