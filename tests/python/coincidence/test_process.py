from dpad.coincidence.base import Coincidence_events
from dpad.coincidence.process import coincidence_with_time_window
import unittest
import pytest
import numpy as np
from doufo.tensor.tensor import all_close
from dpad.correction.actual2theory import Single_event

def test_coinicdence():
    data = np.array([[31,197.503,11296664,3],
                    [86,184.607,11296777,15],
                    [99,272.152,11296778,15],
                    [27,353.988,11298973,13],
                    [75,201.683,11298974,3],
                    [75,623.307,11300156,10],
                    [85,292,11300156,10],
                    [33,295.989,11300303,14],
                    [65,242.934,11300303,14],
                    [17,496.426,11300324,8]])
    single_events = Single_event(data[:,2],data[:,1],data[:,3],data[:,0])
    coincidence = coincidence_with_time_window(single_events,5)
    assert coincidence.block1== 13
    assert coincidence.block2 == 3
    assert coincidence.crystal1 == 27
    assert coincidence.crystal2 == 75