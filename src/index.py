from imageNetParser import get_dico_size, get_features
import numpy as np
from collections import namedtuple
from sklearn.decomposition import PCA
from sklearn.utils import shuffle
import pickle

import matplotlib.pyplot as plt

Dataset = namedtuple("Dataset", ["x_train", "x_test", "y_train", "y_test"])
TrainingSample = namedtuple("TrainingSample", ["x", "y"])

def sample(dataset, size=1, train=True):
    if train:
        ind = np.random.randint(0, len(dataset.x_train), size)  
        return dataset.x_train[ind], dataset.y_train[ind]
    else:
        ind = np.random.randint(0, len(dataset.x_test), size)  
        return dataset.x_test[ind], dataset.y_test[ind]

def compute_bow(feature_list):
    v = np.zeros(get_dico_size())
    for w in feature_list.get_words():
        v[w] += 1
    norm2 = np.linalg.norm(v, ord=2)
    v /= norm2
    return v

def file_to_dataset(fname, label):
    features = get_features(fname)
    x_train = [compute_bow(feat) for feat in features[:800]]
    x_test = [compute_bow(feat) for feat in features[800:]]
    y_train, y_test = np.array([label for _ in range(800)]), np.array([label for _ in features[800:]])
    return x_train, x_test, y_train, y_test

def get_dataset(PATH, class_list):
    X_train, X_test, Y_train, Y_test = [], [], [], []
    print("collecting bow")
    for label, cls in enumerate(class_list):
        fname = PATH + "/{}.txt".format(cls)
        x_train, x_test, y_train, y_test = file_to_dataset(fname, label)
        X_train.append(x_train)
        X_test.append(x_test)
        Y_train.append(y_train)
        Y_test.append(y_test)
        
    print("to numpy")
    X_train = np.concatenate(X_train, axis=0)
    X_test = np.concatenate(X_test, axis=0)
    Y_train = np.concatenate(Y_train, axis=0)
    Y_test = np.concatenate(Y_test, axis=0)

    print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

    print("shuffle")
    X_train, Y_train = shuffle(X_train, Y_train)
    X_test, Y_test = shuffle(X_test, Y_test)

    print("pca")
    X_train = PCA(n_components = 250).fit_transform(X_train)
    X_test = PCA(n_components = 250).fit_transform(X_test)

    print("done !")
    return Dataset(X_train, X_test, Y_train, Y_test)
 
def plot_histo(bow):
    
    bar_width = 5. # set this to whatever you want
    positions = np.arange(1000)
    plt.bar(positions, bow, bar_width)
    #plt.xticks(positions + bar_width / 2, ('0', '1', '2', '3'))
    plt.show()
def save(obj, fname="../res/dataset.bin"):
    with open(fname, "wb") as f:
        pickle.dump(obj, f)

def load(fname="../res/dataset.bin"):
    with open(fname, "rb") as f:
        data = pickle.load(f)
    return data
    
        

    



    
    

