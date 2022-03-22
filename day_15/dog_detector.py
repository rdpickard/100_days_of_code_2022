import glob
import os
import sys
import pathlib

import sklearn.datasets
import sklearn.preprocessing
import keras.utils
import numpy as np
import cv2
import pandas
from matplotlib import pyplot as plt

from keras.applications.resnet import ResNet50,  preprocess_input, decode_predictions

from keras.preprocessing import image
from tqdm import tqdm


def path_to_tensor(img_path):
    # loads RGB image as PIL.Image.Image type
    img = image.load_img(img_path, target_size=(224, 224))
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)


def paths_to_tensor(img_paths):
    list_of_tensors = [path_to_tensor(img_path) for img_path in tqdm(img_paths)]
    return np.vstack(list_of_tensors)


def ResNet50_predict_labels(img_path):
    img = preprocess_input(path_to_tensor(img_path))
    return np.argmax(ResNet50_model.predict(img))


def dog_detector(img_path):
    prediction = ResNet50_predict_labels(img_path)
    return (prediction <= 268) & (prediction >= 151)


def load_dataset(path):
    data = sklearn.datasets.load_files(path)
    dog_files = np.array(data['filenames'])
    dog_targets = keras.utils.np_utils.to_categorical(np.array(data['target']), 133)
    return dog_files, dog_targets


def image_intensity_distribution(path_to_image_file):
    img = cv2.imread(path_to_image_file)
    color = ('b', 'g', 'r')
    histogram_values = {}

    for i, col in enumerate(color):
        histogram_values[col] = cv2.calcHist([img], [i], None, [256], [0, 256])

    return histogram_values


def dist_breed(labels):
    encoder = sklearn.preprocessing.LabelEncoder()
    breeds_encoded = encoder.fit_transform(labels)
    n_classes = len(encoder.classes_)

    breeds = pandas.DataFrame(np.array(breeds_encoded), columns=["breed"]).reset_index(drop=True)
    print(breeds)
    breeds['freq'] = breeds.groupby('breed')['breed'].transform('count')
    avg = breeds.freq.mean()

    title = 'Distribution of Dog Breeds in training Dataset\n (%3.0f samples per class on average)' % avg
    f, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xticks([])

    ax.hlines(avg, 0, n_classes - 1, color='white')
    ax.set_title(title, fontsize=18)
    _ = ax.hist(breeds_encoded, bins=n_classes)
    plt.savefig("dist.png")

    return (breeds["freq"].describe())


training_data_dir = "../local/day_15_training_data"
dog_images_dir = os.path.join(training_data_dir, "dogImages")

train_files, train_targets = load_dataset(os.path.join(dog_images_dir, 'train'))
valid_files, valid_targets = load_dataset(os.path.join(dog_images_dir, 'valid'))
test_files, test_targets = load_dataset(os.path.join(dog_images_dir, 'test'))

# load list of dog names
dog_names = sorted([pathlib.Path(x[0]).parts[-1] for x in os.walk(os.path.join(dog_images_dir, 'train'), True)][1:])

# print statistics about the dataset
print('There are %d total dog categories.' % len(dog_names))
print('There are %s total dog images.\n' % len(np.hstack([train_files, valid_files, test_files])))
print('There are %d training dog images.' % len(train_files))
print('There are %d validation dog images.' % len(valid_files))
print('There are %d test dog images.'% len(test_files))

test_labels = []
for i in range(test_targets.shape[0]):
    test_labels.append(dog_names[np.argmax(test_targets[i])])


train_labels = []
for i in range(train_targets.shape[0]):
    train_labels.append(dog_names[np.argmax(train_targets[i])])

target_index = 4

image_histogram = image_intensity_distribution(train_files[target_index])
print(f"file : {train_files[target_index]} breed name : {dog_names[np.argmax(train_targets[target_index])]}")
for color in image_histogram.keys():
    plt.plot(image_histogram[color], color=color)
    plt.xlim([0, 256])
plt.savefig(dog_names[np.argmax(train_targets[target_index])]+"_histogram.png")

dist_breed(train_labels)


ResNet50_model = ResNet50(weights='imagenet')

for test_dog_file in test_files:
    print(test_dog_file)
    print(dog_detector(test_dog_file))




