
import time
import xml.dom.minidom


#-----------------------------
#
# event class 
#
class event:

    time_fmt = "%Y-%m-%d %H:%M"
    time_fmt_alt1 = "%Y-%m-%d"

    def strptime(self, s):
        try:
            return time.strptime(s, event.time_fmt)
	except ValueError:
            return time.strptime(s, event.time_fmt_alt1)

    # setup event
    # Events have start and end times for the event and a text description.
    # They also have an author (which may be a person or program) and a date
    # that they were added.
    def __init__(self,start,end,author,text,added="",number=0):
        if not added: self.added = time.localtime()
        else: self.added = self.strptime(added)
        
        self.set_start(start)
        self.set_end(end)
	self.set_number(number)
        if self.end < self.start:
            self.end=self.start
        else:
            self.end=self.end
            
        self.set_text(text)
        self.set_author(author)

    # get funtions. 
    def get_author(self): return self.author
    def get_start(self): return time.strftime(event.time_fmt,self.start)
    def get_end(self): return time.strftime(event.time_fmt,self.end)
    def get_added(self): return time.strftime(event.time_fmt,self.added)
    def get_text(self): return self.text
    def get_number(self): return self.number

    # set funtions. 
    def set_author(self, a): self.author = a.replace("<","&lt;")
    def set_start(self,t): self.start = self.strptime(t)
    def set_end(self,t): self.end = self.strptime(t)
    def set_text(self,t):  self.text = t.replace("<","&lt;")
    def set_number(self,n):  self.number = int(n)


    # test event is in a time periiod
    def in_period(self,pstart,pend):
        pstart = self.strptime(pstart)
        pend = self.strptime(pend)
        if pstart <= self.end and pend >= self.start :return 1 
        else: return 0

    # test event contins a substring in the text 
    def contains(self, s):
        return not self.text.find(s) == -1

    # test event has author 
    def has_author(self, a):
        return self.get_author() == a

    # html description of event
    def html(self):
        return """<table><tr><td>Number</td><td width="150">%s</td>
	                  <td rowspan="5" valign="top"><b>%s</b></td></tr>
                         <tr><td>Start</td><td>%s</td></tr>
                         <tr><td>End</td><td>%s</td></tr>
                         <tr><td>Added</td><td>%s</td></tr>
                         <tr><td>Author</td><td>%s</td></tr>
                         </table>
                         """ % (self.get_number(),self.get_text(),self.get_start(),self.get_end(),self.get_added(),
                              self.get_author())

    # html description of event
    def plotlink(self):
        start = self.get_start()
        year = start[0:4]
	month = start[5:7]
	day = start[8:10]
        return '[<a href="http://badc.nerc.ac.uk/cgi-bin/data_browser/data_browser/badc/mst/plots/st-mode/%s/%s/radar-mst_capel-dewi_%s%s%s_st300.png">Data</a>]' \
	        % (year,month,year,month,day)

    # xml description of event
    def xml(self):
        return """<event added="%s" start="%s" 
end="%s" author="%s" number="%s">%s</event>\n""" % (self.get_added(),self.get_start(), self.get_end(),
                                self.get_author(),self.get_number(),self.get_text() )

    # one line description of event   
    def __repr__(self):
        return "%s -> %s: %s... (%s)" % (self.get_start(), self.get_end(),
                                self.get_text()[0:20], self.get_author())

#---------------------------------------------------------------
#
# log class to read and write the xml log files
#

class log:
  
    # setup a log file and read all the events
    # newlog arg overwrites an event log - careful!
    def __init__(self, filename, newlog=0):
        self.filename=filename
        self.events=[]
        if newlog:
            self.store()
        self.dom=xml.dom.minidom.parse(filename)
        self.eventlognode =self.dom.getElementsByTagName("eventlog")[0]
	self.next_number=1
        for e in self.dom.getElementsByTagName("event"):
	    text = self.getText(e)
	    start = e.getAttribute("start")
 	    added = e.getAttribute("added")
	    end = e.getAttribute("end")
	    author = e.getAttribute("author")
	    try:
	      number = int(e.getAttribute("number"))
	    except ValueError:
	      number=0
	    if number >= self.next_number: self.next_number=number+1
	    new_event = event(start,end,author,text,added,number)
            self.add_event(new_event)


    def renumber(self):
        for e in self:
	    for e1 in self: 
                if e.get_number()==e1.get_number(): 
		    e1.number=self.next_number
	            self.next_number =self.next_number+1
        

    # method to read a nodes text value
    def getText(self,node):
        t=""
        for n in node.childNodes:
	    if n.nodeType == xml.dom.minidom.Node.TEXT_NODE: t=t+n.nodeValue
        return t	   

    # method to make a log behave like an sequence    
    def __getitem__(self,i): return self.events[i]
    def __len__(self): return len(self.events)

    # store the log to the same file it came from        
    def store(self):
        f = open(self.filename, "w")
        f.write("<?xml version=\"1.0\" ?>\n")
        f.write("<eventlog>\n")
        for e in self.events:
            f.write(e.xml())
        f.write("</eventlog>\n")
        f.close()

    # add an event to the log. need to use store to commit to file
    def add_event(self,e):
        if e.get_number() == 0: 
	    e.number=self.next_number
	    self.next_number =self.next_number+1
        self.events.append(e)

    # search for events which overlap a period of time
    def in_period(self,pstart,pend):
        results = []
        for e in self:
            if e.in_period(pstart,pend): results.append(e)
        return results

    # search for events which contain a sub string
    def contains(self, s):
        results = []
        for e in self:
            if e.contains(s): results.append(e)
        return results

    # search for events which have a specified author
    def has_author(self,a):
        results = []
        for e in self:
            if e.has_author(a): results.append(e)
        return results

    # search for event by number
    def get_by_number(self,a):
        for e in self:
            if e.get_number() == a: return e
        
    # remove event by number
    def remove(self,a):
        for e in self:
            if e.get_number() == a: self.events.remove(e)

    def sort(self):
        self.events.sort(lambda e1, e2: cmp(e1.start,e2.start))
       
 

if __name__ == "__main__":

    e = event("2004-05-06 12:00","2004-05-06 13:00", "sjp","hell<xx>o sam")
#    print e.contains("sam")
#    print e.in_period("2004-05-06 12:00","2004-05-06 13:00")
#    print e.in_period("2004-05-06 14:00","2004-05-06 15:00")
#    print e.in_period("2004-05-06 11:00","2004-05-06 12:01")
#    print e.in_period("2004-05-06 12:10","2004-05-06 12:11")

    l = log("mst_events.xml")
    for i in range(1,9): l.add_event(event("2004-05-06 12:00","2004-0%s-06 13:00" % i, "sjp","hell<xx>o sam"))
#    print e.html()
#    l.store()

    for e in l: print e 
 
#    print l.in_period("2004-05-06 12:00","2004-05-06 12:00")
#    print l.contains("shit")

    print len(l)
    
