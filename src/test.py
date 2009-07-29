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

from __future__ import division
from lxml import etree

fileHandle = open ('CP_teacher.xml')     # read file
tree = etree.parse(fileHandle)        # parse to ElementTree object
fileHandle.close()            # close file
root = tree.getroot()            # get root as Element object

#print(etree.tostring(tree))

listing = root.getchildren()
#print len(listing)
for i in listing:
    if i.tag == "agent":
        print i.text
    elif i.tag == "concept":
        print "concept: " + str(i.items())
        for j in i:
            if j.tag == "domains":
                for l in j:
                    print "domain: " + str(l.items())
                    for k in l:
                        print k.tag
                        for n in k:
                            print n.tag
                            print n.text
            else:
                for m in j:
                    print m.tag + ": " + m.text