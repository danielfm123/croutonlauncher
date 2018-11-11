#! /usr/bin/env python3
# Configuration happens here
icontheme='kde'
# End of Configuration
import os
import sys
import glob
import http.server
import socketserver
import logging
import cgi
from urllib.parse import urlparse
import xdg.DesktopEntry as entryhandler
import xdg.IconTheme as ic
import re


workingdirectory=os.getcwd()
i = ic.IconTheme()
i.parse('/usr/share/icons/breeze/index.theme')
if not os.path.exists('system'):
	os.symlink("/", "system")
apps = {}
def init():
	global apps
	try:
		os.remove('index.html')
	except:
		print("Old Menu file could not be removed")
	menu = open('index.html', 'a')
	menu.write("<head><script src='list.min.js'></script><link rel='stylesheet' type='text/css' href='style.css'><script language='javascript' type='text/javascript'>\n function closeWindow() { window.open('','_parent',''); window.close(); }</script><script language='javascript' type='text/javascript'>function startList() {var options = {valueNames: [ 'name']};var userList = new List('users', options);}</script></head><body onload='startList()'><div id='users'><input class='search' placeholder='Search' /><button class='sort' data-sort='name'>Sort by name</button><ul class='list'>")
	os.chdir('/usr/share/applications')
	id=0
	for file in glob.glob("*.desktop"):
		entry=entryhandler.DesktopEntry(filename=file)
		iconPath = str(ic.getIconPath(entry.getIcon()))
		if None != iconPath and bool(re.search("png$|svg$",iconPath)):
			apps.update({entry.getName():{'Name': entry.getName(), 'Icon':'system' + str(ic.getIconPath(entry.getIcon())), 'Exec':'xiwi -T '+entry.getExec().split('%',1)[0], 'id':id}})
		id=id+1
	apps = [apps[app] for app in apps]
	names = [app['Name'] for app in apps]
	apps = [x for _, x in sorted(zip(names,apps), key=lambda pair: pair[0])]
	print(apps)
	for app in apps:
		menu.write("<li><a class='name' href='index.html?id=" + str(app['id']) + "' onclick='closeWindow()'><img class='icon' height='48' width='48' src='" + app['Icon'] + "'>" +app['Name'] + '</a></li>')
	menu.write('</div></body>')
	menu.close()

def serve():
	os.chdir(workingdirectory)
	PORT = 8000

	class ServerHandler(http.server.SimpleHTTPRequestHandler):

		def do_GET(self):
			parsed_path = urlparse(self.path)
			try:
				params = dict([p.split('=') for p in parsed_path[4].split('&')])
			except:
				params = {}
			if params:
				for app in apps:
					if str(app['id']) == str(params['id']).strip("/"):
						print(app['Name'], " EXEC : ",app['Exec'])
						os.system(app['Exec']+'&')
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
	Handler = ServerHandler
	httpd = socketserver.TCPServer(("", PORT), Handler)
	print("serving at port", PORT)
	httpd.serve_forever()

init()
serve()
