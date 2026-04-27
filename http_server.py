#!/usr/bin/env python
# -*- coding: utf-8 -*-
import http.server as server
import argparse

class MyHandler(server.BaseHTTPRequestHandler):
	def do_POST(self):
		#print('path=[{}]'.format(self.path))
		response = b'{"result": "ok"}'
		responseLength = str(len(response))
		#print("responseLength={}".format(responseLength))
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.send_header('Content-Length', responseLength)
		self.end_headers()
		self.wfile.write(response)


		# print POST request
		#print(self.headers)
		content_len  = int(self.headers.get("content-length"))
		#body = self.rfile.read(content_len).decode('utf-8')
		body = self.rfile.read(content_len)
		#print("content_len={}".format(content_len))
		#print("type(body)={}".format(type(body)))
		#print("body={}".format(body))
		payload = body.decode('utf-8')
		print(payload)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--port', type=int, help='http port', default=8000)
	args = parser.parse_args() 
	print("args.port={}".format(args.port))

	host = '0.0.0.0'
	httpd = server.HTTPServer((host, args.port), MyHandler)
	#httpd = server.ThreadingHTTPServer((host, port), MyHandler)
	httpd.serve_forever()
