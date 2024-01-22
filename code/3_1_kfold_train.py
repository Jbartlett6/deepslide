'''
Script to perform k-fold cross validation.
    1)Creates n_splits validation sets using sklearn 
    2)loops of these splits and trains a model for each of the different validation sets.
each time train_resnet is called a different val_set is passed as the val_subjects argument 
which means different train and validation datasets are created accordingly. 
    3) ***To be implemented*** For each loop a stopping criteria is implemented as well as 
the strongest validation loss and accuracy is recorded.  
'''
import config
from utils_model import train_resnet

import os
import time

from sklearn.model_selection import KFold

# Lists of the true and false subjects in 
all_true_subjects = ['318', '352', '151', '194', '121', '21', '48', '261', '125', '159', '162']
all_false_subjects = ['118', '146', '119', '213', '62', '27', '294', '128', '6', '124', '206', '193', '136', '20', '5', '163', '111', '202', '153']

# Creating n_splits val_sets to be used for cross validation
kfold_log = os.path.join('logs', 'kfold_logs', str(time.time()))
n_splits = 5
kf_true = KFold(n_splits)
kf_false = KFold(n_splits)

val_subs = []
for ((true_train_index, true_val_index), (false_train_index, false_val_index)) in zip(kf_true.split(all_true_subjects), kf_false.split(all_false_subjects)):
    nth_fold = [all_true_subjects[i] for i in true_val_index]+[all_false_subjects[i] for i in false_val_index]
    print(nth_fold)
    val_subs.append(nth_fold)
 
for i, val_set in enumerate(val_subs):
    print(f'Starting training for the {i}th fold, with validation subjects: {val_set}')
    # Training the ResNet.
    print("\n\n+++++ Running 3_train.py +++++")
    train_output = train_resnet(batch_size=config.args.batch_size,
                checkpoints_folder=config.args.checkpoints_folder,
                classes=config.classes,
                color_jitter_brightness=config.args.color_jitter_brightness,
                color_jitter_contrast=config.args.color_jitter_contrast,
                color_jitter_hue=config.args.color_jitter_hue,
                color_jitter_saturation=config.args.color_jitter_saturation,
                device=config.device,
                learning_rate=config.args.learning_rate,
                learning_rate_decay=config.args.learning_rate_decay,
                log_csv=config.log_csv,
                num_classes=config.num_classes,
                num_layers=config.args.num_layers,
                num_workers=config.args.num_workers,
                path_mean=config.path_mean,
                path_std=config.path_std,
                pretrain=config.args.pretrain,
                resume_checkpoint=config.args.resume_checkpoint,
                resume_checkpoint_path=config.resume_checkpoint_path,
                save_interval=config.args.save_interval,
                num_epochs=config.args.num_epochs,
                train_folder=config.args.train_folder,
                weight_decay=config.args.weight_decay,
                architecture=config.args.architecture,
                val_subjects=val_set,
                early_stopping=True,
                early_stopping_threshold=10)
    
    with open(kfold_log, 'a') as log:
        log.write(f'{train_output}\n')

    
    print("+++++ Finished running 3_train.py +++++\n\n")