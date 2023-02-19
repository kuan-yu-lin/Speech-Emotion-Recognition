import cnn_lstm
import dataload
import tensorflow as tf
import random
import argparse


from tensorflow.keras.utils import normalize, to_categorical
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from keras_self_attention import SeqSelfAttention
from matplotlib import pyplot

# set to GPU
gpus = tf.config.experimental.list_physical_devices("GPU")
tf.config.experimental.set_visible_devices(gpus[3], "GPU")
tf.config.experimental.set_memory_growth(gpus[3], True)

# set random.seed
random.seed(7)


def train(x_tr, y_tr, x_val, y_val, args):

    model = cnn_lstm.emo1d(x_tr, y_tr, args=args)
    model.summary()

    es = EarlyStopping(monitor='val_loss', 
                       mode='min', 
                       verbose=1, 
                       patience=8)

    mc = ModelCheckpoint('model.h5', 
                         monitor='val_categorical_accuracy', 
                         mode='max', 
                         verbose=1,
                         save_best_only=True)

    history = model.fit(x_tr, y_tr,
                        validation_data=(x_val, y_val),
                        epochs=args.num_epochs, 
                        batch_size=args.batch_size, 
                        callbacks=[es, mc])

    return history

def test(x_t, y_t):

    saved_model = load_model('model.h5', custom_objects={'SeqSelfAttention':SeqSelfAttention})
    score = saved_model.evaluate(x_t, y_t, batch_size=20)
    
    return score

def pred(x_d):

    saved_model = load_model('model.h5', custom_objects={'SeqSelfAttention':SeqSelfAttention})
    y_prob = saved_model.predict(x_d)
    y_classes = y_prob.argmax(axis=-1)
    
    return y_classes
    
def get_y_dev(y_classes, dev_data):
    valence = []
    activation = []

    for l in y_classes:
        if l == 0:
            valence.append(0)
            activation.append(0)
        elif l == 1:
            valence.append(1)
            activation.append(0) 
        elif l == 2:
            valence.append(0)
            activation.append(1)
        elif l == 3:
            valence.append(1)
            activation.append(1)

    dev_data['valence'] = valence
    dev_data['activation'] = activation

    dev_label = dev_data.drop('features', axis=1)

    return dev_label



def plotting(history):
    # plot train and validation loss
    pyplot.plot(history.history['loss'])
    pyplot.plot(history.history['val_loss'])
    pyplot.title('model train vs validation loss')
    pyplot.ylabel('loss')
    pyplot.xlabel('epoch')
    pyplot.legend(['train', 'validation'], loc='upper right')
    pyplot.show()

if __name__ == '__main__':

    train_file_path = 'ser_traindev/train.json'
    dev_file_path = 'ser_traindev/dev.json'

    X_train, y_train, X_valid, y_valid, X_test, y_test, X_dev = dataload.load_data(train_file_path, dev_file_path)

    X_train_ = normalize(X_train)
    X_valid_ = normalize(X_valid)
    X_test_ = normalize(X_test)
    X_dev_ = normalize(X_dev)

    y_train_ = to_categorical(y_train)
    y_valid_ = to_categorical(y_valid)
    y_test_ = to_categorical(y_test)

    parser = argparse.ArgumentParser()
    args = parser.parse_args(args=[])
    
    args.num_fc = 20 # num of lstm unit
    args.batch_size = 8
    args.num_epochs = 50  # best model will be saved before number of epochs reach this value
    args.learning_rate = 0.001
    args.decay = 1e-6

    history = train(X_train_, y_train_, X_valid_, y_valid_, args=args)

    score = test(X_test_, y_test_)
    
    y_classes = pred(X_dev_)

    dev_data = dataload.read_json(dev_file_path)
    dev_label = get_y_dev(y_classes, dev_data)
    dev_label.to_json(r'ser_traindev/y_dev_5.json', orient="index")

    plotting(history)
