# globals.py
#import globals as gl

# global variables
agent_set = []              # a collection of agents
training_data = []          # training data
rgb_data_tony =[]           # training data from Tony Belpaeme
lab_data_tony =[]           # training data from Tony Belpaeme
n_guessing_games = 0        # number of guessing games played
n_success_gg = 0             # number of successful guessing games
guessing_success = 0.0       # agents guessing success ratio
loop_running = False        # program is running
current_loop = 0            # current loop of the program
finished = False            # program is finished
stats = []                  # statistics
distance = []              # overall distance between concepts of 2 agents
correctness = []           # percentage of correctness when agents are tested for knowledge
training_data_dist=[]      # distance in training data, test purpose