import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReadyDirHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory and event.src_path.lower().endswith('ready'):
            print(f"Detected a new 'ready' subdirectory: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory and event.dest_path.lower().endswith('ready'):
            print(f"Detected a moved 'ready' subdirectory: {event.dest_path}")

def monitor_directory(path):
    event_handler = ReadyDirHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_to_monitor = r'D:\AGI IMPORTS'
    
    monitor_directory(directory_to_monitor)