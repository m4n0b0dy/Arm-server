import tinyik
import numpy as np
from configs.config import *

arm = tinyik.Actuator(['y', [0.0, .2, 0.],
                       'z', [0.0, 1.0, 0.],
                       'z', [0.0, .9, 0.],
                      'z', [0.0, .6, 0.],
                      'y', [0.0, .5, 0.]])
                      
                      
"""for i in range(1,4):
    for j in range(1,4):
        for k in range(1,4):
            tar = [i,j,k]
            arm.ee = tar
            tinyik.visualize(arm)
            print(np.rad2deg(arm.angles))"""
