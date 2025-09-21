from typing import Tuple
import torch
import torch.nn as nn

class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        proba = torch.Tensor([0.45, 0.55])
        predict = torch.argmax(proba)
        return predict, proba
