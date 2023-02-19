import json
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

def read_json(path):

    with open(path, "r") as file:
        # Load the JSON data from the file
        raw_data = json.load(file)
        # fit data to dataframe
        df_raw_data = pd.DataFrame.from_dict(raw_data, orient='index')

    return df_raw_data

def convert_label(raw_data):

    label_list = []

    for _, a in raw_data.iterrows():
        if a['valence'] == 0 and a['activation'] == 0: label_list.append(0)
        elif a['valence'] == 1 and a['activation'] == 0: label_list.append(1)
        elif a['valence'] == 0 and a['activation'] == 1: label_list.append(2)
        elif a['valence'] == 1 and a['activation'] == 1: label_list.append(3)

    raw_data['labels'] = label_list

    data = raw_data.drop('valence', axis=1)
    data = data.drop('activation', axis=1)

    return data

def seq_length(data):
    return max([len(sequence) for sequence in data])

def padding(data, length):

    padded_X = []

    for timeStep in data:
        if len(timeStep) < length:
            timeStep += [0] * (length - len(timeStep))
            padded_X.append(timeStep)
        else:
            timeStep = timeStep[:length]
            padded_X.append(timeStep[:length])

    return padded_X

def convert_seq_arr(seq, length):
    seq_arr = np.array(seq[0]).reshape(1, 26)
    for timeFrame in seq[1:]:
        if type(timeFrame) == int:
            tf_zero = np.zeros(shape=(1, 26))
            seq_arr = np.concatenate((seq_arr, tf_zero), axis=0)
        else:
            tf_arr = np.array(timeFrame).reshape(1, 26)
            seq_arr = np.concatenate((seq_arr, tf_arr), axis=0)

    return seq_arr.reshape(-1, length, 26)

def convert_data_arr(data, length):
    n = 1
    data_arr = convert_seq_arr(data[0], length)
    for sequence in data[1:]:
        seq_arr = convert_seq_arr(sequence, length)
        data_arr = np.concatenate((data_arr, seq_arr), axis=0)
        n += 1
        if n % 1000 == 0:
            print(f'{n} sequences have been converted.')
    print(f'{n} sequences have been converted.')
    return data_arr

def load_data(path_train, path_dev):

    train_raw_data = read_json(path_train)
    dev_data = read_json(path_dev)

    train = convert_label(train_raw_data)
    X = np.array(train['features'])
    y = np.array(train['labels'])
    X_dev = np.array(dev_data['features'])

    # define the sequence length
    # length = seq_length(X)
    length = 400

    X_pad = padding(X, length)
    X_dev_pad = padding(X_dev, length)

    X_arr = convert_data_arr(X_pad, length)
    X_dev = convert_data_arr(X_dev_pad, length)

    X_train_val, X_test, y_train_val, y_test = train_test_split(X_arr, y, test_size=0.2, random_state=4)
    X_train, X_valid, y_train, y_valid = train_test_split(X_train_val, y_train_val, test_size=0.2, random_state=4)

    return X_train, y_train, X_valid, y_valid, X_test, y_test, X_dev

