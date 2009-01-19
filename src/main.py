# basic model 0.7.1
# main.py

import agent
import data
import random as ran
import aux_functions as aux
import cfg
import globals as gl
import layout
import copy

def main():
    """ main run """
    init()
    for i in gl.agent_set:
        for j in gl.agent_set:
            if i is not j:
                for h in gl.training_data:
                    guessing_game(i, j, h)
        print gl.n_guessing_games
        
    
    for i in gl.agent_set:
        #i.print_matrix()
        print i.lex.labels
        print i.lex.tags
        print len(i.lex.tags)
        print len(i.lex.labels)
    
    print "shared lexicon: " + str(calculate_agents_lexicon()) + "%"    
    layout.run(gl.agent_set, cfg.space)
        
    
    
    
def init():
    """ initialises various parameters and values """
    # initialise agents
    i = 0
    while i < cfg.n_agents:
        agent_name = "agent" + str(i)
        ag = agent.BasicAgent(agent_name)
        gl.agent_set.append(ag)
        i += 1
    gl.n_guessing_games = 0
    gl.training_data = aux.generateTrainingData(cfg.space, cfg.n_training_datasets, cfg.context_size)
    


def guessing_game(agent1, agent2, context, topic_index = False):
    """ Guessing game which is played by two agents. Agent1 knows the topic, finds the closest
        matching concept and communicates the label with the strongest association to agent2.
        Agent2 uses this label and the associated concept to identify the topic from the context.
        If agent2 is able to identify the topic correctly, the guessing game succeeds.
        context = sets of data [ [ [d1, value], [d2, value], ..., [dn, value] ], ....]
    """
    if not topic_index:
        topic_index = ran.randint(0, len(context)-1)
    # agent1 plays discrimination game
    a1_disc_result = agent1.discrimination_game(context, topic_index)
    if a1_disc_result == ("concept_added" or "concept_shifted"):
        guessing_game_result = 0
    # if agent1 discrimination game succeeds, i.e. the result is a string of 4 characters
    elif len(a1_disc_result) == 4:
        a1_topic_label = agent1.get_label(a1_disc_result)
        # if agent1 does not has a label for the topic
        if a1_topic_label == "no_label":
            label = aux.generateRandomLabel(5)
            agent1.lex.add_label(label, a1_disc_result)
            a1_topic_label = label
        a2_presumed_topic_index = agent2.answer_gg(a1_topic_label, context)
        # if agent2 correctly points to the topic the guessing game succeeds
        if a2_presumed_topic_index[0] == topic_index:
            guessing_game_result = 1
            agent1.increase_strength(a1_topic_label, a1_disc_result)
            agent2.increase_strength(a1_topic_label, a2_presumed_topic_index[1])
            agent2.add_exemplar(context[topic_index], a1_topic_label) # shift cat towards topic
        # if agent2 does not know the communicated label
        elif a2_presumed_topic_index == "label_unknown":
            guessing_game_result = 0
            a2_disc_result = agent2.discrimination_game(context, topic_index, a1_topic_label)
            if a2_disc_result != ("concept_added" or "concept_shifted"):
                agent2.add_concept(context[topic_index], a1_topic_label)
            agent1.decrease_strength(a1_topic_label, a1_disc_result)
        # if agent2 knows the label, but does not point to the right topic
        else:
            guessing_game_result = 0
            agent1.decrease_strength(a1_topic_label, a1_disc_result)
            agent2.decrease_strength(a1_topic_label, a2_presumed_topic_index[1])
    
    # statistics
    gl.n_guessing_games += 1
        
        
def calculate_agents_lexicon():
    """ calculates the percentage of agents lexicon which matches the lexicon of other agents
    """
    matching = 1
    for i in gl.agent_set:
        uniques = 0.0
        for j in i.lex.labels:
            check = 0
            for k in gl.agent_set:
                if i is not k:
                    if j in k.lex.labels:
                        check = 1
            if not check:
                uniques += 1
        if len(i.lex.labels) == 0:
            length = 1
        else: 
            length = len(i.lex.labels)
        matching -= (uniques/length/len(gl.agent_set))
    return int(matching * 100)
            
        

# main start
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    