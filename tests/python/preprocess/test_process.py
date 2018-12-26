from dpad.preprocess.process import get_effective_data,split_data_into_module,_rm_loss_data
from dpad.preprocess.base import Carriage_data
from dpad.correction.actual2theory import Module_data
import numpy as np
import pytest
import unittest
from doufo.tensor.tensor import all_close


class Testpreprocess(unittest.TestCase):
    def setUp(self):
        self.data = np.array([[10,128,128,128],
                            [11,128,128,128],
                            [12,128,128,128],
                            [13,128,128,128],
                            [14,128,128,128],
                            [15,128,128,128],
                            [0,2,16,240],
                            [0,87,16,253],
                            [0,0,0,253],
                            [0,88,16,254],
                            [0,0,0,254],
                            [98,1,77,142],
                            [210,234,93,143],
                            [2,128,128,128],
                            [3,128,128,128],
                            [4,128,128,128],
                            [5,128,128,128],
                            [6,128,128,128],
                            [7,128,128,128],
                            [8,128,128,128],
                            [9,128,128,128],
                            [10,128,128,128],
                            [11,128,128,128],
                            [12,128,128,128],
                            [13,128,128,128],
                            [14,128,128,128],
                            [15,128,128,128],
                            [0,2,1,240],
                            [0,88,16,253],
                            [0,0,0,253],
                            [0,89,16,254],
                            [0,0,0,254],
                            [28,2,64,142],
                            [65,170,66,143],
                            [1,1,27,142],
                            [53,194,66,143],
                            [3,1,34,142],
                            [75,197,66,143],
                            [64,1,35,142],
                            [75,197,66,143],
                            [8,128,128,128],
                            [9,128,128,128],
                            [10,128,128,128],
                            [11,128,128,128],
                            [12,128,128,128],
                            [13,128,128,128],
                            [14,128,128,128],
                            [15,128,128,128],
                            [0,8,6,240],
                            [0,89,16,253],
                            [0,0,0,253],
                            [0,90,16,254],
                            [0,0,0,254],
                            [116,1,33,142],
                            [242,229,61,143],
                            [212,0,14,142],
                            [252,255,61,143],
                            [4,128,128,128],
                            [5,128,128,128],
                            [6,128,128,128],
                            [7,128,128,128],
                            [8,128,128,128]])

    def test_rm_loss_data(self):
        carriage1 = Carriage_data(self.data[11:28,:])
        carriage2 = Carriage_data(self.data[32:49,:])
        assert all_close(_rm_loss_data(self.data)[0].data,carriage1.data)
        assert all_close(_rm_loss_data(self.data)[1].data,carriage2.data)


    def test_split(self):
        data = split_data_into_module(_rm_loss_data(self.data),16)
        assert all_close(self.data[11:13,:],data[1].data)
        assert all_close(self.data[32:40,:],data[6].data)
