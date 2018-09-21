with open('mapred-site-jt.xml', 'a+') as f:
     lines = f.readlines()
     for i, line in enumerate(lines):
         if line.startswith('<name>'):
             line[i] = line[i].strip() + '<value> </value>\n'
     f.seek(0)
     for line in lines:
         f.write(line)

