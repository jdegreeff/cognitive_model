# globals.py
import layout
import globals as gl

# global variables
agent_set = []              # a collection of agents
agent1 = []                 # an agent
agent2 = []                 # another agent
training_data = []          # training data
data_tony =[]               # training data from Tony Belpaeme
n_guessing_games = 0        # number of guessing games played all agents
n_succes_gg = 0             # number of successful guessing games
guessing_succes = 0.0       # agents guessing success ratio
loop_running = False
stats = []                  # statistics
overall_stats = []          # average stats


def reset():
    """ resets all globals
    """
    gl.agent_set = []              # a collection of agents
    gl.agent1 = []                 # an agent
    gl.agent2 = []                 # another agent
    gl.training_data = []          # training data
    gl.data_tony =[]               # training data from Tony Belpaeme
    gl.n_guessing_games = 0        # number of guessing games played all agents
    gl.n_succes_gg = 0             # number of successful guessing games
    gl.guessing_succes = 0.0       # agents guessing success ratio
    gl.loop_running = False
