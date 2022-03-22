import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import csv
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

LLD_dataset = "../sheets/LLD_dataset20.csv"

def get_columns():
    with open(LLD_dataset) as data:
        return next(csv.reader(data))

columns = get_columns()
data_cols = columns[3:]
label_col = columns[3]

dataset = tf.data.experimental.make_csv_dataset(
    LLD_dataset,
    batch_size=900,
    header=True,
    shuffle = False,
    label_name=label_col,
    select_columns=data_cols,
    num_epochs=1
)

def dataset_to_np():
    person
    for tuple in dataset.as_numpy_iterator():
        person_data = []
        person_labels = []

        for key, value in tuple[0].items():
            person_data.append(value)

        person_data_np = np.array(person_data)
        print(person_data_np.transpose().shape)

lstm_model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(32, return_sequences=True, input_shape=(900,25)),
    tf.keras.layers.Dense(units=1)
])

lstm_model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)

history = lstm_model.fit(
    train_dataset,
    epochs=1,
    validation_data=test_dataset,
    callbacks=[tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        mode='min')]
)

IPython.display.clear_output()
