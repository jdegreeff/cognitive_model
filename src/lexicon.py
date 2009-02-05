# lexicon.py

from __future__ import division
import numpy
import aux_functions as aux
import cfg
import globals as gl
import copy


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
        # if label and tag are not known
        if (label not in self.labels and tag not in self.tags):
            # create new matrix is none exists
            if len(self.matrix) == 0:   
                self.matrix = [[0.5]]
            # update matrix with new connection
            else:                       
                length_labels = len(self.labels)
                length_tags = len(self.tags)
                #new_zeros = numpy.zeros(length_labels)
                new_zeros = numpy.array([0.0] * length_labels)
                new_zeros.shape = (length_labels, 1)
                try:
                    self.matrix = numpy.hstack((self.matrix, new_zeros))
                except ValueError:
                    pass
                #new = numpy.append(numpy.zeros(length_tags), 0.5)
                new = numpy.append(numpy.array([0.0] * length_tags), 0.5)
                try:
                    self.matrix = numpy.vstack((self.matrix,new))
                except ValueError:
                    pass
            # add label and tag
            self.labels.append(label)
            self.tags.append(tag)
        # if tag is already known, a new label is added
        elif label not in self.labels:
            new = numpy.array([0.0] * len(self.tags))
            for count, i in enumerate(new):
                if count == self.tags.index(tag):
                    new[count] = 0.5
            self.matrix = numpy.vstack((self.matrix,new))
            self.labels.append(label)
        # if label is already known, a new tag is added
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
            
            
    def increase_strength(self, label, tag, amount):
        """ increases the association strength between the given label and tag
            if lateral_inhibition is used, other associations are weakened
        """
        label_index = self.labels.index(label)
        tag_index = self.tags.index(tag)
        if self.matrix[label_index][tag_index] <= (1 - amount):
            self.matrix[label_index][tag_index] += amount
        #decrease competing connections if lateral_inhibition is used
        if cfg.lateral_inhibition:
            for count2, i in enumerate(self.matrix):
                if count2 != label_index:
                    for count, j in enumerate(i):
                        if count == tag_index:
                            if self.matrix[count2][count] >= (0 + amount):
                                self.matrix[count2][count] -= amount
            for count, i in enumerate(self.matrix[label_index]):
                if count != tag_index:
                    if self.matrix[label_index][count] >= (0 + amount):
                        self.matrix[label_index][count] -= amount
        
        
    def decrease_strength(self, label, tag, amount):
        """ decreases the association strength between the given label and tag
        """
        try:
            label_index = self.labels.index(label)
        except ValueError:
            print "agent.lex.decrease_strength Error"
        tag_index = self.tags.index(tag)
        if self.matrix[label_index][tag_index] >= (0 + amount):
            self.matrix[label_index][tag_index] -= amount
            
            
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
            return "label_unknown"
        else:
            max = aux.posMax(self.matrix[label_index])
            return self.tags[max]
    
    
    def get_label(self, tag, inaccuracy):
        """ retrieves the label with the highest association for the given tag 
            if there are more than one labels with the highest association value, 
            the first one will be returned
        """
        tag_index = -1
        for count, i in enumerate(self.tags):
            if i == tag:
                tag_index = count
                break
        if tag_index == -1:
            return "tag_unknown"
        else:
            value_list = []
            for i in self.matrix:
                for count, j in enumerate(i):
                    if count == tag_index:
                        value_list.append(j)
            if inaccuracy:
                return self.labels[aux.posSemiMax(value_list)]
            else:
                return self.labels[aux.posMax(value_list)]

        
    def print_matrix(self):
        """ prints associative matrix """
        print "Lexicon matrix:"
        print "        ",  self.tags
        j = 0
        for i in self.labels:
            print "'", i,"'", 
            for k in self.matrix[j]:
                    print " ",  '%.2f'% k, "     ", 
            print "\n"
            j += 1
        
        
        
        
        
        