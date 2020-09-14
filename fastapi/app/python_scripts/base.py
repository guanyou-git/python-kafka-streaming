import tokenize
import base64
import binascii
import re
import string
from urllib import parse
import subprocess
import codecs
import base64

from subprocess import Popen


def lower(event,input,output,args):
	data = event[input[0]]
	event[output[0]] = str(data).lower()
	return event


def match(event,input,output,args):
	data = event[input[0]]
	regex = re.compile(args[0])
	try:
		if re.search(regex,data):
			data = True
		else:
			data = False
	except:
		data = "==Error in regex=="
	event[output[0]] = data
	return event

def research(event,input,output,args):
	data = event[input[0]]
	try:
		result = re.search(r""+args[0],data)
		if result:
			data = result.group(0)
		else:
			data = "==Invalid=="
	except:
		data = "==Error in regex=="
	event[output[0]] = data
	return event

def resubreplace(event,input,output,args):
	data = event[input[0]]
	try:
		data = re.sub(r""+args[0],event[args[1]],data)
	except:
		pass
	event[output[0]] = data
	return event

def urldecode(event,input,output,args):
	data = event[input[0]]
	try:
		data = parse.unquote(data)
	except Exception as e:
		data = "==Invalid=="
	event[output[0]] = data
	return event

def save(event,input,output,args):
	event[output[0]] = event[input[0]]
	return event

def atob(event,input,output,args):
	data = event[input[0]]
	try:
		missing_padding = len(data) % 4
		if missing_padding != 0:
			data += b'='*(4-missing_padding)
		data = base64.b64decode(data)
	except:
		data = "==Invalid=="
	event[output[0]] = event[input[0]]
	return event
		

def like(event,input,output,args):
	# args is pattern
	data = event[input[0]]
	args = args[0].replace("%",".*")
	args = args.replace("_",".")
	try:
		if re.match(args, data):
			data = True
		else:
			data = False
	except:
		data = "==Error in regex=="
	event[output[0]] = data
	return event


## will be obseleted
def unhex(hexfield):
	return bytes.fromhex(hexfield).decode('utf-8')


def regmatch(decryptfield, matchstring):
	p = re.compile(matchstring)
	if p.findall(decryptfield):
		status = "validated"
	else:
		status = "not validated"
	return status


def sum(a,b):
	return str(a+b)
