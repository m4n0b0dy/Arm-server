from os import getenv
#fetch these from dockerfile
OUTPUT_DIR  = getenv('OUTPUT_DIR','output/')
ARM_SERVER_IP = getenv('ARM_IP','localhost')
ARM_SERVER_PORT = getenv('ARM_PORT','5005')
HAND = getenv('HAND','right')
#the indexes of BODY_25 that are relevant
KEY_BODY_INDEXES = {'shoulder':2,'elbow':3,'wrist':4}
#for now only using key indexes of the openpose models, later can average or something
#the indexes of hand that are relevant
KEY_HAND_INDEXES = {'thumb':4,'pointer':8,'middle':12,'ring':16,'pinky':20}