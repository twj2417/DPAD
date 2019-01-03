from dpad.correction.actual2theory import Module_data,Single_event
import unittest
import pytest
import numpy as np
from doufo.tensor.tensor import all_close

class Test_single_event(unittest.TestCase):
    def setUp(self):
        time = np.array([10422958,10423383,10423758,10424489,10426423,10427495,10427465,
                        10429860,6878008,6882499,6882499,8082068,8084519,8084519,
                        8084830,8088913,8088913,8089688,8090193,8597195])

        energy = np.array([443,277,546,517,218,529,167,228,489,278,322,521,370,176,619,404,324,352,198,286])
        blockid = np.array([0,0,0,0,0,0,0,0,1,1,1,2,2,2,2,2,2,2,2,3])
        crystalid = np.array([35,21,24,11,14,78,92,67,99,64,83,74,70,79,73,19,47,42,23,60])
        self.data = Single_event(time,energy,blockid,crystalid)

    def test_sort_time(self):
        time = np.array([6878008,6882499,6882499,8082068,8084519,8084519,8084830,8088913,
                        8088913,8089688,8090193,8597195,10422958,10423383,10423758,10424489,
                        10426423,10427465,10427495,10429860])
        energy = np.array([489,278,322,521,176,370,619,324,404,352,198,286,443,277,546,517,218,167,529,228])
        blockid = np.array([1,1,1,2,2,2,2,2,2,2,2,3,0,0,0,0,0,0,0,0])
        crystalid = np.array([99,64,83,74,79,70,73,47,19,42,23,60,35,21,24,11,14,92,78,67])
        assert all_close(self.data.sort_by_time().time,time)
        assert all_close(self.data.sort_by_time().energy,energy)
        assert all_close(self.data.sort_by_time().blockid,blockid)
        assert all_close(self.data.sort_by_time().crystalid,crystalid)

    def test_update_time(self):
        time = np.array([6878008,6882499,6882499,8082068,8084519,8084519,8084830,8088913,
                        8088913,8089688,8090193,8597195,10422958,10423383,10423758,10424489,
                        10426423,10427465,10427495,10429860])
        event = self.data.update_time(time)
        assert all_close(event.time,time)

    def test_update_energy(self):
        energy = np.array([489,278,322,521,176,370,619,324,404,352,198,286,443,277,546,517,218,167,529,228])
        event = self.data.update_energy(energy)
        assert all_close(event.energy,energy)

    # def test_smooth(self):
    #     new_data = self.data.smooth_event_time()
    #     assert all_close(new_data)



class Test_module_data(unittest.TestCase):
    def setUp(self):
        data = np.array([[187,1,34,142],
                        [174,10,159,143],
                        [21,1,20,142],
                        [87,12,159,143],
                        [34,2,23,142],
                        [206,13,159,143],
                        [5,2,10,142],
                        [169,16,159,143],
                        [218,0,13,142],
                        [55,24,159,143],
                        [17,2,77,142],
                        [103,28,159,143],
                        [167,0,91,142],
                        [73,28,159,143],
                        [228,0,66,142],
                        [164,37,159,143]])
        self.data = Module_data(0,data)

    def test_time(self):
        time = np.array([10422958,10423383,10423758,10424489,10426423,10427495,10427465,10429860])
        assert all_close(self.data.time,time)

    def test_energy(self):
        energy = np.array([443,277,546,517,218,529,167,228])
        assert all_close(self.data.energy,energy)

    def test_channelid(self):
        channel_id = np.array([34,20,23,10,13,77,91,66])
        assert all_close(self.data.channel_id,channel_id)

    def test_num_events(self):
        assert self.data.num_events == 8

    def test_reshaped_data(self):
        data = np.array([[187,1,34,142,174,10,159,143],
                        [21,1,20,142,87,12,159,143],
                        [34,2,23,142,206,13,159,143],
                        [5,2,10,142,169,16,159,143],
                        [218,0,13,142,55,24,159,143],
                        [17,2,77,142,103,28,159,143],
                        [167,0,91,142,73,28,159,143],
                        [228,0,66,142,164,37,159,143]])
        assert all_close(self.data.reshaped_data,data)

    def test_update_moduleid(self):
        result = self.data.update_module_id(5)
        assert result.module_id == 5

    def test_update_crystalid(self):
        relation = np.arange(1,101)
        result = 100-np.array([35,21,24,11,14,78,92,67])
        assert all_close(self.data.update_crystal_id(relation).channel_id,result)

    def test_effective_data(self):
        self.data = Module_data(0,np.array([[174,10,159,143],
                        [21,1,20,142],
                        [87,12,159,143],
                        [34,2,23,142],
                        [5,2,10,142],
                        [169,16,159,143],
                        [218,0,13,142],
                        [55,24,159,143],
                        [103,28,159,143],
                        [167,0,91,142],
                        [73,28,159,143],
                        [228,0,66,142],
                        [164,37,159,143]]))
        result = np.array([[21,1,20,142],
                        [87,12,159,143],
                        [5,2,10,142],
                        [169,16,159,143],
                        [218,0,13,142],
                        [55,24,159,143],
                        [167,0,91,142],
                        [73,28,159,143],
                        [228,0,66,142],
                        [164,37,159,143]])
        assert all_close(self.data.extract_effective_data().data,result)


