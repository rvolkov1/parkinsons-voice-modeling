import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import csv
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import random

LLD_dataset = "../sheets/LLD_dataset.csv"

def get_columns():
    with open(LLD_dataset) as data:
        return next(csv.reader(data))

columns = get_columns()
data_cols = columns[3:]
label_col = columns[3]

dataset = tf.data.experimental.make_csv_dataset(
    LLD_dataset,
    batch_size=901,
    header=True,
    shuffle = False,
    label_name=label_col,
    select_columns=data_cols,
    num_epochs=1
)

def dataset_to_np():
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    for tuple in dataset.as_numpy_iterator():
        person_data = []
        person_labels = []

        for key, value in tuple[0].items():
            person_data.append(value)

        for value in tuple[1]:
            person_labels.append(value)

        # print(person_labels)

        person_data_np = np.array(person_data).transpose()
        person_labels_np = np.array(person_labels).transpose()

        if random.random() > 0.2:
            x_train.append(person_data_np)
            y_train.append(person_labels_np)
        else:
            x_test.append(person_data_np)
            y_test.append(person_labels_np)
    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

x_train, y_train, x_test, y_test = dataset_to_np()

lstm_model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(32, return_sequences=True, input_shape=(901,25)),
    tf.keras.layers.Dense(units=1)
])

lstm_model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)

history = lstm_model.fit(
    x_train,
    y_train,
    epochs=1,
    validation_data=(x_test, y_test),
    callbacks=[tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        mode='min')]
)

#print(history)
