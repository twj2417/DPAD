from dpad.preprocess.process import get_effective_data,_split_data_into_module,_rm_loss_data
from dpad.preprocess.base import Carriage_data
from dpad.correction.actual2theory import Module_data
import numpy as np
import pytest
import unittest
from doufo.tensor.tensor import all_close


class Testpreprocess(unittest.TestCase):
    def setUp(self):
        self.data = np.load('/mnt/gluster/Techpi/brain16/preprocess/train_data.npy')

    def test_rm_loss_data(self):
        result = np.vstack((self.data[114:386,:],self.data[390:662,:]))
        assert all_close(_rm_loss_data(self.data),result)


    def test_split(self):
        data = _split_data_into_module(_rm_loss_data(self.data),16)
        assert all_close(np.vstack((self.data[114:124,:],self.data[390:404,:])),data[0].data)
        assert all_close(np.vstack((self.data[216:232,:],self.data[492:506])),data[6].data)
