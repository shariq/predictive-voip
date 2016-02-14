'''
this python script must receive udp packets with audio data and play them
'''

from pysoundcard import OutputStream, continue_flag
import time
from Queue import Queue
import threading
import traceback
import numpy
from collections import deque
import random

#from at2 import predict_slice

def predict_slice(x):
    return random.choice(x)

BUFFER = numpy.zeros((32000, 800), 'int32')
HAVE_BUFFER = [False] * 32000

import socket
port = 7485
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', port))

dtype = 'int32'

def play_every_tenth():
    time.sleep(0.3)
    last_time = time.time()
    timestamp = 0
    while True:
        time.sleep(0.1 - (time.time()*10 - int(time.time() * 10))/10.)
        if timestamp < 17:
            if HAVE_BUFFER[timestamp]:
                playback_queue.put(BUFFER[timestamp, :])
        else:
            if HAVE_BUFFER[timestamp]:
                playback_queue.put(BUFFER[timestamp, :])
            else:
                predicted = predict_slice(BUFFER[timestamp-15:timestamp+1, :])
                playback_queue.put(predicted)
        timestamp += 1
        

GOT_BEFORE = False
def got_packet():
    if not globals()['GOT_BEFORE']:
        t = threading.Thread(target = play_every_tenth)
        t.setDaemon(True)
        t.start()
    globals()['GOT_BEFORE'] = True

def get_timestamp(data):
    timestamp = 0
    for i in range(4):
        timestamp += ord(data[i]) * (256**i)
    print timestamp
    return timestamp

currently_playing_timestamp = 0

def forever_receive_from_udp():
    while True:
        try:
            data, addr = sock.recvfrom(7500)
            got_packet()
            # do some stuff with data maybe before sticking it into playback_queue
            timestamp = get_timestamp(data)
            frame = numpy.fromstring(data[4:], dtype = dtype)
            BUFFER[timestamp, :] = frame
            HAVE_BUFFER[timestamp] = True
            print 'got frame of len ', len(data)
        except:
            traceback.print_exc()

t = threading.Thread(target = forever_receive_from_udp)
t.setDaemon(True)
t.start()

playback_stream = OutputStream(samplerate=8000, blocksize=800, dtype='int32', channels=1)
playback_stream.start()
playback_queue = Queue()

def forever_write_to_output():
    while True:
        try:
            playback_stream.write(playback_queue.get())
        except:
            traceback.print_exc()

t = threading.Thread(target = forever_write_to_output)
t.setDaemon(True)
t.start()

# now write something which receives udp packets and sticks
# them into the playback queue

while True:
    try:
        time.sleep(1)
    except:
        break
        
playback_stream.stop()
