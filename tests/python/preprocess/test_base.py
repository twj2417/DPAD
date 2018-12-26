from dpad.preprocess.base import Carriage_data
import unittest
import pytest
import numpy as np
from doufo.tensor.tensor import all_close

class TestCarriage_data(unittest.TestCase):
    def setUp(self):
        self.data = Carriage_data(np.array([[98,1,77,142],
                        [210,234,93,143],
                        [2,128,128,128],
                        [3,128,128,128],
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
                        [0,2,5,240]]))

    
    def test_data_shape(self):
        assert self.data.data_shape == 16

    def test_num_frame(self):
        print(self.data.num_frame)
        assert self.data.num_frame == 2

    def test_carriage_id(self):
        assert self.data.carriage_id == 5

    def test_effective_data(self):
        result = np.array([[98,1,77,142],
                        [210,234,93,143]])
        assert all_close(self.data.extract_effective_data(),result)