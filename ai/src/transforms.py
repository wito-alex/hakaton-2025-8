
import os
import numpy as np
from torchvision import transforms


def get_transform(target_size):
    """
    target_size: tuple (H, W), к которому будут ресайзиться все изображения
    """
    normalize = transforms.Normalize((0.5,), (0.5,))  # для 1 канала

    transform = transforms.Compose([
        # transforms.Lambda(lambda x: x.astype(np.float32)),
        transforms.ToTensor(),
        transforms.Resize(target_size), 
        normalize
    ])
    return transform