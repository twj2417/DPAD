from dpad.correction.energygain import energygain
import unittest
import pytest
import numpy as np
from doufo.tensor.tensor import all_close
from dpad.correction.actual2theory import Module_data
import h5py

def test_energygain():
    data = h5py.File('/mnt/gluster/Techpi/brain16/preprocess/16module_pt3_1GainCorrectt.mat','r')['single_event_data'].value
    data = np.transpose(data)
    data = data[np.where(data[:,3]==0)[0],:]
    # module_data = Module_data()
    pass