'''
this python script must send udp packets from the mic with audio data
'''

from pysoundcard import InputStream, continue_flag
import time
from Queue import Queue
import pdb
import traceback
import threading

import socket
port = 7485
host = 'localhost'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_queue = Queue()

def get_timestamp_str(timestamp):
    timestamp_str = ''
    for i in range(4):
        timestamp_str += chr(timestamp % 256)
        timestamp = timestamp / 256
    return timestamp_str

def forever_send_udp_queue():
    timestamp = 0
    while True:
        try:
            data = udp_queue.get()
            timestamp += 1
            #timestamp_str = get_timestamp_str(timestamp)
            #msg = timestamp_str + data.tostring()
            #sock.sendto(msg, (host, port))
            #sock.sendto(data.tostring(), (host,port))
        except:
            traceback.print_exc()

#threading.Thread(target = forever_send_udp_queue).start()

def callback(in_data, time_info, status):
    #udp_queue.put(in_data)
    sock.sendto((in_data).tostring(), (host, port))
    return continue_flag

record_stream = InputStream(samplerate=16000, blocksize=1024, dtype='int32', channels=1, callback=callback)
record_stream.start()

# now write something which takes stuff from the udp queue and sends it over
# the network

while True:
    try:
        time.sleep(1)
    except:
        break

record_stream.stop()

