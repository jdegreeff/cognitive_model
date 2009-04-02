# cp.py
# Conceptual Space
# basic data of a stimulus: [ ["d1", value], ["d2", value], ..., ["dn", value] ]
# concepts hold by agent: [ [concept1, prototype], [concept2, prototype], ...]
# where concept1 = "string", prototype = [ ["d1", value, SD], ["d2", value, SD],...]
# based on Gardenfors, P. Conceptual Spaces: The Geometry of Thought. MIT Press, 2004

from __future__ import division
import random as ran
from math import sqrt
import math
import copy
import globals as gl
import cfg, aux, concept


class CP():
    """ Conceptual Space which holds conceptual knowledge of an agent
        Regions represent prototypes of concepts, incoming objects can be assigned to 
        the best fitting concept using a distance measure 
        There are two ways in which concepts can be added:
            1) through formation of prototypes: exemplars of concepts are used to 
               calculate a mean prototype, the SD can be used as a radius
               if the label of a given exemplar is known, the concept with the highest association
               will be updated with the new exemplar data
            2) through direct addition of a concept. Coordinates of exemplar data
               are used for this, no prototype formation is used
        Furthermore, concept coordinates may be shifted through language games
        basic format of a concept 
        = [ "tag", [ [ "d1", value], [ "d2", value], [ "d3", value] ], [concept_use, concept_success] ]
    """
    
    def __init__(self, name):
        """ initiate variables """
        self.holder_name = name     # name of the agent holding this CP
        self.dimensions = []        # list of CP dimensions
        self.concepts = []          # list of names and coordinates of concepts the CP holds
        self.prototype_data = []    # data from which the prototypes are extracted


    def get_concepts(self):
        """ returns the list of concepts currently in CP """
        return self.concepts
    
    
    def get_n_concepts(self):
        """ returns the number of concepts currently in CP """
        return len(self.concepts)
    
    
    def get_all_concept_coordinates(self):
        """ returns a list of the coordinates of all concepts currently in CP
            the tag describing the concept is omitted
        """
        concepts_coor = []
        for i in self.concepts:
            coor = []
            for j in i[1]:  
                coor.append([j[0], j[1], j[2]])
            concepts_coor.append(coor)
        return concepts_coor
    

    def get_concept_coordinates(self, tag):
        """ returns a list of the coordinates of the given tag/concept
            the tag describing the concept and the SD values are omitted
        """
        concept_coor = []
        for i in self.concepts:
            if i[0] == tag:
                for j in i[1]:
                    concept_coor.append([j[0], j[1], j[2]])
        return concept_coor
    
    
    def get_concepts_tags(self):
        """ returns a list of the tags of concepts currently in CP """
        concepts_tags = []
        for i in self.concepts:
            concepts_tags.append(i[0])
        return concepts_tags
    
    
    def get_concept_highSD(self):
        """ returns the tag of the concept with the highest SD
        """
        concept = None
        sd = 0.0
        for i in self.concepts:
            sd_tot = 0.0
            for j in i[1]:
                sd_tot += j[2]
            if sd_tot > sd:
                sd = sd_tot
                concept = i
        return concept
    
    
    def get_unsuccessful_concept(self):
        """ returns the tag of the concept which is the must unsuccessful in language games
        """
        concept = None
        success = 1.0
        for i in self.concepts:
            if len(i) == 3:
                con_suc = i[2][1]/i[2][0]
                if con_suc < success:
                    success = con_suc
                    concept = i
        return concept
            
            
    def concept_use(self, tag, result):
        """ measures the success of the concept in the guessing game
            if concepts do not have a measurement structure, [0,0] is added,
            where [0, stands for usage and 0] for success
        """
        count = 0
        for i in self.concepts:
            if i[0] == tag:
                if len(i) == 2:
                    self.concepts[count].append([0,0])
                self.concepts[count][2][0] += 1
                self.concepts[count][2][1] += result
            count += 1
                
                            

    def add_exemplar(self, exemplar, tag):
        """ adds an exemplar of a specific concept to CP 
            coordinates of the concept are updated, along with the SD
            SD can be used as radius for prototypical circle
            exemplar = [ [d1, value], [d2, value], ..., [dn, value] ]
            tag = "string"
        """
        exemplar_copy = copy.deepcopy(exemplar)    # make a copy
        self.prototype_data.append([tag, copy.deepcopy(exemplar_copy)])        # add to data
        new = True
        for i in self.concepts:     # check for existing concept
            if tag in i:               
                new = False
        if new:                   # if concept not exists, add
            for count, i in enumerate(exemplar_copy):    # add SD
                exemplar_copy[count].append(0.0)
            self.concepts.append([tag, exemplar_copy])
        else:
            for count, i in enumerate(self.concepts):       # find concept in agent repertoire
                if i[0] == tag:
                    concept = self.concepts[count]
                    self.concepts.pop(count)
                    break
            if len(concept) == 2:
                concept_new = [concept[0],[]]
            else:
                concept_new = [concept[0],[],concept[2]]
            for i in exemplar_copy:
                for j in concept[1]:
                    if i[0] == j[0]:        # if dimensions match calculate difference
                        number = 0    
                        # find number of exemplars used for prototype                    
                        for count, h in enumerate(self.prototype_data):       
                            if h[0] == concept[0]:
                                for k in self.prototype_data[count][1]:
                                     if k[0] == i[0]:
                                        number += 1
                        # if there is prototypical data 
                        if number > 1:
                            difference = (i[1] - j[1])/ number      # calculate difference
                            mean = j[1] + difference
                            sd = 0
                            # calculate SD: sqrt( sum(x - mean)**2/n-1 )
                            for count, h in enumerate(self.prototype_data):       
                                if h[0] == concept[0]:
                                    for k in self.prototype_data[count][1]:
                                         if k[0] == i[0]:
                                            sd = sd + ((k[1] - mean)**2)
                            sd = sqrt(sd / (number-1))
                            concept_new[1].append([j[0], mean, sd])
                        # if there is no prototypical data
                        else:
                            difference = (i[1] - j[1])/ 2      # calculate difference
                            mean = j[1] + difference
                            concept_new[1].append([j[0], mean, 0.0])
            self.concepts.append(concept_new)
            
            
    def add_concept(self, concept, tag):
        """ adds a new concept to CP, not used for prototyping but as a single datapoint
            hence, the SD is 0.0
            concept = [ [d1, value], [d2, value], ..., [dn, value] ]
        """
        concept_new = copy.deepcopy(concept)         # make a copy of concept, so concept itself is not modified
        for count, i in enumerate(concept_new):      # add SD
            concept_new[count].append(0.0)
        self.concepts.append([tag, concept_new])
        
        
    def calculate_distance(self, point1, point2, list_salience = "empty" ):
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


    def calculate_similarity(self, point1, point2, sensitivity = 1.0 ):
        """ calculates the similarity between two given points
            based on the distance and the sensitivity
            after Nosofsky (1986)
            point = [ [d1, value], [d2, value], ..., [dn, value] ]
            sensitivity = float
        """
        e = math.e
        distance = self.calculate_distance(point1, point2)
        return e**(-sensitivity * distance)
        
            
    def merge_concepts(self):
        """ merges existing concepts in the CP if two concepts are close """
        # currently only works for matching RGB dimensions!!
        concept_coors = self.get_all_concept_coordinates()
        max_dis = aux.calculate_max_dis()
        check = False
        for count, i in enumerate(concept_coors):
            if check:
                break
            else:     
                for count2, j in enumerate(concept_coors):
                    if i is not j:
                        #calculate distance
                        distance = (self.calculate_distance(i, j)/max_dis)
                        # if distance is within threshold, merge concepts
                        if distance < cfg.merging_rate:
                            try:
                                tag1 = self.concepts[count][0]
                            except IndexError:
                                pass
                            tag2 = self.concepts[count2][0] 
                            new_concept = [ ["r", (i[0][1] + j[0][1])/2], ["g", (i[1][1] + j[1][1])/2], ["b", (i[2][1] + j[2][1])/2] ]
                            # SD info is forfeit
                            for count3, h in enumerate(self.concepts):
                                if h[0] == tag1:
                                    self.concepts.pop(count3)
                            for count3, h in enumerate(self.concepts):
                                if h[0] == tag2:
                                    self.concepts.pop(count3)
                            self.add_concept(new_concept, aux.generateRandomTag(6))
                            # print "merged"
                            check = True
                            break
    
                        

class CS():
    """ New implementation of Conceptual Space, using concept class objects
    """

    def __init__(self, name):
        """ initiate variables """
        self.holder_name = name     # name of the agent holding this CS
        self.concepts = []          # list of the concept objects the CS holds
        self.concept_tags = []      # list of concept tags
        self.n_concepts = 0         # number of concepts
        
        
    def add_concept(self, tag, concept_data):
        """ adds concept data to a concept for a given tag
            if no concept exists, a new one is created
            concept_data format = ["domain", [[ "d1", value], [ "d2", value], [ "d3", value]]]
        """
        new = True
        for i in self.concepts:
            if i.tag == tag:
                i.add_exemplar_data(concept_data)
                new = False
        if new:
            new_concept = concept.Concept(tag, concept_data)
            self.concepts.append(new_concept)
            self.concept_tags.append(tag)
            self.n_concepts += 1
            
                  
    def get_concept(self, tag):
        """ returns a concept object based on a given tag
        """
        for i in self.concepts:
            if i.tag == tag:
                return i

    def get_concepts(self):
        """ returns the concept objects currently in CS """
        return self.concepts
            
            
    def get_concepts_data(self):
        """ returns the data of the concepts currently in CS """
        concepts = []
        for i in self.concepts:
            concepts.append(i.get_data())
        return concepts
    
    
    def get_n_concepts(self):
        """ returns the number of concepts currently in CS """
        return len(self.concepts)
            

            