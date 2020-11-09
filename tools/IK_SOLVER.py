import tinyik
import numpy as np
from configs import config


ARM = tinyik.Actuator(config.ARM_STRUCTURE)

#get 3d coordinates and return normalized arm servo angles
def calc_arm_positions(coordinates):
	ARM.ee = coordinates
	return np.deg2rad(ARM.angles)%360/360

#get 2 coordinates and normalize them between 0-1
def normalize_points(point1, point2):
	maxs = np.maximum(point1, point2)
	return point1/maxs, point2/maxs

#calculate wrist servo angle by vector from pinky palm to point palm
def calc_wrist_rotation(pinky_palm, point_palm):
	pinky_palm, point_palm = normalize_points(pinky_palm, point_palm)
	euc_2d = np.linalg.norm(pinky_palm[:2]-point_palm[:2])
	z_direction = np.argmax([pinky_palm[2], point_palm[2]])
	z_direction = z_direction if z_direction == 1 else -1
	vec_mag = (1+euc_2d*z_direction)/2
	return vec_mag

#calculate a finger position from tip and base points
def calc_fingers(tip, base):
	tip, base = normalize_points(tip, base)
	return np.abs(np.linalg.norm(tip-base))