import tensorflow

from numpy import loadtxt
from keras.layers import Dense
from keras.models import Sequential

X = loadtxt('input.txt', delimiter = ',')
Y = loadtxt('output.txt', delimiter =',')

# define the keras model
model = Sequential()
model.add(Dense(13, input_shape=(6,), activation='relu'))
model.add(Dense(7, activation='relu'))
model.add(Dense(4, activation='linear'))

# compile the keras model
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.compile(optimizer='adam', loss='mean_squared_error')

# fit the keras model on the dataset
model.fit(X, Y, epochs=2000, batch_size=550)

# # evaluate the keras model
# _, accuracy = model.evaluate(X, Y)
# print('Accuracy: %.2f' % (accuracy*100))

model.save('lastmodel')