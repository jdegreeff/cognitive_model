# concept.py


from __future__ import division
from math import sqrt
import data


class Concept():
    """ Concept class
    """
    
    def __init__(self, tag, concept_data):
        """ initiate variables """
        self.tag = tag                  # concept tag
        self.domains = []               # domains in which the concepts has coordinates
        self.domain_list = []           # list containing the names of the domains in which the concept has coors
        self.concept_use = 0            # n times the concept is used in language games
        self.concept_success = 0        # n times the concept is used successful
        self.initiate_new(concept_data) # initiates new data

        
    def initiate_new(self, concept_data):
        """ initiates a new concept
            creates a new domain based on given coors
            coors = [ "d1", value], [ "d2", value], [ "d3", value]
        """
        for i in concept_data:
            self.domains.append(Domain(i[0], i[1]))
            self.domain_list.append(i[0])
    

    def add_exemplar_data(self, exemplar_data):
        """ adds exemplar data to the concept
            exemplar_data format = ["domain", [[ "d1", value], [ "d2", value], [ "d3", value]]]
        """
        for i in exemplar_data:
            new = True
            for j in self.domains:   # find domain if it exists and add data
                if j.name == i[0]:
                    j.add_exemplar_data(i[1])
                    new = False
            if new:             # create new domain
                self.domains.append(Domain(i[0], i[1]))
                self.domain_list.append(i[0])
                
                  
    def get_data(self):
        """ returns the data from all domains of the concept
        """
        answer = []
        for i in self.domains:
            answer.append(i.get_data())
        return (self.tag, answer)
    
    
    def get_prototype_data(self):
        """ returns all prototype data from all domains of the concept
        """
        data = []
        for i in self.domains:
            data.append(i.get_prototype_data())
        return data
    
    
    def get_domain_list(self):
        """ returns the list of domains in which the concept has coordinates
        """
        return self.domain_list
    

    def usage(self, result):
        """ records the result of a guessing game
        """
        self.concept_use += 1
        if result:
            self.concept_success += 1
        
        
        
class Domain():
    """ Domain class, containing domain + associated dimensions
        dimensions = [[ "d1", value, SD], [ "d2", value, SD], [ "d3", value, SD]]
    """
    
    def __init__(self, name, coors):
        """ initiate domain 
        """
        self.name = name            # domain name
        self.dimensions = []        # list of dimensions + coors
        self.prototype_data = []    # data from which the prototypes are extracted
        self.init_data(coors)       # sets data on the given coordinates
        
        
    def init_data(self, coors):
        """ initiates data on given coordinates
            coors format = ["d1", value, SD]
        """
        for i in coors:
            self.dimensions.append([i[0], i[1], 0.0])
            self.prototype_data.append([i[0], i[1]])
            
            
    def add_exemplar_data(self, exemplar_data):
        """ adds exemplar data to the domain
            exemplar_data format = [[ "d1", value], [ "d2", value], [ "d3", value]]]
        """
        for i in exemplar_data:
            for j in self.dimensions:
                if i[0] == j[0]:    # if the dimension name match
                    self.prototype_data.append(i)
                    number = 0    
                    # find number of exemplars used for prototype                    
                    for k in self.prototype_data:       
                        if k[0] == i[0]:
                            number += 1
                    difference = (i[1] - j[1])/ number      # calculate difference
                    mean = j[1] + difference
                    # calculate SD: sqrt( sum(x - mean)**2/n )
                    sd = 0
                    for k in self.prototype_data:
                         if k[0] == i[0]:
                            sd = sd + ((k[1] - mean)**2)
                    sd = sqrt(sd / (number))
                    j[1] = mean
                    j[2] = sd
                    
                    
    def get_data(self):
        return [self.name, self.dimensions]
    
    def get_prototype_data(self):
        return self.prototype_data

