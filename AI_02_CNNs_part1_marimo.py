import marimo

__generated_with = "0.24.2"
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
    import matplotlib.pyplot as plt

    import torch
    from torch import nn
    from torch.utils.data import DataLoader, TensorDataset

    from helpers_plot_history import plot_history

    return DataLoader, TensorDataset, nn, np, pd, plt, torch


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
def _(np, sign_test, sign_train):
    y_train = sign_train['label'].to_numpy(dtype=np.int64)
    X_train = sign_train.drop(columns='label').to_numpy(dtype=np.float32) / 255

    y_test = sign_test['label'].to_numpy(dtype=np.int64)
    X_test = sign_test.drop(columns='label').to_numpy(dtype=np.float32) / 255

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

    As we mentioned in previous classes, networks train better with standardized or normalized data. Here, the pixel values are normalized to the range 0-1 when the data are loaded.
    """)
    return


@app.cell
def _(X_train):
    print(X_train.min(), X_train.max())
    return


@app.cell
def _(DataLoader, TensorDataset, X_test, X_train, torch, y_test, y_train):
    train_dataset = TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train))
    test_dataset = TensorDataset(torch.from_numpy(X_test), torch.from_numpy(y_test))
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=256)
    return test_loader, train_loader


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Prepare the labels

    The labels are integer category codes from 0 through 24. PyTorch's `CrossEntropyLoss` uses these integer labels directly, so no one-hot conversion is needed.
    """)
    return


@app.cell
def _(np, y_train):
    num_classes = int(np.unique(y_train).size)
    print(f"Number of classes: {num_classes}")
    return (num_classes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Make our model

    PyTorch models are defined as subclasses of `nn.Module`. This model has two hidden layers with 512 neurons each and an output layer with one score per class. `CrossEntropyLoss` applies the appropriate normalization to those output scores.
    """)
    return


@app.cell
def _(nn, num_classes, torch):
    class SimpleClassifier(nn.Module):
        def __init__(self, num_classes):
            super().__init__()
            self.network = nn.Sequential(
                nn.Flatten(),
                nn.Linear(784, 512),
                nn.ReLU(),
                nn.Linear(512, 512),
                nn.ReLU(),
                nn.Linear(512, num_classes),
            )

        def forward(self, inputs):
            return self.network(inputs)


    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SimpleClassifier(num_classes).to(device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())
    return device, loss_function, model, optimizer


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
def _(device, model):
    print(model)
    print(f"Training on: {device}")
    return


@app.cell
def _(
    device,
    loss_function,
    model,
    optimizer,
    test_loader,
    torch,
    train_loader,
):
    def evaluate(model, data_loader):
        model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in data_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                total_loss += loss_function(outputs, labels).item() * labels.size(0)
                correct += (outputs.argmax(dim=1) == labels).sum().item()
                total += labels.size(0)
        return total_loss / total, correct / total


    history = {"loss": [], "val_loss": [], "accuracy": [], "val_accuracy": []}
    epochs = 20
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_function(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * labels.size(0)
            correct += (outputs.argmax(dim=1) == labels).sum().item()
            total += labels.size(0)

        train_loss = running_loss / total
        train_accuracy = correct / total
        validation_loss, validation_accuracy = evaluate(model, test_loader)
        history["loss"].append(train_loss)
        history["accuracy"].append(train_accuracy)
        history["val_loss"].append(validation_loss)
        history["val_accuracy"].append(validation_accuracy)
        print(f"Epoch {epoch + 1:02d}/{epochs}: loss={train_loss:.4f}, accuracy={train_accuracy:.3f}, val_loss={validation_loss:.4f}, val_accuracy={validation_accuracy:.3f}")
    return (history,)


@app.cell
def _(history, plt):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(history["accuracy"], label="train")
    axes[0].plot(history["val_accuracy"], label="test")
    axes[0].set(title="Model accuracy", xlabel="epoch", ylabel="accuracy")
    axes[0].legend()
    axes[1].plot(history["loss"], label="train")
    axes[1].plot(history["val_loss"], label="test")
    axes[1].set(title="Model loss", xlabel="epoch", ylabel="loss")
    axes[1].legend()
    plt.tight_layout()
    plt.show()
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
