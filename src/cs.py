# cs.py
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


# Description of old CS implementation
#    """ Conceptual Space which holds conceptual knowledge of an agent
#        Regions represent prototypes of concepts, incoming objects can be assigned to 
#        the best fitting concept using a distance measure 
#        There are two ways in which concepts can be added:
#            1) through formation of prototypes: exemplars of concepts are used to 
#               calculate a mean prototype, the SD can be used as a radius
#               if the label of a given exemplar is known, the concept with the highest association
#               will be updated with the new exemplar data
#            2) through direct addition of a concept. Coordinates of exemplar data
#               are used for this, no prototype formation is used
#        Furthermore, concept coordinates may be shifted through language games
#        basic format of a concept 
#        = [ "tag", [ [ "d1", value], [ "d2", value], [ "d3", value] ], [concept_use, concept_success] ]
#    """


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
            
            
    def get_concept_data(self, tag):
        """ returns the data of a concept, based on a given tag
        """
        for i in self.concepts:
            if i.tag == tag:
                return i.get_data()[2]
            

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
            

    def concept_use(self, tag, result):
        """ measures the success of the concept in the guessing game
        """
        for i in self.concepts:
            if i.tag == tag:
                i.usage(result)
                
                
    def get_concept_use(self, tag):
        """ returns the use and success of the concept in the guessing game
        """
        for i in self.cocepts:
            if i.tag == tag:
                return [i.concept_use, i.concept_success]


    def get_unsuccessful_concept(self):
        """ returns the (tag, data) of the concept which is the must unsuccessful in guessing games
        """
        concept = None
        success = 1.0
        for i in self.concepts:
            if (1.0*i.concept_success)/(i.concept_use+1.0) < success:
                concept = i.get_data()
        return concept

            