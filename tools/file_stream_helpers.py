import os.path
import os
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

        self.logs = []
        self.IP = IP
        self.PORT = PORT
        pyinotify.ProcessEvent.__init__(self)
        wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(wm, self)
        wdd = wm.add_watch(watchdir, pyinotify.IN_CREATE)
        self.notifier.start()

    def send_commands(self, command_json):
        #api_res = requests.post('http://{IP}:{PORT}'.format(IP=self.IP, PORT=self.PORT), json=command_json)
        #self.logs.append(api_res)
        print(command_json)

    def process_IN_CREATE(self, event):
        pathname = os.path.join(event.path, event.name)
        raw_data = load_json(pathname)
        #delete the file to save storage
        os.remove(pathname)
        if raw_data:
            data = reduce_data(raw_data)
            data = convert_data(data)
            self.send_commands(data)

    def get_logs(self):
        return self.logs

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
#UPDATE now going only from hand
def reduce_data(data):
    data = data['people'][0]
    #all_body_data = divide_chunks(data['pose_keypoints_2d'], 3)
    #body_data = {k:list(all_body_data[v]) for k,v in config.KEY_BODY_INDEXES.items()}

    all_hand_data = divide_chunks(data['hand_{HAND}_keypoints_2d'.format(HAND=config.HAND)], 3)
    hand_data = {k:np.array(all_hand_data[v]) for k,v in config.KEY_HAND_INDEXES.items()}

    #return {'body_data':body_data, 'hand_data':hand_data}
    return hand_data

def convert_data(hand_data):
    shoulder_rot_pos, shoulder_bend_pos, elbow_pos, wrist_bend_pos = IK_SOLVER.calc_arm_positions(hand_data['WRIST'])
    wrist_rot_pos = IK_SOLVER.calc_wrist_rotation(hand_data['POINTER_BASE'],hand_data['PINKY_BASE'])
    thumb_pos = IK_SOLVER.calc_fingers(hand_data['THUMB_TIP'], hand_data['THUMB_BASE'])
    pointer_pos = IK_SOLVER.calc_fingers(hand_data['POINTER_TIP'], hand_data['POINTER_BASE'])
    middle_pos = IK_SOLVER.calc_fingers(hand_data['MIDDLE_TIP'], hand_data['MIDDLE_BASE'])
    ring_pos = IK_SOLVER.calc_fingers(hand_data['RING_TIP'], hand_data['RING_BASE'])
    pinky_pos = IK_SOLVER.calc_fingers(hand_data['PINKY_TIP'], hand_data['PINKY_BASE'])
    return {'SHOULDER_ROTATE':shoulder_rot_pos,
            'SHOULDER_BEND':shoulder_bend_pos,
            'ELBOW':elbow_pos,
            'WRIST_BEND':wrist_bend_pos,
            'WRIST_ROTATE':wrist_rot_pos,
            'THUMB':thumb_pos,
            'POINTER':pointer_pos,
            'MIDDLE':middle_pos,
            'RING':ring_pos,
            'PINKY':pinky_pos}