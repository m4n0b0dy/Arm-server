import tinyik
import numpy as np
import importlib
import sys
sys.path.insert(0, '../configs/')
import config

ARM = tinyik.Actuator(config.ARM_STRUCTURE)

#the active functions worked for demo purposes but are not ready for full arm movement
#get 3d coordinates and return normalized arm servo angles
def calc_arm_positions(coordinates):
	coordinates[1] = coordinates[1]*-1
	ARM.ee = coordinates
	coordinates = coordinates+.5
	return [.5,.5,.5,coordinates[0]]

#calculate wrist servo angle by vector from pinky palm to point palm
def calc_wrist_rotation(pinky_palm, point_palm):
	pinky_z, point_z = pinky_palm[-1], point_palm[-1]
	z_euc = np.linalg.norm(pinky_z-point_z)
	if z_euc <= .05:
		return .5
	euc_2d = np.linalg.norm(pinky_palm[:2]-point_palm[:2])
	z_direction = np.argmax([pinky_z, point_z])
	z_direction = (z_direction if z_direction == 1 else -1)
	vec_mag = .5+euc_2d*z_direction
	return vec_mag*1.5

#calculate a finger position from tip and base points
def calc_fingers(tip, base, norm):
        dist = np.abs(np.linalg.norm(tip-base))/100
        return dist
"""
# these are equations I thought would work but have not so far
def calc_arm_positions(coordinates):
	coordinates[1] = coordinates[1]*-1
	ARM.ee = coordinates
	coordinates = coordinates+.5
	return np.deg2rad(ARM.angles)%360/360

def normalized(d, mn, mx):
	return min(1,max(0,(d - mn) / (mx - d)))

#calculate wrist servo angle by vector from pinky palm to point palm
def calc_wrist_rotation(pinky_palm, point_palm):
	euc_2d = np.linalg.norm(pinky_palm[:2]-point_palm[:2])
	z_direction = np.argmax([pinky_palm[2], point_palm[2]])
	z_direction = z_direction if z_direction == 1 else -1
	vec_mag = .5+euc_2d*z_direction
	return vec_mag

#calculate a finger position from tip and base points
def calc_fingers(tip, base):
	dist = np.abs(np.linalg.norm(tip-base))
	norm_dist = normalized(dist, *norm)
  return norm_dist
 """
