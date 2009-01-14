# lexicon.py

import numpy
import aux_functions as aux


class Lexicon():
    """ Lexicon of an agent, containing labels known by the agent
        and a associative matrix from lexicon to concept
    """
    
    
    def __init__(self, name):
        """ initiate variables """
        self.holder_name = name        # name of the agent holding this CP
        self.labels = []               # list of labels
        self.tags = []                 # list of tags
        self.matrix = numpy.array([])  # associative matrix
        
        
    def get_labels(self):
        """ returns the list of labels currently in the lexicon """
        return self.labels
    
    
    def get_tags(self):
        """ returns the list of tags used for the concepts currently in the lexicon """
        return self.tags
    
    
    def add_label(self, label, tag):
        """ adds a new label to the repertoire, and/or updates the associative matrix """
        # if label is not known
        if label not in self.labels:
            # create new matrix is none exists
            if len(self.matrix) == 0:   
                self.matrix = [[0.5]]
            # update matrix with new connection
            else:                       
                length_labels = len(self.labels)
                length_tags = len(self.tags)
                new_zeros = numpy.zeros(length_labels)
                new_zeros.shape = length_labels, 1
                self.matrix = numpy.hstack((self.matrix, new_zeros))
                new = numpy.append(numpy.zeros(length_tags), 0.5)
                self.matrix = numpy.vstack((self.matrix,new))
            # add label and tag
            self.labels.append(label)
            self.tags.append(tag)
        # if label is already known
        else:
            new = numpy.array([])
            for count, i in enumerate(self.matrix):
                if count != self.labels.index(label):
                    new = numpy.hstack((new, [0.0]))
                else:
                    new = numpy.hstack((new, [0.5]))
            new.shape = len(self.labels), 1
            self.matrix = numpy.hstack((self.matrix, new))
            self.tags.append(tag)
            
            
    def increase_strength(self, label, tag):
        """ increases the association strength between the given label and tag
            if lateral_inhibition is used, other associations are weakened
        """
        label_index = self.labels.index(label)
        tag_index = self.tags.index(tag)
        if self.matrix[label_index][cat_index] <= 0.9:
            self.matrix[label_index][cat_index] += cfg.label_learning_rate
        #decrease competing connections if lateral_inhibition is used
        if cfg.lateral_inhibition:
            for count2, i in enumerate(self.matrix):
                if count2 != label_index:
                    for count, j in enumerate(i):
                        if count == tag_index:
                            if self.matrix[count2][count] >= 0.1:
                                self.matrix[count2][count] -= cfg.label_learning_rate
            for count, i in enumerate(self.matrix[label_index]):
                if count != tag_index:
                    if self.matrix[label_index][count] >= 0.1:
                        self.matrix[label_index][count] -= cfg.label_learning_rate
        
            
    def get_tag(self, label):
        """ retrieves the tag with the highest association for the given label 
            if there are more than one tags with the highest association value, 
            the first one will be returned
        """
        label_index = -1
        for count, i in enumerate(self.labels):
            if i == label:
                label_index = count
                break
        if label_index == -1:
            return "no_tag"
        else:
            max = aux.posMax(self.matrix[label_index])
            return self.tags[max]
    
    
    def get_label(self, tag):
        """ retrieves the label with the higest association for the given tag 
            if there are more than one labels with the higest association value, 
            the first one will be returned
        """
        tag_index = -1
        for count, i in enumerate(self.tags):
            if i == tag:
                tag_index = count
                break
        if tag_index == -1:
            return "no_label"
        else:
            value_list = []
            for i in self.matrix:
                for count, j in enumerate(i):
                    if count == tag_index:
                        value_list.append(j)
            return self.labels[aux.posMax(value_list)]

        
    def print_matrix(self):
        """ prints associative matrix """
        print "Lexicon matrix:"
        print "        ",  self.tags
        j = 0
        for i in self.labels:
            print "'", i,"'", 
            for k in self.matrix[j]:
                    print " ",  k, "     ", 
            print "\n"
            j += 1
        
        
        
        
        
        