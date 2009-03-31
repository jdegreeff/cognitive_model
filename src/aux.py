# aux_functions.py

from __future__ import division
import random as ran
from math import sqrt
import globals as gl
import data, cfg



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
       minimum distance is not taken into account at the moment
       training data is generated with separated stimuli for each active domain
    """
    training_dataset = []
    count = 0
    while count < n_sets:
        count2 = 0
        set = []
        while count2 < context_size:
            stimulus = []
            empty = True
            check = True
            while empty or check:
                for i in cfg.space:
                    if i == "rgb":
                        if ran.randint(0,1) == 1:
                            stim = []
                            selection = gl.rgb_data_tony[ran.randint(0, 24999)]
                            for j in [["r", selection[0]*255], ["g", selection[1]*255], ["b", selection[2]*255]]:
                                stim.append(j)
                            stimulus.append([i,stim])
                    if i == "lab":
                        if ran.randint(0,1) == 1:
                            stim = []
                            selection = gl.lab_data_tony[ran.randint(0, 24999)]
                            for j in [["l", selection[0]], ["a", selection[1]], ["b", selection[2]]]:
                                stim.append(j)
                            stimulus.append([i,stim])
                    if i == "4df":
                        if ran.randint(0,1) == 1:
                            stim = []
                            for j in [["l", ran.randint(1, 5)], ["n", ran.randint(1, 5)], ["t", ran.randint(1, 5)], ["e", ran.randint(1, 5)]]:
                                stim.append(j)
                            stimulus.append([i,stim])
                    if i == "shape":
                        if ran.randint(0,1) == 1:
                            stimulus.append([i,[["sh", ran.randint(data.shape_range[0],data.shape_range[1])]]])
                if len(stimulus) > 0:
                    empty = False
                if set == []:
                    check = False
                else:   # check if distance is big enough
                    for i in set:
                        distance = calculate_distance_point(i, stimulus)
                        if distance > cfg.sample_minimum_distance:
                            check = False
            set.append(stimulus)
            count2 += 1
        training_dataset.append(set)
        count += 1
    return training_dataset



def calculate_max_dis():
    """ calculates the maximum distance based on the range of the current space """
    if cfg.space == "rgb":
        return 441.67
    
    
    
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
        
        
        
    
