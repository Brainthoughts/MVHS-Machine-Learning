import numpy as np
import torch
from torch.utils.data import Dataset


class PointClusterDataset(Dataset):
    def __init__(self, num_points=1000, noise=1):
        self.points, self.labels = self.generate_points(num_points, noise)

    def __getitem__(self, index):
        return self.points[index], self.labels[index]

    def __len__(self):
        return len(self.points)

    @classmethod
    def generate_points(cls, num_points, noise):
        # Create the dataset
        points1 = torch.empty((num_points // 2, 3), dtype=torch.float32)
        points2 = torch.empty((num_points // 2, 3), dtype=torch.float32)
        for point in points1:
            point[0] = 3 + torch.rand(1) * noise
            point[1] = 3 + torch.rand(1) * noise
            point[2] = 0

        for point in points2:
            point[0] = -3 + torch.rand(1) * noise
            point[1] = -3 + torch.rand(1) * noise
            point[2] = 1

        points = torch.cat((points1, points2))
        labels = points[:, 2]
        points = points[:, :2]
        return points, labels


class PointCircleDataset(Dataset):
    def __init__(self, num_points=1000, noise=1):
        self.points, self.labels = self.generate_points(num_points, noise)

    def __getitem__(self, index):
        return self.points[index], self.labels[index]

    def __len__(self):
        return len(self.points)

    @classmethod
    def generate_points(cls, num_points, noise):
        points1 = torch.empty((num_points // 2, 3), dtype=torch.float32)
        points2 = torch.empty((num_points // 2, 3), dtype=torch.float32)

        for point in points1:
            angle = torch.rand(1) * 2 * np.pi
            point[0] = np.cos(angle) + torch.rand(1) * noise
            point[1] = np.sin(angle) + torch.rand(1) * noise
            point[2] = 0

        for point in points2:
            angle = torch.rand(1) * 2 * np.pi
            point[0] = np.cos(angle) * 3 + torch.rand(1) * noise
            point[1] = np.sin(angle) * 3 + torch.rand(1) * noise
            point[2] = 1

        points = torch.cat((points1, points2))
        labels = points[:, 2]
        points = points[:, :2]
        return points, labels


class PointCornerDataset(Dataset):
    def __init__(self, num_points=1000, noise=0):
        self.points, self.labels = self.generate_points(num_points, noise)

    def __getitem__(self, index):
        return self.points[index], self.labels[index]

    def __len__(self):
        return len(self.points)

    @classmethod
    def generate_points(cls, num_points, noise):
        points1 = torch.empty((num_points // 2, 3), dtype=torch.float32)
        points2 = torch.empty((num_points // 2, 3), dtype=torch.float32)

        for point in points1:
            multiplier = np.random.choice([-1, 1])
            point[0] = 3 * torch.rand(1) * multiplier + (torch.rand(1) - .5) * noise
            point[1] = 3 * torch.rand(1) * multiplier + (torch.rand(1) - .5) * noise
            point[2] = 0

        for point in points2:
            multiplier = np.random.choice([-1, 1])
            point[0] = 3 * torch.rand(1) * multiplier + (torch.rand(1) - .5) * noise
            point[1] = 3 * torch.rand(1) * -multiplier + (torch.rand(1) - .5) * noise
            point[2] = 1

        points = torch.cat((points1, points2))
        labels = points[:, 2]
        points = points[:, :2]
        return points, labels


class PointSpiralDataset(Dataset):
    def __init__(self, num_points=1000, noise=0):
        self.points, self.labels = self.generate_points(num_points, noise)

    def __getitem__(self, index):
        return self.points[index], self.labels[index]

    def __len__(self):
        return len(self.points)

    @classmethod
    def generate_points(cls, num_points, noise):
        points1 = torch.empty((num_points // 2, 3), dtype=torch.float32)
        points2 = torch.empty((num_points // 2, 3), dtype=torch.float32)

        for idx, point in enumerate(points1):
            angle = idx / num_points * 2 * np.pi
            point[0] = angle * np.cos(3*angle) + torch.rand(1) * noise
            point[1] = angle * np.sin(3*angle) + torch.rand(1) * noise
            point[2] = 0

        for idx, point in enumerate(points2):
            angle = idx / num_points * 2 * np.pi
            point[0] = angle * np.cos(3*angle + np.pi) + torch.rand(1) * noise
            point[1] = angle * np.sin(3*angle + np.pi) + torch.rand(1) * noise
            point[2] = 1

        points = torch.cat((points1, points2))
        labels = points[:, 2]
        points = points[:, :2]
        return points, labels
