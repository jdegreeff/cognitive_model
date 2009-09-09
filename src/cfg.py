# cfg.py
# configuration file

# parameters
adapt_threshold = 0.9
lateral_inhibition = 0
label_learning_rate = 0.01
space = ["generic0"]             # "rgb", "lab", "4df", "shape" or "generic"
dataset = "uniform"             # "natural" or "uniform"
n_domains = 1                   # number of domains
n_dimensions = 3                # number of dimensions per domain
range = [0.0, 1.0]              # range of the dimensions
context_size = 3                # number of stimuli in the context, including the topic
sample_minimum_distance = 0.5  # minimum distance between stimuli in the context
calc_statistics = 1             # specifies whether or not statistics are calculated after every guessing game
calc_all = 0                     # specifies whether or not all values from every replica are stored in stats
n_training_datasets = 2000      # number of training interactions
n_replicas = 1                  # number of replica's of the same training simulation
prototype_distance = 0          # distance measure is based on prototype SD, not actual coordinates
active_learning = 0             # if 1, agents use active learning: learning is aimed at new things (i.e. agent chooses topic)
query_knowledge = 0            # if > 0, agent queries knowledge with teacher, 1 is after every guessing game, 10 is after every 10 guessing games etc
contrastive_learning = 0        # if 1, clues about what a concept is not is also used, i.e. if a guessing game ends correctly, label association with context is weakened
teaching_inaccuracy = 0       # teaching inaccuracy
direct_instruction = 0          # if 1, direct instruction is used, otherwise language game style
prune_concepts_xml_output = 0.1   # if > 0, value determines the threshold for successful (used) concepts that are saved to xml
gnuplot = 1                     # specify whether or not to use a gnuplot output

# graphical properties
use_graphics = 0                # whether or not a graphic display should be shown
x_scale = 12
y_scale = 7