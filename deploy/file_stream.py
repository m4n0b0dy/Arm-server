import sys
sys.path.insert(0, '../configs/')
import config
sys.path.insert(0, '../tools/')
from file_stream_helpers import FileWatcher

watcher = FileWatcher(
	config.OUTPUT_DIR,
	config.ARM_SERVER_IP,
	config.ARM_SERVER_PORT)
print('Watcher loaded')