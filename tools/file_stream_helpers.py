import os.path
import pyinotify
import json
import requests
import configs.config
import os
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
def reduce_data(data):
    data = data['people'][0]
    all_body_data = divide_chunks(data['pose_keypoints_2d'], 3)
    body_data = {k:list(all_body_data[v]) for k,v in config.KEY_BODY_INDEXES.items()}

    all_hand_data = divide_chunks(data['hand_{HAND}_keypoints_2d'.format(HAND=config.HAND)], 3)
    hand_data = {k:list(all_hand_data[v]) for k,v in config.KEY_HAND_INDEXES.items()}

    return {'body_data':body_data, 'hand_data':hand_data}
