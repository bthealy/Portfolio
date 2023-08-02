import numpy as np
import cv2
import os
import tqdm
from random import shuffle


dir = r'/kaggle/input/lung-data/D2'

img_size   = 50
model_name = 'test.model'

encode_dic = {'normal':                 [1,0,0,0],
              'adenocarcinoma':         [0,1,0,0],
              'large cell carcinoma':   [0,0,1,0],
              'squamous cell carcinoma':[0,0,0,1]}

class_list = ['normal',
              'adenocarcinoma',
              'large cell carcinoma',
              'squamous cell carcinoma']


def preprocess_img(img, training=False):
    img = cv2.resize(img, (img_size, img_size))

    if training:
        return img[:, :, np.newaxis]
    else:
        return img[np.newaxis, :, :, np.newaxis]


def load_data(dir, f_name):
    data = []

    for cl in class_list:
        cl_dir = dir + f'/{cl}'

        for img_path in tqdm(os.listdir(cl_dir)):
            path = os.path.join(cl_dir, img_path)
            label = np.array(encode_dic[cl])

            img = cv2.imread(path, 0)
            img = preprocess_img(img, training=True)
            data.append([img, np.array(label)])

    shuffle(data)
    np.save(f'{f_name}.npy', data)

    return data


def remove_copies(dir):
    # for each class in train, test, or val directories
    for cl in class_list:
        cl_dir = dir + f'/{cl}'

        #for each image in each class subdirectory
        for img_path in tqdm(os.listdir(cl_dir)):
            full_path  = os.path.join(cl_dir, img_path)

            # delete copies
            lower_path = full_path.lower()
            if lower_path.find('copy') != -1:
                print(full_path)
                os.remove(full_path)