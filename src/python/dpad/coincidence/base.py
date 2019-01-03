#from ..correction.actual2theroy import Single
from srf.data import PETCylindricalScanner
import numpy as np

class Coincidence_events:
    def __init__(self,time,block1,block2,crystal1,crystal2,energy1=None,energy2=None):
        self.time = time
        self.block1 = block1
        self.crystal1 = crystal1
        self.energy1 = energy1
        self.block2 = block2
        self.crystal2 = crystal2
        self.energy2 = energy2

    def filter_with_energy_window(self,time_window):
        index = np.where((self.energy1>time_window[0])&(self.energy1<time_window[1])&
                        (self.energy2>time_window[0])&(self.energy2<time_window[1]))[0]
        block1 = self.block1[index]
        crystal1 = self.crystal1[index]
        block2 = self.block2[index]
        crystal2 = self.crystal2[index]
        return Coincidence_events(self.time,block1,block2,crystal1,crystal2)

    def get_coordinate(self,scanner:PETCylindricalScanner):
        crystal_size = np.array(scanner.blocks[0].size)/np.array(scanner.blocks[0].grid)
        radius = (scanner.inner_radius+scanner.outer_radius)/2
        block_angle1 = self.block1/scanner.nb_blocks_per_ring*2*np.pi
        block_angle2 = self.block2/scanner.nb_blocks_per_ring*2*np.pi
        distance1 = (np.floor(self.crystal1/scanner.blocks[0].grid[2])-(scanner.blocks[0].grid[1]-1)/2)*crystal_size[1]
        distance2 = (np.floor(self.crystal2/scanner.blocks[0].grid[2])-(scanner.blocks[0].grid[1]-1)/2)*crystal_size[1]
        x1 = (radius*np.cos(block_angle1)+ distance1*np.cos(block_angle1+np.pi/2)).reshape(-1,1)
        x2 = (radius*np.cos(block_angle2)+ distance2*np.cos(block_angle2+np.pi/2)).reshape(-1,1)
        y1 = (radius*np.sin(block_angle1)+ distance1*np.sin(block_angle1+np.pi/2)).reshape(-1,1)
        y2 = (radius*np.sin(block_angle2)+ distance2*np.sin(block_angle2+np.pi/2)).reshape(-1,1)
        z1 = ((np.mod(self.crystal1,scanner.blocks[0].grid[2])-(scanner.blocks[0].grid[2]-1)/2)*crystal_size[2]).reshape(-1,1)
        z2 = ((np.mod(self.crystal2,scanner.blocks[0].grid[2])-(scanner.blocks[0].grid[2]-1)/2)*crystal_size[2]).reshape(-1,1)
        coordinate1 = np.hstack((np.hstack((x1,y1)),z1))
        coordinate2 = np.hstack((np.hstack((x2,y2)),z2))
        return np.hstack((coordinate1,coordinate2))


    