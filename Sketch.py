from PIL import Image, ImageDraw

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
		
	def findCorners(self):
		if len(self.strokes) > 0:
			if len(self.strokes[0].points) > 0:
				minx = 1141
				miny = 651
				maxx = 0
				maxy = 0
				
				for stroke in self.strokes:
					for point in stroke.points:
						minx = min(minx,point.x)
						miny = min(miny,point.y)
						maxx = max(maxx,point.x)
						maxy = max(maxy,point.y)
						
				return (int(minx),int(miny),int(maxx),int(maxy))
			else:
				return (0,0,0,0)
		else:
			return (0,0,0,0)
			
	def writeToImage(self,impath):
		draw_offset = 5
		(minx,miny,maxx,maxy) = self.findCorners()
		im = Image.new('RGBA',(maxx-minx+2*draw_offset,maxy-miny+2*draw_offset),(0,0,0,0))
		draw = ImageDraw.Draw(im)
		
		for stroke in self.strokes:
			for i in range(1,len(stroke.points)):
				draw.line((stroke.points[i-1].x-minx+draw_offset,stroke.points[i-1].y-miny+draw_offset,stroke.points[i].x-minx+draw_offset,stroke.points[i].y-miny+draw_offset), fill='black', width=3)
				
		del draw
		im.save(impath,'PNG')
		
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
