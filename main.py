#! /usr/bin/env python3
# Configuration happens here
# End of Configuration
import os
import sys
import json
import glob
import http.server
import socketserver
import logging
import cgi
from urllib.parse import urlparse
import xdg.DesktopEntry as entryhandler
import xdg.IconTheme as ic
import re

#devel

class Apps:
	def __init__(self):
		self.action = {}
		apps_dir = '/usr/share/applications/'

		if not os.path.exists('system'):
			os.symlink("/", "system")

		iconthemes = ['Humanity', 'breeze', 'gnome']
		for icontheme in iconthemes:
			icontheme_path = '/usr/share/icons/{}/index.theme'.format(icontheme)
			if os.path.isfile(icontheme_path):
				break
		self.icons = ic.IconTheme()
		self.icons.parse(icontheme_path)


		#Read deskto files
		files =  glob.glob(apps_dir+"*.desktop")
		entrys = [entryhandler.DesktopEntry(filename=file) for file in files]
		entrys = sorted(entrys, key = lambda e: e.getName().lower())
		id=0
		executables = ["/bin/htop",'"/usr/NX/bin/nxplayer" --recording','"/usr/NX/bin/nxplayer" --session']
		names = ['NoMachine Service']
		for entry in entrys:
			name =  entry.getName()
			#print(name)
			iconPath = str(ic.getIconPath(entry.getIcon()))
			executable = entry.getExec().split('%',1)[0]
			added = executable in executables or name in names
			try:
				isTerminal = entry.content['Desktop Entry']['Terminal'] == 'true'
			except:
				isTerminal = False
			try:
				nodisplay = entry.content['Desktop Entry']['NoDisplay'] == 'true'
			except:
				nodisplay = False
			try:
				categories = entry.content['Desktop Entry']['Categories']
				fobiden_cat = bool(re.search('Settings|System',categories))
			except:
				fobiden_cat = False
			if None != iconPath and bool(re.search("png$|svg$",iconPath)) and \
					not bool(re.search("sbin|pkexec|^none", entry.getExec())) and \
					not isTerminal and \
					not nodisplay and not added and not fobiden_cat:
				self.action[str(id)] = {'Name':name,
									  'Icon':'system' + iconPath,
									  'Exec': executable,
									  'id':str(id),
									  'type': 'app'}
				executables = executables + [executable]
				names = names + [name]
				id = id + 1

		html_items = ""
		#Create HTML
		for app in range(id):
			app = self.action[str(app)]
			html_items = html_items + \
				"<li class ='list-group-item' > " \
				"<a class ='name' href='index.html?id={id}' onclick='closeWindow()' run='{Exec}'> " \
				"<img class ='icon' height='32' width='32' src='{Icon}' >" \
				"{Name}" \
				"</a></li> \n".format_map(app)

		html_items = html_items + '<li class="list-group-item">' \
								  "<a class ='name' href='index.html?id=startx' onclick='closeWindow()'> " \
								  "<img class ='icon' height='32' width='32' src='desktop.png' >" \
								  "Launch Desktop " \
								  "</a></li>\n"
		html_items = html_items + '<li class="list-group-item" data-toggle="modal" data-target="#optionModal">Options</li>\n'

		self.action['tabMode'] = {'type': 'param',
								  'attr': 'newAppMode',
								  'val':'tabMode'}
		self.action['winMode'] = {'type': 'param',
								  'attr': 'newAppMode',
								  'val':'winMode'}
		self.action['kde'] = {'type': 'param',
								  'attr': 'desktop',
								  'val':'startkde -X xiwi'}
		self.action['xfce4'] = {'type': 'param',
								  'attr': 'desktop',
								  'val':'startxfce4 -X xiwi'}
		self.action['gnome'] = {'type': 'param',
								  'attr': 'desktop',
								  'val':'startgnome -X xiwi'}
		self.action['startx'] = {'type': 'startx'}

		with open('index_template.html','r') as t:
			template = t.readlines()

		for n in range(len(template)):
			if(template[n] == '@apps@\n'):
				template[n] = html_items

		try:
			os.remove('index.html')
		except:
			print("Old Menu file could not be removed")

		with open('index.html','w+') as i:
			for t in template:
				i.write(t)

class Server:

	global options
	global apps

	class ServerHandler(http.server.SimpleHTTPRequestHandler):
		def do_GET(self):
			parsed_path = urlparse(self.path)
			try:
				params = dict([p.split('=') for p in parsed_path[4].split('&')])
			except:
				params = {}
			print(params)

			if len(params) > 0:
				param = str(params['id']).strip("/")
				action = apps.action[param]
				if action['type'] == 'app':
					if options['newAppMode'] == 'winMode':
						command_line = 'xiwi ' + action['Exec']
					elif options['newAppMode'] == 'tabMode':
						command_line = 'xiwi -T ' + action['Exec']
					print(command_line)
					os.system(command_line+'&')
				elif action['type'] == 'param':
					attr = action['attr']
					val = action['val']
					options[attr] = val
					with open('options.json', 'w') as file:
						file.writelines(json.dumps(options))
					print('parameters updated')
				elif action['type'] == 'startx':
					print('Launching Desktop...')
					command_line = options['desktop']
					print(command_line)
					os.system(command_line + '&')

			http.server.SimpleHTTPRequestHandler.do_GET(self)

		def do_POST(self):
			logging.error(self.headers)
			form = cgi.FieldStorage(
				fp=self.rfile,
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
					 'CONTENT_TYPE':self.headers['Content-Type'],
					 })
			for item in form.list:
				logging.error(item)
			http.server.SimpleHTTPRequestHandler.do_GET(self)

	def __init__(self):
		pass

	def launch(self,PORT):
		httpd = socketserver.TCPServer(("", PORT), self.ServerHandler)
		print("serving at port", PORT)
		httpd.serve_forever()

if __name__ == '__main__':
	try:
		workingdirectory = os.path.dirname(os.path.realpath(__file__))
		os.chdir(workingdirectory)
	except:
		workingdirectory = os.getcwd()
	print(workingdirectory)

	with open('options.json', 'r') as f:
		options = json.load(f)

	apps = Apps()
	server = Server()
	server.launch(8000)
