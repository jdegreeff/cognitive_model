# aux_functions.py

import random as ran
import data


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
        training_dataset = generateRGBTrainingDataUniform(n_sets, context_size)
    if space == "4df":
        training_dataset = generate4DFigureTrainingData(n_sets, context_size, type)
    return training_dataset


def generateRGBTrainingDataUniform(n_sets,  n_stimuli):
    """ generates n_sets training data sets: context of n_stimuli 
        space: RGB
        values are drawn randomly from uniform distribution
    """
    training_data = []
    count = 0
    while count < n_sets:
        count2 = 0
        set = []
        while count2 < n_stimuli:
            stimulus = [["r", ran.uniform(0.0, 255.0)], ["g", ran.uniform(0.0, 255.0)], ["b", ran.uniform(0.0, 255.0)]]
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


