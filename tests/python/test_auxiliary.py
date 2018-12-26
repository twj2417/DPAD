import unittest
import pytest
import numpy as np
from doufo.tensor.tensor import all_close
from dpad.auxiliary import hadd_by_row

def test_hadd():
    part1 = np.array([[1,2],[2,3]])
    part2 = np.array([[2,8]])
    part3 = np.array([[1],[3]])
    assert all_close(hadd_by_row([part1,part2]),np.array([[1,2],[2,3],[2,8]]))
    assert all_close(hadd_by_row([part2]),part2)
    