from Tkinter import *
from Sketch import *

class LogCanvas(Canvas):
	def __init__(self,master,**options):
		Canvas.__init__(self,master,options)
		self.configure(background='white')
		self.sketch = Sketch(self)
		self.pack(side=LEFT)
		
	def drawStream(self,stream):
		self.sketch.clearSketch()
		
		for item in stream:
			tokens = str(item).split(',')
			
			if len(tokens) > 1:
				if tokens[1] == 'STRSTART':
					if tokens[7] == 'false':
						self.sketch.openStroke(DRAWING_STROKE)
					else:
						self.sketch.openStroke(ERASER_STROKE)
				elif tokens[1] == 'CLEAR':
					self.sketch.clearSketch()
				else:
					self.sketch.addPoint(float(tokens[1]),float(tokens[2]))
				
		self.sketch.repaintOnCanvas()
