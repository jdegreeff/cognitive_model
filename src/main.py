# basic model 0.8
# CONCEPT project
# University of Plymouth
# Joachim de Greeff
# More information at http://www.tech.plym.ac.uk/SoCCE/CONCEPT/
# main.py

from __future__ import division
import agent
import data
import random as ran
import aux_functions as aux
import cfg
import globals as gl
import layout
import copy
import io

def main():
    """ main run """
    init()
    
#    gl.agent_set[0].add_concept(data.exemplar1, "CONC1")
#    gl.agent_set[0].add_exemplar(data.exemplar2, "CONC1")
#    gl.agent_set[0].add_exemplar(data.exemplar3, "CONC1")
#    
#    gl.agent_set[0].add_exemplar(data.exemplar4, "CONC2")
#    gl.agent_set[0].add_exemplar(data.exemplar5, "CONC2")
#    
#    concept_coors = gl.agent_set[0].cp.get_all_concept_coordinates()
#    print gl.agent_set[0].cp.calculate_distance(concept_coors[0], concept_coors[1])
#    print gl.agent_set[0].cp.calculate_distance(data.test_points[0], data.test_points[1])
    
    # discrimination game section
#    for i in gl.agent_set:
#        for j in gl.training_data:
#            i.discrimination_game(j, 0)
#        
#    print gl.agent_set[0].get_concepts()
#    for i in gl.agent_set:
#        print i.get_n_concepts()
#        print i.cp.prototype_data
#        print len(i.cp.prototype_data)
#    layout.run(gl.agent_set, cfg.space)

    
    #layout.run2()
    main_loop()

    for i in gl.agent_set:
#        i.print_matrix()
#        print i.lex.labels
#        print i.lex.tags
#        print i.get_concepts()
#        print i.cp.prototype_data
        print len(i.lex.tags)
        print len(i.get_concepts())
        print len(i.lex.labels)
    
    print "shared lexicon: " + str(calculate_agents_lexicon()) + "%"    
    layout.run(gl.agent_set, cfg.space)
        
    
def main_loop():
    """ main loop """
    for i in gl.agent_set:
        for j in gl.agent_set:
            if i is not j:
                for h in gl.training_data:
                    guessing_game(i, j, h)
                    if gl.n_guessing_games % 2:
                        guessing_game(i, j, h)
                    else:
                        guessing_game(j, i, h)
                    # practical printout, may be reconsidered
                    if (gl.n_guessing_games % (cfg.n_training_datasets/2)) == 0:
                        print "%.2f percent done" % ((gl.n_guessing_games/((cfg.n_training_datasets * (cfg.n_agents-1)) * cfg.n_agents)/2)*100) 
                        print "communication success: " + str(gl.guessing_succes)
                    
                    
                    
    
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
    gl.data_tony = io.open_datafile("natural", "rgb")
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
    if a1_disc_result == "concept_shifted":
        guessing_game_result = 0
    # if agent1 discrimination game succeeds, i.e. the result is a string of 4 characters
    elif len(a1_disc_result) == 4:
        a1_topic_label = agent1.get_label(a1_disc_result)
        # if agent1 does not has a label for the topic, a new label is created and added to the lexicon
        if a1_topic_label == "tag_unknown":
            label = aux.generateRandomLabel(5)
            agent1.add_label(label, a1_disc_result)
            a1_topic_label = label
        a2_guessing_game_answer = agent2.answer_gg(a1_topic_label, context)
        # if agent2 correctly points to the topic the guessing game succeeds
        if a2_guessing_game_answer[0] == topic_index:
            guessing_game_result = 1
            agent1.increase_strength(a1_topic_label, a1_disc_result)
            agent2.increase_strength(a1_topic_label, a2_guessing_game_answer[1])
            agent2.add_exemplar(context[topic_index], a2_guessing_game_answer[1]) # shift cat towards topic
        # if agent2 does not know the communicated label
        elif a2_guessing_game_answer == "label_unknown":
            guessing_game_result = 0
            a2_disc_result = agent2.discrimination_game(context, topic_index)
            agent2.add_label(a1_topic_label, a2_disc_result)
            agent1.decrease_strength(a1_topic_label, a1_disc_result)
        # if agent2 knows the label, but points to the wrong topic
        else:
            guessing_game_result = 0
            agent1.decrease_strength(a1_topic_label, a1_disc_result)
            agent2.decrease_strength(a1_topic_label, a2_guessing_game_answer[1])
    
    # statistics
    gl.n_guessing_games += 1
    agent1.n_guessing_games += 1
    agent2.n_guessing_games += 1
    if guessing_game_result:
        agent1.n_succes_gg += 1
        agent2.n_succes_gg += 1
        gl.n_succes_gg += 1
    agent1.guessing_succes = agent1.n_succes_gg/agent1.n_guessing_games
    agent2.guessing_succes = agent1.n_succes_gg/agent1.n_guessing_games
    gl.guessing_succes = gl.n_succes_gg/gl.n_guessing_games
        
        
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
    
    
    
    
    
    
    