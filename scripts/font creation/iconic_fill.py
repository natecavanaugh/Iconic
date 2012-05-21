#Copyright (C) 2012  P.J. Onori (pj@somerandomdude.com)

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.



#!/usr/bin/env python

import fontforge
import json
import math
import shutil
import fileinput
from pprint import pprint

json_data = open('iconic_fill.json')

data = json.load(json_data)

font = fontforge.open('blank_fill.sfd')

for file_name, char in data.iteritems():
	c = font.createChar(int("0x" + char, 16))

	c.importOutlines('svg/' + file_name + '.svg')
	c.autoHint()

	c.left_side_bearing = 15
	c.right_side_bearing = 15

#font files

font.generate('aui_icons.svg')
font.generate('aui_icons.ttf')
font.generate('aui_icons.eot')
font.generate('aui_icons.otf')
font.generate('aui_icons.woff')

#css file

theString='''@font-face {
	font-family: 'AlloyIcons';
	font-weight: normal;
	font-style: normal;
	src: url('aui_icons.eot');
	src: url('aui_icons.eot?#iefix') format('embedded-opentype'),
		url('aui_icons.ttf') format('truetype'),
		url('aui_icons.svg#iconic') format('svg');
}

'''
# theString += '''.aui-icon''' + ''.join([', .aui-icon-' + name for name, char in data.iteritems()]) + ''' {
# 	display:inline-block;
# 	font-family: 'IconicFill';
# }

# '''
theString += '''.aui-icon {
	display:inline-block;
	font-family: 'AlloyIcons';
}

'''
for file_name, char in data.iteritems():
	theString += '.aui-icon-' + file_name + """:before {
	content: '\\""" + char + """';
}

"""

f = open("aui_icons.css", 'w')
f.write(theString)
f.close()

#html file
# theString="<html><head><title>Iconic Font-embedding demo</title><link rel='stylesheet' href='aui_icons.css' type='text/css' media='screen' /><style> body {font-family:'Helvetica', arial, sans-serif;} span { font-size:36px; }</style><body>"
# theString += "<table><tr><th>Name</th><th>Iconic Icon</th><th>Unicode Icon</th><th>Hexidecimal Code</th>"
# for file_name, char in data.iteritems():
# 	theString += "<tr><td>" + file_name + "</td><td><span class='iconic " + file_name + "'></span></td><td><span class='" + file_name + "'></span></td><td>" + char + "</td></tr>"

# theString += "</table></body></html>"

theString = '''<!DOCTYPE html>

<html>
<head>
	<script src="../../build/aui/aui.js" type="text/javascript"></script>

	<link rel="stylesheet" href="../../build/aui-skin-classic/css/aui-skin-classic-all-min.css" type="text/css" media="screen" />

	<style type="text/css" media="screen">
		body {
			font-size: 12px;
		}

		#wrapper {
			padding: 10px;
			width: 80%;
			margin: 0 auto;
		}

		[class*=" aui-icon-"]:hover {
			color: #00c;
			cursor: pointer;
		}

		.the-icons {
			float: left;
			font-size: 24px;
			line-height: 2;
			margin: 1em;
		}

		.the-icons li {
			border-bottom: 1px solid #999;
			list-style: none;
		}

		.the-icons .label-text {
			margin-left: 10px;
		}
	</style>
</head>

<body>

<div id="wrapper">
	<h1>Alloy - Icons Demo</h1>
'''
# for file_name, char in data.iteritems():
# 	theString += "<tr><td>" + file_name + "</td><td><span class='iconic " + file_name + "'></span></td><td><span class='" + file_name + "'></span></td><td>" + char + "</td></tr>"

items = data.iteritems()
length = len(data)
# 4 columns
columns = 4
split = int(math.ceil(float(length) / float(4)))
i = 1
tmp = ''

theString += '''
	<ul class="the-icons">'''
for file_name, char in data.iteritems():
# 	theString += '''
# 			<li class="aui-icon aui-icon-''' + file_name + '''"></li>
# '''

	theString += '''
		<li class="''' + file_name + '"><span class="aui-icon aui-icon-' + file_name + '"></span><span class="label-text">' + file_name + '</span></li>'

	if (i % split == 0):
		theString += '''
	</ul>
	<ul class="the-icons">'''

	i += 1

theString += '''
	</ul>
</div>

</body>
</html>
'''

f = open("aui_icons_demo.html", 'w')
f.write(theString)
f.close()

# Copy demo
shutil.copyfile('aui_icons_demo.html', '../../../../demos/icons/index.html')
# Copy fonts
shutil.copyfile('aui_icons.svg', '../../../../src/aui-skin-base/font/aui_icons.svg')
shutil.copyfile('aui_icons.ttf', '../../../../src/aui-skin-base/font/aui_icons.ttf')
shutil.copyfile('aui_icons.eot', '../../../../src/aui-skin-base/font/aui_icons.eot')
shutil.copyfile('aui_icons.otf', '../../../../src/aui-skin-base/font/aui_icons.otf')
shutil.copyfile('aui_icons.woff', '../../../../src/aui-skin-base/font/aui_icons.woff')
# Copy css
shutil.copyfile('aui_icons.css', '../../../../src/aui-skin-base/css/icons.css')

for line in fileinput.FileInput('../../../../src/aui-skin-base/css/icons.css', inplace=1):
	line = line.replace("url('aui_icons", "url('../font/aui_icons")
	print line,
