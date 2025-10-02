import torch
import torch.nn as nn
import torch.nn.functional as F


class AELoss(nn.Module):
    def __init__(self, grad_score=False, anomaly_score=False, keepdim=False):
        super(AELoss, self).__init__()
        self.grad_score = grad_score
        self.anomaly_score = anomaly_score
        self.keepdim = keepdim

    def forward(self, net_in, net_out):
        x_hat = net_out['x_hat']
        loss = (net_in - x_hat) ** 2

        if self.anomaly_score:
            if self.grad_score:
                grad = torch.abs(torch.autograd.grad(loss.mean(), net_in)[0])
                return torch.mean(grad, dim=[1], keepdim=True) if self.keepdim else torch.mean(grad, dim=[1, 2, 3])
            else:
                return torch.mean(loss, dim=[1], keepdim=True) if self.keepdim else torch.mean(loss, dim=[1, 2, 3])
        else:
            return loss.mean()