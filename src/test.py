#
#i = 3
#if i == (1 or 2):
#    print "yes"
#else:
#    print "no"


#def function(i):
#    x = 0 
#    while x < i:
#        print "test"
#        return x
#        x += 1
#    print "end"
#    
#print function(5)

#!/usr/bin/python

# burning.py

#import time
#import sys
#from PyQt4 import QtGui, QtCore
#
#
#class Widget(QtGui.QLabel):
#    def __init__(self, parent):
#        QtGui.QLabel.__init__(self, parent)
#        self.setMinimumSize(1, 30)
#        self.parent = parent
#
#    def paintEvent(self, event):
#        paint = QtGui.QPainter()
#        paint.begin(self)
#
#        paint.drawText(30, 30, str(self.parent.count))
#        paint.end()
#
#
#class Burning(QtGui.QWidget):
#    def __init__(self, parent=None):
#        QtGui.QWidget.__init__(self, parent)
#        self.count = 0
#
#        self.wid = Widget(self)
#
#        hbox = QtGui.QHBoxLayout()
#        hbox.addWidget(self.wid)
#        vbox = QtGui.QVBoxLayout()
#        vbox.addStretch(1)
#        vbox.addLayout(hbox)
#        self.setLayout(vbox)
#
#        self.setGeometry(300, 300, 300, 220)
#        self.setWindowTitle('Burning')
#        self.start()
#        
#    def start(self):
#        while self.count < 1000000:
#            self.wid.repaint()
#            #time.sleep(1)
#            self.count += 1
#
#    def changeValue(self, event):
#        self.cw = self.slider.value()
#        self.wid.repaint()
#
#
#app = QtGui.QApplication(sys.argv)
#dt = Burning()
#dt.show()
#app.exec_()



#!/usr/bin/python

# progressbar.py

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore


class ProgressBar(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('ProgressBar')

        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.button = QtGui.QPushButton('Start', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(40, 80)

        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.onStart)

        self.timer = QtCore.QBasicTimer()
        self.step = 0;


    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText('Start')
        else:
            self.timer.start(100, self)
            self.button.setText('Stop')


app = QtGui.QApplication(sys.argv)
icon = ProgressBar()
icon.show()
app.exec_()

