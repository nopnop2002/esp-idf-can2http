#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple REST Server

import os
import sys
import json
import datetime
import argparse
from flask import Flask, request, render_template
app = Flask(__name__)

database = []

@app.route("/")
def root():
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
	return render_template("index.html", lines=app.config['lines'], items=items)

#curl -X POST -H "Content-Type: application/json" -d '{"canid":101, "frame":"standard" , "data": [1,2,3,4,5,6,7,8]}' http://192.168.10.43:8000/post
@app.route("/post", methods=["POST"])
def post():
	function = sys._getframe().f_code.co_name
	#print("{}: request={}".format(function, request))
	#print("{}: request.data={}".format(function, request.data))
	dict = json.loads(request.data)
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
	print("lines={}".format(app.config['lines']))
	#if(len(database) >= 20):
	if(len(database) >= app.config['lines']):
		database.pop(0)
	database.append(items)

	data = json.dumps(['result', 'ok'])
	return data

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-port', type=int, default=8000)
	parser.add_argument('-lines', type=int, default=20)
	args = parser.parse_args()
	print("port={}".format(args.port))
	print("lines={}".format(args.lines))
	app.config['lines'] = args.lines
	#app.run()
	app.run(host='0.0.0.0', port=args.port, debug=True)

