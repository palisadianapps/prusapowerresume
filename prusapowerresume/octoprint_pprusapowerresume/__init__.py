# coding=utf-8
from __future__ import absolute_import
import os
import re

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin



class PprusapowerresumePlugin(octoprint.plugin.SettingsPlugin,
							  octoprint.plugin.AssetPlugin,
							  octoprint.plugin.TemplatePlugin,
							  octoprint.plugin.UiPlugin,
							  octoprint.plugin.ProgressPlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/pprusapowerresume.js"],
			css=["css/pprusapowerresume.css"],
			less=["less/pprusapowerresume.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			pprusapowerresume=dict(
				displayName="Pprusapowerresume Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="palisadianapps",
				repo="prusapowerresume",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/palisadianapps/prusapowerresume/archive/{target_version}.zip"
			)
		)

	def get_settings_defaults(self):
		return dict(
			message="{bar} {progress:>3}%"
		)

	##~~ EventHandlerPlugin

	def on_event(self, event, payload):
		if event == octoprint.events.Events.PRINT_STARTED:
			self._send_message(payload["origin"], payload["path"], 0)
		elif event == octoprint.events.Events.PRINT_DONE:
			self._send_message(payload["origin"], payload["path"], 100)

	##~~ ProgressPlugin

	def on_print_progress(self, storage, path, progress):
		if not self._printer.is_printing():
			return
		self._send_message(storage, path, progress)

	##~~ helpers

	def _send_message(self, storage, path, progress):
		message = self._settings.get(["message"]).format(progress=progress,
														 storage=storage,
														 path=path,
														 bar=self.__class__._progress_bar(progress))

		if os.path.exists("gpowerresume.txt"):
			os.remove("gpowerresume.txt")
		else:
			print("The file does not exist")

		if os.path.exists("temppower.txt"):
			os.remove("temppower.txt")
		else:
			print("The file does not exist")

		print(progress)
		f = open("gpowerresume.txt", "w")
		f.write(progress + "\n")
		f.close()
		temps = octoprint.comm.protocol.temperatures.received
		bedtemps = temps["B"]
		bedtemp = bedtemps(1)

		endtemps = temps["T0"]
		endtemp = endtemps(1)
		f = open("temppower.txt", "w")
		f.write(bedtemp + ", " + endtemp)
		f.close()

		a = open("pathtogfile.txt", "w")
		a.write(path)
		a.close()

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

	def get_lines_in_file(self, file_name):
		with open(file_name, 'r') as read_obj:
			# Read all lines in the file one by one
			count = 0
			for line in read_obj:
				count += 1
		return count

	def createresumefile(self, file_name, startline, endline, endtemp, bedtemp):
		"""Search for the given string in file and return lines containing that string,
		along with line numbers"""
		line_number = 0
		list_of_results = []
		# Open the file in read only mode
		# "/home/pi/.octoprint/uploads/powerresumefile.gcode"
		import os
		if os.path.exists("/home/pi/.octoprint/uploads/powerresumefile.gcode"):
			os.remove("/home/pi/.octoprint/uploads/powerresumefile.gcode")
		else:
			print("The file does not exist")
		f = open("/home/pi/.octoprint/uploads/powerresumefile.gcode", "w")
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
					f = open("/home/pi/.octoprint/uploads/powerresumefile.gcode", "a")
					f.write(line)
					f.close()
					print(line_number)

				if line_number == endline:
					f = open("/home/pi/.octoprint/uploads/powerresumefile.gcode", "a")
					f.write(
						"M107\n ; Filament-specific end gcode\n G4 ; wait\n M221 S100\n M104 S0 ; turn off temperature\n M140 S0 ; turn off heatbed\n M107 ; turn off fan\n G1 Z110.95 ; Move print head up\n G1 X0 Y200 F3000 ; home X axis\n M84 ; disable motors\n M73 P100 R0\n M73 Q100 S0\n")
					f.close()
					print(line_number)
					print("done")
					return

	def creategcodefile(self):

		f = open("pathtogfile.txt", "r")
		targetfile = f.read()

		# Return list of tuples containing line numbers and lines where string is found
		# return list_of_results

		adddd = self.search_string_in_file(targetfile, "G")
		print(adddd)

		adddda = self.search_string_in_file_from_back(targetfile, "G")
		lll = adddda[0]
		vvvv = lll
		print(vvvv)
		adddddf = self.get_lines_in_file(targetfile)
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

		self.createresumefile(targetfile, lll, upuntilline, str(bedtemp), str(endtemp))

	def on_after_startup(self):
		self._logger.info("OctoPrint-DetailedProgress loaded!")

		fname = "gpowerresume.txt"
		count = 0
		with open(fname, 'r') as f:
			for line in f:
				count += 1

		if count >= 98:
			return
		else:
			self.creategcodefile(count)

	@classmethod
	def _progress_bar(cls, progress):
		hashes = "#" * int(round(progress / 10))
		spaces = " " * (10 - len(hashes))
		return "[{}{}]".format(hashes, spaces)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Pprusapowerresume Plugin"


# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
# __plugin_pythoncompat__ = ">=3,<4" # only python 3
# __plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PprusapowerresumePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
