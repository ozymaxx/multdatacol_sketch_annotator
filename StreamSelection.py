from LogCanvas import *

class StreamSelection(Frame):
	def __init__(self,stream,canvas):
		Frame.__init__(self)
		self.canvas = canvas
		self.s = Scrollbar(self)
		self.L = Listbox(self,selectmode=EXTENDED)
		self.L.bind('<<ListboxSelect>>',self.poll)

		self.s.pack(side=RIGHT, fill=BOTH)
		self.L.pack(side=LEFT, fill=BOTH)

		self.s['command'] = self.L.yview
		self.L['yscrollcommand'] = self.s.set
		
		for item in stream:
			self.L.insert(END, item)
			
		self.pack(side=RIGHT)
		
	def poll(self,*args):
		sel = self.L.curselection()
		
		if len(sel) == 1:
			strDrawn = self.L.get(0,sel[0])
			self.canvas.drawStream(strDrawn)
		else:
			self.canvas.drawStream([self.L.get(selc) for selc in sel])
