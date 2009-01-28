# layout.py

from __future__ import division
import sys, random, time
from PyQt4 import QtGui, QtCore
#from qt import *
import main
import globals as gl
from threading import *
import cfg

colour_black = QtGui.QColor(0, 0, 0, 255)
colour_white = QtGui.QColor(255, 255, 255, 255)
pen = QtGui.QPen(colour_black)


class MainWindow(QtGui.QWidget):
    """ Main graphical window
    """
    def __init__(self, agents,  space,  parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ag = agents
        self.space = space
        self.setGeometry(300, 100, gl.x_scale * 100,  gl.y_scale * 100)
        title = 'Categories'
        self.setWindowTitle(title)

    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        
        if gl.loop_running:
#            label = str(self.ag[1].get_n_concepts())
#            paint.drawText(15, 50, label)  
            
            x_size = (gl.x_scale * 0.66) * 100
            y_size = (gl.y_scale * 0.9) * 100
            paint.drawLine(20,40, 20, y_size)
            paint.drawLine(20, y_size, x_size, y_size)
            for i in self.ag:
                if i.agent_type is "basic":
                    x_step = x_size/cfg.n_training_datasets
                    x = 1
                    old_y = 0
                    for j in i.concept_history:
                        paint.drawLine( 20 + (x * x_step), y_size - (j*20), 20 + ((x-1) * x_step), y_size - (old_y*20) )
                        x += 1
                        old_y = j
            
        else:
            #RGB colour space
            if self.space == "rgb":
                y2 = 0
                for i in self.ag:
                    text = 'Categories of "' + i.agent_name + '"'
                    paint.drawText(900, 20 + y2, text)
                    count = 0
                    x = 0
                    y = 0
                    y += y2
                    data_list = i.cp.get_all_concept_coordinates()
                    #label_list = i.get_labels()
                    while count < len(data_list):
                        r = data_list[count][0][1]
                        g = data_list[count][1][1]
                        b = data_list[count][2][1]
                        color = QtGui.QColor(r, g, b, 255)
                        paint.setPen(colour_black)
                        paint.setBrush(color)
                        paint.drawRect(15+x, 15+y, 30, 20)
                        try:
                            label = i.get_label(i.cp.concepts[count][0])
                            paint.drawText(15+x, 50+y, label)
                        except IndexError:
                            pass                   
                        if x < 800:
                            x += 60   
                        else:
                            x = 0
                            y += 50
                        count += 1
                    
                    y2 += 250
                
            # 4D figure space
            if self.space == "4df":
                y2 = 0
                for i in self.ag:
                    text = 'Categories of "' + i.agent_name + '"'
                    paint.drawText(1000, 20 + y2, text)
                    x = 0
                    y = 10
                    y += y2
                    count = 0                
                    data_list = i.cp.get_all_concept_coordinates()
                    label_list = i.get_labels()
                    paint.setBrush(colour_black)
                    while count < len(data_list):
                        legs = data_list[count][0][1]
                        neck = data_list[count][1][1]
                        tail = data_list[count][2][1]
                        ears = data_list[count][3][1]
                        pen.setWidth(1)
                        paint.setPen(pen)
                        paint.drawEllipse(15+x, 15+y, 10, 10) # body
                        pen.setWidth(legs)
                        paint.setPen(pen)
                        paint.drawLine( 17+x, 25+y, 17+x, 33+y ) #leg1
                        paint.drawLine( 23+x, 25+y, 23+x, 33+y ) #leg2
                        pen.setWidth(neck)
                        paint.setPen(pen)
                        paint.drawLine( 20+x, 20+y, 35+x, 8+y ) #neck
                        pen.setWidth(tail)
                        paint.setPen(pen)
                        paint.drawLine( 15+x, 17+y, 12+x, 15+y ) #tail
                        pen.setWidth(ears)
                        paint.setPen(pen)
                        paint.drawLine( 34+x, 4+y, 34+x, 0+y ) # ear
                        pen.setWidth(1)
                        paint.setPen(pen)
                        paint.setBrush(colour_white)
                        paint.drawEllipse(30+x, 4+y, 8, 8) # head
                        paint.setBrush(colour_black)
                        try:
                            label = label_list[count] + ":"
                            paint.drawText(15+x, 50+y, label)
                        except IndexError:
                            pass
                        text = str((count/4)+1)
                        paint.drawText(x + 67, y + 50, text)
    
                        if x < 800:
                            x += 72   
                        else:
                            x = 0
                            y += 55
                        count += 1
                        
                    y2 += 250
                
        paint.end()
        


    
class StartLayout():
    """ Starts the main graphical window and initiates the main running thread
    """
    def __init__(self, agents,  space):
        app = QtGui.QApplication(sys.argv)
        main_window = MainWindow(agents, space)
        main_window.show()
        self.thread1 = main.MainThread(main_window)
        self.thread1.start()
        app.exec_()
    
