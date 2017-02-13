# -*- coding: utf-8 -*-

import BaseHTTPServer,json

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):    

	def do_POST(self): 
		resp = self.makeResponce()
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.send_header("Content-Length", str(len(resp)))
		self.end_headers()
		self.wfile.write(resp)

	def makeResponce(self):  
		length = int(self.headers.getheader('content-length'))
		if length:
			reqbody = self.rfile.read(length)
			print reqbody
			# request = json.loads(reqbody)          
			# print "Request:"
			# print json.dumps(request, sort_keys=True, indent=4)

		responce = {"My_key":"idzie wąż wąską dróżką"}
		# print responce['My_key'].decode('utf8')
		return json.dumps(responce)

PORT = 8800
httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
print "serving at port", PORT
httpd.serve_forever()