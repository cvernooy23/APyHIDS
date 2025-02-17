import random, time, multiprocessing, yaml, logging
from utils.network import netmon
from utils.filemonitor import watcher
from pathlib import Path

SENTINEL = None  # Define a constant for the sentinel value

def load_settings(config_file):
    """Loads settings from a YAML file."""
    try:
        with config_file.open('r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"File not found at {config_file}.")
        exit(2)
    
def network_worker(queue):
    """Monitors network utilization at regular intervals."""
    processes = []
    process = multiprocessing.Process(target=netmon, args=(queue,))
    process.start()
    processes.append(process)
    return processes

def filewatcher_worker(queue, paths):
    """Monitors file creation, modification, and deletion in specified directories or flat files using watchdog observer."""
    processes = []
    process = multiprocessing.Process(target=watcher, args=(queue,paths,))
    process.start()
    processes.append(process)
    return processes

def consumer(queue,monitor_num):
    """Starts a single consumer to read messages off the queue"""
    active_workers = monitor_num # Number of producers expected
    while active_workers > 0:
        item = queue.get()
        if item is None:  # Sentinel value received
            active_workers-= 1
            print("Consumer: Producer has died.")
        else:
            print(f"Consumer: Retrieved {item}")
        time.sleep(1)

def start_execution(output_file):
    log_level = 'INFO'
    config_file=Path(__file__).with_name('config.yml')
    all_started_procs = []
    settings = load_settings(config_file)
    monitor_list = settings['monitors']
    for monitor in monitor_list:
        if "network" in monitor:
            print("Network Metrics:", monitor["network"].get("metrics", []))
        if "file_watcher" in monitor:
            print("File Watcher Paths:", monitor["file_watcher"].get("paths", []))
            filewatcher_paths = monitor["file_watcher"].get("paths", [])
            print(type(filewatcher_paths))
    monitor_num = len(monitor_list)
    if log_level == 'DEBUG':
        print(monitor_num)
    """Runs multiple workers and a single consumer."""
    queue = multiprocessing.Queue()
    net_procs = network_worker(queue)
    file_procs = filewatcher_worker(queue, filewatcher_paths)
    print(net_procs)
    print(file_procs)

    consumer_process = multiprocessing.Process(target=consumer, args=(queue,monitor_num,))
    consumer_process.start()

if __name__ == "__main__":
    output_filename = "results.txt"
    start_execution(output_filename)
