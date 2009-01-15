# basic model 0.6
# main.py

import agent
import data
import random as ran

def main():
    """ main run """
    agent1 = agent.BasicAgent("agent_one")
    agent1.add_exemplar(data.exemplar1, "CONC1")
    agent1.add_exemplar(data.exemplar2, "CONC1")
    agent1.add_exemplar(data.exemplar3, "CONC1")
    agent1.add_exemplar(data.exemplar4, "CONC1")
    
    agent1.add_exemplar(data.exemplar4, "CONC2")
    agent1.add_exemplar(data.exemplar5, "CONC2")
    agent1.add_exemplar(data.exemplar6, "CONC2")
    agent1.add_exemplar(data.exemplar7, "CONC2")
    agent1.add_exemplar(data.exemplar9, "CONC3")

#    agent1.lex.add_label("test1", "adff")

    print agent1.cp.prototype_data
    print agent1.get_concepts()
    print agent1.get_labels()

    print agent1.discrimination_game(data.disc_game_data1, 0)
    
    agent1.print_matrix()
    print agent1.get_concepts()
    

def guessing_game(agent1, agent2, context, topic_index = False):
    """ Guessing game which is played by two agents. Agent1 knows the topic, finds the closest
        matching concept and communicates the label with the strongest association to agent2.
        Agent2 uses this label and the associated concept to identify the topic from the context.
        If agent2 is able to identify the topic correctly, the guessing game succeeds.
        context = sets of data [ [ [d1, value], [d2, value], ..., [dn, value] ], ....]
    """
    if not topic_index:
        topic_index = ran.randint(0, len(context))
    # agent1 plays discrimination game
    a1_disc_result = agent1.discrimination_game(context, topic_index)
    if disc_result_agent1 == ("concept_added" or "concept_shifted"):
        guessing_game_result = 0
    # if agent1 discrimination game succeeds
    else:
        a1_topic_label = agent1.get_label(disc_result_agent1)
        a2_presumed_topic_index = agent2.answer_gg(a1_topic_label, context)
        # if agent2 correctly points to the topic the guessing game succeeds
        if a2_presumed_topic_index[0] == topic_index:
            guessing_game_result = 1
            agent1.increase_strength(a1_topic_label, a1_disc_result)
            agent2.increase_strength(a1_topic_label, a2_presumed_topic_index[1])
            agent2.add_exemplar(context[topic_index], a1_topic_label) # shift cat towards topic
        # if agent2 does not know the communicated label
        elif a2_presumed_topic_index == "label_unknown":
            a2_disc_result = agent2.discrimination_game(context, topic_index, "no_label_addition")
        # if agent2 knows the label, but does not point to the right topic
        else:
            agent1.decrease_strength(a1_topic_label, a1_disc_result)
            agent2.decrease_strength(a1_topic_label, a2_presumed_topic_index[1])
        
        
        



# main start
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    