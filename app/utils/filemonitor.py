import time, os, queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    """Handles file system events and adds them to a queue."""
    def __init__(self, event_queue):
        self.event_queue = event_queue

    def on_modified(self, event):
        """feature: add loglevel to pass for each worker to print on remote machine"""
#        print(f"Modified: {event.src_path}")
        self.event_queue.put(("modified", event.src_path))

    def on_created(self, event):
        """feature: add loglevel to pass for each worker to print on remote machine"""
#        print(f"Created: {event.src_path}")
        self.event_queue.put(("created", event.src_path))

    def on_deleted(self, event):
        """feature: add loglevel to pass for each worker to print on remote machine"""
#        print(f"DELETED: {event.src_path}")        
        self.event_queue.put(("deleted", event.src_path))

def watcher(event_queue, paths):  
    event_handler = FileChangeHandler(event_queue)
    observer = Observer()
    for path in paths:
        if os.path.isdir(path):
            observer.schedule(event_handler, path, recursive=True)
        else:
            observer.schedule(event_handler, path)
        print(f"Watching: {path}") 
    observer.start()
    try:
        while True:
            if not observer.is_alive():
                observer.start()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("Watchdog Stopped watching, WOOF.")
    