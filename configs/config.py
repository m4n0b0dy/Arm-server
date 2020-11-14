from os import getenv
#fetch these from dockerfile
OUTPUT_DIR  = getenv('OUTPUT_DIR','../output/')
ARM_SERVER_IP = getenv('ARM_IP','arm')
ARM_SERVER_PORT = getenv('ARM_PORT','5005')
HAND = getenv('HAND','right')
#HAND='left'
#the indexes of BODY_25 that are relevant
#KEY_BODY_INDEXES = {'shoulder':2,'elbow':3,'wrist':4}
#for now only using key indexes of the openpose models, later can average or something
#the indexes of hand that are relevant
KEY_HAND_INDEXES = {
'THUMB_TIP':4,
'THUMB_BASE':5,
'POINTER_TIP':8,
'POINTER_BASE':5,
'MIDDLE_TIP':12,
'MIDDLE_BASE':9,
'RING_TIP':16,
'RING_BASE':13,
'PINKY_TIP':20,
'PINKY_BASE':17,
'WRIST':0
}


HAND_NORM = {
'THUMB':(.3,.3),
'POINTER':(.1,.4),
'MIDDLE':(.15,.4),
'RING':(.15,.4),
'PINKY':(.15,.3)
}


ARM_STRUCTURE = ['y', [0.0, .074, 0.],
'z', [0.0, .37, 0.],
'z', [0.0, .33, 0.],
'z', [0.0, .22, 0.]]
