import psutil, time

def netmon(queue):
    while True:
        net_io = psutil.net_io_counters()
        """feature: add loglevel to pass for each worker to print on remote machine"""
#        print(f"Bytes Sent: {net_io.bytes_sent}, Bytes Received: {net_io.bytes_recv}")
        queue.put(net_io)
        time.sleep(5)

