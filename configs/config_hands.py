import os
from configs import path_common

dir_data_hand_raw = os.path.join(path_common.dir_raw_data,"hand")
dir_data_hand_processed = os.path.join(path_common.dir_processed_data,"hand")

dir_train_hand = os.path.join(dir_data_hand_raw ,"train")
dir_val_hand = os.path.join(dir_data_hand_processed,"val")

# config make data
number_of_sequences = 100
sequence_length = 30

# config model
categories = os.listdir(dir_data_hand_raw)
num_class = len(categories)

#config train
batch_size = 32
num_epochs = 100
learning_rate = 0.001

# directory model
dir_save_model_hand = os.path.join(path_common.root_project,"trained_models")
path_best_model_hand = os.path.join(dir_save_model_hand,"best_hands.pt")

# directory tensorboard
dir_tensorboard_hand = os.path.join(path_common.root_project,"reports","tensorboard")

# config parameter mediapip
max_num_hands=1
min_detection_confidence=0.6
min_tracking_confidence=0.6

# test
confidence_threshold = 0.7

