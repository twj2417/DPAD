#from ..correction.actual2theroy import Single
from srfnef import PetEcatScanner
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

    def filter_with_energy_window(self,energy_window):
        index = np.where((self.energy1>energy_window[0])&(self.energy1<energy_window[1])&
                        (self.energy2>energy_window[0])&(self.energy2<energy_window[1]))[0]
        block1 = self.block1[index]
        crystal1 = self.crystal1[index]
        block2 = self.block2[index]
        crystal2 = self.crystal2[index]
        return Coincidence_events(self.time,block1,block2,crystal1,crystal2)

    def get_coordinate(self,scanner:PetEcatScanner):
        crystal_size = np.array(scanner.blocks.size)/np.array(scanner.blocks.shape)
        radius = (scanner.inner_radius+scanner.outer_radius)/2
        block_angle1 = self.block1/scanner.nb_blocks_per_ring*2*np.pi
        block_angle2 = self.block2/scanner.nb_blocks_per_ring*2*np.pi
        distance1 = (np.floor(self.crystal1/scanner.blocks.shape[2])-(scanner.blocks.shape[1]-1)/2)*crystal_size[1]
        distance2 = (np.floor(self.crystal2/scanner.blocks.shape[2])-(scanner.blocks.shape[1]-1)/2)*crystal_size[1]
        x1 = (radius*np.cos(block_angle1)+ distance1*np.cos(block_angle1+np.pi/2)).reshape(-1,1)
        x2 = (radius*np.cos(block_angle2)+ distance2*np.cos(block_angle2+np.pi/2)).reshape(-1,1)
        y1 = (radius*np.sin(block_angle1)+ distance1*np.sin(block_angle1+np.pi/2)).reshape(-1,1)
        y2 = (radius*np.sin(block_angle2)+ distance2*np.sin(block_angle2+np.pi/2)).reshape(-1,1)
        z1 = ((np.mod(self.crystal1,scanner.blocks.shape[2])-(scanner.blocks.shape[2]-1)/2)*crystal_size[2]).reshape(-1,1)
        z2 = ((np.mod(self.crystal2,scanner.blocks.shape[2])-(scanner.blocks.shape[2]-1)/2)*crystal_size[2]).reshape(-1,1)
        coordinate1 = np.hstack((np.hstack((x1,y1)),z1))
        coordinate2 = np.hstack((np.hstack((x2,y2)),z2))
        # coordinate1 = index2pos(self.block1,self.crystal1,scanner)
        # coordinate2 = index2pos(self.block2,self.crystal2,scanner)
        # coordinate1 = (self.block1*scanner.nb_crystals_per_block + self.crystal1).reshape(-1,1)
        # coordinate2 = (self.block2*scanner.nb_crystals_per_block + self.crystal2).reshape(-1,1)
        return np.hstack((coordinate1,coordinate2))


def index2pos(blockid,crystalid,scanner):
    iy = crystalid//scanner.blocks.shape[2]
    iz = crystalid%scanner.blocks.shape[2]
    pos = np.zeros((iy.size, 3), dtype = np.float32)
    x0 = scanner.average_radius
    y0 = (iy + 0.5) * scanner.blocks.unit_size[1] - scanner.blocks.size[1] / 2
    theta = scanner.angle_per_block * blockid
    pos[:,0] = x0 * np.cos(theta) - y0 * np.sin(theta)
    pos[:,1] = x0 * np.sin(theta) + y0 * np.cos(theta)
    pos[:,2] = (iz+0.5) * scanner.blocks.unit_size[2] - scanner.axial_length / 2
    return pos
      