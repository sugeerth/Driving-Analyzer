#!/usr/bin/env python

import cv2
import pygame
import pygame.midi
from PySide.QtGui import QWidget, QLabel, QPixmap, QVBoxLayout, QIntValidator, QApplication, QComboBox, QCheckBox, QSpacerItem, qRgba
from PySide import QtGui
import random
import sys

# Class for the Sprites in the application!!!
class Block(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.speed = [2, 2]
        pygame.init()
        self.screen_width = 700
        self.screen_height = 400
        self.bitmap = pygame.image.load("turtle.png")
        self.bitmap.set_colorkey((0, 0, 0))
        self.Turtle = self.bitmap.get_rect()
        self.Turtle.topleft = [100, 200]
        self.soundObj = pygame.mixer.Sound('beepingsound.wav')
        self.soundObj.play()
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

    def move(self, x, y):
        self.Turtle.center[0] += x
        self.Turtle.center[1] += y

    def render(self):
        self.screen.blit(self.bitmap, (self.Turtle))

class CamShift:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("OPenCV_App", 1)
        cv2.namedWindow("Histogram", 1)
        cv2.setMouseCallback("OPenCV_App", self.on_mouse)
        self.line_mode = False
        self.drag_start = None
        self.track_window = None
        self.Start_turtle = False
        self.Turn = False

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
        if event == cv2.EVENT_LBUTTONUP:
            self.drag_start = None
            self.track_window = self.selection
        if self.drag_start:
            xmin = min(x, self.drag_start[0])
            ymin = min(y, self.drag_start[1])
            xmax = max(x, self.drag_start[0])
            ymax = max(y, self.drag_start[1])
            self.selection = (xmin, ymin, xmax - xmin, ymax - ymin)

    def hue_histogram_as_image(self, hist):
        histimg_hsv = cv2.CreateImage((320, 200), 8, 3)
        mybins = cv2.CloneMatND(hist.bins)
        cv2.Log(mybins, mybins)
        (_, hi, _, _) = cv2.MinMaxLoc(mybins)
        cv2.ConvertScale(mybins, mybins, 255. / hi)
        w, h = cv2.GetSize(histimg_hsv)
        hdims = cv2.GetDims(mybins)[0]
        for x in range(w):
            xh = (180 * x) / (w - 1)
            val = int(mybins[int(hdims * x / w)] * h / 255)
            cv2.Rectangle(histimg_hsv, (x, 0), (x, h - val), (xh, 255, 64), -1)
            cv2.Rectangle(histimg_hsv, (x, h - val), (x, h), (xh, 255, 255), -1)
        histimg = cv2.CreateImage((320, 200), 8, 3)
        cv2.CvtColor(histimg_hsv, histimg, cv2.CV_HSV2BGR)
        return histimg

    def run(self):
        hist = cv2.CreateHist([180], cv2.CV_HIST_ARRAY, [(0, 180)], 1)
        backproject_mode = False
        self.i = 20
        self.j = 600
        Information_mode = False
        text_font = cv2.InitFont(cv2.CV_FONT_HERSHEY_COMPLEX, .5, .5, 0.0, 1, cv2.CV_AA)
        text_font1 = cv2.InitFont(cv2.CV_FONT_HERSHEY_COMPLEX, 1, 1, 0.0, 1, cv2.CV_AA)
        text_coord = (10, 40)
        text_coord2 = (1 + 10, 40 + 100)
        text_coord1 = (10 + 50, 40 + 50)
        text_coord3 = (10 + 50 + 50, 40 + 50)
        text_color = cv2.CV_RGB(0, 0, 255)
        self.flag = True
        self.flag2 = True

        while True:
            frame = cv2.QueryFrame(self.capture)
            hsv = cv2.CreateImage(cv2.GetSize(frame), 8, 3)
            gray = cv2.CreateImage(cv2.GetSize(frame), 8, 1)
            cv2.CvtColor(frame, hsv, cv2.CV_BGR2HSV)
            cv2.CvtColor(frame, gray, cv2.CV_BGR2GRAY)
            self.String = str(str(self.i) + " " + str(self.j))
            self.hue = cv2.CreateImage(cv2.GetSize(frame), 8, 1)
            cv2.Split(hsv, self.hue, None, None, None)
            cv2.PutText(frame, "SCORE  :" + str(self.score), text_coord, text_font1, (0, 0, 255))
            cv2.PutText(frame, "DISTANCE  :" + str(self.dist), text_coord2, text_font1, (0, 0, 255))
            if self.total:
                cv2.PutText(frame, "SCORE PERCENT:" + str(self.Percent) + "   TOTAL SCORE:" + str(self.Total),
                            text_coord3, text_font1, (0, 0, 255))
            if Information_mode:
                cv2.PutText(frame, "Follow the instructions", text_coord1, text_font, text_color)
                cv2.PutText(frame, "1.Select the object by drawing a square around it", (60, 105), text_font,
                            text_color)
                cv2.PutText(frame, "2.Start the game by pressing s button", (60, 120), text_font, text_color)
                cv2.PutText(frame, "3.place the object through the rectangle to score maximum points", (60, 135),
                            text_font, text_color)
            backproject = cv2.CreateImage(cv2.GetSize(frame), 8, 1)
            cv2.CalcArrBackProject([self.hue], backproject, hist)
            if self.track_window and is_rect_nonzero(self.track_window):
                self.last_x = self.x
                self.last_y = self.y
                crit = (cv2.CV_TERMCRIT_EPS | cv2.CV_TERMCRIT_ITER, 10, 1)
                (iters, (area, value, rect), track_box) = cv2.CamShift(backproject, self.track_window, crit)
                self.track_window = rect
                self.x = track_box[0][0]
                self.y = track_box[0][1]
            if self.drag_start and is_rect_nonzero(self.selection):
                sub = cv2.GetSubRect(frame, self.selection)
                save = cv2.CloneMat(sub)
                cv2.ConvertScale(frame, frame, 0.5)
                cv2.Copy(save, sub)
                x, y, w, h = self.selection
                cv2.Rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255))
                sel = cv2.GetSubRect(self.hue, self.selection)
                cv2.CalcArrHist([sel], hist, 0)
                (_, max_val, _, _) = cv2.GetMinMaxHistValue(hist)
                if max_val != 0:
                    cv2.ConvertScale(hist.bins, hist.bins, 255. / max_val)
            elif self.track_window and is_rect_nonzero(self.track_window):
                cv2.EllipseBox(frame, track_box, cv2.CV_RGB(255, 0, 0), 3, cv2.CV_AA, 0)
            if not backproject_mode:
                cv2.ShowImage("OPenCV_App", frame)
            else:
                cv2.ShowImage("OPenCV_App", backproject)
            c = cv2.WaitKey(7)
            if c == 27:
                break
            if c == ord("l"):
                self.line_mode = not self.line_mode
                file = 'wrecking.mid'
                pygame.init()
                pygame.midi.init()
                print(pygame.midi.get_device_info(1))
                for x in range(0, pygame.midi.get_count()):
                    print(pygame.midi.get_device_info(x))
                pygame.mixer.init(44100, -16, 2, 1024 * 4)
                pygame.mixer.music.load(file)
                pygame.mixer.music.play()
                pygame.mixer.music.queue('jaiho.ogg')
                pygame.event.wait()t
                if not self.line_mode:
                    pygame.mixer.music.pause()
                self.newxy = []
                self.oldxy = []
                self.i = 20
                self.j = 400
            if c == ord("b"):
                backproject_mode = not backproject_mode
            if c == ord("o"):
                Information_mode = not Information_mode
            if c == ord("w"):
                enemy.centerx.move_ip(0, 5)
            if c == ord("a"):
                enemy.centerx.move_ip(-5, 0)
            if c == ord("s"):
                self.Start_turtle = not self.Start_turtle
            if c == ord("d"):
                enemy.centerx.move_ip(5, 0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = CamShift()
    demo.run()
    sys.exit(app.exec_())
