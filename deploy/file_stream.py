from watch import FileWatcher
import config

watcher = FileWatcher(
	config.OUTPUT_DIR,
	config.ARM_SERVER_IP,
	config.ARM_SERVER_PORT)
print('Watcher loaded')