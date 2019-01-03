from dpad.coincidence.base import Coincidence_events
import unittest
import pytest
import numpy as np
from doufo.tensor.tensor import all_close
from srf.external.stir.function import get_scanner
from srf.data import ScannerClass

class Test_coincidence_events(unittest.TestCase):
    def setUp(self):
        block1 = np.array([13,9,1,11,11,0,4,12,4])
        crystal1 = np.array([27,33,82,50,86,49,47,28,86])
        energy1 = np.array([353.98,180,365.81,354.28,358.07,153.96,344.54,464.54,222.83])
        block2 = np.array([3,3,8,3,4,3,9,1,2])
        crystal2 = np.array([75,20,58,89,71,94,47,42,10])
        energy2 = np.array([201.68,269.60,476.38,200.63,215.67,197.50,525,434.58,235.06])
        self.data = Coincidence_events(10,block1,block2,crystal1,crystal2,energy1,energy2)

    def test_filter(self):
        energy_window = np.array([350,650])
        events = self.data.filter_with_energy_window(energy_window)
        assert all_close(events.block1,np.array([1,12])) 
        assert all_close(events.crystal1,np.array([82,28]))
        assert all_close(events.block2,np.array([8,1])) 
        assert all_close(events.crystal2,np.array([58,42]))

    def test_get_coordinate(self):
        config = {
            "ring": {
                "inner_radius": 99.0,
                "outer_radius": 119.0,
                "axial_length": 33.4,
                "nb_rings": 1,
                "nb_blocks_per_ring": 16,
                "gap": 0.0
            },
            "block": {
                "grid": [
                    1,
                    10,
                    10
                ],
                "size": [
                    20.0,
                    33.4,
                    33.4
                ],
                "interval": [
                    0.0,
                    0.0,
                    0.0
                ]
            }
        }
        scanner = get_scanner(config)
        coordinate = self.data.filter_with_energy_window(np.array([350,650])).get_coordinate(scanner)
        comprison = np.array([[96.22929972,52.51264586,-8.35,-109,-1.67,11.69],[-8.35,-109,11.69,101.34195038,40.16961531,-8.35]])
        assert all_close(coordinate,comprison)