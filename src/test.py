from Tkinter import *

root = Tk()

# All of this would do better as a subclass of Canvas with specialize methods

def drawcircle(canv,x,y,rad):
    # changed this to return the ID
    return canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')

def movecircle(canv, cir):
    canv.move(cir,-1,-1)

def callback(event):
    movecircle(canvas, circ1)
    movecircle(canvas, circ2)
    
canvas = Canvas(width=600, height=200, bg='white')
canvas.bind("<Button-1>", callback)
canvas.pack(expand=YES, fill=BOTH)


text = canvas.create_text(50,10, text="tk test")

#i'd like to recalculate these coordinates every frame
circ1=drawcircle(canvas,100,100,20)          
circ2=drawcircle(canvas,500,100,20)

root.mainloop()
#
#import time
#from numpy import *
#import Gnuplot, Gnuplot.funcutils
#
#
#g = Gnuplot.Gnuplot(debug=0)
#g.title('A simple example') # (optional)
#g('set data style linespoints') # give gnuplot an arbitrary command
#
#d = Gnuplot.Data([0.0, 0.0, 0.0], [0.0, 1.0, 2.0])
#g.title('test')
#g.xlabel('interactions')
#g.ylabel('test')
#g.set_range("xrange", (0.0, 3.0))
#g.set_range("yrange", (0.0, 3.0))
## Plot a function alongside the Data PlotItem defined above:
#g.plot(d)
#raw_input('Please press return to continue...\n')

#x = [0.0, 0.5, 1.0]
#y1 = [0.0, 1.0, 2.0]

#stop = 100000
#count = 50
#x = range(count)
#y = range(count)
#w = range(50,0,-1)
#z = range(50,0,-1)
#g.set_range("yrange", (0.0, 50.0))
#g.set_range("xrange", (0.0, 50.0))
#d1 = Gnuplot.Data(x, y)
#d2 = Gnuplot.Data(x, z)
#g.plot(d1,d2)
#while count < stop:
#    x = range(count)
#    y = range(count)
#    g.refresh()
#    count += 1
# Notice how this plotitem is created here but used later?  This
# is convenient if the same dataset has to be plotted multiple
# times.  It is also more efficient because the data need only be
# written to a temporary file once.
#d = Gnuplot.Data(x, y1,
#                 title='calculated by python',
#                 with_='points 3 3')
#g.title('Data can be computed by python or gnuplot')
#g.xlabel('x')
#g.ylabel('x squared')
## Plot a function alongside the Data PlotItem defined above:
#g.plot(d)
raw_input('Please press return to continue...\n')


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



#import sys, time
#import globals as gl
#from threading import *
#from qt import *
#
#
#class Painting(QWidget):
#
#    def __init__(self, *args):
#        apply(QWidget.__init__,(self, ) + args)
#        self.repaint(1)
#
#    def paintEvent(self, ev):
#        self.p = QPainter()
#        self.p.begin(self)
#        
#        label = str(gl.number)
#        self.p.drawText(15, 50, label)
#        
#        self.p.flush()
#        self.p.end()
#
#class TextThread(Thread):
#
#    def __init__(self, name, painter, *args):
#        self.counter=0
#        self.name=name
#        self.p = painter
#        apply(Thread.__init__, (self, ) + args)
#
#    def run(self):
#        while self.counter < 200:
#            gl.number += 1
#            self.counter = self.counter + 1
#            time.sleep(1)
#            self.p.repaint()
#
#
#class MainWindow(QMainWindow):
#
#    def __init__(self, *args):
#        apply(QMainWindow.__init__, (self,) + args)
#        self.setGeometry(300, 100, 1200, 700)
#        self.number = 0
#        self.painting=Painting(self)
#        self.setCentralWidget(self.painting)
#        self.thread1=TextThread("thread1", self.painting)
#        self.thread1.start()
#
#
#def main(args):
#    app=QApplication(args)
#    win=MainWindow()
#    win.show()
#    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
#    app.exec_loop()
#  
#if __name__=="__main__":
#    main(sys.argv)



#from lxml import etree
#
#root = etree.Element("root")
#etree.SubElement(root, "child").text = "Child 1"
#etree.SubElement(root, "child").text = "Child 2"
#another = etree.SubElement(root, "another")
#another.text = "try"
#
#etree.SubElement(another, "test").text = "test 3"
#
#print(etree.tostring(root, pretty_print=True))
#
#out = open('output.xml','w')
#out.write ( etree.tostring(root, xml_declaration=True,) )



# -*- coding: utf-8 -*-
# parser.py
# parses agents cs xml
#
#from __future__ import division
#from lxml import etree
#
#fileHandle = open ('CS_teacher.xml')     # read file
#tree = etree.parse(fileHandle)        # parse to ElementTree object
#fileHandle.close()            # close file
#root = tree.getroot()            # get root as Element object
#
##print(etree.tostring(tree))
#
#listing = root.getchildren()
##print len(listing)
#for i in listing:
#    if i.tag == "agent":
#        print i.text
#    elif i.tag == "concept":
#        print "concept: " + str(i.items())
#        for j in i:
#            if j.tag == "domains":
#                for l in j:
#                    print "domain: " + str(l.items())
#                    for k in l:
#                        print k.tag
#                        for n in k:
#                            print n.tag
#                            print n.text
#            else:
#                for m in j:
#                    print m.tag + ": " + m.text