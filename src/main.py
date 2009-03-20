# basic model 0.8.6.1
# CONCEPT project
# University of Plymouth
# Joachim de Greeff
# More information at http://www.tech.plym.ac.uk/SoCCE/CONCEPT/
# main.py

# TODO: implementation of manhattan distance calculation for discrete metric
# TODO: implement a manner for compositionality; Gardenfors solution:  within a pair of concepts
#       one concept can override properties of the other concept based on salience

from __future__ import division
from PyQt4 import QtGui, QtCore
import random as ran
from threading import *
from math import *
import sys
import aux_functions as aux
import globals as gl
import agent
import data
import cfg
import layout
import copy
import io


def main():
    """ main in which various aspects of the program are initiated 
    """
    init()
    StartLayout([gl.agent1, gl.agent2], cfg.space)


class StartLayout():
    """ Starts the main graphical window and initiates the main running thread
    """
    def __init__(self, agents,  space):
        app = QtGui.QApplication(sys.argv)
        if cfg.use_graphics:
            main_window = layout.MainWindow(agents, space)
            main_window.show()
            self.thread1 = MainThread(main_window)
        else:
            self.thread1 = MainThread()
        self.thread1.start()
        sys.exit(app.exec_())
    
        
class MainThread(Thread):
    """ main thread 
    """
    def __init__(self, main_window = None, *args):
        apply(Thread.__init__, (self, ) + args)
        self.window = main_window
        
    def run(self):
        gl.loop_running = True
        while gl.current_loop < cfg.n_replicas:
            count = 0
            for i in gl.training_data:
                if cfg.direct_instruction:
                    direct_instruction(gl.agent1, gl.agent2)
                else:
                    guessing_game(gl.agent1, gl.agent2, i)
                if cfg.query_knowledge > 0:
                    if gl.n_guessing_games % cfg.query_knowledge == 0:
                        query_knowledge(gl.agent1, gl.agent2)
                if cfg.calc_statistics:
                    gl.stats[count][0] += float(gl.agent2.get_n_concepts())
                    gl.stats[count][1] += measure_agents_concepts_dist(gl.agent1, gl.agent2)
                    if cfg.calc_all:
                        gl.stats[count][2].append(measure_agent_knowledge(gl.agent1, gl.agent2, 100))
                    else:
                        gl.stats[count][2] += measure_agent_knowledge(gl.agent1, gl.agent2, 100)
                count += 1
                if self.window is not None:
                    self.window.update()
            print "replica " + str(gl.current_loop)
            if (gl.current_loop < cfg.n_replicas-1):
                reset()  
            gl.current_loop += 1
        gl.loop_running = False
        # statistics
        if cfg.calc_statistics:
            if cfg.calc_all:
                calculate_statistics2()
            else:
                calculate_statistics()
        print "done"
        gl.agent1.save_cp_to_xml()
        gl.agent2.save_cp_to_xml()
        


def calculate_statistics():
    """ calculates statistics and writes output file in the source directory,
        typically called after all loops are finished
    """
    count = 0           
    for i in gl.stats:
        count2 = 0
        for j in i:
            gl.stats[count][count2] = gl.stats[count][count2]/cfg.n_replicas
            count2 += 1
        count += 1
    name = "_direct" + str(cfg.direct_instruction) +"_" + str(cfg.space) + "_" + str(cfg.dataset) + "_tr" + str(cfg.n_training_datasets) + "_l" + str(cfg.n_replicas) \
            + "_al" + str(cfg.active_learning) + "_cl" + str(cfg.contrastive_learning) + "_qk" + str(cfg.query_knowledge)
    io.write_output(name, gl.stats)
    
    
def calculate_statistics2():
    """ calculates statistics and writes output file in the source directory,
        typically called after all loops are finished, SD is included as well
    """
    count = 0           
    for i in gl.stats:
        gl.stats[count][0] = gl.stats[count][0]/cfg.n_replicas
        gl.stats[count][1] = gl.stats[count][1]/cfg.n_replicas
        count += 1
    name = "_direct" + str(cfg.direct_instruction) +"_" + str(cfg.space) + "_" + str(cfg.dataset) + "_tr" + str(cfg.n_training_datasets) + "_l" + str(cfg.n_replicas) \
            + "_al" + str(cfg.active_learning) + "_cl" + str(cfg.contrastive_learning) + "_qk" + str(cfg.query_knowledge)
    io.write_output2(name, gl.stats)
    
    
    
def init():
    """ initialises various parameters and values 
    """
    gl.agent1 = agent.OmniAgent("om1")
    gl.agent2 = agent.BasicAgent("ag1")
    #gl.data_tony = io.open_datafile(cfg.dataset, cfg.space)
    gl.training_data = aux.generateTrainingData(cfg.space, cfg.n_training_datasets, cfg.context_size)
    counter = 0
    while counter < cfg.n_training_datasets:
        if cfg.calc_all:
            gl.stats.append([0.0, 0.0, []])
        else:
            gl.stats.append([0.0, 0.0, 0.0])
        counter += 1


    
def reset():
    """ resets all global variables
    """
    gl.agent1 = agent.OmniAgent("om1")
    gl.agent2 = agent.BasicAgent("ag1")
    gl.training_data = aux.generateTrainingData(cfg.space, cfg.n_training_datasets, cfg.context_size)
    gl.n_guessing_games = 0
    gl.n_success_gg = 0
    gl.guessing_success = 0.0
    gl.loop_running = False



def guessing_game(agent1, agent2, context, topic_index = False):
    """ Guessing game which is played by two agents. Agent1 knows the topic, finds the closest
        matching concept and communicates the label with the strongest association to agent2.
        Agent2 uses this label and the associated concept to identify the topic from the context.
        If agent2 is able to identify the topic correctly, the guessing game succeeds.
        context = sets of data [ [ [d1, value], [d2, value], ..., [dn, value] ], ....]
    """
    if not topic_index:
        if cfg.active_learning and (agent2.get_n_concepts() > 0):
            a2_context_distance = []
            a2_known_concepts = agent2.cp.get_all_concept_coordinates()
            for i in context:
                distances = []
                for j in a2_known_concepts:
                    distances.append(agent2.cp.calculate_distance(i, j))
                a2_context_distance.append(min(distances))
            topic_index = aux.posMax(a2_context_distance)
        else:
            topic_index = ran.randint(0, len(context)-1)
    # agent1 plays discrimination game
    a1_disc_result = agent1.discrimination_game(context, topic_index) 
    if a1_disc_result == "concept_shifted":
        guessing_game_result = 0
    # if agent1 discrimination game succeeds, i.e. the result is a string of 4 characters
    elif len(a1_disc_result) == 6:
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
            agent2.add_exemplar(context[topic_index], a2_guessing_game_answer[1]) # shift matching concept towards topic
            agent2.concept_use(a2_guessing_game_answer[1], 1) # measure concept use
            if cfg.contrastive_learning:
                count = 0
                for i in context:
                    if count is not topic_index:
                        a2_matching_concept = agent2.get_matching_concept(context[count])
                        agent2.decrease_strength(a1_topic_label, a2_matching_concept)
                    count += 1
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
            a2_disc_result = agent2.discrimination_game(context, topic_index)   # possibly learn new concept
            agent2.add_label(a1_topic_label, a2_disc_result)
            agent2.concept_use(a2_guessing_game_answer[1]) # measure concept use
    
    # statistics
    gl.n_guessing_games += 1
    agent1.n_guessing_games += 1
    agent2.n_guessing_games += 1
    if guessing_game_result:
        agent1.n_success_gg += 1
        agent2.n_success_gg += 1
        gl.n_success_gg += 1
    agent1.guessing_success = agent1.n_success_gg/agent1.n_guessing_games
    agent2.guessing_success = agent1.n_success_gg/agent1.n_guessing_games
    agent1.concept_history.append(agent1.get_n_concepts())
    agent2.concept_history.append(agent2.get_n_concepts())
    gl.guessing_success = gl.n_success_gg/gl.n_guessing_games
    
    
    
def direct_instruction(agent1, agent2):
    """ direct instruction involving a teacher (agent1) with a body of knowledge and a learner (agent2)
        a random stimulus is picked, and presented to both teacher and learner. The teacher 
        expresses its associated label for the stimulus and the learner stores both label and
        stimulus into its knowledge body
    """
    stimulus = aux.generateTrainingData(cfg.space, 1, 1)[0][0]
    if cfg.teaching_inaccuracy:
        int = ran.randint(1,100)
        if int > (1-cfg.teaching_inaccuracy) * 100:
            a1_label = agent1.get_label(agent1.get_matching_concept(stimulus), 1)
        else:
            a1_label = agent1.get_label(agent1.get_matching_concept(stimulus))
    else:
        a1_label = agent1.get_label(agent1.get_matching_concept(stimulus))
    a2_tag = agent2.get_tag(a1_label)
    if a2_tag == "label_unknown":
        tag = aux.generateRandomTag(6)
        agent2.add_exemplar(stimulus, tag)
        agent2.add_label(a1_label, tag)
    else:
        agent2.add_exemplar(stimulus, a2_tag)
    
    
    
def query_knowledge(agent1, agent2):
    """ agent2 queries knowledge with agent1, 
        based on the answer, agent2 updates it's association matrix
    """
    a2_label_concept = agent2.get_unsure_concept()
    if a2_label_concept:
        a1_answer = agent1.answer_query(a2_label_concept)
        if a1_answer:
            agent2.increase_strength(a2_label_concept[0], a2_label_concept[1][0], 0.1)
        else:
            agent2.decrease_strength(a2_label_concept[0], a2_label_concept[1][0], 0.1)



def measure_agent_knowledge(agent1, agent2, n_tests):
    """ teacher (agent1) and learner (agent2) are given a random test concept
        teacher gives the label and learner has to label it as well
        if the labels are the same, learner succeeds the test, of not, learner fails
        measurement is repeated for n_tests times, return is % of success
    """
    count = 0
    correctness = 0.0
    while count < n_tests:
        test_concept = aux.generateTrainingData(cfg.space, 1, 1)[0][0]
        a1_label = agent1.get_label(agent1.get_matching_concept(test_concept))
        a2_label = agent2.get_label(agent2.get_matching_concept(test_concept))
        #a2_label = agent2.get_label(agent2.get_random_concept())
        if a1_label == a2_label:
            correctness += 1
        count += 1
    return correctness/count
    

        
        
def measure_agents_lexicon():
    """ calculates the percentage of agents lexicon which matches the lexicon of other agents
        TODO: modify this function so that it counts only proper labels,
        right now it is taking all labels into account, also the ones which have a very low connection
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
            
        
        
def measure_agents_concepts_dist(agent1, agent2):
    """ measures the distance between the concepts of two given agents
        for each concept of one agent, the closest concept of the second agent is found
        and the difference is added to the overall distance, and this is done vice versa
    """
    agent1_concepts = agent1.get_all_concept_coordinates()
    agent2_concepts = agent2.get_all_concept_coordinates()
    concepts_distance = 0.0
    for i in agent1_concepts:
        distances = []
        for j in agent2_concepts:
            distance = aux.calculate_distance_general(i, j)
            distances.append(distance)
        if distances:
            concepts_distance += min(distances)
    for i in agent2_concepts:
        distances = []
        for j in agent1_concepts:
            distance = aux.calculate_distance_general(i, j)
            distances.append(distance)
        if distances:
            concepts_distance += min(distances)
    return sqrt(concepts_distance)
        
        

# main start
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    