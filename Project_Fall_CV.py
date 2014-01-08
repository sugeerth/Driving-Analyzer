#!/usr/bin/env python

import cv

from PySide.QtGui import QWidget,QLabel,QPixmap,QLineEdit,QHBoxLayout,qRgba,\
    QImage,QVBoxLayout,QComboBox,QCheckBox,QSpacerItem,QIntValidator
from PySide import QtGui
import pygame
import random
import pygame.midi
import cv2
import numpy as np
import sys

#Class for the Sprites in the application!!!

class Block(pygame.sprite.Sprite):
	# Constructor. Pass in the colorc of the block,
	# and its x and y position	
	def __init__(self, width, height):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		self.speed = [2,2]
		pygame.init()
		# Create an image of the block, and fill it with a color.
		# This could also be an image loaded from the disk.
		
		# Define some colors
		black = ( 0, 0, 0)
		white = ( 255, 255, 255)
		red = ( 255, 0, 0)
		# Initialize Pygame

		#pygame.init()
		# Set the height and width of the screen
		screen_width=700
		screen_height=400



		# This is a list of 'sprites.' Each block in the program is
		# added to this list. The list is managed by a class called 'Group.'

		all_sprites_list = pygame.sprite.Group()
		block_list = pygame.sprite.Group()


		self.bitmap = pygame.image.load("turtle.png")
		#print self.bitmap
		self.bitmap.set_colorkey((0,0,0))
		self.Turtle = self.bitmap.get_rect()
		self.Turtle.topleft = [100,200]
		self.soundObj = pygame.mixer.Sound('beepingsound.wav')
		self.soundObj.play()
		screen=pygame.display.set_mode([screen_width,screen_height])

		# Fetch the rectangle object that has the dimensions of the image
		# image.
		# Update the position of this object by setting the values
		# of rect.x and rect.y

        def move(self, x, y):
	        self.Turtle.center[0] += x
	        self.Turtle.center[1] += y
	def render(self):
	    screen.blit(self.bitmap, (self.Turtle))

a=Block(34,22)
#Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0

# This class represents the ball
# It derives from the "Sprite" class in Pygame

def is_rect_nonzero(r):
    (_,_,w,h) = r
    return (w > 0) and (h > 0)

class CamShift:   
    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
	cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
	cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT, 720);
	self.score=0
	self.newxy=[]
	self.oldxy=[]
	self.state=True
	self.x=0
	self.y=0
	self.Total=0
	self.dist=0
	self.total=False
	self.InitializeQtWidgets()
        cv.NamedWindow( "OPenCV_App", 1 )
        cv.NamedWindow( "Histogram", 1 )
        cv.SetMouseCallback( "OPenCV_App", self.on_mouse)
	self.line_mode= False
        self.drag_start = None      # Set to (x,y) when mouse starts drag
        self.track_window = None    # Set to rect when the mouse drag finishes
	self.Start_turtle=False
	self.Turn=False

        print( "Keys:\n"
            "    ESC - quit the program\n"
            "    b - switch to/from backprojection view\n"
            "To initialize tracking, drag across the object with the mouse\n" )

    def InitializeQtWidgets(self):
		
		
		print "Inside Qt Widgets!!!"
		#self.glview = Patch3dGLWidget(self) 	


    def hue_histogram_as_image(self, hist):
        """ Returns a nice representation of a hue histogram """

        histimg_hsv = cv.CreateImage( (320,200), 8, 3)
        
        mybins = cv.CloneMatND(hist.bins)
        cv.Log(mybins, mybins)
        (_, hi, _, _) = cv.MinMaxLoc(mybins)
        cv.ConvertScale(mybins, mybins, 255. / hi)

        w,h = cv.GetSize(histimg_hsv)
        hdims = cv.GetDims(mybins)[0]
        for x in range(w):
            xh = (180 * x) / (w - 1)  # hue sweeps from 0-180 across the image
            val = int(mybins[int(hdims * x / w)] * h / 255)
            cv.Rectangle( histimg_hsv, (x, 0), (x, h-val), (xh,255,64), -1)
            cv.Rectangle( histimg_hsv, (x, h-val), (x, h), (xh,255,255), -1)

        histimg = cv.CreateImage( (320,200), 8, 3)
        cv.CvtColor(histimg_hsv, histimg, cv.CV_HSV2BGR)
        return histimg

    def on_mouse(self, event, x, y, flags, param):
        if event == cv.CV_EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
        if event == cv.CV_EVENT_LBUTTONUP:
            self.drag_start = None
            self.track_window = self.selection
        if self.drag_start:
            xmin = min(x, self.drag_start[0])
            ymin = min(y, self.drag_start[1])
            xmax = max(x, self.drag_start[0])
            ymax = max(y, self.drag_start[1])
            self.selection = (xmin, ymin, xmax - xmin, ymax - ymin)



    def run(self):
        hist = cv.CreateHist([180], cv.CV_HIST_ARRAY, [(0,180)], 1 )
        backproject_mode = False
	self.i=20
	self.j=600
	Information_mode = False
	text_font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX, .5, .5, 0.0, 1, cv.CV_AA )
	text_font1 = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX, 1, 1, 0.0, 1, cv.CV_AA )
	text_coord = ( 10, 40 )
	text_coord2 = ( 1+10, 40+100 )
	text_coord1=(10+50,40+50)
	text_coord3=(10+50+50,40+50)
	text_color = cv.CV_RGB(0,0,255)
	self.flag=True;
	self.flag2=True;
	#app = QtGui.QApplication(sys.argv)

	#wid = QtGui.QWidget()
	#wid.resize(250, 150)
	#wid.setWindowTitle('Simple')
	#wid.show()


	#widget = QtGui.QWidget()
	#layout = QtGui.QVBoxLayout()

	#grid = QtGui.QGridLayout()

	#grid.setSpacing(10)
#Infinite loop for the open cv process!!! 
        while True:

	    frame = cv.QueryFrame( self.capture )
	    #image = QImage(frame.tostring(), frame.width, frame.height, QImage.Format_RGB888).rgbSwapped()
	    #pixmap = QPixmap.fromImage(image)
	    #self.label.setScaledContents(True)

            # Convert to HSV and keep the hue
            hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
	    gray = cv.CreateImage(cv.GetSize(frame), 8, 1)
            cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
            cv.CvtColor(frame, gray,cv.CV_BGR2GRAY)
	    self.String=str(str(self.i)+" "+str(self.j))
            self.hue = cv.CreateImage(cv.GetSize(frame), 8, 1)
            cv.Split(hsv, self.hue, None, None, None)
            cv.PutText( frame, "SCORE  :"+str(self.score), text_coord, text_font1, (0,0,255) )
	    cv.PutText( frame, "DISTANCE  :"+str(self.dist), text_coord2, text_font1, (0,0,255) )
	    if self.total:	    	
		cv.PutText( frame, "SCORE PERCENT:"+str(self.Percent)+"   TOTAL SCORE:"+str(self.Total), text_coord3, text_font1, (0,0,255) )
	    #cv.PutText( frame, "Position  :"+self.String, text_coord3, text_font1, (0,0,255) )
            if Information_mode:
            	cv.PutText( frame, "Follow the instructions", text_coord1 , text_font, text_color )
		cv.PutText( frame, "1.Select the object by drawing a square around it", (60,105) , text_font, text_color )
                cv.PutText( frame, "2.Start the game by pressing s button", (60,120) , text_font, text_color )
            	cv.PutText( frame, "3.place the object through the rectabgle to score maximum points", (60,135) , text_font, text_color )

            # Compute back projection
            backproject = cv.CreateImage(cv.GetSize(frame), 8, 1)
	    
            # Run the cam-shift
            cv.CalcArrBackProject( [self.hue], backproject, hist )
            if self.track_window and is_rect_nonzero(self.track_window):
		self.last_x=self.x
		self.last_y=self.y
                crit = ( cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, 10, 1)
                (iters, (area, value, rect), track_box) = cv.CamShift(backproject, self.track_window, crit)
                self.track_window = rect
		self.x=track_box[0][0]
		self.y=track_box[0][1]
            # If mouse is pressed, highlight the current selected rectangle
            # and recompute the histogram

            if self.drag_start and is_rect_nonzero(self.selection):
                sub = cv.GetSubRect(frame, self.selection)
                save = cv.CloneMat(sub)
                cv.ConvertScale(frame, frame, 0.5)
                cv.Copy(save, sub)
                x,y,w,h = self.selection
                cv.Rectangle(frame, (x,y), (x+w,y+h), (255,255,255))
                sel = cv.GetSubRect(self.hue, self.selection )
                cv.CalcArrHist( [sel], hist, 0)
                (_, max_val, _, _) = cv.GetMinMaxHistValue( hist)
                if max_val != 0:
                    cv.ConvertScale(hist.bins, hist.bins, 255. / max_val)
            elif self.track_window and is_rect_nonzero(self.track_window):
		#print track_box[0][0],track_box[0][1]	
                cv.EllipseBox( frame, track_box, cv.CV_RGB(255,0,0), 3, cv.CV_AA, 0 )
		#cv.Line(imgScribble, cvPoint(posX, posY), cvPoint(lastX, lastY), cvScalar(0,255,255), 5);


		if self.Start_turtle:
              		cv.Line(frame, (10,3),(10,100), (255,0,0), 3, cv.CV_AA, 0)


		if self.line_mode:
			
			cv.Circle(frame, (int(self.i),int(self.j)),6, (0,0,255), 3, cv.CV_AA, 0 )
			Difference_x=abs(self.x-self.i)
			Difference_y=abs(self.y-self.j)
			Distance=round(Difference_x+Difference_y)
			self.dist=Distance			
			#print Distance
		
			if Distance < 250: 
				if not (Distance == 0):
					self.score+= int(1/Distance * 50)
				else:
					self.score+= int(1/1 * 50)
				self.Total+= int(1*20)
			#if (self.x<200 and self.x>0) and (self.y> 350 and self.y< 450) and (self.i<200 and self.i>0) and (self.j> 350 and self.j< 450):
				    #self.score+=10
			#if (self.x>150 and self.x<250) and (self.y< 450 and self.y> 50) and (self.i>150 and self.i<250) and (self.j< 450 and self.j> 50):
				    #self.score+=10		   
			#if (self.x>250 and self.x<600) and (self.y< 150 and self.y> 50) and (self.i>250 and self.i<600) and (self.j< 150 and self.j> 50):
				    #self.score+=10
                                    #cv.Rectangle(frame, (int(200),int(0)), (511,100), (0,0,255))
			cv.PutText( frame, "INSIDE THE BOX  "+str(self.score), (1100,670), text_font, text_color )
			

			if (self.i < 200 + 400) and self.state:
				self.i=self.i+2
				self.j=self.j
			else:
				self.i=self.i
				self.j=self.j-1
				if self.j == 0:
					self.state=False
					self.Percent=float(self.score/self.Total)*100
					self.total=True
			        
				if (self.j < 500) and self.flag:
					self.Turn=True					
					self.i=self.i+5
					self.j=self.j+1
					
				if (self.i > 500) and self.flag2:
					self.flag=False
					self.Turn=True
					#print "asda"
					self.i=self.i
					self.j=self.j+6
					
					if (self.j > 700):
						self.Turn=True
						self.flag2=False
						self.j=self.j
						self.i=self.i+2
					if self.Turn:
						print "Stuff Finished!!"
						 
			self.newxy.append((self.x,self.y))
			self.oldxy.append((self.last_x,self.last_y))
			#print len(self.newxy),"\n"
			if len(self.newxy) > 50 and len(self.oldxy) > 50:
				self.newxy=self.newxy[49:]
				self.oldxy=self.oldxy[49:]
			for new,old in zip(self.newxy,self.oldxy):
				cv.Line(frame, (int(new[0]),int(new[1])),(int(old[0]),int(old[1])), (0,255,0), 3, cv.CV_AA, 0 ) 		


		#cv.Rectangle(frame, (0,400), (511,400), (0,0,255))
		#cv.PutText( frame, "AREA FOR SCORING:", (15,70), text_font, text_color )
		#cv.line( frame, self.x,scelf.y , text_color, int thickness=1, int connectivity=8 );
		
		#A bounded rectangle for it!!! 
		
            if not backproject_mode:
                cv.ShowImage( "OPenCV_App", frame )
            else:
                cv.ShowImage( "OPenCV_App", backproject)
	 	
		
                #cv.Rectangle(frame, (10,50), (511,100), (0,0,255))
            cv.ShowImage( "Histogram", self.hue_histogram_as_image(hist))

#Input for the different keys!!! 

	    if self.Turn:	
		self.Turn=False
            c = cv.WaitKey(7)
            if c == 27:
                break
	    if c == ord("l"):
		self.line_mode= not self.line_mode
		file = 'wrecking.mid'
		pygame.init()
		pygame.midi.init()
		#a=pygame.midi.Input.read()

		print a
		print (pygame.midi.get_device_info(1))
		for x in range( 0, pygame.midi.get_count() ):
     			print pygame.midi.get_device_info(x)

		pygame.mixer.init(44100,-16,2,1024*4)
		pygame.mixer.music.load(file)
		pygame.mixer.music.play()
		pygame.mixer.music.queue('jaiho.ogg')
		pygame.event.wait()
		#pygame.mixer.music.fadeout(3000)
		if(not self.line_mode):
			 pygame.mixer.music.pause()
		self.newxy=[]
		self.oldxy=[]
		self.i=20
		self.j=400
		
            if c == ord("b"):
                backproject_mode = not backproject_mode
	    if c == ord("o"):
                Information_mode = not Information_mode
	    if c == ord("w"):
		enemy.centerx.move_ip(0,5)
 	    if c == ord("a"):
		enemy.centerx.move_ip(-5,0)
	    if c == ord("s"):
                self.Start_turtle = not self.Start_turtle
            #if c == ord("s"):
		#enemy.centerx.move_ip(0,-5)
            if c == ord("d"):
		enemy.centerx.move_ip(5,0)

if __name__=="__main__":
    demo = CamShift()
    demo.run()
