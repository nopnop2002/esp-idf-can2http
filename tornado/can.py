#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple REST Server

import os
import sys
import json
import datetime
import werkzeug
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define("lines", default=20, help="number of lines displayed", type=int)

database = []

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		global database
		items = []
		for data in database:
			#print("{}".format(data))
			datetime = data[0].split()
			#print("data={} datetime={}".format(data[0], datetime))

			items.append({
				"date": datetime[0],
				"time": datetime[1],
				"id": data[1],
				"frame": data[2],
				"value": data[3]
			})
		#print("items={}".format(items))
		self.render("index.html", lines=options.lines, items=items)

#curl -X POST -H "Content-Type: application/json" -d '{"canid":101, "frame":"standard" , "data": [1,2,3,4,5,6,7,8]}' http://192.168.10.43:8000/post
class PostHandler(tornado.web.RequestHandler):
	def post(self):
		#print("{}".format(self.request.body))
		function = sys._getframe().f_code.co_name
		dict = tornado.escape.json_decode(self.request.body)
		print("{} dict={}".format(function, dict))

		items = []
		now = datetime.datetime.now()
		items.append(now.strftime("%Y/%m/%d %H:%M:%S"))
		if ("canid" in dict):
			print("{} canid=0x{:x}".format(function, dict['canid']))
			items.append(dict['canid'])

		if ("frame" in dict):
			print("{} frame={}".format(function, dict['frame']))
			items.append(dict['frame'])

		if ("data" in dict):
			print("{} data length={}".format(function, len(dict['data'])))
			print("{} data={}".format(function, dict['data']))
			items.append(dict['data'])

		global database
		#print("{} {} {}".format(type(database), len(database), database))
		print("lines={}".format(options.lines))
		#if(len(database) >= 20):
		if(len(database) >= options.lines):
			database.pop(0)
		database.append(items)

		self.write(json.dumps({"result":"ok"}))

if __name__ == "__main__":
		tornado.options.parse_command_line()
		print("port={}".format(options.port))
		print("lines={}".format(options.lines))
		app = tornado.web.Application(
			handlers=[
				(r"/", IndexHandler),
				(r"/post", PostHandler),
			],
			template_path=os.path.join(os.getcwd(), "templates"),
			debug=True
		)
		http_server = tornado.httpserver.HTTPServer(app)
		http_server.listen(options.port)
		tornado.ioloop.IOLoop.current().start()
