'''
this python script must receive udp packets with audio data and play them
'''

from pysoundcard import OutputStream, continue_flag
import time
from Queue import Queue
import threading
import traceback

playback_stream = OutputStream(samplerate=16000, blocksize=16, dtype='int8', channels=1)
playback_stream.start()
write_queue = Queue()

def forever_write_to_output():
    while True:
        try:
            playback_stream.write(write_queue.get())
        except:
            traceback.print_exc()

threading.Thread(target = forever_write_to_output).start()

# now write something which receives udp packets and sticks
# them into the write queue

while True:
    try:
        time.sleep(1)
    except:
        break
        
playback_stream.stop()
