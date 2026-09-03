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
    # Introduction to Convolutional Neural Networks, part 2

    In [part 1](AI_02_CNNs_part1.ipynb) of this section, we loaded the ASL data, visualized some sample images, normalized the data, and created and trained a model. That model had three layed, the first two had 512 neurons and the last had 25 and used the softmax activation function to generate a prediction that was the probablity that an image belonged to each of the 25 categories.

    With that model, we achieved an accuract of about 80%.

    We looked at some [slides on convolutional kernels, padding, pooling, dropout and data augmentation](https://docs.google.com/presentation/d/1uSk7xHWZ9H6YihUP4OdHpIVws_2py_HBfbby7GpZDCA/edit?usp=sharing). Now we can implement these.

    ## Reload and pre-process our data as in [part 1](AI_02_CNNs_part1.ipynb)
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    # '%matplotlib inline' command supported automatically in marimo
    from PIL import Image
    import matplotlib.image as mpimg

    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.preprocessing import image_dataset_from_directory
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.preprocessing import image as image_utils

    from tensorflow.keras.models import Sequential
    from tensorflow.keras import layers
    from tensorflow.keras.layers import Dense

    from helpers_plot_history import plot_history # Some helper functions for the CNN notebooks.

    return (
        Dense,
        ImageDataGenerator,
        Sequential,
        image_utils,
        keras,
        mpimg,
        np,
        pd,
        plot_history,
        plt,
    )


@app.cell
def _(keras, pd):
    # Load the data
    sign_train = pd.read_csv("data/sign_mnist/sign_mnist_train.csv")
    sign_test = pd.read_csv("data/sign_mnist/sign_mnist_test.csv")

    # Prepare X and y
    y_train = sign_train['label']
    X_train = sign_train.drop(columns='label').values

    y_test = sign_test['label']
    X_test = sign_test.drop(columns='label').values

    # Normalize the data
    X_train = X_train/255
    X_test = X_test/255

    # Convert our classes to categorical
    num_classes = 25 # Not entirely sure what the 25th category is...

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    return X_test, X_train, num_classes, y_test, y_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Add Convolutional Kernels, Max Pooling, and Dropout

    In part 1, we treated the image data as a row of 784 pixels. But our images are 28 rows of 28 pixels (a matrix of pixels). There is information in that spacial arrangement that is lost by simplifying the data into a row.

    Most computer vision tasks work best with the images in that matrix format. So, let's transform the data into the 28X28 shape.

    ### Reshape our data into a 28X28 matrix per image
    """)
    return


@app.cell
def _(X_test, X_train):
    print(f'Shape before: {X_train.shape}')
    X_train_1 = X_train.reshape(-1, 28, 28, 1)
    X_test_1 = X_test.reshape(-1, 28, 28, 1)
    print(f'Shape after: {X_train_1.shape}')
    return X_test_1, X_train_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Our new model

    Here's a diagram of the model that we'll use. There are *some* theoretical reasons behind this model, but a **lot** of it is "someone tried it and it worked well".

    ![Diagram of the model implemented in code below](images/asl_model.png)
    """)
    return


@app.cell
def _(Dense, Sequential, num_classes):
    from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dropout, BatchNormalization
    model = Sequential()
    model.add(Conv2D(75, (3, 3), strides=1, padding='same', activation='relu', input_shape=(28, 28, 1)))
    model.add(BatchNormalization())
    model.add(MaxPool2D((2, 2), strides=2, padding='same'))
    model.add(Conv2D(50, (3, 3), strides=1, padding='same', activation='relu'))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(MaxPool2D((2, 2), strides=2, padding='same'))
    model.add(Conv2D(25, (3, 3), strides=1, padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPool2D((2, 2), strides=2, padding='same'))
    model.add(Flatten())
    model.add(Dense(units=512, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(units=num_classes, activation='softmax'))
    return (model,)


@app.cell
def _(model):
    model.summary()
    return


@app.cell
def _(model):
    model.compile(loss="categorical_crossentropy", metrics=["accuracy"])
    return


@app.cell
def _(X_test_1, X_train_1, model, y_test, y_train):
    history = model.fit(X_train_1, y_train, epochs=5, verbose=1, validation_data=(X_test_1, y_test))
    return (history,)


@app.cell
def _(history, plot_history):
    plot_history(history)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Getting better, but still not great
    ### Add some data augmentation

    This is implemented using a data flow generator. This image from Adrian Rosenbrock's article [Keras ImageDataGenerator and Data Augmentation](https://pyimagesearch.com/2019/07/08/keras-imagedatagenerator-and-data-augmentation/) is a good summary:

    ![Data flow generator diagram](https://929687.smushcdn.com/2633864/wp-content/uploads/2019/07/keras_data_augmentation_in_place.png?lossy=1&strip=1&webp=1)
    """)
    return


@app.cell
def _(ImageDataGenerator):
    datagen = ImageDataGenerator(
        rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range=0.1,  # Randomly zoom image
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images horizontally
        vertical_flip=False, # Don't randomly flip images vertically
    )
    return (datagen,)


@app.cell
def _(X_train_1, datagen, np, plt, y_train):
    batch_size = 32
    img_iter = datagen.flow(X_train_1, y_train, batch_size=batch_size)
    x, y = img_iter.next()
    fig, ax = plt.subplots(nrows=4, ncols=8)
    for _i in range(batch_size):
        image = x[_i]
        ax.flatten()[_i].imshow(np.squeeze(image))
    plt.show()
    return batch_size, img_iter


@app.cell
def _(X_train_1, datagen, model):
    # Fit the generator o nthe taining data.
    datagen.fit(X_train_1)
    # Compile the new model
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From the Nvidia notebooks:

    > When using an image data generator with Keras, a model trains a bit differently: instead of just passing the `[X]_train` and `y_train` datasets into the model, we pass the generator in, calling the generator's [flow](https://keras.io/api/preprocessing/image/) method. This causes the images to get augmented live and in memory right before they are passed into the model for training.
    >
    > Generators can supply an indefinite amount of data, and when we use them to train our data, we need to explicitly set how long we want each epoch to run, or else the epoch will go on indefinitely, with the generator creating an indefinite number of augmented images to provide the model.
    >
    > We explicitly set how long we want each epoch to run using the `steps_per_epoch` named argument. Because `steps * batch_size = number_of_images_trained in an epoch` a common practice, that we will use here, is to set the number of steps equal to the non-augmented dataset size divided by the batch_size (which has a default value of 32).
    >
    > Run the following cell to see the results. The training will take longer than before, which makes sense given we are now training on more data than previously:

    Note that I have reduced the number of epochs to 5. That generally works, but was mostly done because we are doing this on CPUs, not GPUS. This is really where we would want to transition to using a GPU for AI model training.
    """)
    return


@app.cell
def _(X_test_1, X_train_1, batch_size, img_iter, model, y_test):
    history_1 = model.fit(img_iter, epochs=5, steps_per_epoch=len(X_train_1) / batch_size, validation_data=(X_test_1, y_test))  # Run same number of steps we would if we were not using a generator.
    return (history_1,)


@app.cell
def _(history_1, plot_history):
    plot_history(history_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Let's see how well the model does with new data

    Let's play with some new images that aren't necessarily in the format the model was trained on. First we'll need to modify the new images to match what the model was trained on. The functions below help with that.
    """)
    return


@app.cell
def _(image_utils, model, mpimg, np, plt):
    def show_image(image_path):
        """Shows the image at a given path as it is."""
        image = mpimg.imread(image_path)
        plt.imshow(image, cmap='gray')

    def load_and_scale_image(image_path):
        """Loads and scales the image to a 28x28 greyscale image, like the training data"""
        image = image_utils.load_img(image_path, color_mode='grayscale', target_size=(28, 28))
        return image
    alphabet = 'abcdefghijklmnopqrstuvwxy'
    # Creates a dictionary to lookup what category number is what. 
    # NOTE: this is based on there being 24 categories, we have 25, somehwere this will go wrong...
    dictionary = {}
    for _i in range(24):
        dictionary[_i] = alphabet[_i]
    dictionary

    def predict_letter(file_path):
        """Given an image, load it, scale for model and predict letter"""
        show_image(file_path)
        image = load_and_scale_image(file_path)
        image = image_utils.img_to_array(image)
        image = image.reshape(1, 28, 28, 1)
        image = image / 255
        prediction = model.predict(image)
        print(prediction)
        predicted_letter = dictionary[np.argmax(prediction)]  # print the whole prediction array, probability for each category.
        return predicted_letter  # convert prediction to letter

    return (predict_letter,)


@app.cell
def _(predict_letter):
    predict_letter("data/sign_mnist/b.png")
    return


@app.cell
def _(predict_letter):
    predict_letter('data/sign_mnist/c.jpeg')
    return


@app.cell
def _(predict_letter):
    predict_letter('data/sign_mnist/a.png')
    return


@app.cell
def _(predict_letter):
    predict_letter('data/sign_mnist/l.png')
    return


@app.cell
def _(predict_letter):
    predict_letter('data/sign_mnist/j.jpeg')
    return


if __name__ == "__main__":
    app.run()
