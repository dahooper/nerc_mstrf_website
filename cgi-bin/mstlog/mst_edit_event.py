#!/usr/bin/python
#
# CGI program to enter MST radar site events into the event log
#
# SJP 13/1/05

import mstlog, cgi, time, sys


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
number=int(checkset("number"))
delete=checkset("delete")
msg=""


# get event from log
l = mstlog.log("mst_events.xml")
e = l.get_by_number(number)

# if different from log then change
modified=0
if start and e.get_start() != start: e.set_start(start); modified = 1
if end and e.get_end()   != end:   e.set_end(end); modified = 1
if author and e.get_author() != author: e.set_author(author); modified = 1
if text and e.get_text() != text: e.set_text(text); modified = 1

# if delete remove event and exit
if delete: 
    print  "Content-type: text/html\n"
    print """<HTML>
      <HEAD>
      <TITLE>Delete MST log entry</TITLE>
      </HEAD>
      
      <BODY>
      
      <a href="mst_event_search.py">Search events...</a>
       <form>
      <h1>Event %s deleted. </h1>

       </BODY>
      </HTML>""" % e.get_number()
    l.remove(e.get_number())
    l.store()
    sys.exit()
      


# if form data attempt to add an event
if modified: 
    l.sort()
    l.store()
    msg = """<font color="red">Event edited! %s</font>""" % e 

#print form
print  "Content-type: text/html\n"

print """<HTML>
      <HEAD>
      <TITLE>Edit MST log entry</TITLE>
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
           <option value="%s" selected>%s</option>
           <option value="ZKO">Tony</option>
           <option value="DAH">Davey</option>
           <option value="SJP">Sam</option>
          </select>
	</td>
	<td></td>
	<td><input type="submit" value="Edit Event" name="edit"></td>
	<td><input type="submit" value="Delete Event" name="delete"></td>
	</tr>
	<tr>
        <td colspan="4"><textarea cols="80" rows="8" name="text">%s</textarea></td>
       </tr>
	<tr><td><input type="text" size="15" name="number" value="%s"></td></tr>
        </table>
        </form>
       </BODY>
      </HTML>""" % (msg,e.get_start(),e.get_end(),e.get_author(),e.get_author(),
                    e.get_text(),e.get_number())
