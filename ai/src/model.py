# from typing import Tuple
# import torch
# import torch.nn as nn

# class DummyModel(nn.Module):
#     def __init__(self):
#         super().__init__()

#     def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
#         proba = torch.Tensor([0.45, 0.55])
#         predict = torch.argmax(proba)
#         return predict, proba

import torch.nn as nn


def down_conv(in_planes, out_planes):
    return nn.Conv2d(in_planes, out_planes, kernel_size=4, stride=2, padding=1, bias=False)


def up_conv(in_planes, out_planes):
    return nn.ConvTranspose2d(in_planes, out_planes, kernel_size=4, stride=2, padding=1, bias=False)


def conv3x3(in_planes: int, out_planes: int, stride: int = 1, groups: int = 1, dilation: int = 1) -> nn.Conv2d:
    """3x3 convolution with padding"""
    return nn.Conv2d(
        in_planes,
        out_planes,
        kernel_size=3,
        stride=stride,
        padding=dilation,
        groups=groups,
        bias=False,
        dilation=dilation,
    )

import torch
import torch.nn as nn


class BasicBlock(nn.Module):
    def __init__(self, inplanes, planes, num_layers, downsample=False, upsample=False, last_layer=False):
        super(BasicBlock, self).__init__()
        assert not (downsample and upsample)
        layers = []
        if downsample:
            layers.append(down_conv(inplanes, planes))
        elif upsample:
            layers.append(up_conv(inplanes, planes))
        else:
            layers.append(conv3x3(inplanes, planes))
        layers.append(nn.BatchNorm2d(planes))
        layers.append(nn.ReLU(inplace=True))

        # Deeper block
        if upsample:
            for _ in range(1, num_layers):
                add_layer = [conv3x3(inplanes, inplanes),
                             nn.BatchNorm2d(inplanes),
                             nn.ReLU(inplace=True)]

                layers = add_layer + layers
        else:
            for _ in range(1, num_layers):
                add_layer = [conv3x3(planes, planes),
                             nn.BatchNorm2d(planes),
                             nn.ReLU(inplace=True)]

                layers = layers + add_layer

        if last_layer:
            layers = layers[:-2]  # remove the BN and ReLU for the output layer.

        self.model = nn.Sequential(*layers)

    def forward(self, x):
        out = self.model(x)
        return out


class ResBlock(nn.Module):
    def __init__(self, inplanes, planes, num_layers, downsample=False, upsample=False, last_layer=False):
        super(ResBlock, self).__init__()
        assert not (downsample and upsample)
        self.last_layer = last_layer
        self.relu = nn.ReLU(inplace=True)

        layers = []
        if downsample:
            layers.append(down_conv(inplanes, planes))
            self.skip = nn.Sequential(
                down_conv(inplanes, planes),
                nn.BatchNorm2d(planes)
            )
        elif upsample:
            layers.append(up_conv(inplanes, planes))
            self.skip = nn.Sequential(
                up_conv(inplanes, planes),
                nn.BatchNorm2d(planes)
            )
        else:
            layers.append(conv3x3(inplanes, planes))
            self.skip = nn.Identity()
        layers.append(nn.BatchNorm2d(planes))

        # Deeper block
        if upsample:
            for _ in range(1, num_layers):
                add_layer = [conv3x3(inplanes, inplanes),
                             nn.BatchNorm2d(inplanes),
                             nn.ReLU(inplace=True)]

                layers = add_layer + layers
        else:
            for _ in range(1, num_layers):
                add_layer = [nn.ReLU(inplace=True),
                             conv3x3(planes, planes),
                             nn.BatchNorm2d(planes)]

                layers = layers + add_layer

        if last_layer:  # remove the BN for the output layer.
            layers = layers[:-1]

        self.model = nn.Sequential(*layers)

    def forward(self, x):
        identity = x

        out = self.model(x)

        identity = self.skip(identity)
        out += identity

        if not self.last_layer:  # remove the relu for the output layer.
            out = self.relu(out)

        return out


class BottleNeck(nn.Module):
    def __init__(self, in_planes, feature_size, mid_num=2048, latent_size=16):
        super(BottleNeck, self).__init__()
        self.in_planes = in_planes
        self.feature_size = feature_size
        self.linear_enc = nn.Sequential(
            nn.Linear(in_planes * feature_size * feature_size, mid_num),
            nn.BatchNorm1d(mid_num),
            nn.ReLU(True),
            nn.Linear(mid_num, latent_size))

        self.linear_dec = nn.Sequential(
            nn.Linear(latent_size, mid_num),
            nn.BatchNorm1d(mid_num),
            nn.ReLU(True),
            nn.Linear(mid_num, in_planes * feature_size * feature_size))

    def forward(self, x):
        x = x.view(x.size(0), -1)
        z = self.linear_enc(x)
        out = self.linear_dec(z)

        out = out.view(x.size(0), self.in_planes, self.feature_size, self.feature_size)

        return {'out': out, 'z': z}
    

class SpatialBottleNeck(nn.Module):
    def __init__(self, in_planes, feature_size, mid_num=2048, latent_size=16):
        super(SpatialBottleNeck, self).__init__()
        self.in_planes = in_planes
        self.feature_size = feature_size
        self.linear_enc = nn.Sequential(
            nn.Conv2d(in_channels=in_planes, out_channels=mid_num, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(mid_num),
            nn.ReLU(True),
            nn.Conv2d(in_channels=mid_num, out_channels=latent_size, kernel_size=1, stride=1, padding=0, bias=False))

        self.linear_dec = nn.Sequential(
            nn.Conv2d(in_channels=latent_size, out_channels=mid_num, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(mid_num),
            nn.ReLU(True),
            nn.Conv2d(in_channels=mid_num, out_channels=in_planes, kernel_size=1, stride=1, padding=0, bias=False),)

    def forward(self, x):
        z = self.linear_enc(x)
        out = self.linear_dec(z)

        return {'out': out, 'z': z}



class AE(nn.Module):
    def __init__(self, input_size=64, in_planes=1, base_width=16, expansion=1, mid_num=2048, latent_size=16,
                 en_num_layers=1, de_num_layers=1, spatial=False):
        super(AE, self).__init__()

        bottleneck = SpatialBottleNeck if spatial else BottleNeck

        self.fm = input_size // 16  # down-sample for 4 times. 2^4=16

        self.en_block1 = BasicBlock(in_planes, 1 * base_width * expansion, en_num_layers, downsample=True)

        self.en_block2 = BasicBlock(1 * base_width * expansion, 2 * base_width * expansion, en_num_layers,
                                    downsample=True)
        self.en_block3 = BasicBlock(2 * base_width * expansion, 4 * base_width * expansion, en_num_layers,
                                    downsample=True)
        self.en_block4 = BasicBlock(4 * base_width * expansion, 4 * base_width * expansion, en_num_layers,
                                    downsample=True)

        self.bottle_neck = bottleneck(4 * base_width * expansion, feature_size=self.fm, mid_num=mid_num,
                                      latent_size=latent_size)

        self.de_block1 = BasicBlock(4 * base_width * expansion, 4 * base_width * expansion, de_num_layers,
                                    upsample=True)
        self.de_block2 = BasicBlock(4 * base_width * expansion, 2 * base_width * expansion, de_num_layers,
                                    upsample=True)
        self.de_block3 = BasicBlock(2 * base_width * expansion, 1 * base_width * expansion, de_num_layers,
                                    upsample=True)
        self.de_block4 = BasicBlock(1 * base_width * expansion, in_planes, de_num_layers, upsample=True,
                                    last_layer=True)

    def forward(self, x):
        en1 = self.en_block1(x)
        en2 = self.en_block2(en1)
        en3 = self.en_block3(en2)
        en4 = self.en_block4(en3)

        bottle_out = self.bottle_neck(en4)
        z, de4 = bottle_out['z'], bottle_out['out']

        de3 = self.de_block1(de4)
        de2 = self.de_block2(de3)
        de1 = self.de_block3(de2)
        x_hat = self.de_block4(de1)

        return {'x_hat': x_hat, 'z': z, 'en_features': [en1, en2, en3], 'de_features': [de1, de2, de3]}
