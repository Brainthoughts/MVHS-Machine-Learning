import math

import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from examples.neural_networks.tf_datasets import PointClusterDataset, PointCircleDataset, PointCornerDataset, PointSpiralDataset


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(2, 4)  # Input layer: 2 input neurons, 4 hidden neurons in layer 1
        self.fc2 = nn.Linear(4, 2)  # Hidden layer 1: 4 input neurons, 2 hidden neurons in layer 2
        self.fc3 = nn.Linear(2, 1)  # Hidden layer 2: 2 input neurons, 1 output neuron

    def forward(self, x):
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        return x


# Create a dataloader for the dataset
batch_size = 64
dataset = PointCircleDataset(noise=1)  # PointCircleDataset(noise=1) # PointSpiralDataset(noise=0) # PointCornerDataset(noise=1) # PointClusterDataset(noise=1)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Instantiate the neural network
net = Net()

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)

def visualize_decision_boundary(model, X, Y, point_spacing = .5, show_training_data=True, interpolate=True, color_map = colormaps['bwr']):
    # Generate a grid of points from -5 to 5 with a step of point_spacing
    xx, yy = np.meshgrid(np.arange(-5, 5, point_spacing), np.arange(-5, 5, point_spacing))
    # Flatten the grids into a 1D array
    xx_flattened = xx.ravel()
    yy_flattened = yy.ravel()
    # Concatenate the flattened grids to create a matrix of input points and transpose that matrix
    input_points = np.vstack((xx_flattened, yy_flattened)).T
    # Convert the input points to a torch tensor
    input_points = torch.tensor(input_points, dtype=torch.float32)
    # Get the predictions for the input points from the trained model
    with torch.no_grad():
        predictions = model(input_points)
    # Convert the predictions to a numpy array
    predictions = predictions.numpy()
    # Reshape the predictions to match the shape of the original grids
    zz = predictions.reshape(xx.shape)

    # Plot the decision boundary
    if interpolate:
        plt.contourf(xx, yy, zz, cmap=color_map, alpha=0.8)  # plot a smooth-ish filled contour
    else:
        plt.scatter(xx, yy, c=zz, cmap=color_map)  # scatter plot of tested points
    if show_training_data:
        plt.scatter(X[Y == 0][:, 0], X[Y == 0][:, 1], c=color_map(0.0), marker='o', label='Class 0')  # plot the training data
        plt.scatter(X[Y == 1][:, 0], X[Y == 1][:, 1], c=color_map(1.0), marker='s', label='Class 1')
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.legend()
    plt.title('Decision Boundary')
    plt.show()

# Training loop
num_epochs = 500
for epoch in range(num_epochs):
    epoch_loss = 0.
    if epoch % math.ceil(num_epochs/(30-1)) == 0:  # max of 30 plots, 29 while training and 1 after
        visualize_decision_boundary(net, dataset.points, dataset.labels)
    for i, (inputs, targets) in enumerate(dataloader):
        # Zero the gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = net(inputs)
        loss = criterion(outputs.squeeze(), targets)

        # Backward pass
        loss.backward()

        # Update weights
        optimizer.step()
        epoch_loss += loss.item()

    # Print loss for this epoch
    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {epoch_loss/len(dataloader):.4f}')  # see https://fstring.help/cheat/

print('Training finished.')

visualize_decision_boundary(net, dataset.points, dataset.labels, show_training_data=False, interpolate=False)
