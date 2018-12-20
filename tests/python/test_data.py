from dpad.data import Carriage_data,Train_data
import unittest
import pytest

class TestCarriage_data(unittest.TestCase):
    def setUp(self):
        self.data = Carriage_data(367,90,16,67)
    
    def test_