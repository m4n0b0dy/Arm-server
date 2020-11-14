import math
import os.path
import os
import glob
import pyinotify
import json
import requests
import sys
sys.path.insert(0, '../configs/')
import config
import numpy as np
import IK_SOLVER

class FileWatcher(pyinotify.ProcessEvent):
    def __init__(self, watchdir, IP, PORT):
        #remove all files in watchdir to save space
        files = glob.glob(watchdir+'*')
        for f in files:
                os.remove(f)
        self.logs = []
        self.IP = IP
        self.PORT = PORT
        pyinotify.ProcessEvent.__init__(self)
        wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(wm, self)
        wdd = wm.add_watch(watchdir, pyinotify.IN_CREATE)
        self.notifier.start()

    def send_commands(self, command_json):
        api_res = requests.post('http://{IP}:{PORT}'.format(IP=self.IP, PORT=self.PORT), json=command_json)
        #self.logs.append(api_res)
        #print(command_json)

    def process_IN_CREATE(self, event):
        pathname = os.path.join(event.path, event.name)
        raw_data = load_json(pathname)
        #delete the file to save storage
        os.remove(pathname)
        if raw_data:
            data = reduce_data(raw_data)
            data = convert_data(data)
            data = clean_data(data)
            self.send_commands(data)

def load_json(path):
    try:
        #going to try one after the other
        with open(path, 'r', encoding="utf-8") as f:
            return json.load(f)
        #if above doesn't work can use a bytes open
        with open(path, 'r', encoding="utf-8") as f:
            return json.loads(f.read())
    except:
        pass

def divide_chunks(l, n): 
    return list(zip(*[iter(l)]*n))

#very specialized function to extract the x,y,z coordinates I want
def reduce_data(data):
    if not data['people']:
        return
    data = data['people'][0]
    all_hand_data = divide_chunks(data['hand_{HAND}_keypoints_2d'.format(HAND=config.HAND)], 3)
    hand_data = {k:np.array(all_hand_data[v]) for k,v in config.KEY_HAND_INDEXES.items()}
    return hand_data

def convert_data(hand_data):
    shoulder_rot_pos, shoulder_bend_pos, elbow_pos, wrist_bend_pos = IK_SOLVER.calc_arm_positions(hand_data['WRIST'])
    wrist_rot_pos = IK_SOLVER.calc_wrist_rotation(hand_data['POINTER_BASE'],hand_data['PINKY_BASE'])
    thumb_pos = IK_SOLVER.calc_fingers(hand_data['THUMB_TIP'], hand_data['THUMB_BASE'], config.HAND_NORM['THUMB'])
    pointer_pos = IK_SOLVER.calc_fingers(hand_data['POINTER_TIP'], hand_data['POINTER_BASE'],config.HAND_NORM['POINTER'])
    middle_pos = IK_SOLVER.calc_fingers(hand_data['MIDDLE_TIP'], hand_data['MIDDLE_BASE'],config.HAND_NORM['MIDDLE'])
    ring_pos = IK_SOLVER.calc_fingers(hand_data['RING_TIP'], hand_data['RING_BASE'],config.HAND_NORM['RING'])
    pinky_pos = IK_SOLVER.calc_fingers(hand_data['PINKY_TIP'], hand_data['PINKY_BASE'],config.HAND_NORM['PINKY'])
    return {'SHOULDER_ROTATE':shoulder_rot_pos,
            'SHOULDER_BEND':shoulder_bend_pos,
            'ELBOW':elbow_pos,
            'WRIST_BEND':wrist_bend_pos,
            'WRIST_ROTATE':wrist_rot_pos, #not great needs more work
            'THUMB':thumb_pos,
            'INDEX':pointer_pos,
            'MIDDLE':middle_pos,
            'RING':ring_pos,
            'PINKY':pinky_pos
}

def clean_data(hand_data):
     ret_dic={}
     for k, v in hand_data.items():
          if not math.isnan(v) and v !=0:
               ret_dic[k]=v
     return ret_dic
