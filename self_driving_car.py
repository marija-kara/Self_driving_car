# -*- coding: utf-8 -*-
"""Self_driving_car.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JiZGpRI77K6_6IJntxPtS_idmY426oBd
"""

from google.colab import drive
drive.mount('/content/drive')

!unzip drive/MyDrive/Classroom/Brainster/IMG.zip -d data

"""## **Import libraries**"""

import numpy as np
import pandas as pd
import os
import cv2 as cv 
from google.colab.patches import cv2_imshow
from skimage import io
from PIL import Image 
import matplotlib.pylab as plt
import random
from sklearn.utils import shuffle
import tensorflow as tf

from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import core, convolutional, pooling
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras import optimizers, backend

"""## **DATASET PREPARATION**"""

dataset = pd.read_csv('data/driving_log.csv', names= ['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed'])

dataset['center'][0]

dataset.columns

copy_dataset = dataset.copy()

copy_dataset['center'] = copy_dataset['center'].apply(lambda x : x.split('\\')[3])
copy_dataset['left'] = copy_dataset['left'].apply(lambda x : x.split('\\')[3])
copy_dataset['right'] = copy_dataset['right'].apply(lambda x : x.split('\\')[3])

copy_dataset.head()

"""> **Definition of image read function**




"""

def read_image(path_):
  final_path = os.path.join("data/IMG", path_)
  picture = cv.imread(final_path)
  picture_rgb = cv.cvtColor(picture, cv.COLOR_BGR2RGB)
  return picture_rgb

inputs = []
targets = []
for c1, c2, c3, angle in zip(copy_dataset['center'], copy_dataset['left'], copy_dataset['right'], copy_dataset['steering']):
   inputs.append(c1)
   targets.append(angle)
   inputs.append(c2)
   targets.append(angle)
   inputs.append(c3)
   targets.append(angle)

print(len(inputs))
print(len(targets))

plt.imshow(read_image(inputs[225]))
plt.title(targets[225])
plt.show()

"""# **Definition of image augmentation functions**

Function for croping the upper segment of the picture
"""

def crop(img, crop_size=60):

    new_slika = img.copy()
    cropped = new_slika[crop_size:, :, :]

    return cropped

f = plt.figure()
f.set_figheight(15)
f.set_figwidth(20)
f.add_subplot(1,2, 1)
plt.imshow(read_image(inputs[225]))
plt.title('{0:.10f}'.format(targets[225]))
f.add_subplot(1,2, 2)
plt.imshow(crop(read_image(inputs[225])))
plt.title('{0:.10f}'.format(targets[225]))
plt.show(block=True)

"""> **Function that returns flipped image**

"""

def flip_image(img, steering_angle):
    flip_img = cv.flip(img, 1)
    steering_angle = steering_angle * (-1)
    return flip_img, steering_angle

original_image = read_image(inputs[225])
original_angle = targets[225]

fliped_image, fliped_angle = flip_image(original_image, original_angle)

f = plt.figure()
f.set_figheight(15)
f.set_figwidth(20)
f.add_subplot(1,2, 1)
plt.imshow(read_image(inputs[225]))
plt.title(targets[225])
f.add_subplot(1,2, 2)
plt.imshow(fliped_image)
plt.title(fliped_angle)

plt.show(block=True)

"""Function for changing image brithness"""

def change_image_brightness(img, s_low=0.3, s_high=0.7):
    img = img.astype(np.float32)
    s = np.random.uniform(s_low, s_high)
    img[:,:,:] *= s
    np.clip(img, 0, 255)
    return  img.astype(np.uint8)

f = plt.figure()
f.set_figheight(15)
f.set_figwidth(20)
f.add_subplot(1,2, 1)
plt.imshow(read_image(inputs[225]))
plt.title(targets[225])
f.add_subplot(1,2, 2)
plt.imshow(change_image_brightness(read_image(inputs[225])))
plt.title(targets[225])
plt.show(block=True)

"""Function for adding random shadow"""

def add_random_shadow(img, w_low=0.5, w_high=0.9):
    cols, rows = (img.shape[0], img.shape[1])
    
    top_y = np.random.random_sample() * rows
    bottom_y = np.random.random_sample() * rows
    bottom_y_right = bottom_y + np.random.random_sample() * (rows - bottom_y)
    top_y_right = top_y + np.random.random_sample() * (rows - top_y)
    if np.random.random_sample() <= 0.5:
        bottom_y_right = bottom_y - np.random.random_sample() * (bottom_y)
        top_y_right = top_y - np.random.random_sample() * (top_y)
    
    poly = np.asarray([[ [top_y,0], [bottom_y, cols], [bottom_y_right, cols], [top_y_right,0]]], dtype=np.int32)
        
    mask_weight = np.random.uniform(w_low, w_high)
    origin_weight = 1 - mask_weight
    
    mask = np.copy(img).astype(np.int32)
    cv.fillPoly(mask, poly, (0, 0, 0))
    
    return cv.addWeighted(img.astype(np.int32), origin_weight, mask, mask_weight, 0).astype(np.uint8)

f = plt.figure()
f.set_figheight(15)
f.set_figwidth(20)
f.add_subplot(1,2, 1)
plt.imshow(read_image(inputs[225]))
plt.title(targets[225])
f.add_subplot(1,2, 2)
plt.imshow(add_random_shadow(read_image(inputs[225])))
plt.title(targets[225])
plt.show(block=True)

def random_noise(image,prob=0.05):

    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

f = plt.figure()
f.set_figheight(15)
f.set_figwidth(20)
f.add_subplot(1,2, 1)
plt.imshow(read_image(inputs[225]))
plt.title(targets[225])
f.add_subplot(1,2, 2)
plt.imshow(random_noise(read_image(inputs[225])))
plt.title(targets[225])
plt.show(block=True)

"""# **Generator**

Image augmentation function
"""

def augment_image(img, angle, p=1.0):
    aug_img = img
    
    if np.random.random_sample() <= p: 
        aug_img, angle = flip_image(aug_img, angle)
     
    if np.random.random_sample() <= p:
        aug_img = change_image_brightness(aug_img)
    
    if np.random.random_sample() <= p: 
        aug_img = add_random_shadow(aug_img)

    if np.random.random_sample() <= p:
        aug_img = random_noise(aug_img)
            
    return aug_img, angle

"""Image generator function"""

def generator(inputs, targets, batch_size = 32, is_training=True):
    images = inputs
    while True:
      for i in range(0, len(images), batch_size):
          X_batch = []
          target_batch  = []
          for image, target in zip(images[i:i+batch_size], targets[i:i+batch_size]):
              slika = read_image(image)
              slika = crop(slika)
              if is_training:
                slika, ang = augment_image(slika, target, p=0.5)

              X_batch.append(slika)
              target_batch.append(ang)
      
          yield np.array(X_batch), np.array(target_batch)

train_generator = generator(inputs, targets, 64)
valid_generator = generator(inputs, targets, 64, is_training=False)

batch_data = next(train_generator)

list(map('{0:.20f}'.format,batch_data[1]))

plt.hist(batch_data[1], bins = 10)
plt.show()

X_train, Y_Train = next(train_generator)

Y_Train

"""# **Dataset split**"""

X_train, X_test, y_train, y_test = train_test_split(inputs, targets, test_size = 0.20, random_state = 1)

"""# **Building Neural Networks**"""

model1 = Sequential()
model1.add(Convolution2D(16, 3, 3, input_shape=(160, 320, 3), activation='relu'))
model1.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
model1.add(Convolution2D(32, 3, 3, activation='relu'))
model1.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
model1.add(Convolution2D(64, 3, 3, activation='relu'))
model1.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
model1.add(core.Flatten())
model1.add(core.Dense(500, activation='relu'))
model1.add(core.Dropout(.5))
model1.add(core.Dense(100, activation='relu'))
model1.add(core.Dropout(.25))
model1.add(core.Dense(20, activation='relu'))
model1.add(core.Dense(1))
model1.compile(optimizer=optimizers.Adam(learning_rate=1e-04), loss='mse')

"""Model summary"""

model1.summary()

callback1 = ModelCheckpoint('best_model.pt', monitor='val_loss', save_best_only=True, mode='min', verbose=1)
callback2 = EarlyStopping(patience=15)
callback_list = [callback1, callback2]

"""**Model training**"""

history = model1.fit(
        train_generator,
        steps_per_epoch = len(X_train)//32,
        validation_data  = valid_generator,
        validation_steps = len(X_test)//32,
        callbacks = callback_list,
        epochs=3)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['training', 'validation'])
plt.title('Loss')
plt.xlabel('Epoch')

model1.save('model1.h5')

model2 = Sequential()
model2.add(Convolution2D(24, 2, 2, input_shape=(160, 320, 3), activation='relu'))
model2.add(MaxPooling2D(pool_size=(2, 2), padding='same'))

model2.add(Convolution2D(36, 2, 2, activation='relu'))
model2.add(MaxPooling2D(pool_size=(2, 2), padding='same'))

model2.add(Convolution2D(48, 2, 2, activation='relu'))
model2.add(MaxPooling2D(pool_size=(2, 2), padding='same'))

model2.add(Convolution2D(64, 2, 2, activation='relu'))
model2.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
model2.add(Dropout(0.5))

model2.add(core.Flatten())
model2.add(core.Dense(100, activation='relu'))
model2.add(core.Dropout(0.5))

model2.add(core.Dense(50, activation='relu'))
model2.add(core.Dropout(0.5))

model2.add(core.Dense(10, activation='relu'))
model2.add(core.Dense(1))

model2.compile(optimizer=optimizers.Adam(learning_rate=1e-3), loss='mse')

model2.summary()

callback12 = ModelCheckpoint('best_model_2.pt', monitor='val_loss', save_best_only=True, mode='min', verbose=1)
callback22 = EarlyStopping(patience=15)
callback_list_2 = [callback12, callback22]

history_2 = model2.fit(
        train_generator,
        steps_per_epoch = len(X_train)//32,
        validation_data  = valid_generator,
        validation_steps = len(X_test)//32,
        callbacks = callback_list_2,
        epochs=3)

plt.plot(history_2.history['loss'])
plt.plot(history_2.history['val_loss'])
plt.legend(['training', 'validation'])
plt.title('Loss')
plt.xlabel('Epoch')

model2.save('model2.h5')

model3 = Sequential()
model3.add(Convolution2D (64, 3, 3, input_shape=(160, 320, 3), padding ='same', activation='elu'))
model3.add(MaxPooling2D(pool_size =(2,2), strides =2, padding ='same'))

model3.add(Convolution2D (128, 3, 3, padding ='same', activation='elu'))
model3.add(MaxPooling2D(pool_size =(2,2), strides =2, padding ='same'))

model3.add(Convolution2D (256, 3, 3, padding ='same', activation='elu'))
model3.add(MaxPooling2D(pool_size =(2,2), strides =2, padding ='same'))

model3.add(Convolution2D (512, 3, 3, padding ='same', activation='elu'))
model3.add(MaxPooling2D(pool_size =(2,2), strides =2, padding ='same'))
model3.add(Dropout(0.5))

model3.add(Flatten())
model3.add(Dense(1024, activation ='elu'))
model3.add(Dropout(0.5))

model3.add(Dense(1))

model3.compile(optimizer=optimizers.Adam(learning_rate=1e-3), loss='mse')

model3.summary()

callback13 = ModelCheckpoint('best_model_3.pt', monitor='val_loss', save_best_only=True, mode='min', verbose=1)
callback23 = EarlyStopping(patience=15)
callback_list_3 = [callback13, callback23]

history_3 = model3.fit(
        train_generator,
        steps_per_epoch = len(X_train)//32,
        validation_data  = valid_generator,
        validation_steps = len(X_test)//32,
        callbacks = callback_list_3,
        epochs=10)

plt.plot(history_3.history['loss'])
plt.plot(history_3.history['val_loss'])
plt.legend(['training', 'validation'])
plt.title('Loss')
plt.xlabel('Epoch')

model3.save('model3.h5')

model4 = Sequential()
model4.add(Convolution2D(24, 5, 5, input_shape = (160,320,3), activation='relu'))
model4.add(BatchNormalization())

model4.add(Convolution2D(36, 5, 5, activation='relu'))
model4.add(BatchNormalization())

model4.add(Convolution2D(64, 3, 3, activation='relu'))
model4.add(MaxPooling2D(pool_size =(2,2), strides =2, padding ='same'))
model4.add(BatchNormalization())
    
model4.add(Flatten())
    
model4.add(Dense(1164, activation='relu'))
model4.add(BatchNormalization())
    
model4.add(Dense(200, activation='relu'))
model4.add(BatchNormalization())
    
model4.add(Dense(50, activation='relu'))
model4.add(BatchNormalization())
    
model4.add(Dense(10, activation='relu'))
model4.add(BatchNormalization())
    
model4.add(Dense(1))
    
model4.compile(loss = "MSE", optimizer = Adam(learning_rate = 0.001))

model4.summary()

callback14 = ModelCheckpoint('best_model_4.pt', monitor='val_loss', save_best_only=True, mode='min', verbose=1)
callback24 = EarlyStopping(patience=15)
callback_list_4 = [callback14, callback24]

history_4 = model4.fit(
        train_generator,
        steps_per_epoch = len(X_train)//32,
        validation_data  = valid_generator,
        validation_steps = len(X_test)//32,
        callbacks = callback_list_3,
        epochs=10)

plt.plot(history_4.history['loss'])
plt.plot(history_4.history['val_loss'])
plt.legend(['training', 'validation'])
plt.title('Loss')
plt.xlabel('Epoch')

model4.save('model4.h5')