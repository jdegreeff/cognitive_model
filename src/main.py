# basic model 0.7
# main.py

import agent
import data
import random as ran
import aux_functions as aux
import cfg

def main():
    """ main run """

    training_data = aux.generateRGBTrainingDataUniform(300, 3)
    for i in training_data:
        guessing_game(agent1, agent2, i)
    
    
#    agent1.add_exemplar(data.exemplar1, "CONC1")
#    print agent1.cp.prototype_data
#    print agent1.get_concepts()
#    print agent1.get_labels()
#    print agent1.discrimination_game(data.disc_game_data1, 0)
    agent1.print_matrix()
    agent2.print_matrix()
    print agent1.get_concepts()
    print agent2.get_concepts()
    print len(agent1.lex.tags)
    print len(agent2.lex.tags)
    print len(agent1.lex.labels)
    print len(agent2.lex.labels)
    print agent1.lex.labels
    print agent2.lex.labels
    
    
def initialize():
    """ initialises various parameters and values """
    global agent_set = []
    i = 0
    while i < cfg.n_agents:
        agent_name = "agent" + str(i)
        agent = agent.BasicAgent(agent_name)
        agent_set.append(agent)
        i += 1
    

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
    # if agent1 discrimination game succeeds
    else:
        a1_topic_label = agent1.get_label(a1_disc_result)
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
        # if agent2 knows the label, but does not point to the right topic
        else:
            guessing_game_result = 0
            agent1.decrease_strength(a1_topic_label, a1_disc_result)
            agent2.decrease_strength(a1_topic_label, a2_presumed_topic_index[1])
        
        
        

# main start
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    