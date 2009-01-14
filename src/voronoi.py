## Code for constructing and displaying Voronoi Diagrams

import Image, ImageDraw
from math import sqrt
from operator import add
from random import uniform

points = []     # Contains Feature points as list of point objects
lines = []      # Contains Voronoi lines and segments as list of Line objects

queue = []      # Contains event queue as list of ['point', [x,y]] entries or
                # ['circle', [x,y],radius,line1,line2] entries (line1 and line2
                # are Line objects. Sorted by increasing x, then increasing y

class Point:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.lines = []

    def dist(self,other):
        if other.isSeg():
            return other.dist(self)
        else:
            dx = self.x - other.x
            dy = self.y - other.y
            return sqrt(dx*dx + dy*dy)

    def ldist(self, other):
        return self.dist(other)

    def adjacent(self, other):
        "Is this point and endpoint for that segment?"
        if other.isPt():
            return 0
        return other.adjacent(self)

    def isPt(self):
        return 1

    def isSeg(self):
        return 0

    def __repr__(self):
        return "Point:(%2.4f,%2.4f)"%(self.x,self.y)

    def bisect(self, other):
        "Line equidistant from two points"
        if other.isSeg():
            return other.bisect(self)
        x = float(self.x+other.x)/2
        y = float(self.y+other.y)/2
        li = Line(self.x-other.x, self.y-other.y, x, y)
        li.points = [self, other]
        return li

class Segment:
    def __init__(self, pt1, pt2):
        self.x1 = pt1[0]
        self.y1 = pt1[1]
        self.p1 = Point(pt1)
        self.x2 = pt2[0]
        self.y2 = pt2[1]
        self.p2 = Point(pt2)
        self.line = line_via(self.x1, self.y1, self.x2, self.y2)
        t1 = self.line.get_t(self.x1, self.y1)
        t2 = self.line.get_t(self.x2, self.y2)
        if t1>t2:
            self.line.tmax = t1
            self.line.tmin = t2
        else:
            self.line.tmin = t1
            self.line.tmax = t2
            
        self.lines = []

    def dist(self,other):
        if other.isSeg():
            return min(self.dist(other.p1),
                       self.dist(other.p2),
                       other.dist(self.p1),
                       other.dist(self.p2))
        else:
            [x1,y1] = self.line.nearest_pt(other.x,other.y)
            t1 = self.line.get_t(x1,y1)
            if self.line.in_range(t1):
                dx = x1 - other.x
                dy = y1 - other.y
                return sqrt(dx*dx + dy*dy)
            else:
                return min(self.p1.dist(other), self.p2.dist(other))

    def ldist(self,point):
        "Distance to point, treating self as line, not segment"
        return self.line.dist(point.x,point.y)
    
    def adjacent(self, other):
        "Does this segment have that point as an endpoint?"
        if other.isSeg():
            return 0
        return self.line.get_t(other.x,other.y) != None

    def bisect(self, other):
        if other.isSeg():
            li = self.line.bisect(other.line)
            li.points = [self, other]
            return li
        else:
            # If point is on line, return perpendicular
            if self.line.get_t(other.x, other.y) != None:
                li = Line(-self.line.b, self.line.a, other.x, other.y)
                li.points = [self, other]
                return li
            else:           # If not, return parabola
                return Parabola(other, self)

    def over_pt(self, pt):
        "Is point pt 'over' self, i.e. between perpendiculars?"
        pt_on_line = self.line.nearest_pt(pt.x, pt.y)
        linet = self.line.get_t(pt_on_line[0], pt_on_line[1])
        return -0.00001 <= linet <= 1.00001
    
    # Type checking functions
    def isPt(self):
        return 0

    def isSeg(self):
        return 1

class Line:
    def __init__(self, a, b, x1, y1):
        if a==0 and b==0:
            raise InvalidCoefficientError
        self.a = a
        self.b = b
        self.x1 = x1
        self.y1 = y1
        self.c = a*x1+b*y1
        self.tmin = None
        self.tmax = None
        self.points = []

    def __repr__(self):
        return "Line : " + `self.a`+"*x + "+`self.b` + "*y = " + `self.c`

    def get_t(self, x, y):
        "Determine t for given point (if on line)."
        if self.b==0 and self.a==0:
            return None
        if self.b==0:
            if abs(x-self.x1)<0.001:
                return float(y-self.y1)/self.a
            else:
                return None
        elif self.a == 0:
            if abs(y-self.y1)<0.001:
                return float(self.x1-x)/self.b
            else:
                return None
        else:
            t1 = float(y-self.y1)/self.a
            t2 = float(self.x1-x)/self.b
            p1 = Point(self.eval_t(t1))
            p2 = Point(self.eval_t(t2))
            if p1.dist(p2) > 0.001:
                return None
            else:
                return (t1+t2)/2

    def eval_t(self, t):
        "Find x-y point for given t"
        x = self.x1 - self.b*t
        y = self.y1 + self.a*t
        return [x,y]

    def in_range(self, t):
        "Is t within preset t ranges?"
        if self.tmin != None and t<self.tmin:
            return 0
        if self.tmax != None and t>self.tmax:
            return 0
        return 1

    def line_isect(self, other):
        "Determine intersection of 2 lines"
        if other.isParab():
            return other.line_isect(self)
        d = self.b*other.a-self.a*other.b
        if d==0:
            return []
        f1 = self.b*other.c - self.c*other.b
        f2 = self.c*other.a - self.a*other.c
        return [[float(f1)/d, float(f2)/d]]

    def seg_isect(self, other):
        """Determine intersection of two lines.  This function
        Takes into account the fact that lines can also be rays or segments."""
        z = self.line_isect(other)
        rv = []
        for i in z:
            [x,y] = i
            t1 = self.get_t(x,y)
            t2 = other.get_t(x,y)
            if self.in_range(t1) and other.in_range(t2):
                rv.append(i)
        return rv

    def dist(self, x, y):
        "Distance from line to point"
        F = self.a*x + self.b*y - self.c
        d = self.a**2 + self.b**2
        return abs(F)/sqrt(d)

    def nearest_pt(self, x, y):
        "Point on line closest to given point"
        F = self.b*x - self.a*y
        d = float(self.a**2 + self.b**2)
        cx = (self.a*self.c + self.b*F)/d
        cy = (self.b*self.c - self.a*F)/d
        return [cx,cy]

    def bisect(self, other):
        "Angle bisector of intersection between two lines."
        ipoint = self.line_isect(other)
        if ipoint == []:    # bisect parallel lines
            midx = float(self.x1 + other.x1)/2
            midy = float(self.y1 + other.y1)/2
            return Line(self.a,self.b,midx, midy)
        else:               # bisect intersecting lines with angle bisector
            [ix, iy] = ipoint[0]
            t1 = self.get_t(ix,iy)
            # There are two angle bisectors
            # By default, this method divides the respective p1's (t=0)
            # of each line.  However, if either p1 is very near the intersecting
            # point, the corresponding p2 is used instead.
            # This method finds two points on each line equidistant from
            # the intersection, and draws a line through their midpoint.
            if -0.01 < t1 < 0.01:
                if t1>1:
                    t1 = t1 - sqrt(other.a**2 + other.b**2)
                else:
                    t1 = t1 + sqrt(other.a**2 + other.b**2)
            else:
                if t1>0:
                    t1 = t1 - sqrt(other.a**2 + other.b**2)
                else:
                    t1 = t1 + sqrt(other.a**2 + other.b**2)
            t2 = other.get_t(ix,iy)
            if -0.01 < t2 < 0.01:
                if t2>1:
                    t2 = t2 - sqrt(self.a**2 + self.b**2)
                else:
                    t2 = t2 + sqrt(self.a**2 + self.b**2)
            else:
                if t2>0:
                    t2 = t2 - sqrt(self.a**2 + self.b**2)
                else:
                    t2 = t2 + sqrt(self.a**2 + self.b**2)
            [x1,y1] = self.eval_t(t1)
            [x2,y2] = other.eval_t(t2)
            midx = float(x1+x2)/2
            midy = float(y1+y2)/2
            return line_via(ix, iy, midx, midy)

    def cap_t(self, newt, other_pt):
        'Set a new endpoint on this line away from the "other" point'
        delta = 0
        center = Point(self.eval_t(newt))
        radius = max(other_pt.ldist(center),1)
        unit = radius*0.1/sqrt(self.a**2+self.b**2)
        # In general, the wrong direction is the one where the other point is closer
        # than the feature points.  Certain issues with lines and adjacencies make this
        # a bit more complicated.  This method moves along the line in both directions until
        # it is clear which direction is correct.  The wrong one is capped off.
        while delta < 20*unit:       #This should only take 1 point, but just in case...
            delta = delta + unit
            pdec = Point(self.eval_t(newt-delta))
            pinc = Point(self.eval_t(newt+delta))
            if self.points[0].adjacent(other_pt) and self.points[1].adjacent(other_pt):
                #Feature segments are adjacent edges
                if self.points[0].dist(pinc) < other_pt.dist(pinc):
                    self.tmin = newt
                    break
                elif self.points[0].dist(pdec) < other_pt.dist(pdec):
                    self.tmax = newt
                    break
            elif self.points[0].adjacent(self.points[1]) and (self.points[0].adjacent(other_pt) or self.points[1].adjacent(other_pt)):
                #Features are adjacent vertex and edge, other feature is next edge
                if other_pt.over_pt(pdec):
                    self.tmin = newt
                    break
                elif other_pt.over_pt(pinc):
                    self.tmax = newt
                    break
            elif self.points[0].adjacent(other_pt):
                if self.points[0].dist(pinc) < other_pt.dist(pinc) - 0.01 or \
                   self.points[0].dist(pdec) > other_pt.dist(pdec) + 0.01:
                    self.tmin = newt
                    break
                elif self.points[0].dist(pdec) < other_pt.dist(pdec) - 0.01 or \
                     self.points[0].dist(pinc) > other_pt.dist(pinc) + 0.01:
                    self.tmax = newt
                    break
            elif self.points[1].adjacent(other_pt):
                if self.points[1].dist(pinc) < other_pt.dist(pinc) - 0.01 or \
                   self.points[1].dist(pdec) > other_pt.dist(pdec) + 0.01:
                    self.tmin = newt
                    break
                elif self.points[1].dist(pdec) < other_pt.dist(pdec) - 0.01 or \
                     self.points[1].dist(pinc) > other_pt.dist(pinc) + 0.01:
                    self.tmax = newt
                    break
            else:
                #Default case: three independent features
                if self.points[0].ldist(pdec) > other_pt.ldist(pdec) + 0.01:
                    self.tmin = newt
                    break
                elif self.points[0].ldist(pinc) > other_pt.ldist(pinc) + 0.01:
                    self.tmax = newt
                    break
        else:       #Somehow above method failed.
            print self, self.tmin, self.tmax, newt, other_pt
            raise Cap_tError
            
    # Type checking.
    def isLine(self):
        return 1

    def isParab(self):
        return 0



class Parabola:
    def __init__(self, focus, directrix):
        self.focus = focus
        self.directrix = directrix.line
        direc = directrix.line
        d = direc.a**2 + direc.b**2
        F = direc.a*focus.x+direc.b*focus.y-direc.c
        self.a = direc.a*F/(2.0*d)
        self.b = direc.b*F/(2.0*d)
        x0 = (0.5*direc.a**2 + direc.b**2)*focus.x + 0.5*direc.a*direc.c - 0.5*direc.a*direc.b*focus.y
        y0 = (direc.a**2 + 0.5*direc.b**2)*focus.y + 0.5*direc.b*direc.c - 0.5*direc.a*direc.b*focus.x
        self.x1 = x0/d
        self.y1 = y0/d
        self.tmin = None
        self.tmax = None
        self.points = [focus, directrix]

    def eval_t(self, t):
        "Determine x-y coordinates for given t"
        x = self.a*t*t + 2*self.b*t + self.x1
        y = self.b*t*t - 2*self.a*t + self.y1
        return [x,y]

    def get_t(self, x, y):
        "Find t given coordinates"
        tx = quadratic(self.a, 2*self.b, self.x1-x)
        ty = quadratic(self.b, -2*self.a, self.y1-y)
        for i in tx:
            dist = Point(self.eval_t(i)).dist(Point([x,y]))
            if dist < 0.01:
                return i
        for j in ty:
            dist = Point(self.eval_t(j)).dist(Point([x,y]))
            if dist < 0.01:
                return j
        return None

    def in_range(self, t):
        "Is t within preset t ranges?"
        if self.tmin != None and t<self.tmin:
            return 0
        if self.tmax != None and t>self.tmax:
            return 0
        return 1

    def line_isect(self, other):
        "Determine intersection with other line or parabola"
        if other.isLine():
            qa = self.a*other.a + self.b*other.b
            qb = 2.0*(self.b*other.a - self.a*other.b)
            qc = self.x1*other.a + self.y1*other.b - other.c
            tset = quadratic(qa, qb, qc)
            return map(self.eval_t, tset)
        else:       #Parabola intersects parabola; find a line to intersect
            if self.focus == other.focus:
                li = self.directrix.bisect(other.directrix)
                rv = self.seg_isect(li)
                if rv==[]:          #Wrong line, try perpendicular
                    li = Line(-li.b, li.a, li.x1, li.y1)
                    rv =  self.seg_isect(li)
                return rv
            else:
                return self.seg_isect(self.focus.bisect(other.focus))
            
    def seg_isect(self, other):
        """Determine intersection of two lines.  This function
        Takes into account the fact that lines can also be rays or segments."""
        z = self.line_isect(other)
        rv = []
        for i in z:
            [x,y] = i
            t1 = self.get_t(x,y)
            t2 = other.get_t(x,y)
            if self.in_range(t1) and other.in_range(t2):
                rv.append(i)
        return rv

    def cap_t(self, newt, other_pt):
        'Set a new endpoint on this line away from the "other" point'
        if self.points[0].isSeg():
            dirseg = self.points[0]
        else:
            dirseg = self.points[1]
        if dirseg.adjacent(other_pt):
            # Other point adjacent to directrix, cap over directrix segment
            unit = 1/sqrt(self.a**2+self.b**2)
            pdec = Point(self.eval_t(newt-0.5))
            pinc = Point(self.eval_t(newt+0.5))
            if dirseg.dist(pdec) == other_pt.dist(pdec):
                self.tmin = newt
            else:
                self.tmax = newt
        elif self.focus.adjacent(other_pt):
            # Other segment adjacent to focus, cap away form other segment.
            unit = 0.2/sqrt(self.a**2+self.b**2)
            pdec = Point(self.eval_t(newt-0.5))
            pinc = Point(self.eval_t(newt+0.5))
            if self.focus.dist(pdec) == other_pt.dist(pdec):
                self.tmax = newt
            else:
                self.tmin = newt
        else:   # Otherwise, cap away from third point
            delta = 0
            unit = 0.2/sqrt(self.a**2+self.b**2)
            while delta < 20*unit:
                delta = delta + unit
                pdec = Point(self.eval_t(newt-delta))
                pinc = Point(self.eval_t(newt+delta))
                if self.focus.dist(pdec) > other_pt.dist(pdec) or \
                   self.focus.dist(pinc) < other_pt.dist(pinc):
                    self.tmin = newt
                    break
                elif self.focus.dist(pinc) > other_pt.dist(pinc) or \
                     self.focus.dist(pdec) < other_pt.dist(pdec):
                    self.tmax = newt
                    break
            else:
                raise Cap_tError

    def isLine(self):
        return 0

    def isParab(self):
        return 1

qsort = lambda x,y: cmp(x[1],y[1]) or cmp(y[0],x[0])

def line_via(x1, y1, x2, y2):
    "Line through two points"
    return Line(y2-y1, x1-x2, x1, y1)

def quadratic(a, b, c):
    "Solve a*x**2+b*x+c=0"
    if a**2<=0.00001:
        if b**2 <=0.00001:
            return []
        else:
            return [-float(c)/b]
    d = b*b-4*a*c
    if d<-0.0001:
        return []
    if -0.0001<=d<=0.0001:
        return [-b/(2.0*a)]
    else:
        return [(-b-sqrt(d))/(2*a), (-b+sqrt(d))/(2*a)]

def bisect(x1, y1, x2, y2):
    "Line equidistant from two points"
    x = float(x1+x2)/2
    y = float(y1+y2)/2
    return Line(x1-x2, y1-y2, x, y)

def generate_graph():
    "Construct Voronoi Diagram.  Queue must be preset and sorted."
    global points, lines
    while queue != []:
        next = queue.pop(0)
        if next[0] == 'point':
            others = []
            # If this point has adjacent segments, process them too.
            while queue and queue[0][0] == 'line' and queue[0][1] == next[1]:
                others.append(queue.pop(0)[2])
            if others == []:
                new_pt = process_pt(next[1])
            else:
               new_pt = process_line(next[1],others)
            while queue and queue[0][0] == 'bisect' and queue[0][1] == next[1]:
                process_bisect(new_pt, queue.pop(0)[2])
        #elif next[0] == 'line':
        #    new_pt = process_pt(next[1],next[2])
        #    while queue and queue[0][0] == 'bisect' and queue[0][1] == next[1]:
        #        process_bisect(new_pt, queue.pop(0)[2])
        else:
            apex,radius,line1,line2 = next[1:]
            process_circle(apex[0],apex[1],radius,line1,line2)

def animate_graph(path):
    "Construct Voronoi diagram and animate steps.  Queue must be preset and sorted."
    index = 0
    global points, lines
    im = anim_preprocess()
    while queue != []:
        tmp = im.copy()
        next = queue.pop(0)
        print "index=%d, next=%s"%(index,`next`)
        #Draw red vertical scan line
        scanx = next[1][0]
        draw_line(line_via(scanx,-1000,scanx,1000),tmp,color=(255,0,0))
        if next[0] == 'point':
            others = []
            # If this point has adjacent segments, process them too.
            while queue and queue[0][0] == 'line' and queue[0][1] == next[1]:
                others.append(queue.pop(0)[2])
            if others == []:
                new_pt = process_pt(next[1])
            else:
                new_pt = process_line(next[1],others)
            while queue and queue[0][0] == 'bisect' and queue[0][1] == next[1]:
                process_bisect(new_pt, queue.pop(0)[2])
        #elif next[0] == 'line':
        #    new_pt = process_pt(next[1],next[2])
        #    while queue and queue[0][0] == 'bisect' and queue[0][1] == next[1]:
        #        process_bisect(new_pt, queue.pop(0)[2])
        else:
            apex,radius,line1,line2 = next[1:]
            process_circle(apex[0],apex[1],radius,line1,line2)
        for pt in points:       #Draw processed points in black.
            if pt.isPt():
                draw_pt(pt,tmp)
            else:
                draw_line(pt.line,tmp,color=(0,0,0))
        for q in queue: 
            if q[0]=='point':   #Draw unprocessed points and segments in cyan
                draw_pt(Point(q[1]),tmp,color=(0,255,255))
            elif q[0]=='line':
                draw_seg(q[1],q[2],tmp,color=(0,255,255))
            elif q[0] == 'circle':               #Draw radii of unprocessed intersection points in brown.
                apex, radius = q[1:3]
                center = [apex[0]-radius,apex[1]]
                draw_seg(apex,center,tmp,color=(200,200,0))
        for li in lines:
            if li.tmin == None or li.tmax == None:
                if li.isLine():
                    draw_line(li,tmp)                   #Draw rays and lines in green
                else:
                    draw_parab(li,tmp)
            else:                                       #Draw segments in blue  
                if li.isLine():
                    draw_line(li,tmp,color=(0,0,255))
                else:                                   
                    draw_parab(li,tmp,color=(0,0,255))
        tmp.save('%s/frame%03d.gif'%(path,index))   #Save frame
        index = index+1
    #Save image of final diagram with endpoint/segment divisions
    tmp = im.copy()
    for pt in points:
        if pt.isPt():
            draw_pt(pt,tmp)
        else:
            draw_line(pt.line,tmp,color=(0,0,0))
    for li in lines:
        if li.isLine():
            draw_line(li,tmp,(0,0,255))
        else:
            draw_parab(li,tmp,(0,0,255))
    tmp.save('%s/frame%03d.gif'%(path,index))
    #Save image of final diagram without endpoint/segment divisions
    index = index+1
    tmp = im.copy()
    for pt in points:
        if pt.isPt():
            draw_pt(pt,tmp)
        else:
            draw_line(pt.line,tmp,color=(0,0,0))
    for li in lines:
        if li.isLine():
            if li.points[0].isSeg() == li.points[1].isSeg():
                draw_line(li,tmp,(0,0,255))
        else:
            draw_parab(li,tmp,(0,0,255))
    tmp.save('%s/frame%03d.gif'%(path,index))

def process_pt(pt,pt2=None):
    """Process single point:
        1: Add perpendicular bisector to closest point
        2: Check intersections with this new line
        3: Add new events for corresponding intersections
    """
    if pt2:
        point = Segment(pt,pt2)
    else:
        point = Point(pt)
    if points != []:
        min_dist = point.dist(points[0])
        #Find closest point
        closest = points[0]
        for i in points[1:]:
            if i.adjacent(point):
                min_dist = 0
                closest = i
                break
            newdist = point.dist(i)
            if newdist < min_dist:
                closest = i
                min_dist = newdist
            elif newdist == min_dist and i.isPt() and closest.isSeg():
                #Points are closer then lines, if there is a tie
                closest = i
        # Points should not be too close together.
        # This is not a problem for lines.
        #if min_dist < 0.1 and point.isPt() and not point.adjacent(closest):
        #    return None
        # If the closest points involve a point that is not yet processed (like a second
        # point in a segment), enqueue the bisector and add it later.
        if closest.isSeg() and closest.dist(point) >= closest.p2.dist(point) and not closest.adjacent(point):
            add_bisector(closest.x2,closest.y2,point)
        elif point.isSeg() and point.dist(closest) >= point.p2.dist(closest) and not closest.adjacent(point):
            add_bisector(point.x2,point.y2,closest)
        else:
            # Add and process bisector
            newline = point.bisect(closest)
            lines.append(newline)
            newline.points = [point, closest]
            point.lines = [newline]
            # Process new intersections
            # Note: an intersection only counts if it intersects another line
            # corresponding to the closest point.
            for li in closest.lines:
                for center in li.seg_isect(newline):     # For each intersection found;
                    [x,y]=center                          # Add circle event
                    cpoint = Point([x,y])
                    radius = point.ldist(cpoint)
                    add_center(x,y,radius,li,newline)
            # Processing done; add new point and line to list
            closest.lines.append(newline)
    points.append(point)
    return point

def process_line(pt,others):
    """Process point and one or more lines:
        1: Add perpendicular bisector to closest point
        2: Check intersections with this new line
        3: Add new events for corresponding intersections
    """
    newF = [Point(pt)]      # New features
    newL = []               # New lines
    for i in others:
        newF.append(Segment(pt,i))
    for i in newF[1:]:
        newline = newF[0].bisect(i)
        i.lines.append(newline)
        newF[0].lines.append(newline)
        newL.append(newline)
    if len(newL)>=2:
        for i in range(len(newL)-1):
            for j in range(i+1,len(newL)):
                add_center(pt[0],pt[1],0,newL[i],newL[j])
    if points != []:
        # Add one more bisector, corresponding to closest feature pair.
        min_dist = newF[0].dist(points[0])
        #Find closest feature pair
        closest = points[0]
        closestN = newF[0]
        for i in points:
            if i.adjacent(newF[0]):
                min_dist = 0
                closest = i
                closestN = newF[0]
                break
            for j in newF:
                newdist = j.dist(i)
                if newdist < min_dist:
                    closest = i
                    closestN = j
                    min_dist = newdist
                elif newdist == min_dist and j == closestN and i.isPt() and closest.isSeg():
                    #Points are closer then lines, if there is a tie
                    closest = i
                #elif newdist == min_dist and i == closest and j.isPt() and closestN.isSeg():
                #    closestN = j
        # If the closest points involve a point that is not yet processed (like a second
        # point in a segment), enqueue the bisector and add it later.
        if closest.isSeg() and closest.dist(closestN) > closest.p2.dist(closestN) and not closest.adjacent(closestN):
            add_bisector(closest.x2,closest.y2,closestN)
        elif closestN.isSeg() and closestN.dist(closest) >= closestN.p2.dist(closest) and not closest.adjacent(closestN):
            add_bisector(closestN.x2,closestN.y2,closest)
        else:
            # Add and process bisector
            newline = closestN.bisect(closest)
            lines.append(newline)
            # Process new intersections
            # Note: an intersection only counts if it intersects another line
            # corresponding to the closest point.
            for li in closest.lines:
                for center in li.seg_isect(newline):     # For each intersection found;
                    [x,y]=center                          # Add circle event
                    cpoint = Point([x,y])
                    radius = closestN.ldist(cpoint)
                    add_center(x,y,radius,li,newline)
            for li in closestN.lines:
                for center in li.seg_isect(newline):     # For each intersection found;
                    [x,y]=center                          # Add circle event
                    cpoint = Point([x,y])
                    radius = closest.ldist(cpoint)
                    add_center(x,y,radius,li,newline)
            # Line processing done; add to graph
            closestN.lines.append(newline)
            closest.lines.append(newline)
    # Point and segment processing done; add to graph.
    points.extend(newF)
    lines.extend(newL)
    return newF[0]

def add_center(cx,cy,radius,line1,line2):
    "Add circle event to queue"
    global queue
    apex = [cx+radius,cy]       # Apex is point in circle furthest to right
    new_entry = ['circle',apex,radius,line1,line2]
    # Add new entry to where the apex would be, as a point
    for i in range(len(queue)):
        if apex < queue[i][1]:
            queue.insert(i,new_entry)
            break
    else:
        queue.append(new_entry)

def add_bisector(x,y,other_pt):
    "Add bisection event to queue"
    global queue
    pt = [x,y]
    new_entry = ['bisect',pt, other_pt]
    # Add new entry to where the apex would be, as a point
    for i in range(len(queue)):
        if pt < queue[i][1]:
            queue.insert(i,new_entry)
            break
    else:
        queue.append(new_entry)


def process_circle(cx,cy,radius,line1,line2):
    """Process circle event:
        1. Verify point is valid intersection.
        2. Add third line.
        3. Convert intersection point to endpoints
        4. Check new line for intersection points
    """
    cpoint = Point([cx-radius,cy])
    print "Processing circle at ",cx,cy, ", radius ",radius
    for i in points:
        # The circle goes through 3 feature points.  If there are any points
        # inside, then the center is not the closest point to all 3 feature points.
        # Thus, it is not a valid intersection point.
        if i in line1.points or i in line2.points:
            continue
        if i.dist(cpoint) < radius-0.01:
            break
    else:
        # Check that lines still intersect
        if not line1.seg_isect(line2):
            return None
        t1 = line1.get_t(cpoint.x,cpoint.y)
        t2 = line2.get_t(cpoint.x,cpoint.y)
        if not(line1.in_range(t1) and line2.in_range(t2)):
            return None
        # Add third line
        common_point = filter(lambda x,y=line2.points:x in y,line1.points)[0]
        if common_point == line1.points[0]:
            point1 = line1.points[1]
        else:
            point1 = line1.points[0]
        if common_point == line2.points[0]:
            point2 = line2.points[1]
        else:
            point2 = line2.points[0]
        # If center point is not over a feature segment, don't process.
        if point1.isSeg() and not point1.over_pt(cpoint):
            return None
        if point2.isSeg() and not point2.over_pt(cpoint):
            return None
        if common_point.isSeg() and not common_point.over_pt(cpoint):
            return None
        line3 = point1.bisect(point2)
        t3 = line3.get_t(cpoint.x,cpoint.y)
        if point1.isSeg() and point2.isSeg() and t3==None:
            # If new line is angle bisector, it may be the wrong bisector.
            # If so, replace it with its perpendicular.
            line3 = Line(line3.b, -line3.a,cpoint.x, cpoint.y)
            t3 = line3.get_t(cpoint.x,cpoint.y)
        line3.points = [point1, point2]
        # Set the intersection point as an endpoint for the three lines.
        t1 = line1.get_t(cpoint.x,cpoint.y)
        line1.cap_t(t1,point2)
        t2 = line2.get_t(cpoint.x,cpoint.y)
        line2.cap_t(t2,point1)
        t3 = line3.get_t(cpoint.x,cpoint.y)
        #if t3 != None:
        line3.cap_t(t3,common_point)
        # Now check the new line for intersections.
        # This code is just like in process_pt
        #print "line3 = ", line3
        for li in point1.lines:
            for center in li.seg_isect(line3):
                if abs(center[0]-cpoint.x)<.01 and abs(center[1]-cpoint.y)<.01:
                    continue
                [x,y]=center
                p = Point([x,y])
                radius = point1.ldist(p)
                add_center(x,y,radius,li,line3)
        point1.lines.append(line3)
        for li in point2.lines:
            for center in li.seg_isect(line3):
                if abs(center[0]-cpoint.x)<.01 and abs(center[1]-cpoint.y)<.01:
                    continue
                [x,y]=center
                p = Point([x,y])
                radius = point2.ldist(p)
                add_center(x,y,radius,li,line3)
        # Processing done; add new line to diagram.
        point2.lines.append(line3)
        lines.append(line3)

def process_bisect(point1, point2):
    """Process bisection event:
        1. Add bisecting line between points
        2. Check new line for intersection points
    """
    newline = point1.bisect(point2)
    # Now check the new line for intersections.
    # This code is just like in process_pt
    for li in point1.lines:
        for center in li.seg_isect(newline):
            [x,y]=center
            p = Point([x,y])
            radius = point1.ldist(p)
            add_center(x,y,radius,li,newline)
    point1.lines.append(newline)
    for li in point2.lines:
        for center in li.seg_isect(newline):
            [x,y]=center
            p = Point([x,y])
            radius = point2.ldist(p)
            add_center(x,y,radius,li,newline)
    # Processing done; add new line to diagram.
    point2.lines.append(newline)
    lines.append(newline)

def img_preprocess():
    "Preprocessing for single, final image."
    global height, width, scale, xtrans, ytrans
    pts = filter(lambda x:x.isPt(),points)
    num_pts = len(pts)
    xcoords = map(lambda p:p.x,pts)
    ycoords = map(lambda p:p.y,pts)
    centroid = [0,0]
    xtrans = -float(reduce(add,xcoords))/num_pts
    ytrans = -float(reduce(add,ycoords))/num_pts
    pwidth = max(xcoords)-min(xcoords)
    pheight = max(ycoords)-min(ycoords)
    height = 400
    width = height*pwidth/pheight
    scale = height/(1.5*pheight)
    #Now, create the image
    im = Image.new('RGB',(width, height),(255,255,255))
    return im

def anim_preprocess():
    "Preprocessing for animation frames"
    global height, width, scale, xtrans, ytrans
    pts = filter(lambda x:x[0]=='point',queue)
    num_pts = len(pts)
    xcoords = map(lambda p:p[1][0],pts)
    ycoords = map(lambda p:p[1][1],pts)
    centroid = [0,0]
    print "xcoords = ",xcoords
    print "ycoords = ",ycoords
    xtrans = -float(reduce(add,xcoords))/num_pts
    ytrans = -float(reduce(add,ycoords))/num_pts
    pwidth = max(xcoords)-min(xcoords)
    pheight = max(ycoords)-min(ycoords)
    height = 400
    width = height*pwidth/pheight
    scale = height/(1.5*pheight)
    #Now, create the image
    im = Image.new('RGB',(width, height),(255,255,255))
    return im

### Functions for generating random examples

def rand_pts(num,min,max):
    pts = []
    for i in range(num):
        x = uniform(min,max)
        y = uniform(min,max)
        pts.append([x,y])
    return pts

def rand_seg(num,min,max):
    lines = []
    while len(lines)<num:
        x1 = uniform(min,max)
        y1 = uniform(min,max)
        x2 = uniform(min,max)
        y2 = uniform(min,max)
        if x1>x2:
            x1,x2=x2,x1
        seg = Segment([x1,y1],[x2,y2])
        for i in lines:
            s2 = Segment(i[0],i[1])
            if seg.line.seg_isect(s2.line):
                break
            if seg.dist(s2)<0.1:
                break
        else:
            lines.append([x1,y1],[x2,y2])
    return lines

def add_rand(npts,nlines,min,max):
    pts = rand_pts(npts,min,max)
    queue.extend(map(lambda x:['point',x],pts))
    lines = rand_seg(nlines,min,max)
    for i in lines:
        queue.extend([['point',i[0]],['point',i[1]],['line',i[0],i[1]]])
    queue.sort(qsort)

def draw_pt(point,im, color=(0,0,0)):
    "Draw feature point on image"
    x = (point.x + xtrans) * scale + width/2
    y = -(point.y + ytrans) * scale + height/2
    draw = ImageDraw.Draw(im)
    draw.polygon(((x-2,y-2), (x+2,y-2), (x+2,y+2), (x-2,y+2)), fill=color)
    del draw
    
def draw_line(line, im,color=(0,255,0)):
    "Draw line on image"
    if line.tmin == None:
        x1,y1 = line.eval_t(-1000)
    else:
        x1,y1 = line.eval_t(line.tmin)
    if line.tmax == None:
        x2,y2 = line.eval_t(1000)
    else:
        x2,y2 = line.eval_t(line.tmax)
    x1 = (x1+xtrans)*scale+width/2
    y1 = -(y1+ytrans)*scale+height/2
    x2 = (x2+xtrans)*scale+width/2
    y2 = -(y2+ytrans)*scale+height/2
    draw = ImageDraw.Draw(im)
    draw.line((x1, y1, x2, y2),fill=color)
    del draw

def draw_seg(p1,p2, im,color=(255,255,0)):
    "Draw line segment (from p1 to p2) on image"
    x1 = (p1[0]+xtrans)*scale+width/2
    y1 = -(p1[1]+ytrans)*scale+height/2
    x2 = (p2[0]+xtrans)*scale+width/2
    y2 = -(p2[1]+ytrans)*scale+height/2
    draw = ImageDraw.Draw(im)
    draw.line((x1, y1, x2, y2),fill=color)
    del draw

def draw_parab(parab, im,color=(0,255,0)):
    "Draw parabola on image"
    draw = ImageDraw.Draw(im)
    tmin = parab.tmin
    if tmin==None:
        tmin = -10
    tmax = parab.tmax
    if tmax==None:
        tmax = 10
    t = tmin
    tstep = 0.1
    lastp = parab.eval_t(t)
    t = t + tstep
    while t < tmax:
        nextp = parab.eval_t(t)
        x1 = (lastp[0]+xtrans)*scale+width/2
        y1 = -(lastp[1]+ytrans)*scale+height/2
        x2 = (nextp[0]+xtrans)*scale+width/2
        y2 = -(nextp[1]+ytrans)*scale+height/2
        draw.line((x1, y1, x2, y2),fill=color)
        lastp = nextp
        t = t + tstep
    nextp = parab.eval_t(tmax)
    x1 = (lastp[0]+xtrans)*scale+width/2
    y1 = -(lastp[1]+ytrans)*scale+height/2
    x2 = (nextp[0]+xtrans)*scale+width/2
    y2 = -(nextp[1]+ytrans)*scale+height/2
    draw.line((x1, y1, x2, y2),fill=color)
    del draw

def draw_voronoi(path):
    "Draw completed Voronoi diagram on image"
    im=img_preprocess()
    for pt in points:
        if pt.isPt():
            draw_pt(pt,im)
        else:
            draw_line(pt.line,im,(0,0,0))
    for li in lines:
        if li.isLine():
            draw_line(li,im)
        else:
            draw_parab(li,im)
    im.save(path)
    