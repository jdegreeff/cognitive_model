# cpf.py
# configuration file


# parameters
n_agents = 2
adapt_threshold = 0.9
lateral_inhibition = 0
label_learning_rate = 0.01
merge_concepts = 0
merging_rate = 0.15
space = "shape"                   # "rgb", "lab" or "4df"
dataset = "uniform"             # "natural" or "uniform"
context_size = 4                # number of stimuli in the context, including the topic
sample_minimum_distance = 50    # minimum distance between stimuli in the context
calc_statistics = 1             # specifies whether or not statistics are calculated after every guessing game
calc_all = 0                     # specifies whether or not all values from every replica are stored in stats
n_training_datasets = 100      # number of training interactions
n_replicas = 1                  # number of replica's of the same training simulation
prototype_distance = 1          # distance measure is based on prototype SD, not actual coordinates
active_learning = 0             # if 1, agents use active learning: learning is aimed at new things (i.e. agent chooses topic)
query_knowledge = 0            # if > 0, agent queries knowledge with teacher, 1 is after every guessing game, 10 is after every 10 guessing games etc
contrastive_learning = 0        # if 1, clues about what a concept is not is also used, i.e. if a guessing game ends correctly, label association with context is weakened
teaching_inaccuracy = 0       # teaching inaccuracy
direct_instruction = 0          # if 1, direct instruction is used, otherwise language game style


# graphical properties
use_graphics = 0                # whether or not a graphic display should be shown
x_scale = 12
y_scale = 7