##!/usr/bin/env python
#import sys, time
#from qt import * # Generally advertised as safe
#import cfg
#import globals as gl
#import main
#
#class MainWindow(QWidget):
#    def __init__(self, *args):
#        QWidget.__init__(self, *args)
#        self.setGeometry(300, 100, cfg.x_scale * 100,  cfg.y_scale * 100)
#        self.setCaption("Categories")
#        self.layout = QGridLayout(self, 3, 2, 5, 10)
#        self.tsdisp = QTextEdit(self)
#        self.tsdisp.setMinimumSize(250, 300)
#        self.tsdisp.setTextFormat(Qt.PlainText)
#        self.tscount = QLabel("", self)
#        self.tscount.setFont(QFont("Sans", 24))
#        self.log = QPushButton("&Log Timestamp", self)
#        self.quit = QPushButton("&Quit", self)
#        self.layout.addMultiCellWidget(self.tsdisp, 0, 2, 0, 0)
#        self.layout.addWidget(self.tscount, 0, 1)
#        self.layout.addWidget(self.log, 1, 1)
#        self.layout.addWidget(self.quit, 2, 1)
#        self.connect(self.log, SIGNAL("clicked()"), self.counter)
#        self.connect(self.quit, SIGNAL("clicked()"), self.close)
#
#        
#    def paintEvent(self, event):
#        paint = QPainter()
#        paint.begin(self)
#
#        n_games = str(gl.agent1.n_discrimination_games)
#        test = "test"
#        self.tscount.setText(test)
#        
#        paint.end()
#
#        
#    def log_timestamp(self):
#        stamp = time.ctime()
#        self.tsdisp.append(stamp)
#        self.tscount.setText(str(self.tsdisp.lines()))
#        
#        
#    def counter(self):
#        i = 0
#        while i < 1000:
#            i += 1
#            time.sleep(0.1)
#            self.tsdisp.append(str(i))
#            self.tscount.setText(str(self.tsdisp.lines()))
#        

# This is a much more sophisticated example using more of Tkinter's
# features to show how to create a new custom class of widgets called
# MinMax made of two Entry widgets and a Scale widget.  When more that
# one widget are combined to make a more complex one, it is called a
# "compound widget". The Entry widgets hold the minimum and maximum
# values of the scale. When the user changes these values, the Scale
# is updated.  
# compound widget that allows the user to set the min and max values of a scale

import sys
from qt import *

class MainWindow(QMainWindow):
    val = 17
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)

        self.vlayout = QHBoxLayout(self, 10, 5)

        self.labelValue = QLabel(str(MainWindow.val), self)
        self.down = QPushButton("Lower", self)
        self.up = QPushButton("Higher", self)

        self.vlayout.addWidget(self.down)
        self.vlayout.addWidget(self.labelValue)
        self.vlayout.addWidget(self.up)

        self.connect(self.down, SIGNAL("clicked()"), self.reduce)
        self.connect(self.up, SIGNAL("clicked()"), self.increase)

    def reduce(self):
        MainWindow.val -= 1
        self.setval()

    def increase(self):
        MainWindow.val += 1
        self.setval()

    def setval(self):
        self.labelValue.setText(str(MainWindow.val))

def main(args):
    app=QApplication(args)
    win=MainWindow()
    win.show()
    app.connect(app, SIGNAL("lastWindowClosed()")
                , app
                , SLOT("quit()")
                )
    app.exec_loop()

if __name__=="__main__":
        main(sys.argv)