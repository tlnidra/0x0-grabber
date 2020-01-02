#!/usr/bin/env python

import httplib2, sys, os, random, string
import time

ENDLINE = '\033[0m'
BOLD = '\033[1m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
GREYBACK = '\033[40m'

scantime = time.ctime(time.time())
dirname = scantime

pngCount = 0
foundss = 0

def empty_abort():
	print '\n\n' + RED + BOLD + '[+]' + ENDLINE + ' Nothing found'
	sys.exit()

def generate_id(size=3):
	return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(size))

def save_pic(content, pic_id, ext):
	f = open(dirname + '/' +str(pic_id) + ext,'wb')
	f.write(content)
	f.close

def print_status(png_count, link, color):
	print BLUE + BOLD + '[+] ' + ENDLINE + str(png_count) + ' Objects Found - ' + color + BOLD + link + ENDLINE

def abort():
	print '\n\n' + GREEN + BOLD + '[+]' + ENDLINE + ' All found Objects were saved to: ' + BOLD + os.getcwd() + '/' + dirname + ENDLINE
	sys.exit(0)

print YELLOW + BOLD + '''
0x0.st file grabber
 ''' + ENDLINE + GREYBACK + YELLOW + BOLD + 'Author:' + ENDLINE + ' @libgdx2_0\n'

if not os.path.exists(dirname):
    os.makedirs(dirname)
Ext = raw_input('Enter file extension: ')
if Ext.isdigit():
	print 'Wrong extension!'
	sys.exit()
else:
	print Ext

while 1:

	try:

		status_color = RED
		pic_id = generate_id()
		link = 'http://0x0.st/' + 'z' + pic_id + '.' + Ext
		h = httplib2.Http(timeout=100)
		resp = h.request(link)

		if 'content-location' in resp[0]:
			pngUrl = resp[0]['content-location']
			ext = '.' + pngUrl[-3:]

			if  (ext == '.' + Ext or ext == '.' + Ext):
				pngCount += 1
				save_pic(resp[1], pngCount, ext)
				status_color = GREEN
			
		print_status(pngCount, link, status_color)

	except httplib2.RelativeURIError:
		pass
	except KeyboardInterrupt:
		if pngCount > 0:
			abort()
		else:
			os.rmdir(dirname)
			empty_abort()
	except Exception as e:
		print '\n\n' + GREEN + BOLD + '[+]' + ENDLINE + ' An error occurred: ' + str(e)
		sys.exit(1)
