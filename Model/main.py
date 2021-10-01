import matplotlib.pyplot as plt
import numpy as np
import os, PIL
import tensorflow as tf
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


lable_path = "C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Lables/Lables.xlsx"
labels = pd.read_excel(lable_path)

images = []

for i in range(len(labels)):
    image_path = f"C:/Users/ad/Desktop/Github/AI-Stock-Prediction/ImageData/Features/{i}.png"
    image = Image.open(image_path)
    image = image.resize((128, 128))
    images.append(np.array(image)/255)
print(images[0])
plt.imshow(images[0])
plt.show()
images = np.array(images)

X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.1, random_state=42)

print(X_train.shape)

model = Sequential([
    layers.Conv2D(16, 3, padding="same",activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding="same", activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding="same", activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(128, 3, padding="same", activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(256, activation="relu"),
    layers.Dense(128, activation="relu"),
    layers.Dense(64, activation="relu"),
    layers.Dense(32, activation="relu"),
    layers.Dense(3, activation="softmax")
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs=100
history = model.fit(
    x=X_train, y=y_train,
    epochs=epochs
)