
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/06Magda_convnet.ipynb

from exp.nb_03Magda import *
from exp.nb_04Magda_corrected import *
from exp.nb_05bMagda import *
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F

def norm_all(tr, val, tst):
    tr, val, tst = map(lambda x: normalize(tr, x), (tr, val, tst))
    return tr, val, tst

class ReshapeMnist(Callback):
    def train_batch_begin(self, *args):
        self.learner.batch_x = self.learner.batch_x.view(-1, 1, 28, 28)

    def validation_batch_begin(self, *args):
        self.train_batch_begin()


class Flatten(nn.Module):
    def forward(self, x):
        return x.view(x.shape[0], -1)


class LearnerCnn(Learner):
    def _get_model(self, num_out=10):
        self.model = nn.Sequential(
            nn.Conv2d(1, 8, 5, padding=2, stride=2), nn.ReLU(),
            nn.Conv2d(8, 16, 3, padding=1, stride=2), nn.ReLU(),
            nn.Conv2d(16, 32, 3, padding=1, stride=2), nn.ReLU(),
            nn.Conv2d(32, 64, 3, padding=1, stride=2), nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1, stride=2), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
            Flatten(),
            nn.Linear(64, num_out)
        )


class CudaCallback(Callback):
    def __init__(self, device):
        self.device = device
        super(CudaCallback, self).__init__()

    def fit_begin(self, *args):
        self.learner.model = self.learner.model.to(device=self.device)

    def train_batch_begin(self, *args):
        self.learner.batch_x = self.learner.batch_x.to(device=self.device)
        self.learner.batch_y = self.learner.batch_y.to(device=self.device)

    def validation_batch_begin(self, *args):
        self.train_batch_begin()
