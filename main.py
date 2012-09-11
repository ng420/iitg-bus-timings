#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import sys
import os
import time
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

def change_time(time_val,am_pm):
	time_elements = []
	if (time_val.find('.') != -1):
		time_elements = time_val.split('.')
	else:
		time_elements = time_val.split(':')
	t=int(time_elements[0])*100+int(time_elements[1])
	if(am_pm=='pm'):
		t=t+1200
	if(t>=2400):
                t=t-1200
	return t

def gh_time_list():

	now_time=time.localtime(int(time.time()))
	h=now_time.tm_hour+5
	m=now_time.tm_min+30
	if m>60:
		m=m-60
		h=h+1
	now_conv_time= h*100+m
	
        if(now_time.tm_wday==5):
                f=open("parse_from_holi.txt")
        elif(now_time.tm_wday==6):
                f=open("parse_from_holi.txt")
        else:
                f = open("parsethis.txt")
	text = f.read()
	text_lines = text.split('\n')

	final_time_list = []
	bus_list = []
	bus_count = 3

	for line in text_lines:

		line_elements = line.split(' ')

		bus_time = line_elements[0]

		am_pm = line_elements[1]

		bus_no = line_elements[2]

		start_point = line_elements[3]

		last_elem = len(line_elements) -1

		end_point = line_elements[last_elem]

		route_list = line_elements[4:last_elem]

		final_time_list.append( [bus_time.strip('?'), am_pm , bus_no , start_point])
		conv_time=change_time(bus_time,am_pm)
		if(conv_time>now_conv_time):
			bus_count = bus_count -1
			bus_list.append( [bus_time+am_pm,bus_no,start_point,end_point,' '.join(route_list)] )
			if(bus_count == 0) :
				break
	return bus_list
	
def iit_time_list():

	final_time_list = []
	now_time=time.localtime(int(time.time()))
	h=now_time.tm_hour+5
	m=now_time.tm_min+30
	if m>60:
		m=m-60
		h=h+1
	now_conv_time= h*100+m

	if(now_time.tm_wday==5): 
                f=open("parse_to_holi.txt")
        elif(now_time.tm_wday==6): 
                f=open("parse_to_holi.txt")
        else:
                f = open("parse2.txt")

	text = f.read()
	text_lines = text.split('\n')
	bus_list = []
	bus_count = 3

	for line in text_lines:

		line_elements = line.split(' ')

		bus_time = line_elements[0]

		am_pm = line_elements[1]

		bus_no = line_elements[2]

		start_point = line_elements[3]

		last_elem = len(line_elements) -1

		end_point = line_elements[last_elem]

		route_list = line_elements[4:last_elem]

		final_time_list.append( [bus_time.strip('?'), am_pm , bus_no , start_point])
		conv_time=change_time(bus_time,am_pm)
	
		if(conv_time>now_conv_time):
			bus_count = bus_count -1
			bus_list.append( [bus_time+am_pm,bus_no,start_point,end_point,' '.join(route_list)] )
			if(bus_count == 0) :
				break
				
	return bus_list


class MainHandler(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write ("<html><head>")
		self.response.out.write('''<style type="text/css">
		/* Reset Body Property */
body{border:0; margin:0; padding:0;}
#navbar-container{background:#000000;}
#int-site-container{
background:url(img/int-bg.png) left top repeat-x;
height:166px;
}
#logo, #navbar, #int-site{
width:800px;
margin:0 auto;
}
/*------------------*/
/* LOGO */
#logo{height:54px;}

/*------------------*/
/* Nav Bar */
#navbar{
height:26px;
line-height:26px;
}
#navbar a:link, #navbar a:visited, #navbar a:hover{
color:#FFFFFF;
font-weight:bold;
margin-right:20px;
text-decoration:none;
}
#table-2 {
	border: 1px solid #e3e3e3;
	background-color: #f2f2f2;
        width: 100%;
	border-radius: 6px;
	-webkit-border-radius: 6px;
	-moz-border-radius: 6px;
}
#table-2 td, #table-2 th {
	padding: 5px;
	color: #333;
}
#table-2 thead {
	font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
	padding: .2em 0 .2em .5em;
	text-align: left;
	color: #4B4B4B;
	background-color: #C8C8C8;
	background-image: -webkit-gradient(linear, left top, left bottom, from(#f2f2f2), to(#e3e3e3), color-stop(.6,#B3B3B3));
	background-image: -moz-linear-gradient(top, #D6D6D6, #B0B0B0, #B3B3B3 90%);
	border-bottom: solid 1px #999;
}
#table-2 th {
	font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
	background-color:#B7CEEC;
	font-size: 17px;
	line-height: 20px;
	font-color: white;
	font-weight: normal;
	text-align: left;
	text-shadow: white 1px 1px 1px;
}
#table-2 td {
	line-height: 20px;
	font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
	font-size: 14px;
	border-bottom: 1px solid #fff;
	border-top: 1px solid #fff;
}
#table-2 td:hover {
	background-color: #fff;
}
</style>''')
		self.response.out.write ("</head>")
		self.response.out.write ('<body><font face="Bookman Old Style"> <center><h1>IIT Guwahati Bus Service</h1></center></font> ' )
		self.response.out.write ('<font face="Bookman Old Style"> <center><h2>From Guwahati City</h2></center></font> ' )



		self.response.out.write("<br />")
		
		bus_list = gh_time_list()
		self.response.out.write( '<table id="table-2">')
		self.response.out.write( "<tr> <th> Bus Time </th>  <th> Bus No </th> <th>Starting Point </th> <th> To </th> <th> Pick-up Points</td> </tr>")
		for schedule in bus_list:
			self.response.out.write( "<tr>") 
			for element in schedule:
				self.response.out.write( "<td>")
				self.response.out.write (element)
				self.response.out.write( "</td>" )
			self.response.out.write( "</tr>" )
			
		self.response.out.write( "</table><br> <br> <br>" )
		
		self.response.out.write ('<h2><center><font face="Bookman Old Style">To Guwahati City</font></center></h2>')
		
		bus_list = iit_time_list()
		self.response.out.write( '<table id="table-2">')
		self.response.out.write( "<tr> <th> Bus Time </th>  <th> Bus No </th> <th>Starting Point </th> <th> To </th> <th> Dropping Points</td> </tr>")
		for schedule in bus_list:
			self.response.out.write( "<tr>") 
			for element in schedule:
				self.response.out.write( "<td>")
				self.response.out.write (element)
				self.response.out.write( "</td>" )
			self.response.out.write( "</tr>" )
			
		self.response.out.write( "</table>" )
		
		
		
		
		self.response.out.write( "</body></div>" )
		self.response.out.write ("</html>")
			
				
		
        

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
