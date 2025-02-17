import psutil, time

def netmon(queue):
    while True:
        net_io = psutil.net_io_counters()
        """feature: add loglevel to pass for each worker to print on remote machine"""
#        print(f"Bytes Sent: {net_io.bytes_sent}, Bytes Received: {net_io.bytes_recv}")
        queue.put(net_io)
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            try:
                queue.put(f"Local Address: {conn.laddr.ip}:{conn.laddr.port}, Remote Address: {conn.raddr.ip}:{conn.raddr.port}, Status: {conn.status}")   
            except AttributeError as AE:
                queue.put((f"Local Address: {conn.laddr}:{conn.laddr}, Remote Address: {conn.raddr}:{conn.raddr}, Status: {conn.status}"))   
        time.sleep(5)

#def conmon(queue):
#    while True:
#        connections = psutil.net_connections(kind='inet')
#        for conn in connections:
#            print(f"Local Address: {conn.laddr} -> Remote Address: {conn.raddr} | Status: {conn.status}")    
#            queue.put(f"Local Address: {conn.laddr} -> Remote Address: {conn.raddr} | Status: {conn.status}")
#        time.sleep(5)