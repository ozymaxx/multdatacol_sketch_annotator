from MainPanel import *
from tkFileDialog import *

streamfile = askopenfile(mode='r')

stream = []
for line in streamfile:
	tokens = line.split(',')
	
	if tokens[0] == '0':
		if tokens[1] != 'STREND' and tokens[1] != 'HOVER' and tokens[1] != 'STARTHOVER' and tokens[1] != 'ENDHOVER' and tokens[1] != 'VIDEOOPEN':
			stream.append(line)

streamfile.close()
mainpanel = MainPanel(stream)

mainloop()
