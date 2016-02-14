'''
this python script must send udp packets from the mic with audio data
'''

from pysoundcard import InputStream, continue_flag
import time
from Queue import Queue
udp_queue = Queue()

def callback(in_data, time_info, status):
    udp_queue.put(in_data)
    return continue_flag

record_stream = InputStream(samplerate=16000, blocksize=16, dtype='int8', channels=1)
record_stream.start()

# now write something which takes stuff from the udp queue and sends it over
# the network

while True:
    try:
        time.sleep(1)
    except:
        break

record_stream.stop()

