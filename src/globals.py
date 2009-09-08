# globals.py

# global variables
training_data = []          # training data
rgb_data_tony =[]           # training data from Tony Belpaeme
lab_data_tony =[]           # training data from Tony Belpaeme
n_guessing_games = 0        # number of guessing games played
n_success_gg = 0             # number of successful guessing games
guessing_success = 0.0       # agents guessing success ratio
guessing_success_history = []# agents guessing success ratio history
loop_running = False
current_loop = 0            # current loop of the program
stats = []                  # statistics
distance = []              # overall distance between concepts of 2 agents
training_data_dist=[]      # distance in training data, test purpose