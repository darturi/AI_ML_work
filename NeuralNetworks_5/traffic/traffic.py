import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # Create the lists that will later be returned as a tuple
    images = []
    labels = []
    # Make sure that the only sub directories that we look at have names
    # comprised of digits to avoid looking in hidden, non applicable files
    data_list = [elem for elem in os.listdir(data_dir)
                 if elem.isdigit()]

    # Iterate through directory names that are digits
    for filename in data_list:
        # Save the folder name as an int to later append to the labels list
        folder = int(filename)
        # Create a path from the directory through to the sub directory
        sub_path = os.path.join(data_dir, filename)
        # Iterate through image files in the sub directory
        for sub_file in os.listdir(sub_path):
            # Create a numpy array from the image
            img = cv2.imread(os.path.join(sub_path, sub_file))
            # Resize the image to the specified height and width
            img = cv2.resize(img, dsize=(IMG_WIDTH, IMG_HEIGHT),
                             interpolation=cv2.INTER_CUBIC)
            # Add resized array and folder label to proper lists
            images.append(img)
            labels.append(folder)
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Create a sequential model
    model = tf.keras.models.Sequential([
        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        # specify the correct input shape for our arrays
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu",
            input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # apply batch normalization to standardize input values
        tf.keras.layers.BatchNormalization(),
        # Learn 15 filers using a kernel with size 3
        tf.keras.layers.Conv2D(15, activation='selu', kernel_size=3,
                               padding="same"),
        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
        # apply batch normalization to standardize input values
        tf.keras.layers.BatchNormalization(),
        # Learn 10 filers using a kernel with size 3
        tf.keras.layers.Conv2D(10, activation='selu', kernel_size=3,
                               padding="same"),
        # Max - pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
        # apply batch normalization to standardize input values
        tf.keras.layers.BatchNormalization(),
        # Learn 5 filers using a kernel with size 3
        tf.keras.layers.Conv2D(5, activation='selu', kernel_size=3,
                               padding="same"),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add four hidden layers with 80, 70, 70, and 70 units respectively
        # After each hidden layer apply batch normalization to standardize
        # layer inputs.
        tf.keras.layers.Dense(80, activation="selu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(70, activation="selu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(70, activation="selu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(70, activation="selu"),
        tf.keras.layers.BatchNormalization(),

        # Add a dropout of 0.6 to avoid overfitting
        tf.keras.layers.Dropout(0.6),

        # Add an output layer with output units for all 43 categories
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Compile model before returning
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


if __name__ == "__main__":
    main()
