from StreamSelection import *

class MainPanel(Frame):
	def __init__(self,stream):
		Frame.__init__(self,width=1400,height=660)
		self.logcanvas = LogCanvas(self,width=1140,height=650)
		self.streamselection = StreamSelection(stream,self.logcanvas)
		self.pack()
