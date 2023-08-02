import numpy as np
from copy import deepcopy

def smooth_curve(loss_list, alpha):
    l1 = np.array(loss_list)

    l = deepcopy(loss_list)
    l.insert(0, l1[0])
    l.pop(len(l) - 1)
    l2 = np.array(l)

    return (1 - alpha) * l1 + (alpha) * l2

def over_fit_score(train_loss, val_loss):
    overfitting = np.array(val_loss[int(len(train_loss) / 2):]) - np.array(train_loss[int(len(val_loss) / 2):])
    overfitting[overfitting < 0] = 0
    return np.sum(overfitting) / len(train_loss)