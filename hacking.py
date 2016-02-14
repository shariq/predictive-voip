'''record audio frames
send audio frames (callback which just sticks into play)
play audio frames on callback

pysoundcard


server which forwards all udp packets from one ip, port to everyone connected to it via udp


erasure codes later if time permits
'''

from pysoundcard import Stream, continue_flag
import time

"""Loop back five seconds of audio data."""

def callback(in_data, out_data, time_info, status):
    out_data[:] = in_data
    return continue_flag

s = Stream(samplerate=44100, blocksize=16, callback=callback)
s.start()
time.sleep(5)
s.stop()
