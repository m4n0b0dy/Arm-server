import tinyik
import numpy as np
import importlib
import sys
sys.path.insert(0, '../configs/')
import config

import math

def sigmoid(x):
	return 1 / (1 + math.exp(-x))

ARM = tinyik.Actuator(config.ARM_STRUCTURE)

#get 3d coordinates and return normalized arm servo angles
def calc_arm_positions(coordinates):
	coordinates[1] = coordinates[1]*-1
	ARM.ee = coordinates
	coordinates = coordinates+.5
#	print(coordinates[0])
	return [.5,.5,.5,coordinates[0]]
#print(ARM.ee)
#	res= ((np.rad2deg(ARM.angles)+180)%360)/360
	#print(res)
#	return [.5,.5,.5,.5]
#	return res

#get 2 coordinates and normalize them between 0-1
def normalize_points(point1, point2):
	maxs = np.maximum(point1, point2)
#	mins = np.minimum(point1, point2)
#	point1 = point1
	return point1/maxs, point2/maxs

def normalized_vector(point1, point2):
	vec = float(sum(np.abs(point1-point2)))
#	print(vec,point1,point2)
#	vec = vec/sum(vec)
	return vec


#calculate wrist servo angle by vector from pinky palm to point palm
def calc_wrist_rotation(pinky_palm, point_palm):
	pinky_z, point_z = pinky_palm[-1], point_palm[-1]
	z_euc = np.linalg.norm(pinky_z-point_z)
	if z_euc <= .05:
#		print(.5)
		return .5
#	if pinky_z/point_z <= .2:
#		print(.5)
#		return .5
#	pinky_palm, point_palm = normalize_points(pinky_palm, point_palm)
	euc_2d = np.linalg.norm(pinky_palm[:2]-point_palm[:2])
#	euc_2d*=.5
#	print(euc_2d)
	z_direction = np.argmax([pinky_z, point_z])
	z_direction = (z_direction if z_direction == 1 else -1)
#	vec_mag = sigmoid(euc_2d) # + z_direction*euc_2d*.5
	vec_mag = .5+euc_2d*z_direction
#	print(vec_mag, z_euc)
#	print((5/euc_2d)*z_direction)
#	print(euc_2d, vec_mag)
#	vec_mag = 1/(euc_2d*z_direction)
#	print(pinky_palm, point_palm, z_direction)
#	print(vec_mag*1.5)
	return vec_mag*1.5


def normalized(d, mn, mx):
	return min(1,max(0,(d - mn) / (mx - d)))

#calculate a finger position from tip and base points
def calc_fingers(tip, base, norm):
#	tip=tip[:2]
#	base=base[:2]
#	tip, base = normalize_points(tip, base)
	#trying a new way of normalizing
	#this number is totally dependent on how far from your camera smh
	dist = np.abs(np.linalg.norm(tip-base))
	norm_dist = normalized(dist, *norm)
#	print(norm_dist, dist)
#	dist = live_normalization(tip,base)
#	print(dist, tip, base, GLOBAL_MAX)
	return norm_dist
#	return normalized_vector(tip, base)

#calculate a finger position from tip and base points
def calc_fingers(tip, base, norm):
#       tip=tip[:2]
#       base=base[:2]
#       tip, base = normalize_points(tip, base)
        #trying a new way of normalizing
        #this number is totally dependent on how far from your camera smh
        dist = np.abs(np.linalg.norm(tip-base))/100
#        norm_dist = normalized(dist, *norm)
#        print(norm_dist, dist)
#       dist = live_normalization(tip,base)
#       print(dist, tip, base, GLOBAL_MAX)
        return dist
#       return normalized_vector(tip, base)

