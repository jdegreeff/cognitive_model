# agent.py

import cp
import lexicon
import aux_functions as aux
import cfg
import copy


class BasicAgent():
    """ Basic Agent consisting of conceptual space linked to lexicon
    """
    
    def __init__(self, name):
        """ initiate variables """
        self.agent_name = name                      # agent name
        self.cp = cp.CP(self.agent_name)            # agents conceptual space
        self.lex = lexicon.Lexicon(self.agent_name) # agents lexicon
        self.n_discrimination_games = 0             # number of discrimination games played by the agent
        self.n_succes_games = 0                     # number of successful discrimination games
        self.discrimination_succes = 0.0            # agents discrimination success ratio


    def get_cp(self):
        """ Returns the conceptual space of the agent """
        return self.cp
    
    
    def get_name(self):
        return self.agent_name
                            
                                
    def add_exemplar(self, exemplar, label):
        """ adds exemplar data to the CP and the label to the lexicon """
        exemplar_new = copy.deepcopy(exemplar)    # make a copy
        # label is known
        if label in self.lex.get_labels():   
            tag = self.lex.get_tag(label)
        # label is not known
        else:                           
            tag = aux.generateRandomTag(4)
            self.lex.add_label(label, tag)
        self.cp.add_exemplar(exemplar_new, tag)
        
        
    def add_concept(self, concept, label):
        """ adds a concept to the CP and the label to the lexicon 
            it is not be used for the prototype however, and hence the data 
            will not be stored in the cp.prototype_data
        """                      
        concept_new = copy.deepcopy(concept)    # make a copy     
        tag = aux.generateRandomTag(4)
        self.lex.add_label(label, tag)
        self.cp.add_concept(concept, tag)
        
        
    def discrimination_game(self, context, topic_index):
        """ Discrimination game in which an agent has to distinguish the topic
            from the context. The game succeeds if the agent has a concept 
            which uniquely matches the topic and no other stimuli from the context.
            If this is not the case, a new concept is build, or the existing concepts
            are shifted.
            The return is either the concept tag, or a string description of the action taken by the agent
            context = sets of data [ [ [d1, value], [d2, value], ..., [dn, value] ], ....]
        """
        context_new = copy.deepcopy(context)    # make a copy   
        # get the coordinates of the current known concepts
        known_concept_coors = self.cp.get_all_concept_coordinates()
        if len(known_concept_coors) == 0:
            label = aux.generateRandomLabel(5)
            self.add_concept(context[topic_index], label)
            answer = "concept_added"
        else:
            # select the best matching concept for every stimulus from the context (including the topic)
            best_matching_concepts = []
            for i in context:
                distances = []
                for j in known_concept_coors:
                    distances.append(self.cp.calculate_distance(i, j))
                best_matching_concept = self.cp.get_concepts_tags()[aux.posMin(distances)]
                best_matching_concepts.append(best_matching_concept)
            if best_matching_concepts.count(best_matching_concepts[topic_index]) == 1:
                self.n_succes_games += 1.0
                answer = best_matching_concepts[topic_index]
            else:
                # if agent discrimination success is below threshold a new concept is created
                if self.discrimination_succes < cfg.adapt_threshold:
                    label = aux.generateRandomLabel(5)
                    self.add_concept(context[topic_index], label)
                    answer = "concept_added"
                # if agent discrimination success is above threshold, 
                # topic is added as exemplar for the best matching concept, 
                # i.e. the best matching concept is shifted towards the topic
                else:
                    self.lex.get_label(best_matching_concepts[topic_index])
                    self.add_exemplar(context[topic_index], label)
                    answer = "concept_shifted"
                    
        # calculate statistics
        self.n_discrimination_games += 1.0
        self.discrimination_succes = self.n_succes_games/self.n_discrimination_games
        return answer
        
        
    def answer_gg(self, label, context):
        """ Guessing game answer. Agent uses the incoming label and the associated 
            concept to identify the topic from the context, 
            the presumed topic index is communicated to the other agent.
        """
        tag = self.get_tag(label)
        if tag == "no_tag":
            return tag
        else:
            context_distances = []
            for i in context:
                distance = self.cp.calculate_distance(i, self.cp.get_concept_coordinates(tag))
                context_distances.append(distance)
            return [aux.posMin(context_distances), tag]
        
        
    def increase_strength(self, label, tag):
        """ increases the association strength between the given label and tag
        """
        self.lex.increase_strenth(label, tag)
            

    def get_concepts(self):
        return self.cp.get_concepts()
       
       
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
            
            
            
            
            
            