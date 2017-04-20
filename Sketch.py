DRAWING_STROKE = 1
ERASER_STROKE = 2

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		
class Stroke:
	def __init__(self,color):
		self.points = []
		self.color = color
		
	def addPoint(self,x,y):
		self.points.append(Point(x,y))
		
class Sketch:
	def __init__(self,canvas):
		self.strokes = []
		self.canvas = canvas
		
	def openStroke(self,color):
		self.strokes.append(Stroke(color))
		
	def addPoint(self,x,y):
		if len(self.strokes) == 0:
			self.openStroke(DRAWING_STROKE)
			
		self.strokes[len(self.strokes)-1].addPoint(x,y)
		
	def clearSketch(self):
		self.strokes = []
		
	def repaintOnCanvas(self):
		self.canvas.delete('all')
		
		for stroke in self.strokes:
			drawcolor = 'black'
			
			if stroke.color == ERASER_STROKE:
				drawcolor = 'red'
				
			for i in range(1,len(stroke.points)):
				self.canvas.create_line(stroke.points[i-1].x,stroke.points[i-1].y,stroke.points[i].x,stroke.points[i].y,width=3,fill=drawcolor)
