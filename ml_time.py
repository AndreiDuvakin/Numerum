import random

import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(100, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

speeds = list(map(lambda x: random.randint(1, 100), range(4000)))
distances = list(map(lambda x: random.randint(1, 100), range(4000)))
times = list(map(lambda x: speeds[x] / distances[x], range(4000)))

# times = list(map(lambda x: (distances[x] / (int(speeds[x]) * 1.852)) * 60, range(4000)))
# print(speeds[0], distances[0], times[0])

model.fit(list(zip(speeds, distances)), times, epochs=800)

predicted_time = model.predict([[200, 100]])
print("Predicted time:", round(float(predicted_time[0])))
