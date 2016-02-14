'''
this python script must receive udp packets with audio data and play them
'''

from pysoundcard import OutputStream, continue_flag
import time
from Queue import Queue
import threading
import traceback
import numpy

import socket
port = 7485
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', port))

last_timestamp = 0

def get_timestamp(data):
    timestamp = 0
    for i in range(4):
        timestamp += ord(data[i]) * (256**i)
    return timestamp

def forever_receive_from_udp():
    while True:
        try:
            data, addr = sock.recvfrom(1000)
            # do some stuff with data maybe before sticking it into playback_queue
            #timestamp = get_timestamp(data)
            #playback_queue.put(numpy.fromstring(data[4:]))
            playback_stream.write(numpy.fromstring(data))
        except:
            traceback.print_exc()

t = threading.Thread(target = forever_receive_from_udp)
t.setDaemon(True)
t.start()

playback_stream = OutputStream(samplerate=16000, blocksize=1024, dtype='int32', channels=1)
playback_stream.start()
playback_queue = Queue()

def forever_write_to_output():
    while True:
        try:
            playback_stream.write(playback_queue.get())
        except:
            traceback.print_exc()

#threading.Thread(target = forever_write_to_output).start()

# now write something which receives udp packets and sticks
# them into the playback queue

while True:
    try:
        time.sleep(1)
    except:
        break
        
playback_stream.stop()
