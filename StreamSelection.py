from LogCanvas import *
from tkSimpleDialog import *
from tkMessageBox import *
from tkFileDialog import *
import time
import os

class StreamSelection(Frame):
	def __init__(self,stream,canvas):
		Frame.__init__(self)
		self.canvas = canvas
		self.save_path = None
		self.s = Scrollbar(self)
		self.L = Listbox(self,height=40,selectmode=EXTENDED)
		self.L.bind('<<ListboxSelect>>',self.poll)
		self.L.bind('<Key>',self.respondToKey)

		self.s.pack(side=RIGHT, fill=Y)
		self.L.pack(side=LEFT, fill=Y)

		self.s['command'] = self.L.yview
		self.L['yscrollcommand'] = self.s.set
		
		for item in stream:
			self.L.insert(END, item)
			
		self.pack(side=RIGHT)
		
	def currentStream(self):
		sel = self.L.curselection()
		
		if len(sel) == 1:
			return self.L.get(0,sel[0])
		else:
			return [self.L.get(selc) for selc in sel]
		
	def saveStreamAsSketch(self,curStream,annotation):
		save_to = '%s/%s' % (self.save_path,annotation)
		
		if not os.path.exists(save_to):
			os.makedirs(save_to)
			os.makedirs('%s/sketch' % save_to)
			os.makedirs('%s/image' % save_to)
			
		filename = '%s/sketch/%s.txt' % (save_to,str(time.time()).replace('.',''))
		imfilename = '%s/image/%s.png' % (save_to,str(time.time()).replace('.',''))
		
		sketchfile = open(filename,'w')
		
		strokeNumber = 0
		firstTokens = curStream[0].split(',')
		
		if firstTokens[1] == 'STRSTART':
			strokeNumber = -1
		
		for item in curStream:
			tokens = item.split(',')
			
			if tokens[1] != 'STRSTART' and tokens[1] != 'CLEAR':
				sketchfile.write('%s\t%s\t%d\t%s' % (tokens[1],tokens[2],strokeNumber,tokens[len(tokens)-1]))
			elif tokens[1] == 'STRSTART':
				strokeNumber = strokeNumber + 1
			elif tokens[1] == 'CLEAR':
				sketchfile.write('----SKETCH CLEARED----')
				
		sketchfile.close()
		self.canvas.sketch.writeToImage(imfilename)
		os.system('/usr/bin/canberra-gtk-play --id="complete"')
		
	def respondToKey(self,event):
		curStream = self.currentStream()
		
		charPressed = str(event.char)
		
		if charPressed == 'a':
			if len(curStream) > 0:
				for item in curStream:
					tokens = item.split(',')
					
					if tokens[1] == 'CLEAR':
						showerror('Clearing','Canvas clearing is not a sketch point!')
						return
						
				annotation = askstring('Label','Enter the name of the symbol:')
				annotation = annotation.strip()
				
				if annotation == '':
					showerror('Empty Input','Label cannot be empty!')
				else:
					if self.save_path == None:
						self.save_path = askdirectory()
						
					self.saveStreamAsSketch(curStream,annotation)
			else:
				showerror('No selection','You must choose a part of the sketch stream!')
		
	def poll(self,*args):
		self.canvas.drawStream(self.currentStream())
