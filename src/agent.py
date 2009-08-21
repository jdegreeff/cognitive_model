# agent2.py

from __future__ import division
import random as ran
import copy
import globals as gl
import cs, lexicon, aux, cfg, data, io


class LearningAgent():
    """ Learning Agent consisting of conceptual space linked to lexicon
    """
    
    def __init__(self, name):
        """ initiate variables """
        self.agent_name = name                      # agent name
        self.agent_type = "learner"                 # agent type: "learner" or "teacher"
        self.cs = cs.CS(self.agent_name)            # agents conceptual space
        self.lex = lexicon.Lexicon(self.agent_name) # agents lexicon
        self.n_discrimination_games = 0             # number of discrimination games played by the agent
        self.n_success_dg = 0                       # number of successful discrimination games
        self.discrimination_success = 0.0           # agents discrimination success ratio
        self.n_guessing_games = 0                   # number of guessing games played by the agent
        self.n_success_gg = 0                       # number of successful guessing games
        self.guessing_success = 0.0                 # agents guessing success ratio
        self.concept_history = []                   # list containing number of concepts agent has after each interaction (game)
        
        
    def add_concept(self, tag, concept_data):
        """ adds concept data to the concept for the given tag """ 
        self.cs.add_concept(tag, concept_data)
        
        
    def add_label(self, label, tag):
        """ adds a label for the given tag the given tag """ 
        self.lex.add_label(label, tag)
        

    def discrimination_game(self, context, topic_index):
        """ Discrimination game in which an agent has to distinguish the topic
            from the context. The game succeeds if the agent has a concept 
            which uniquely matches the topic and no other stimuli from the context.
            If this is not the case, a new concept is build, or the existing concepts
            are shifted.
            The tag of the concept (either successful, shifted or new) is returned
            context = sets of data [  [ "domain", [ [d1, value], [d2, value], ..., [dn, value] ]], ..., ]
        """
        if self.n_discrimination_games > 10:
            pass
        context_new = copy.deepcopy(context)    # make a copy
        # if no concepts exits, create a new one on the topic coordinates
        if self.cs.get_n_concepts() == 0:
            tag = aux.generateRandomTag(6)
            self.add_concept(tag, context[topic_index])
            answer = tag
        else:
            # select the best matching concept for each item in the context
            best_matching_concepts = []
            for i in context_new:
                distances = []
                for j in self.cs.concepts:
                    data = j.get_data()
                    distances.append(aux.calculate_distance(i, data[1]))
                best_matching_concept = self.cs.concept_tags[aux.posMin(distances)]
                best_matching_concepts.append(best_matching_concept)
            # determine the outcome of the guessing game
            if best_matching_concepts.count(best_matching_concepts[topic_index]) == 1:
                self.n_success_dg += 1.0
                answer = best_matching_concepts[topic_index]
            else:
                # if agent discrimination success is below threshold a new concept is created
                if self.discrimination_success < cfg.adapt_threshold:
                    tag = aux.generateRandomTag(6)
                    self.add_concept(tag, context[topic_index])
                    answer = tag
                # else, the best matching concept is shifted towards the topic
                else:
                    tag = best_matching_concepts[topic_index]
                    self.add_concept(tag, context[topic_index])
                    answer = tag
        # calculate statistics
        self.n_discrimination_games += 1
        self.discrimination_success = self.n_success_dg/self.n_discrimination_games
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
                distance = aux.calculate_distance(i, self.cs.get_concept_data(tag))
                context_distances.append(distance)
            return [aux.posMin(context_distances), tag]
        
        
    def get_matching_concept(self, coors):
        """ returns the closest matching concept tag, based on incoming coordinates
        """
        distances = []
        for i in self.cs.concepts:
            distances.append(aux.calculate_distance(coors, i.get_data()[1]))
        if distances:
            return self.cs.concept_tags[aux.posMin(distances)]
        else:
            return "----"
        

    def concept_use(self, tag, result = 0):
        """ measures the success of the concept in the guessing game
        """
        self.cs.concept_use(tag, result)


    def increase_strength(self, label, tag, amount = None):
        """ increases the association strength between the given label and tag with the given amount """
        if amount == None:
            amount = cfg.label_learning_rate
        self.lex.increase_strength(label, tag, amount)
        
        
    def decrease_strength(self, label, tag, amount = None):
        """ decreases the association strength between the given label and tag with the given amount"""
        if amount == None:
            amount = cfg.label_learning_rate
        self.lex.decrease_strength(label, tag, amount)
        

    def get_tag(self, label):
        return self.lex.get_tag(label)


    def get_label(self, tag, inaccuracy = None):
        return self.lex.get_label(tag, inaccuracy)
    
    
    def get_n_concepts(self):
        """ returns the number of concepts currently in the agents CS """
        return self.cs.get_n_concepts()
    
    
    def get_unsuccessful_concept(self):
        """ returns the [label, concept_data] of the concept which is the must unsuccessful in guessing games """
        concept_data = self.cs.get_unsuccessful_concept()
        label = self.get_label(concept_data[0])
        return [label, concept_data]



class TeachingAgent():
    """ Learning Agent consisting of conceptual space linked to lexicon
    """
    
    def __init__(self, name):
        """ initiate variables """
        self.agent_name = name                      # agent name
        self.agent_type = "teacher"                 # agent type: "learner" or "teacher"
        self.cs = cs.CS(self.agent_name)            # agents conceptual space
        self.lex = lexicon.Lexicon(self.agent_name) # agents lexicon
        self.load_knowledge()                       # loads existing body of conceptual knowledge into cs and lexicon
        self.n_discrimination_games = 0             # number of discrimination games played by the agent
        self.n_success_dg = 0                       # number of successful discrimination games
        self.discrimination_success = 0.0           # agents discrimination success ratio
        self.n_guessing_games = 0                   # number of guessing games played by the agent
        self.n_success_gg = 0                       # number of successful guessing games
        self.guessing_success = 0.0                 # agents guessing success ratio
        self.concept_history = []                   # list containing number of concepts agent has after each interaction (game)
        
    def add_concept(self, tag, concept_data):
        """ adds concept data to the concept for the given tag """ 
        self.cs.add_concept(tag, concept_data)
        
        
    def add_label(self, label, tag):
        """ adds a label for the given tag the given tag """ 
        self.lex.add_label(label, tag)
        
        
    def load_knowledge(self):
        """ loads existing body of conceptual knowledge into cs and lexicon body
            domain determines which type of knowledge is used. 
            Knowledge is added as concepts
            Format of knowledge structures is: [ "label", [ ["d1", value], ["d2", value], ..., ["dn", value] ] ]
        """
        for i in cfg.space:
            if i == "rgb":
                knowledge = data.basic_colour_rgb
            if i == "lab":
                knowledge = data.basic_colour_lab
            if i == "shape":
                knowledge = data.shape_data
            for j in knowledge:
                tag = aux.generateRandomTag(6)
                self.add_concept(tag, [[i, j[1]]])
                self.add_label(j[0], tag)
            for count, j in enumerate(self.lex.matrix):     # increase connections strength to 1
                j[count] = 1.0
                
    def discrimination_game(self, context, topic_index):
        """ Discrimination game in which an agent has to distinguish the topic
            from the context. The game succeeds if the agent has a concept 
            which uniquely matches the topic and no other stimuli from the context.
            If this is not the case, a new concept is build, or the existing concepts
            are shifted.
            The tag of the concept (either successful, shifted or new) is returned
            context = sets of data [  [ "domain", [ [d1, value], [d2, value], ..., [dn, value] ]], ..., ]
        """
        context_new = copy.deepcopy(context)    # make a copy
        # select the best matching concept for each item in the context
        best_matching_concepts = []
        for i in context_new:
            distances = []
            for j in self.cs.concepts:
                data = j.get_data()
                distances.append(aux.calculate_distance(i, data[1]))
            best_matching_concept = self.cs.concept_tags[aux.posMin(distances)]
            best_matching_concepts.append(best_matching_concept)
        # determine the outcome of the guessing game
        if best_matching_concepts.count(best_matching_concepts[topic_index]) == 1:
            self.n_success_dg += 1.0
            answer = best_matching_concepts[topic_index]
        else:
            answer = "concept_shifted" # method to cause the guessing game to fail and do nothing
        # calculate statistics
        self.n_discrimination_games += 1
        self.discrimination_success = self.n_success_dg/self.n_discrimination_games
        return answer
    

    def get_matching_concept(self, coors):
        """ returns the closest matching concept tag, based on incoming coordinates
        """
        distances = []
        for i in self.cs.concepts:
            distances.append(aux.calculate_distance(coors, i.get_data()[1]))
        if distances:
            return self.cs.concept_tags[aux.posMin(distances)]
        else:
            return "----"
        
        
    def answer_query(self, label_concept):
        """ incoming concept = ["label", concept]
            agent checks if the label and concept are associated in agent's own lexicon
            if so, answer is True, otherwise False
        """
        coors = label_concept[1][1]
        tag = self.get_matching_concept(coors)
        label = self.get_label(tag)
        if label == label_concept[0]:
            return True
        else:
            return False
        
        
    def get_label(self, tag, inaccuracy = None):
        return self.lex.get_label(tag, inaccuracy)
    
    def get_n_concepts(self):
        """ returns the number of concepts currently in the agents CS """
        return self.cs.get_n_concepts()

    def increase_strength(self, label, tag):
        """ NOT USED """
        pass
        
    def decrease_strength(self, label, tag):
        """ NOT USED """
        pass
        