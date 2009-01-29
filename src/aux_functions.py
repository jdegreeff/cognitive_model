# aux_functions.py

from __future__ import division
import random as ran
import data
import cfg
from math import sqrt
import globals as gl


def generateRandomTag(length):
    """ generates a random alphanumeric tag with a given length """
    i = 0
    tag = ""
    while i < length:
        tag += str((ran.choice(data.alphanumeric_set)))
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


def generateTrainingData(space, n_sets, context_size, type = 0):
    training_dataset = []
    if space == "rgb":
        training_dataset = generateRGBTrainingDataUniform(n_sets, context_size, cfg.sample_minimum_distance)
    if space == "4df":
        training_dataset = generate4DFigureTrainingData(n_sets, context_size, type)
    return training_dataset


def generateRGBTrainingDataUniform(n_sets,  n_stimuli, sample_minimum_distance):
    """ generates n_sets training data sets: context of n_stimuli
        space: RGB
        values are drawn randomly from uniform distribution,
        minimum distance between values is taken into account
    """
    training_data = []
    count = 0
    while count < n_sets:
        count2 = 0
        set = []
        while count2 < n_stimuli:
            check = True
            while check:
                #stimulus = [["r", ran.uniform(0.0, 255.0)], ["g", ran.uniform(0.0, 255.0)], ["b", ran.uniform(0.0, 255.0)]]
                data = gl.data_tony[ran.randint(0, 24999)]
                stimulus = [ ["r", data[0]*255], ["g", data[1]*255], ["b", data[2]*255] ] 
                if set == []:
                    check = False
                else:
                    for i in set:
                        distance = calculate_distance_general(i, stimulus)
                        if distance > sample_minimum_distance:
                            check = False
                        else:
                            check = True
            set.append(stimulus)
            count2 += 1
        training_data.append(set)
        count += 1
    return training_data


def generate4DFigureTrainingData(n_sets,  n_stimuli, type = 0):
    """ generates n_sets training data sets: context of n_stimuli 
        space: 4D stick figures
        discrete values are drawn randomly [1-5]
        type can be specified to generate figures with small or large features, default is random
        dimensions are "l" = legs, "n" = neck, "t" = tail, "e" = ears
    """
    training_data = []
    count = 0
    while count < n_sets:
        count2 = 0
        set = []
        if type == 0:
            while count2 < n_stimuli:
                stimulus = [["l", ran.randint(1, 5)], ["n", ran.randint(1, 5)], ["t", ran.randint(1, 5)], ["e", ran.randint(1, 5)] ]
                set.append(stimulus)
                count2 += 1
        if type == "SMALL":
            while count2 < n_stimuli:
                stimulus = [["l", ran.randint(1, 3)], ["n", ran.randint(1, 3)], ["t", ran.randint(1, 3)], ["e", ran.randint(1, 3)] ]
                set.append(stimulus)
                count2 += 1
        if type == "LARGE":
            while count2 < n_stimuli:
                stimulus = [["l", ran.randint(3, 5)], ["n", ran.randint(3, 5)], ["t", ran.randint(3, 5)], ["e", ran.randint(3, 5)] ]
                set.append(stimulus)
                count2 += 1
        training_data.append(set)
        count += 1
    return training_data


def calculate_max_dis():
    """ calculates the maximum distance based on the range of the current space """
    if cfg.space == "rgb":
        return 441.67
    
    
    
def calculate_distance_general(point1, point2, list_salience = "empty" ):
    """ calculates the distance between two given points
        only matching dimensions are taken into account
        point1 used as reference, list of salience should be according to 
        dimensions of point1, if non given, default salience of 1 is used
        point = [ [d1, value], [d2, value], ..., [dn, value] ]
        list_salience = [s1, s2,...,sn]
    """
    distance = 0
    if list_salience == "empty":
        list_salience = [1] * len(point1)
    for count, i in enumerate(point1):
        for j in point2:
            if i[0] == j[0]:
                distance += ( list_salience[count] * ((i[1] - j[1])**2) )
    return sqrt(distance)
    
    
def calculate_stats(stats):
    """ calculates the average number of concepts learned for a given number of training loops
        stats = [ data_loop1, data_loop2, ...data_loopn ]
        data_loop = [ n_game, n_concepts, guessing_succes ] 
    """
    overall = []
    counter = 0
    while counter < cfg.n_training_datasets:
        overall.append([0.0] * 3)
        counter += 1
    for i in stats:
        for count, j in enumerate(i):
            for count2, h in enumerate(j):
                overall[count][count2] = overall[count][count2] + h
    for count, i in enumerate(overall):
        for count2, j in enumerate(i):
            overall[count][count2] = j/len(stats)
    print "done"
    gl.overall_stats = overall
        
        
        
        
        
        
    
