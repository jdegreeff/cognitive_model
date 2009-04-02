# agent2.py

from __future__ import division
import random as ran
import copy
import globals as gl
import cp, lexicon, aux, cfg, data, io


class LearningAgent():
    """ Learning Agent consisting of conceptual space linked to lexicon
    """
    
    def __init__(self, name):
        """ initiate variables """
        self.agent_name = name                      # agent name
        self.agent_type = "learner"                 # agent type: "learner" or "teacher"
        self.cs = cp.CS(self.agent_name)            # agents conceptual space
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
