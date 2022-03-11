]import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
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

# dataset = tf.data.experimental.make_csv_dataset(
#     LLD_dataset,
#     batch_size=900,
#     header=True,
#     shuffle = False,
#     label_name=label_col,
#     select_columns=data_cols,
#     num_epochs=1
# )

# for element in dataset.as_numpy_iterator():
#   print(element)
#print(list(dataset.as_numpy_iterator()))

tf.data.TFRecordDataset(
    LLD_dataset,

)

lstm_model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(32, return_sequences=True, input_shape=(25,900)),
    tf.keras.layers.Dense(units=1)
])

lstm_model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)

test_dataset = dataset.take(5)
train_dataset = dataset.skip(5)

history = lstm_model.fit(
    train_dataset,
    epochs=1,
    validation_data=test_dataset,
    callbacks=[tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        mode='min')]
)

IPython.display.clear_output()
