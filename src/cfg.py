# cpf.py
# configuration file
import globals as gl

# parameters
n_agents = 2
adapt_threshold = 0.9
lateral_inhibition = 0
label_learning_rate = 0.01
merge_concepts = 0
merging_rate = 0.15
space = "rgb" # "rgb" or "4df"
n_training_datasets = 10000
context_size = 4
sample_minimum_distance = 10
prototype_distance = 1  # distance measure is based on prototype SD, not actual coordinates
gl.x_scale = 12
gl.y_scale = 7