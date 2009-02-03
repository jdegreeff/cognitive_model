# basic model 0.8.5
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
        while gl.current_loop < cfg.n_loops:
            count = 0
            for i in gl.training_data:
                guessing_game(gl.agent1, gl.agent2, i)
                gl.stats[count][0] += float(gl.agent2.get_n_concepts())
                gl.stats[count][1] += gl.guessing_succes
                count += 1
                if self.window is not None:
                    self.window.update()
            gl.current_loop += 1
            print "loop " + str(gl.current_loop)
            gl.distance += measure_agents_concepts_dist(gl.agent1, gl.agent2)
            reset()  
        gl.loop_running = False 
        
        # calculate statistics
        gl.distance = gl.distance/cfg.n_loops
        count = 0           
        for i in gl.stats:
            count2 = 0
            for j in i:
                gl.stats[count][count2] = gl.stats[count][count2]/cfg.n_loops
                count2 += 1
            count += 1
        name = "_overall_tr" + str(cfg.n_training_datasets) + "_l" + str(cfg.n_loops) + "_ac" + str(cfg.active_learning)
        io.write_output(name, gl.stats)
        print "done"
        print gl.distance
        


    
def init():
    """ initialises various parameters and values 
    """
    gl.agent1 = agent.BasicAgent("om1")
    gl.agent2 = agent.BasicAgent("ag1")
    gl.data_tony = io.open_datafile("natural", "rgb")
    gl.training_data = aux.generateTrainingData(cfg.space, cfg.n_training_datasets, cfg.context_size)
    counter = 0
    while counter < cfg.n_training_datasets:
        gl.stats.append([0.0] * 2)
        counter += 1


    
def reset():
    """ resets all global variables
    """
    gl.agent1 = agent.OmniAgent("om1")
    gl.agent2 = agent.BasicAgent("ag1")
    gl.training_data = aux.generateTrainingData(cfg.space, cfg.n_training_datasets, cfg.context_size)
    gl.n_guessing_games = 0        # number of guessing games played all agents
    gl.n_succes_gg = 0             # number of successful guessing games
    gl.guessing_succes = 0.0       # agents guessing success ratio
    gl.loop_running = False



def guessing_game(agent1, agent2, context, topic_index = False):
    """ Guessing game which is played by two agents. Agent1 knows the topic, finds the closest
        matching concept and communicates the label with the strongest association to agent2.
        Agent2 uses this label and the associated concept to identify the topic from the context.
        If agent2 is able to identify the topic correctly, the guessing game succeeds.
        context = sets of data [ [ [d1, value], [d2, value], ..., [dn, value] ], ....]
    """
    if not topic_index:
        if cfg.active_learning:
            a2_context_distance = []
            for i in context:
                a2_known_concepts = agent2.cp.get_all_concept_coordinates()
                distance = 0
                for j in a2_known_concepts:
                    distance += agent2.cp.calculate_distance(i, j)
                a2_context_distance.append(distance)
            topic_index = aux.posMax(a2_context_distance)
        else:
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
    agent1.concept_history.append(agent1.get_n_concepts())
    agent2.concept_history.append(agent2.get_n_concepts())
    gl.guessing_succes = gl.n_succes_gg/gl.n_guessing_games
    
        
        
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
        and the difference is added to the overall distance, and this is done vise versa
    """
    agent1_concepts = agent1.get_all_concept_coordinates()
    agent2_concepts = agent2.get_all_concept_coordinates()
    concepts_distance = 0.0
    for i in agent1_concepts:
        distances = []
        for j in agent2_concepts:
            distance = aux.calculate_distance_general(i, j)
            distances.append(distance)
        concepts_distance += min(distances)
    for i in agent2_concepts:
        distances = []
        for j in agent1_concepts:
            distance = aux.calculate_distance_general(i, j)
            distances.append(distance)
        concepts_distance += min(distances)
    return sqrt(concepts_distance)
        
        

# main start
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    