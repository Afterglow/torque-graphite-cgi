#! /usr/bin/env python
import cgi
import cgitb
import pickle
import socket
import sys
import struct
from time import gmtime, strftime
cgitb.enable(1)

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2004
CAR_ID = 'VXR8'

form = cgi.FieldStorage()
print "Content-Type: text/html"
print
if "session" not in form or "time" not in form or "id" not in form:
  print "ERROR!"
  sys.exit(1)


id = form["id"].value
time = str(int(form["time"].value)/1000)
session = int(form["session"].value)/1000

pids = []

for k in form.keys():
  if not k.startswith('k'):
    continue
  value = form[k].value
  sess = strftime("%a-%b-%y/%H:%M", gmtime(session))
  datakey = CAR_ID+'.'+sess+'.'+k
  datapoint = (datakey, (time, value))
  pids.append(datapoint)

payload = pickle.dumps(pids)
header = struct.pack("!L", len(payload))
message = header + payload
try:
  sock = socket.socket()
  sock.connect((CARBON_SERVER, CARBON_PORT))
  sock.sendall(message)
  sock.close()
  print "OK!"
except:
  print "EXCEPTION!"
