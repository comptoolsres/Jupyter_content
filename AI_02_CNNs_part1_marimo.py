import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introduction to Convolutional Neural Networks, part 1

    We will start looking at image classification, the task of training a model to classify an image into one of a pre-set number of categories. The image below shows common computer vision tasks and is from [Shivani Kolungade](https://medium.com/@kolungade.s/object-detection-image-classification-and-semantic-segmentation-using-aws-sagemaker-e1f768c8f57d)

    ![Image classification, object detection and segmentation by Shivani Kolungade](images/classification_detection_segmentation.png)

    ## Image classification of an American Sign Language Dataset

    For this exercise, we will explore image classification, starting with a "simple" neural network and then adding convolutional layers, data augmentation and more to build better models.

    This notebook is inspired by the Nvidia [Fundamentals of Deep Learning](https://www.nvidia.com/en-us/training/instructor-led-workshops/fundamentals-of-deep-learning/) (instructor led)/ [Getting Started with Deep Learning](https://courses.nvidia.com/courses/course-v1:DLI+S-FX-01+V1/about) (online, asynchronous) exercises.

    ## American Sign Language Dataset

    The American Sign Language [manual alphabet](https://en.wikipedia.org/wiki/American_manual_alphabet) has signs for each letter. We will skip J and Z because those signs require motion.

    The dataset we'll use is from [Kaggle](https://www.kaggle.com/arjaiswal/sign-mnist-using-cnn/data). There should be 24 classes...but for some reason, there are 25...We'll stick with the Kaggle data, but keep this in mind...

    We'll start with this dataset because it helps with the transition from the tabular data we've been working with to image data. Images are a grid of pixels, where each pixel has a brightness. For greyscale images, there is one grid, for color images, there are typically three grids, for the red, green and blue colors (RGB), often called color channels.

    Let's start by loading the data and examining some images.

    ## Load the data and examine some images
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd

    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    # '%matplotlib inline' command supported automatically in marimo

    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.preprocessing import image_dataset_from_directory
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.preprocessing import image as image_utils

    from tensorflow.keras.models import Sequential
    from tensorflow.keras import layers
    from tensorflow.keras.layers import Dense

    from helpers_plot_history import plot_history # A function to plot training history. 
                                # We 1st used the code in 15_neural_networks.ipynb.
    return Dense, Sequential, keras, pd, plot_history, plt


@app.cell
def _(pd):
    sign_train = pd.read_csv("data/sign_mnist/sign_mnist_train.csv")
    sign_test = pd.read_csv("data/sign_mnist/sign_mnist_test.csv")
    return sign_test, sign_train


@app.cell
def _(sign_train):
    sign_train.head()
    return


@app.cell
def _(sign_test, sign_train):
    y_train = sign_train['label']
    X_train = sign_train.drop(columns='label').values

    y_test = sign_test['label']
    X_test = sign_test.drop(columns='label').values

    X_test.shape
    return X_test, X_train, y_test, y_train


@app.cell
def _(X_train, plt, y_train):
    plt.figure(figsize=(40,40))

    num_images = 20
    for i in range(num_images):
        row = X_train[i]
        label = y_train[i]
    
        image = row.reshape(28,28)  # Note that we reshape the row into a 28X28 pixel image
        plt.subplot(1, num_images, i+1)
        plt.title(label, fontdict={'fontsize': 30})
        plt.axis('off')
        plt.imshow(image, cmap='gray')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Normalize the data

    As we mentioned in previous classes, networks train better with standardized or normalized data. Normalization tends to work best with images, so can look at the min and max of our dataset to get those and divide by the max value
    """)
    return


@app.cell
def _(X_train):
    print(X_train.min(), X_train.max())
    return


@app.cell
def _(X_test, X_train):
    # Normalize our data (get values between 0-1)
    X_train_1 = X_train / 255
    X_test_1 = X_test / 255
    return X_test_1, X_train_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Labels to categorical

    We want out labels to be categorical. As they are now, the labels are 0, 1,...,24 (to be honest, I am not sure why there are 25 classes. Should only be 24...). That would imply label 1 is more similar to label 2 than to label 23 and that label 3 is less than label 4. Converting to categorical labels converts these to named categories, removing the order/associations among the names.
    """)
    return


@app.cell
def _(keras, y_test, y_train):
    # Convert our classes to categorical
    num_classes = 25
    y_train_1 = keras.utils.to_categorical(y_train, num_classes)  # Not entirely sure what the 25th category is...
    y_test_1 = keras.utils.to_categorical(y_test, num_classes)
    return num_classes, y_test_1, y_train_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Make our model

    I've kept the code format here as it was in the Nvidia exercise. This is another common method of making a model. So far, I've used the format below to keep things similar to `sklearn Pipelines`, but I want to expose you to this `model.add` format too. The code in the block below is the same as this:

        model = Sequential([
            layers.Dense(units = 512, activation='relu', input_shape=(784,))),
            layers.Dense(units = 512, activation='relu')),
            layers.Dense(units = num_classes, activation='softmax'))
            ])
    """)
    return


@app.cell
def _(Dense, Sequential, num_classes):
    model = Sequential()
    model.add(Dense(units = 512, activation='relu', input_shape=(784,)))
    model.add(Dense(units = 512, activation='relu'))
    model.add(Dense(units = num_classes, activation='softmax'))
    return (model,)


@app.cell
def _(model):
    model.summary()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compile and fit our model
    """)
    return


@app.cell
def _(model):
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'])
    return


@app.cell
def _(X_test_1, X_train_1, model, y_test_1, y_train_1):
    history = model.fit(X_train_1, y_train_1, epochs=20, verbose=1, validation_data=(X_test_1, y_test_1))
    return (history,)


@app.cell
def _(history, plot_history):
    # Call the plot_history function we made and imported from helpers_plot_history.py

    plot_history(history)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How can we improve our model?

    Honestly, that's not too bad with the data we have. About 80% accuracy for greyscale images 28X28 pixels seems remarkable to me! But, notice that the test accuracy is well below the training accuracy and test loss is going up or staying the same. We are overfitting our data.

    We can do a number of things to improve on these results! Let's take a look.

    Let's look at some slides that cover convolutional kernels, pooling, dropout and data augmentation for image classification in neural networks: [Lect_06_CNNs slides](https://docs.google.com/presentation/d/1uSk7xHWZ9H6YihUP4OdHpIVws_2py_HBfbby7GpZDCA/edit?usp=sharing)

    Then, we can move to [part 2](AI_03_CNNs_part2.ipynb) of this section.
    """)
    return


if __name__ == "__main__":
    app.run()
