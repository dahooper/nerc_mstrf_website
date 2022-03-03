#!/usr/bin/python
#
# CGI to search mst log entries
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

# open event log
l = mstlog.log("mst_events.xml")

# if start or end defined search period. else results are all entries
if start and end: 
    results = l.in_period(start,end)
elif start:
    results = l.in_period(start,start)
else:
    results = l.events[:]

# if text search filter results for that substring    
if text:
    tr=[]
    for e in results:
        if e.contains(text):
	    tr.append(e)
    results = tr

# if author search filter results for that author	    
if author:
    tr=[]
    for e in results:
        if e.has_author(author): 
	    tr.append(e)   
    results = tr

# print search form
print  "Content-type: text/html\n"
print """<HTML>
      <HEAD>
      <TITLE>MST log search</TITLE>
      </HEAD>
      
      <BODY>
<a href="mst_add_event.py">Add event...</a>
       <form>
      <h1>search MST log entry</h1>
      <table>
       <tr>
        <td>Event period search, Start:</td>
        <td><input type="text" size="15" name="start" value="%s"></td>
        <td>End:</td>
        <td><input type="text" size="15" name="end" value="%s"></td>
       </tr>
       <tr>
        <td>Event Author search</td>
        <td>
	  <select name="author">
           <option value="" selected>Any</option>
           <option value="ZKO">Tony</option>
           <option value="DAH">Davey</option>
           <option value="SJP">Sam</option>
          </select>
	</td>
	<td></td>
	<td><input type="submit" value="Search"></td>
	</tr>
	<tr>
	<td>Sub string search:</td>
        <td><input type="text" size="15" name="text" value="%s"></td>
	
       </tr>
        </table>
        </form>
       </BODY>
      </HTML>""" % (start,end, text)

# print results 
print "%s entries found" %len(results)
for e in results:

    print "<hr>"
    print '[<a href="mst_edit_event.py?number=%s">Edit</a>]' % e.get_number()
    print e.plotlink()
    print e.html()
   

 

