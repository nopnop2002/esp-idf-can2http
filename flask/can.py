#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple REST Server

import sys
import json
import datetime
from flask import Flask, request
app = Flask(__name__)

database = []

@app.route("/")
def root():
	global database
	res = ""
	for data in database:
		print("{}".format(data))
		#print("{}".format(len(data[2])))
		res = res + "{} {:x} {} {}".format(data[0],data[1],data[2],data[3]) + "<br>"
	#return "Hello World!"
	return res

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
	if(len(database) >= 20):
		database.pop(0)
	database.append(items)

	data = json.dumps(['result', 'ok'])
	return data

if __name__ == "__main__":
	#app.run()
	app.run(host='0.0.0.0', port=8000, debug=True)

