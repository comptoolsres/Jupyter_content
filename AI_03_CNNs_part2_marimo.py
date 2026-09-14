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
    # Introduction to Convolutional Neural Networks, part 2

    In [part 1](AI_02_CNNs_part1.ipynb) of this section, we loaded the ASL data, visualized sample images, normalized the data, and created and trained a model. That model had three layers: the first two had 512 neurons, and the last had 25. It used the softmax activation function to generate a prediction representing the probability that an image belonged to each category.

    With that model, we achieved an accuracy of about 80%.

    We looked at some [slides on convolutional kernels, padding, pooling, dropout and data augmentation](https://docs.google.com/presentation/d/1uSk7xHWZ9H6YihUP4OdHpIVws_2py_HBfbby7GpZDCA/edit?usp=sharing). Now we can implement these.

    ## Reload and pre-process our data as in [part 1](AI_02_CNNs_part1.ipynb)
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from PIL import Image

    import torch
    from torch import nn
    from torch.utils.data import DataLoader, Dataset, TensorDataset
    from torchvision import transforms

    import matplotlib.image as mpimg

    return (
        DataLoader,
        Dataset,
        Image,
        TensorDataset,
        nn,
        np,
        pd,
        plt,
        torch,
        transforms,
    )


@app.cell
def _(np, pd):
    sign_train = pd.read_csv("data/sign_mnist/sign_mnist_train.csv")
    sign_test = pd.read_csv("data/sign_mnist/sign_mnist_test.csv")

    y_train = sign_train['label'].to_numpy(dtype=np.int64)
    X_train = sign_train.drop(columns='label').to_numpy(dtype=np.float32) / 255

    y_test = sign_test['label'].to_numpy(dtype=np.int64)
    X_test = sign_test.drop(columns='label').to_numpy(dtype=np.float32) / 255

    num_classes = int(np.unique(y_train).size)
    return X_test, X_train, num_classes, y_test, y_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Add Convolutional Kernels, Max Pooling, and Dropout

    In part 1, we treated the image data as a row of 784 pixels. But our images are 28 rows of 28 pixels (a matrix of pixels). There is information in that spatial arrangement that is lost by simplifying the data into a row.

    Most computer vision tasks work best with the images in that matrix format. So, let's transform the data into the 28X28 shape.

    ### Reshape our data into a 28X28 matrix per image
    """)
    return


@app.cell
def _(DataLoader, TensorDataset, X_test, X_train, torch, y_test, y_train):
    X_train_1 = torch.from_numpy(X_train).reshape(-1, 1, 28, 28)
    X_test_1 = torch.from_numpy(X_test).reshape(-1, 1, 28, 28)
    y_train_1 = torch.from_numpy(y_train)
    y_test_1 = torch.from_numpy(y_test)
    train_dataset = TensorDataset(X_train_1, y_train_1)
    test_dataset = TensorDataset(X_test_1, y_test_1)
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=256)
    print(f'Training shape: {X_train_1.shape}')
    print(f'Test shape: {X_test_1.shape}')
    return X_train_1, test_loader, train_loader, y_train_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Our new model

    Here's a diagram of the model that we'll use. There are *some* theoretical reasons behind this model, but a **lot** of it is "someone tried it and it worked well".

    ![Diagram of the model implemented in code below](images/asl_model.png)
    """)
    return


@app.cell
def _(nn, num_classes, torch):
    class CNNClassifier(nn.Module):
        def __init__(self, num_classes):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(1, 75, kernel_size=3, padding='same'),
                nn.BatchNorm2d(75),
                nn.ReLU(),
                nn.MaxPool2d(2, stride=2),
                nn.Conv2d(75, 50, kernel_size=3, padding='same'),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.BatchNorm2d(50),
                nn.MaxPool2d(2, stride=2),
                nn.Conv2d(50, 25, kernel_size=3, padding='same'),
                nn.ReLU(),
                nn.BatchNorm2d(25),
                nn.MaxPool2d(2, stride=2),
            )
            self.classifier = nn.Sequential(
                nn.Flatten(),
                nn.Linear(25 * 4 * 4, 512),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(512, num_classes),
            )

        def forward(self, inputs):
            return self.classifier(self.features(inputs))


    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = CNNClassifier(num_classes).to(device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())
    return device, loss_function, model, optimizer


@app.cell
def _(model):
    model.summary()
    return


@app.cell
def _(model):
    model.compile(loss="categorical_crossentropy", metrics=["accuracy"])
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
                inputs, labels = (inputs.to(device), labels.to(device))
                outputs = model(inputs)
                total_loss = total_loss + loss_function(outputs, labels).item() * labels.size(0)
                correct = correct + (outputs.argmax(dim=1) == labels).sum().item()
                total = total + labels.size(0)
        return (total_loss / total, correct / total)

    def train_model(model, data_loader, epochs=5):
        history = {'loss': [], 'val_loss': [], 'accuracy': [], 'val_accuracy': []}
        for epoch in range(epochs):
            model.train()
            running_loss = 0.0
            correct = 0
            total = 0
            for inputs, labels in data_loader:
                inputs, labels = (inputs.to(device), labels.to(device))
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = loss_function(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss = running_loss + loss.item() * labels.size(0)
                correct = correct + (outputs.argmax(dim=1) == labels).sum().item()
                total = total + labels.size(0)
            train_loss = running_loss / total
            train_accuracy = correct / total
            validation_loss, validation_accuracy = evaluate(model, test_loader)
            history['loss'].append(train_loss)
            history['accuracy'].append(train_accuracy)
            history['val_loss'].append(validation_loss)
            history['val_accuracy'].append(validation_accuracy)
            print(f'Epoch {epoch + 1:02d}/{epochs}: loss={train_loss:.4f}, accuracy={train_accuracy:.3f}, val_loss={validation_loss:.4f}, val_accuracy={validation_accuracy:.3f}')
        return history
    history = train_model(model, train_loader, epochs=5)
    return history, train_model


@app.cell
def _(history, plt):
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))
    _axes[0].plot(history['accuracy'], label='train')
    _axes[0].plot(history['val_accuracy'], label='test')
    _axes[0].set(title='Model accuracy', xlabel='epoch', ylabel='accuracy')
    _axes[0].legend()
    _axes[1].plot(history['loss'], label='train')
    _axes[1].plot(history['val_loss'], label='test')
    _axes[1].set(title='Model loss', xlabel='epoch', ylabel='loss')
    _axes[1].legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Getting better, but still not great
    ### Add some data augmentation

    Data augmentation creates varied training examples by applying random transformations to the original images. In the next cell, `torchvision.transforms.RandomAffine` rotates, shifts, and scales images as they are loaded.
    """)
    return


@app.cell
def _(DataLoader, Dataset, X_train_1, transforms, y_train_1):
    augmentation = transforms.Compose([transforms.RandomAffine(degrees=10, translate=(0.1, 0.1), scale=(0.9, 1.1))])

    class AugmentedDataset(Dataset):

        def __init__(self, images, labels, transform):
            self.images = images
            self.labels = labels
            self.transform = transform

        def __len__(self):
            return len(self.labels)

        def __getitem__(self, index):
            return (self.transform(self.images[index]), self.labels[index])
    augmented_dataset = AugmentedDataset(X_train_1, y_train_1, augmentation)
    augmented_loader = DataLoader(augmented_dataset, batch_size=128, shuffle=True)
    return augmented_dataset, augmented_loader


@app.cell
def _(DataLoader, augmented_dataset, plt):
    images, labels = next(iter(DataLoader(augmented_dataset, batch_size=32, shuffle=True)))
    _fig, _axes = plt.subplots(nrows=4, ncols=8, figsize=(12, 6))
    for index, axis in enumerate(_axes.flat):
        axis.imshow(images[index].squeeze(), cmap='gray')
        axis.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(model, torch):
    # PyTorch applies the augmentation when each training sample is loaded.
    optimizer_1 = torch.optim.Adam(model.parameters())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Data augmentation applies a random transform each time a training sample is loaded. This gives us a new augmented version of the image during each epoch, helping the model generalize beyond the original training examples.

    The example below uses `torchvision.transforms.RandomAffine` to rotate, shift, and scale the images. The training will take longer than before because each sample is transformed as it is loaded.

    Note that I have reduced the number of epochs to 5. That generally works, but was mostly done because we are doing this on CPUs, not GPUs. This is really where we would want to transition to using a GPU for AI model training.
    """)
    return


@app.cell
def _(augmented_loader, model, train_model):
    history_augmented = train_model(model, augmented_loader, epochs=5)
    return (history_augmented,)


@app.cell
def _(history_augmented, plt):
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))
    _axes[0].plot(history_augmented['accuracy'], label='train')
    _axes[0].plot(history_augmented['val_accuracy'], label='test')
    _axes[0].set(title='Model accuracy after augmentation', xlabel='epoch', ylabel='accuracy')
    _axes[0].legend()
    _axes[1].plot(history_augmented['loss'], label='train')
    _axes[1].plot(history_augmented['val_loss'], label='test')
    _axes[1].set(title='Model loss after augmentation', xlabel='epoch', ylabel='loss')
    _axes[1].legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Let's see how well the model does with new data

    Let's play with some new images that aren't necessarily in the format the model was trained on. First we'll need to modify the new images to match what the model was trained on. The functions below help with that.
    """)
    return


@app.cell
def _(Image, device, model, num_classes, plt, torch, transforms):
    def show_image(image_path):
        image = Image.open(image_path).convert('L')
        plt.imshow(image, cmap='gray')
        plt.axis('off')


    def load_and_scale_image(image_path):
        image = Image.open(image_path).convert('L').resize((28, 28))
        return transforms.ToTensor()(image)


    alphabet = 'abcdefghijklmnopqrstuvwxy'
    dictionary = {index: letter for index, letter in enumerate(alphabet[:num_classes])}


    def predict_letter(file_path):
        show_image(file_path)
        image = load_and_scale_image(file_path).unsqueeze(0).to(device)
        model.eval()
        with torch.no_grad():
            prediction = model(image)
            predicted_letter = dictionary[prediction.argmax(dim=1).item()]
        print(prediction.softmax(dim=1))
        return predicted_letter

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
