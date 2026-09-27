import os

# root project
root_project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# directory data
dir_raw_data = os.path.join(root_project,"data","raw")
dir_processed_data = os.path.join(root_project,"data","processed")
dir_train = os.path.join(dir_processed_data,"train")
dir_val = os.path.join(dir_processed_data,"val")

# config make data
number_of_sequences = 100
sequence_length = 30

# config model
categories = os.listdir(dir_raw_data)
num_class = len(categories)

#config train
batch_size = 32
num_epochs = 100
learning_rate = 0.001

# directory model
dir_save_model = os.path.join(root_project,"trained_models")
path_best_model = os.path.join(dir_save_model,"best_hands.pt")

# directory tensorboard
dir_tensorboard = os.path.join(root_project,"reports","tensorboard")

# config parameter mediapip
max_num_hands=1
min_detection_confidence=0.5
min_tracking_confidence=0.5

# test
confidence_threshold = 0.

