# aux_functions.py

from __future__ import division
import random as ran
from math import sqrt
import time
import globals as gl
import data, cfg, io



def generateRandomTag(length):
    """ generates a random alphanumeric tag with a given length """
    i = 0
    tag = ""
    while i < length:
        #tag += str((ran.choice(data.alphanumeric_set)))
        tag += str((ran.choice(data.alphabet_set)))
        i += 1
    return tag



def generateRandomLabel(length):
    """ generates a random LABEL with a given length """
    i = 0
    label = ""
    while i < length:
        if i % 2 == 0:
            label += str((ran.choice(data.consonant_set)))
            i += 1
        else:
            label += str((ran.choice(data.vowel_set)))
            i += 1
    return label


def posMax(list):
    """ returns the index of the highest value of a given list
        if multiple highest values exist, the first is returned
    """
    m = list[0]
    index = 0
    for i, x in enumerate(list):
        if x > m:
            m = x
            index = i
    return index


def posSemiMax(list):
    """ returns the index of the semi-highest value of a given list
        if multiple values exist, the first is returned
    """
    m = list[0]
    index1 = 0
    for i, x in enumerate(list):
        if x > m:
            m = x
            index1 = i
    list.pop(index1)
    m = list[0]
    index2 = 0
    for i, x in enumerate(list):
        if x > m:
            m = x
            index2 = i
    if index1 <= index2:
        index2 += 1
    return index2


def posMin(list):
    """ returns the index of the lowest value of a given list
        if multiple highest values exist, the first is returned
    """
    m = list[0]
    index = 0
    for i, x in enumerate(list):
        if x < m:
            m = x
            index = i
    return index


def generateTrainingData(n_sets, context_size):
    """generates training datasets, based on the specified domains in cfg
       training data is generated with separated stimuli for each active domain
    """
    training_dataset = []
    count = 0
    start_time = time.time()
    while count < n_sets:
        count2 = 0
        set = []
        while count2 < context_size:
            check = True
            while check:
                stimulus = []
                for i in cfg.space:
                    if i == "rgb":
                        stim = []
                        selection = gl.rgb_data_tony[ran.randint(0, 24999)]
                        for j in [["r", selection[0]*255], ["g", selection[1]*255], ["b", selection[2]*255]]:
                            stim.append(j)
                        stimulus.append([i,stim])
                    if i == "lab":
                        stim = []
                        selection = gl.lab_data_tony[ran.randint(0, 24999)]
                        for j in [["l", selection[0]], ["a", selection[1]], ["b", selection[2]]]:
                            stim.append(j)
                        stimulus.append([i,stim])
                    if i == "4df":
                        stim = []
                        for j in [["l", ran.randint(1, 5)], ["n", ran.randint(1, 5)], ["t", ran.randint(1, 5)], ["e", ran.randint(1, 5)]]:
                            stim.append(j)
                        stimulus.append([i,stim])
                    if i == "shape":
                        stimulus.append([i,[["sh", ran.randint(data.shape_range[0],data.shape_range[1])]]])
                if set == []:
                    check = False
                else:   # check if distance is big enough
                    sequence = []
                    for i in set:
                        if cfg.sample_minimum_distance < calculate_distance(i, stimulus):
                            sequence.append("1")
                        else:
                            sequence.append("0")
                    if "0" not in sequence:
                        check = False
            set.append(stimulus)
            count2 += 1
        training_dataset.append(set)
        count += 1
        if count % (n_sets/10) == 0:
            print str((count/n_sets)*100) + "% of stimuli sets generated (" + str( time.time()-start_time) + ")"
            start_time = time.time()
#    for i in training_dataset:
#        dist = []
#        for j in i:
#            distance = calculate_distance(j, i[0])
#            dist.append(distance)
#        gl.training_data_dist.append(dist)
#    io.write_output("dist", gl.training_data_dist)
    return training_dataset



def calculate_max_dis():
    """ calculates the maximum distance based on the range of the current space """
    if cfg.space == "rgb":
        return 441.67
    
    
    
def calculate_distance(data_point1, data_point2, salience = "empty"):
    """ calculates the distance between two given data points
        at least one matching domain is required, only matching domains are taken into account
        data_point1 is used as reference, list of salience should be according to the
        domains of data_point1, if non given, default salience of 1.0 is used
        data_point1 = [ [ "domain", [ ["d1", value], ["d2", value]]], ...]
        data_point2 = [ [ "domain", [ ["d1", value, SD], ["d2", value, SD]]], ...] (if no SD, 0 is added)
        salience = [s1, s2,...,sn]
        for each domain, the maximum distance is 1
    """
    distance = None
    if salience == "empty":
        salience = [1.0] * len(data_point1)
    for count, i1 in enumerate(data_point1):
        for j1 in data_point2:
            if i1[0] == j1[0]:          # if domains match
                if distance == None:    # initiate overall distance
                    distance = 0
                dist = 0    # distance per domain
                for i2 in i1[1]:    
                    for j2 in j1[1]:
                        if len(j2) == 2:    # make sure there is an SD
                            j2.append(0.0)
                        if i2[0] == j2[0]:  # if dimensions match
                            if cfg.prototype_distance:
                                if i2[1] <= j2[1]:
                                    difference = (i2[1] - (j2[1] - j2[2]))/get_range(i2[0])
                                    dist += difference/len(i1[1])
                                else:
                                    difference = (i2[1] - (j2[1] + j2[2]))/get_range(i2[0])
                                    dist += difference/len(i1[1])
                            else:
                                difference = (i2[1] - j2[1] )/get_range(i2[0])
                                dist += difference/len(i1[1])
                dist = dist**2
                distance += (salience[count] * dist)     # take salience for the dimension into account
    if distance == None:
        return distance
    else:
        return sqrt(distance)
    
    
    
def get_range(dim_name):
    """ get range of dimension
    """
    for i in data.dimension_ranges:
        if dim_name == i[0]:
            return (i[1][1] - i[1][0])

    
def calculate_distance_general(point1, point2, list_salience = "empty" ):
    """ calculates the distance between two given points
        only matching dimensions are taken into account
        point1 used as reference, list of salience should be according to 
        dimensions of point1, if non given, default salience of 1 is used
        point1 = [ [d1, value], [d2, value], ..., [dn, value] ]
        point2 = [ [d1, value, SD], [d2, value, SD], ..., [dn, value, SD] ]
        list_salience = [s1, s2,...,sn]
    """
    distance = 0
    if list_salience == "empty":
        list_salience = [1] * len(point1)
    for count, i in enumerate(point1):
        for j in point2:
            if i[0] == j[0]:
                if cfg.prototype_distance:  # if the SD of prototypes is used 
                    if len(j) == 2:         # make sure there is an SD value
                        j.append(0.0)
                    if i[1] <= j[1]:
                        distance += ( list_salience[count] * ((i[1] - (j[1] - j[2]))**2) )
                    else:
                        distance += ( list_salience[count] * ((i[1] - (j[1] + j[2]))**2) )
                else:
                    distance += ( list_salience[count] * ((i[1] - j[1])**2) )
    return sqrt(distance)
        
        
        
def rgb_2_xyz(rgb):
    """ takes a rgb point [r,g,b] as input and returns [x,y,z]
        PAL/SECAM RGB, D65 conversion matrix
    """
    #matrix from Tony's paper
    x_value = (rgb[0] * 0.430587  + rgb[1] * 0.341545 + rgb[2] * 0.178336)
    y_value = (rgb[0] * 0.222021  + rgb[1] * 0.706645 + rgb[2] * 0.0713342)
    z_value = (rgb[0] * 0.0201837 + rgb[1] * 0.129551 + rgb[2] * 0.939234)

    #matrix from http://www.brucelindbloom.com/index.html?ColorCalcHelp.html
#    x_value = (rgb[0] * 0.4306190  + rgb[1] * 0.2220379 + rgb[2] * 0.0201853)
#    y_value = (rgb[0] * 0.3415419  + rgb[1] * 0.7066384 + rgb[2] * 0.1295504)
#    z_value = (rgb[0] * 0.1783091 + rgb[1] * 0.0713236 + rgb[2] * 0.9390944)

    return [x_value, y_value, z_value]


def xyz_2_lab(xyz):
    """ takes an xyz point [x,y,z] as input and returns [l,a,b]
    """
    xx = xyz[0]/0.9504682
    yy = xyz[1]/1.0
    zz = xyz[2]/1.08883
    if yy > 0.008856:
        l = (116 * pow(yy,(1/3.0))) - 16
    else:
        l = 903.3 * yy
    a = 500 * ( f(xx) - f(yy) )
    b = 200 * ( f(yy) - f(zz) )
    return [l, a, b]
    

# help function for xyz_2_lab
def f(x):
    if x > 0.008856:        
        return pow(x,(1/3.0))
    else:
        return (7.787 * x) + (16/116)
    
    
    
def lab_2_xyz(lab):
    """ takes a lab point [l,a,b] as input and returns [x,y,z]
    """
    con = 6/29.0
    fy = (lab[0] + 16)/116
    fx = fy + lab[1]/500
    fz = fy - lab[2]/200
    if fy > con:
        y = fy**3
    else:
        y = (fy - 16/116)*3*(con**2)
    if fx > con:
        x = fx**3
    else:
        x = (fx - 16/116)*3*(con**2)
    if fz > con:
        z = fz**3
    else:
        z = (fz - 16/116)*3*(con**2)
    # normalisation seems to be possible afterwards    
    x = x*0.9504682
    z = z*1.08883
    return [x,y,z]


def xyz_2_rgb(xyz):
    """ takes a xyz point [x,y,z] as input and returns [r,g,b]
        PAL/SECAM RGB, D65 conversion matrix from http://www.brucelindbloom.com/index.html?ColorCalcHelp.html
    """
    r = (xyz[0] * 3.0628971  + xyz[1] * -0.9692660 + xyz[2] * 0.0678775)
    g = (xyz[0] * -1.3931791  + xyz[1] * 1.8760108 + xyz[2] * -0.2288548)
    b = (xyz[0] * -0.4757517 + xyz[1] * 0.0415560 + xyz[2] * 1.0693490)
    return [r, g, b]

#test = xyz_2_lab(rgb_2_xyz([1,0,0]))
#print test
#text_back = xyz_2_rgb(lab_2_xyz(test))
#print text_back
    
