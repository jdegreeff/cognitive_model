# layout.py

import sys, random
from PyQt4 import QtGui, QtCore

colour_black = QtGui.QColor(0, 0, 0, 255)
colour_white = QtGui.QColor(255, 255, 255, 255)
pen = QtGui.QPen(colour_black)

class ColorWindow(QtGui.QWidget):
    def __init__(self, agents,  space,  parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ag = agents
        self.space = space
        self.setGeometry(300, 100, 1200, 700)
        title = 'Categories'
        self.setWindowTitle(title)

    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
#        text = "Number of categories: " + str(len(self.ag.get_tags()))
#        paint.drawText(440, 20, text)
        
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
                label_list = i.get_labels()
                print len(data_list), len(label_list)
                while count < len(data_list):
                    r = data_list[count][0][1]
                    g = data_list[count][1][1]
                    b = data_list[count][2][1]
                    color = QtGui.QColor(r, g, b, 255)
                    paint.setPen(colour_black)
                    paint.setBrush(color)
                    paint.drawRect(15+x, 15+y, 30, 20)
                    try:
                        label = label_list[count]
                    except IndexError:
                        print "Error"
                    paint.drawText(15+x, 50+y, label)
                    if x < 800:
                        x += 50   
                    else:
                        x = 0
                        y += 50
                    count += 1
                
                y2 += 250
            
        # 4D figure space
        if self.space == "4df":
            x = 0
            y = 10
            count = 0
            paint.setBrush(colour_black)
            while count < len(self.ag.structure):
                legs = self.ag.structure[count][1][3]
                neck = self.ag.structure[count+1][1][3]
                tail = self.ag.structure[count+2][1][3]
                ears = self.ag.structure[count+3][1][3]
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
                text = str((count/4)+1)
                paint.drawText(x + 15, y + 50, text)
                if x < 360:
                    x += 40   
                else:
                    x = 0
                    y +=70
                count += 4
                
            # draw connected category for every label
            x = 0
            y += 100
            for i in self.ag.labels:
                values = self.ag.matrix[self.ag.labels.index(i)]
                max_index = basic_model.posMax(values)
                cat = self.ag.categories[max_index]
                for count, j in enumerate(self.ag.structure):
                    if cat == j[0]:
                        legs = self.ag.structure[count][1][3]
                        neck = self.ag.structure[count+1][1][3]
                        tail = self.ag.structure[count+2][1][3]
                        ears = self.ag.structure[count+3][1][3]
                        break
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
                paint.drawLine( 15+x, 17+y, 12+x, 15+yi ) #tail
                pen.setWidth(ears)
                paint.setPen(pen)
                paint.drawLine( 34+x, 4+y, 34+x, 0+y ) # ear
                pen.setWidth(1)
                paint.setPen(pen)
                paint.setBrush(colour_white)
                paint.drawEllipse(30+x, 4+y, 8, 8) # head
                paint.setBrush(colour_black)
                
                text = i + ": " + str(max_index+1)
                paint.drawText(x + 10, y + 50, text)
                
                x +=60
                
            
        paint.end()


def run(agents,  space):
    app = QtGui.QApplication(sys.argv)
    dt = ColorWindow(agents,  space)
    dt.show()
    app.exec_()

