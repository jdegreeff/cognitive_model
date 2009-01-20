#colour_space.py

import Image

# parameters
e = 0.008856

# takes an RGB image as argument and returns XYZ image
def rgb2xyz(rgb_image):
    rgb_values = list(rgb_image[0,0])
    tmp = []
    for i in rgb_values:
        i = i/254.0
        tmp.append(i)
    # [x y z] = [r g b] * [11   12  13]
    #                     [21   22  23]
    #                     [31   32  33]
    x_value = (tmp[0] * 0.430587 + tmp[1] * 0.341545  + \
               tmp[2] * 0.178336)
    y_value = (tmp[0] * 0.222021 + tmp[1] * 0.706645 + \
               tmp[2] * 0.0713342)
    z_value = (tmp[0] * 0.0201837 + tmp[1] * 0.129551 + \
               tmp[2] * 0.939234)
    return [x_value, y_value, z_value]
    

# takes an XYZ image as argument and returns CIE L*a*b* image
def xyz2lab(xyz_image):
    xx = xyz_image[0]/0.9504682
    yy = xyz_image[1]/1.0
    zz = xyz_image[2]/1.08883
    if yy > e:
        l = (116 * pow(yy,(1/3.0))) - 16
    else:
        l = 903.3 * yy
    a = 500 * ( f(xx) - f(yy) )
    b = 200 * ( f(yy) - f(zz) )
    return [l, a, b]

    
# help function for xyz2lab
def f(x):
    if x > e:        
        return pow(x,(1/3.0))
    else:
        return (7.787 * x) + (16/116)
    

im = Image.open("test_blue.png")
# print im.format, im.size, im.mode

pix = im.load()
print "\n RGB: " + str(pix[0, 0])

xyz_image = rgb2xyz(pix)
lab_image = xyz2lab(xyz_image)
    
x_value = (xyz_image[0] + 0.0)/(xyz_image[0] + xyz_image[1] + xyz_image[2])
y_value = (xyz_image[1] + 0.0)/(xyz_image[0] + xyz_image[1] + xyz_image[2])

print "\n Yxy values - x: " + str(x_value), "y: " + str(y_value), "Y: " + str(xyz_image[1])

print "\n L*a*b* values - L: " + str(lab_image[0]), "a: " + str(lab_image[1]), "b: " + \
        str(lab_image[2])

