# cpf.py
# configuration file


# parameters
n_agents = 2
adapt_threshold = 0.95
lateral_inhibition = 0
label_learning_rate = 0.01
merge_concepts = 0
merging_rate = 0.15
space = "rgb"                   # "rgb" or "4df"
context_size = 4
sample_minimum_distance = 50
n_training_datasets = 10000
n_loops = 500                    # number of loops the agents go through the learning loop
prototype_distance = 1          # distance measure is based on prototype SD, not actual coordinates
active_learning = 1             # if 1, agents use active learning: learning is aimed at new things (i.e. agent chooses topic)

# graphical properties
use_graphics = 0                # whether or not a graphic display should be shown
x_scale = 12
y_scale = 7