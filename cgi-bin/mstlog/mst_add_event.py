#!/usr/bin/python
#
# CGI program to enter MST radar site events into the event log
#
# SJP 13/1/05

import mstlog, cgi, time


import cgitb; cgitb.enable()


#---------------------------
# set and check html form elements
def checkset(field):
    form = cgi.FieldStorage()
    if form.has_key(field): return form[field].value
    else: return ""

# set form variables
start=checkset("start")
end=checkset("end")
author=checkset("author")
text=checkset("text")
msg=""

# if form data attempt to add an event
if start: 
    l = mstlog.log("mst_events.xml")
    e = mstlog.event(start,end, author,text,number=l.next_number)
    l.add_event(e)
    l.sort()
    l.store()
    msg = """<font color="red">Event added! %s</font>""" % e 

# default entry time
t = time.strftime(mstlog.event.time_fmt,time.localtime())

#print form
print  "Content-type: text/html\n"

print """<HTML>
      <HEAD>
      <TITLE>Add MST log entry</TITLE>
      </HEAD>
      
      <BODY>
      %s
      <a href="mst_event_search.py">Search events...</a>
       <form>
      <h1>Add MST log entry</h1>
      <table>
       <tr>
        <td>Event Start</td>
        <td><input type="text" size="15" name="start" value="%s"></td>
        <td>Event End</td>
        <td><input type="text" size="15" name="end" value="%s"></td>
       </tr>
       <tr>
        <td>Event Author</td>
        <td>
	  <select name="author">
           <option value="ZKO" selected>Tony</option>
           <option value="DAH">Davey</option>
           <option value="SJP">Sam</option>
          </select>
	</td>
	<td></td>
	<td><input type="submit" value="Add Event"></td>
	</tr>
	<tr>
        <td colspan="4"><textarea cols="80" rows="8" name="text"></textarea></td>
	
       </tr>
        </table>
        </form>
       </BODY>
      </HTML>""" % (msg,t,t)
