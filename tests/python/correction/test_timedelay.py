from dpad.correction.timedelay import timedelay
import unittest
import pytest
import numpy as np
from doufo.tensor.tensor import all_close
from dpad.correction.actual2theory import Single_event
import h5py

def testdelay():
    data = h5py.File('/mnt/gluster/Techpi/brain16/preprocess/16module_pt3_1GainCorrectt.mat','r')['single_event_data'].value
    data = np.transpose(data)
    event = Single_event(data[:,2],data[:,1],data[:,3],data[:,0])
    block_grid = np.array([1,10,10])
    time = timedelay(event,2**24,16,block_grid)
    assert all_close(np.transpose(time),np.array([0,-2434447, -5862977, -4415601, -4675805, -4838861, -4203983,
                                                    -5791165, -4576211, -6638585, -4152363, -5494579, -5930491,
                                                    -6143003, -6245015, -5597371]))
    
    