import json


def get_lines_in_file(file_name):
	with open(file_name, 'r') as read_obj:
		# Read all lines in the file one by one
		count = 0
		for line in read_obj:
			count += 1

	return count


def search_string_in_file(file_name, string_to_search):
	"""Search for the given string in file and return lines containing that string,
	along with line numbers"""
	line_number = 0
	list_of_results = []
	# Open the file in read only mode
	with open(file_name, 'r') as read_obj:
		# Read all lines in the file one by one
		for line in read_obj:
			# For each line, check if line contains the string
			line_number += 1
			if "G" in line and ";   " not in line and "; " not in line:
				# If yes, then add the line number & line as a tuple in the list
				list_of_results.append((line_number, line.rstrip()))
				return list_of_results
			if "M" in line and ";   " not in line and "; " not in line:
				# If yes, then add the line number & line as a tuple in the list
				list_of_results.append((line_number, line.rstrip()))
				return list_of_results





def search_string_in_file_from_back(file_name, string_to_search):
	"""Search for the given string in file and return lines containing that string,
	along with line numbers"""
	line_number = 0
	list_of_results = []
	# Open the file in read only mode
	with open(file_name, 'r') as read_obj:
		# Read all lines in the file one by one
		for line in reversed(list(read_obj)):
			# For each line, check if line contains the string
			line_number += 1
			if "G" in line and ";   " not in line and "; " not in line:
				# If yes, then add the line number & line as a tuple in the list
				list_of_results.append((line_number, line.rstrip()))
				return list_of_results
			if "M" in line and ";   " not in line and "; " not in line:
				# If yes, then add the line number & line as a tuple in the list
				list_of_results.append(line_number)
				return list_of_results


def createresumefile(file_name, startline, endline, endtemp, bedtemp):
	"""Search for the given string in file and return lines containing that string,
	along with line numbers"""
	line_number = 0
	list_of_results = []
	# Open the file in read only mode
	# "/home/pi/.octoprint/uploads/powerresumefile.gcode"
	import os
	if os.path.exists("powerresumefile.gcode"):
		os.remove("powerresumefile.gcode")
	else:
		print("The file does not exist")
	f = open("powerresumefile.gcode", "w")
	f.write("G90 \n G92 E0 \n T0 \n M82 \n")
	f.write("M104 " + endtemp + " ; \n")
	f.write("M140 " + bedtemp + " ; \n")
	f.close()

	with open(file_name, 'r') as read_obj:
		# Read all lines in the file one by one
		for line in read_obj:
			# For each line, check if line contains the string
			line_number += 1
			if startline <= line_number <= endline:
				f = open("powerresumefile.gcode", "a")
				f.write(line)
				f.close()
				print(line_number)

			if line_number == endline:
				f = open("powerresumefile.gcode", "a")
				f.write("M107\n ; Filament-specific end gcode\n G4 ; wait\n M221 S100\n M104 S0 ; turn off temperature\n M140 S0 ; turn off heatbed\n M107 ; turn off fan\n G1 Z110.95 ; Move print head up\n G1 X0 Y200 F3000 ; home X axis\n M84 ; disable motors\n M73 P100 R0\n M73 Q100 S0\n")
				f.close()
				print(line_number)
				print("done")
				return


# Return list of tuples containing line numbers and lines where string is found
# return list_of_results


# open and read the file after the appending:
f = open("mask123.gcode", "r")
adsfas = f.read()

adddd = search_string_in_file("mask123.gcode", "G")
print(adddd)


# open and read the file after the appending:
f = open("mask123.gcode", "r")
adsfas = f.read()

adddda = search_string_in_file_from_back("mask123.gcode", "G")
lll = adddda[0]
vvvv = lll
print(vvvv)
adddddf = get_lines_in_file("mask123.gcode")
reallineback = adddddf - (vvvv - 1)
print(reallineback)

actualrange = reallineback - lll
print(actualrange)

percentage = 50

upuntilline = actualrange * (percentage * 0.01)
print(upuntilline)

upuntilline = round(upuntilline)

print(upuntilline)

d = open("temppower.txt", "r")
tempsss = d.read()

tempsss = json.loads(tempsss)
print(repr(tempsss))
bedtemp = tempsss["bedtemp"]
endtemp = tempsss["endtemp"]
print(bedtemp)
print(endtemp)

createresumefile("mask123.gcode", lll, upuntilline, str(bedtemp), str(endtemp))
