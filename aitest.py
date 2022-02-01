import tensorflow as tf
import numpy as np
import pandas as pd
import sklearn
import random

# learn how to square numbers
miles = tf.keras.models.Sequential()
miles.add(tf.keras.layers.Dense(1, activation="relu"))
miles.compile(optimizer='adam', loss='mean_absolute_percentage_error')


def datagen(num):
    x = []
    y = []
    for _ in range(num):
        val = random.randint(1,100)
        x.append(val)
        y.append(val**3)
    return x, y


x, y = datagen(1000)
print(x)
print(y)
miles.fit(x, y, batch_size=32, epochs=100)
print(miles.predict([5]))
