import sys
import re

for filename in sys.argv[1:]:
    print(filename)
    lines = open(filename).readlines()
    # check its got the right lines
    title = None
    startline = None
    endline = None
    for i, line in enumerate(lines): 
        if '<!*** Page contents to go here ***>' in line or '<!*** Beginning of page content ***>' in line: 
            startline = i
        if '<!*** Close page ***>' in line or '<!*** End of page content ***>' in line: 
            endline = i
        m = re.search("<(TITLE|title)>(.*?)</", line)
        if m: 
            title = m.group(2)    
    
    # unless all the bits are there then move to the next file 
    print(filename, title, startline, endline)
    if title is None or startline is None or endline is None:
        continue

    f = open(filename, "w")
    # jekyell header
    f.write(f"---\nlayout: default\ntitle: {title}\n---\n\n")

    for line in lines[startline+2:endline]: 
        f.write(line)
    f.close()


