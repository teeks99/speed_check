'''
Created on Aug 15, 2011

@author: tomkent
'''

import urllib2
import time

def push_block_size(remote_file, block_size, block_window=1.0, telemetry=False):
    """ Grow the blocksize to a suitable value for this connection
    
    If the block is downloaded in less than block_window seconds, then double it. 
    Repeat until we have two runs in a row that take longer than block_window
    """
    start = time.time()
    previous = start
    last = False
    second = False
    while not last and not second:
        temp = f.read(block_size)
        if len(temp)==0: #We've gotten all the file
            raise IOError("file was to short to complete setup")
        current = time.time()
        if(current-previous) < block_window:
            block_size = block_size * 2
            if telemetry:
                print "doubling block size to: " + str(block_size) + "B"
            last = False
            second = False
        elif last:
            second = True
        else: 
            last = True
        previous = current
    return block_size

def speed_check(remote_file, test_seconds, block_size, output_time=0):
    average, bytes, elapsed, block_size = speed_check_info(remote_file,  
        test_seconds, block_size, output_time)
    return average

def speed_check_info(remote_file, test_seconds, block_size, output_time=0):
    start = time.time()
    bytes = 0
    previous = start
    last_output = start

    while previous < (start + seconds):
        temp = f.read(block_size)
        if len(temp)==0: #We've gotten all the file
            break
        bytes += block_size
        current = time.time()
            
        if (current - last_output) > output_time and output_time != 0:
            print str(bytes/(current-start))
            last_output = current
            
        previous = current
        
    finish = previous
    elapsed = finish-start
    average = bytes / elapsed
   
    return average, bytes, elapsed, block_size

if __name__ == '__main__':
    url = "http://speedtest.wdc01.softlayer.com/downloads/test500.zip"
    seconds = 60
    block_size = 1024
    output_time = 5
    block_window = 0.5
    append_file = 'log.txt'
    
    f = urllib2.urlopen(url)
    block_size = push_block_size(f, block_size, block_window)
    average = speed_check(url, seconds, block_size)
    f.close()
     
    out = open(append_file,'a')
    out.write(str(average)+'\n')
    out.close()
    
    