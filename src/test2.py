from array import array
from random import *
from math import *

class image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rgb = array('B')
        i = 0
        while i < width * height * 3:
            self.rgb.append(255)
            i = i + 1

def noisify(image):
    x = 0
    y = 0
    while y < image.height:
        while x < image.width:
            i = (y * image.width + x) * 3
            image.rgb[i + 0] = int(random() * 255)
            image.rgb[i + 1] = int(random() * 255)
            image.rgb[i + 2] = int(random() * 255)
            x = x + 1
        y = y + 1
        x = 0

def crystallize(image, cellsize):
    rows = image.height / cellsize
    if (image.height % cellsize) != 0:
        rows = rows + 1
    cols = image.width / cellsize
    if (image.width % cellsize) != 0:
        cols = cols + 1
    row = 0
    col = 0
    points = []
    while row < rows:
        while col < cols:
            x = randint(col * cellsize, (col + 1) * cellsize - 1)
            y = randint(row * cellsize, (row + 1) * cellsize - 1)
            points.append(x)
            points.append(y)
            col = col + 1
        row = row + 1
        col = 0
    def distance(x0, y0, x1, y1):
        return sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    def cellstocheck(x, y):
        curcellx =  x / cellsize
        curcelly = y / cellsize
        cells = []
        x = 0
        y = 0
        while y < 5:
            while x < 5:
                cellx = curcellx - 2 + x
                celly = curcelly - 2 + y
                if cellx >= 0 and celly >= 0:
                    if cellx < cols and celly < rows:
                        index = (celly * cols) + cellx
                        cells.append(index)
                x = x + 1
            y = y + 1
            x = 0
        return cells
    def color(x, y):
        cells = cellstocheck(x, y)
        i = cells[0] * 2
        mindist = distance(x, y, points[i], points[i + 1])
        j = 0
        for cellindex in cells:
            i = cellindex * 2
            dist = distance(x, y, points[i], points[i + 1])
            if (dist < mindist):
                mindist = dist
                j = i
        xx = points[j]
        yy = points[j + 1]
        k = (yy * image.width + xx) * 3
        r = image.rgb[k + 0]
        g = image.rgb[k + 1]
        b = image.rgb[k + 2]
        return r, g, b
    x = 0
    y = 0
    while y < image.height:
        while x < image.width:
            r, g, b = color(x, y)
            i = (y * image.width + x) * 3
            image.rgb[i + 0] = r
            image.rgb[i + 1] = g
            image.rgb[i + 2] = b
            x = x + 1
        y = y + 1
        x = 0

def writeimage(file, image):
    fileheader = array('B')
    fileheader.fromstring(
        "\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    fileheader.append(image.width & 0xff)
    fileheader.append(image.width >> 8)
    fileheader.append(image.height & 0xff)
    fileheader.append(image.height >> 8)
    fileheader.append(24)
    fileheader.append(0x30)
    fileheader.tofile(file)
    image.rgb.tofile(file)

def test1():
    print "Test 1"
    M = image(320, 200)
    print "Noisifying..."
    noisify(M)
    f = file("before1.tga", "wb")
    writeimage(f, M)
    f.close()
    print "Crystallizing..."
    crystallize(M, 20)
    f = file("after1.tga", "wb")
    writeimage(f, M)
    f.close()
    print "Done."
    print

def test2():
    print "Test 2"
    M = image(320, 200)
    print "Creating image..."
    x = 0
    y = 0
    while y < M.height:
        while x < M.width:
            c = int(round((x / (M.width / 10)) *
                (255.0 / (10 - 1))))
            i = (y * M.width + x) * 3
            M.rgb[i + 0] = c
            M.rgb[i + 1] = c
            M.rgb[i + 2] = c
            x = x + 1
        y = y + 1
        x = 0
    f = file("before2.tga", "wb")
    writeimage(f, M)
    f.close()
    print "Crystallizing..."
    crystallize(M, 10)
    f = file("after2.tga", "wb")
    writeimage(f, M)
    f.close()
    print "Done."
    print

test1()
test2()
