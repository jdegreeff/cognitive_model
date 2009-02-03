# agent.py

from __future__ import division
import cp
import lexicon
import aux_functions as aux
import cfg
import copy
import globals as gl
import data


class BasicAgent():
    """ Basic Agent consisting of conceptual space linked to lexicon
    """
    
    def __init__(self, name):
        """ initiate variables """
        self.agent_name = name                      # agent name
        self.agent_type = "basic"                   # agent type: "basic" or "omni"
        self.cp = cp.CP(self.agent_name)            # agents conceptual space
        self.lex = lexicon.Lexicon(self.agent_name) # agents lexicon
        self.n_discrimination_games = 0             # number of discrimination games played by the agent
        self.n_succes_dg = 0                        # number of successful discrimination games
        self.discrimination_succes = 0.0            # agents discrimination success ratio
        self.n_guessing_games = 0                   # number of guessing games played by the agent
        self.n_succes_gg = 0                        # number of successful guessing games
        self.guessing_succes = 0.0                  # agents guessing success ratio
        self.concept_history = []                   # list containing number of concepts agent has after each interaction (game)
        
        
    def add_exemplar(self, exemplar, tag):
        """ adds exemplar data to the concept of the given tag """ 
        self.cp.add_exemplar(copy.deepcopy(exemplar), tag)
        
        
    def add_concept(self, concept, tag):
        """ adds a concept to the CP
            it is not be used for the prototype however, and hence the data 
            will not be stored in the cp.prototype_data
        """                                
        self.cp.add_concept(copy.deepcopy(concept), tag)
        
        
    def add_label(self, label, tag):
        """ adds a label for the given tag the given tag """ 
        self.lex.add_label(label, tag)
        
        
    def discrimination_game(self, context, topic_index):
        """ Discrimination game in which an agent has to distinguish the topic
            from the context. The game succeeds if the agent has a concept 
            which uniquely matches the topic and no other stimuli from the context.
            If this is not the case, a new concept is build, or the existing concepts
            are shifted.
            The return is either the concept tag, a string description of the action taken by the agent
            context = sets of data [ [ [d1, value], [d2, value], ..., [dn, value] ], ....]
        """
        context_new = copy.deepcopy(context)    # make a copy
        # get the coordinates of the current known concepts
        known_concept_coors = self.cp.get_all_concept_coordinates()
        if len(known_concept_coors) == 0:
            tag = aux.generateRandomTag(4)
            #self.add_concept(context_new[topic_index], tag)
            self.add_exemplar(context_new[topic_index], tag)    # no new concepts are stored, only exemplars
            answer = tag
        else:
            # select the best matching concept for every stimulus from the context (including the topic)
            best_matching_concepts = []
            for i in context_new:
                distances = []
                for j in known_concept_coors:
                    distances.append(self.cp.calculate_distance(i, j))
                best_matching_concept = self.cp.get_concepts_tags()[aux.posMin(distances)]
                best_matching_concepts.append(best_matching_concept)
            if best_matching_concepts.count(best_matching_concepts[topic_index]) == 1:
                self.n_succes_dg += 1.0
                answer = best_matching_concepts[topic_index]
            else:
                # if agent discrimination success is below threshold a new concept is created
                if self.discrimination_succes < cfg.adapt_threshold:
                    tag = aux.generateRandomTag(4)
                    #self.add_concept(context_new[topic_index], tag)
                    self.add_exemplar(context_new[topic_index], tag)    # no new concepts are stored, only exemplars
                    answer = tag
                # if agent discrimination success is above threshold, 
                # topic is added as exemplar for the best matching concept, 
                # i.e. the best matching concept is shifted towards the topic
                else:
                    tag = best_matching_concepts[topic_index]
                    self.add_exemplar(context_new[topic_index], tag)
                    answer = tag
                    
        # merge concepts
        if cfg.merge_concepts:
            self.cp.merge_concepts()
                    
        # calculate statistics
        self.n_discrimination_games += 1.0
        self.discrimination_succes = self.n_succes_dg/self.n_discrimination_games
        return answer
        
        
    def answer_gg(self, label, context):
        """ Guessing game answer. Agent uses the incoming label and the associated 
            concept to identify the topic from the context, 
            the presumed topic index is communicated to the other agent.
        """
        tag = self.get_tag(label)
        if tag == "label_unknown":
            return tag
        else:
            context_distances = []
            for i in context:
                distance = self.cp.calculate_distance(i, self.cp.get_concept_coordinates(tag))
                context_distances.append(distance)
            return [aux.posMin(context_distances), tag]
        
        
    def increase_strength(self, label, tag):
        """ increases the association strength between the given label and tag """
        self.lex.increase_strength(label, tag)
        
    def decrease_strength(self, label, tag):
        """ decreases the association strength between the given label and tag """
        self.lex.decrease_strength(label, tag)
        
    def get_name(self):
        return self.agent_name
    
    def get_cp(self):
        """ Returns the whole conceptual space of the agent """
        return self.cp
    
    def get_concepts(self):
        return self.cp.get_concepts()
    
    def get_all_concept_coordinates(self):
        """ returns the coordinates of all concepts in the CP """
        return self.cp.get_all_concept_coordinates()
    
    def get_n_concepts(self):
        """ returns the number of concepts currently in CP """
        return self.cp.get_n_concepts()
       
    def get_labels(self):
        return self.lex.get_labels()
    
    def get_label(self, tag):
        return self.lex.get_label(tag)
    
    def get_tags(self):
        return self.lex.get_tags()
    
    def get_tag(self, label):
        return self.lex.get_tag(label)
    
    def print_matrix(self):
        return self.lex.print_matrix()
            
            
            
            
class OmniAgent():
    """ Omniscient Agent used for training purpose. Agent has static knowledge of colour concept names.
    """
    
    def __init__(self, name):
        """ initiate variables """
        self.agent_name = name                      # agent name
        self.agent_type = "omni"                    # agent type: "basic" or "omni"
        self.cp = cp.CP(self.agent_name)            # agents conceptual space
        self.lex = lexicon.Lexicon(self.agent_name) # agents lexicon
        self.load_knowledge("rgb")                  # loads existing body of conceptual knowledge into cp and lexicon
        self.n_discrimination_games = 0             # number of discrimination games played by the agent
        self.n_succes_dg = 0                        # number of successful discrimination games
        self.discrimination_succes = 0.0            # agents discrimination success ratio
        self.n_guessing_games = 0                   # number of guessing games played by the agent
        self.n_succes_gg = 0                        # number of successful guessing games
        self.guessing_succes = 0.0                  # agents guessing success ratio
        self.concept_history = []                   # list containing number of concepts agent has after each interaction (
        
        
    def load_knowledge(self, domain):
        """ loads existing body of conceptual knowledge into cp and lexicon body
            domain determines which type of knowledge is used. Knowledge is added as concepts, 
            so no prototyping is done.
            Format of knowledge structures is: [ "label", [ ["d1", value], ["d2", value], ..., ["dn", value] ] ]
        """
        if domain == "rgb":
            knowledge = data.basic_colour_set
        for i in knowledge:
            tag = aux.generateRandomTag(4)
            self.add_concept(i[1], tag)
            self.add_label(i[0], tag)
        for count, i in enumerate(self.lex.matrix):     # increase connections strength to 1
            i[count] = 1.0
            
            
    def discrimination_game(self, context, topic_index):
        """ Discrimination game in which an agent has to distinguish the topic
            from the context. The game succeeds if the agent has a concept 
            which uniquely matches the topic and no other stimuli from the context.
            The return is either the concept tag, a string description of the action taken by the agent
            context = sets of data [ [ [d1, value], [d2, value], ..., [dn, value] ], ....]
        """
        context_new = copy.deepcopy(context)    # make a copy 
        # select the best matching concept for every stimulus from the context (including the topic)
        # get the coordinates of the current known concepts
        known_concept_coors = self.cp.get_all_concept_coordinates()
        best_matching_concepts = []
        for i in context_new:
            distances = []
            for j in known_concept_coors:
                distances.append(self.cp.calculate_distance(i, j))
            best_matching_concept = self.cp.get_concepts_tags()[aux.posMin(distances)]
            best_matching_concepts.append(best_matching_concept)
        if best_matching_concepts.count(best_matching_concepts[topic_index]) == 1:
            self.n_succes_dg += 1.0
            answer = best_matching_concepts[topic_index]
        else:
            answer = "concept_shifted" # method to cause the guessing game to fail and do nothing
 
        # calculate statistics
        self.n_discrimination_games += 1.0
        self.discrimination_succes = self.n_succes_dg/self.n_discrimination_games
        return answer
            
        
    def add_concept(self, concept, tag):
        """ adds a concept to the CP
            it is not be used for the prototype however, and hence the data 
            will not be stored in the cp.prototype_data
        """                                   
        self.cp.add_concept(copy.deepcopy(concept), tag)
        
        
    def add_label(self, label, tag):
        """ adds a label for the given tag the given tag """ 
        self.lex.add_label(label, tag)
        
        
    def increase_strength(self, label, tag):
        """ NOT USED
            increases the association strength between the given label and tag
        """
        pass
        
        
    def decrease_strength(self, label, tag):
        """ NOT USED
            decreases the association strength between the given label and tag
        """
        pass
    
    
    def get_all_concept_coordinates(self):
        """ returns the coordinates of all concepts in the CP """
        return self.cp.get_all_concept_coordinates()
    
    def get_n_concepts(self):
        """ returns the number of concepts currently in CP """
        return self.cp.get_n_concepts()        
        
    def print_matrix(self):
        return self.lex.print_matrix()
        
    def get_concepts(self):
        return self.cp.get_concepts
    
    def get_label(self, tag):
        return self.lex.get_label(tag)
        
            
            
            