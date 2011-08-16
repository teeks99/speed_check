'''
Created on Aug 15, 2011

@author: tomkent
'''

import urllib2
import time

if __name__ == '__main__':
    url = "http://speedtest.wdc01.softlayer.com/downloads/test500.zip"
    seconds = 60
    block_size = 1024
    output_time = 5
    
    f = urllib2.urlopen(url)
    
    start = time.time()
    bytes = 0
    previous = 0
    last_output = start
    while previous < (start + seconds):
        temp = f.read(block_size)
        if len(temp)==0: 
            break
        bytes += block_size
        current = time.time()
        
        # We want to push the block size up as high as we can, to
        # avoid unknowns surrounding what happens at the start/stop of 
        # a read() call.
        if (current - previous) < 0.5:
            block_size = block_size * 2
            #print "doubled to: " + str(block_size)
            
        if (current - last_output) > output_time:
            #print str(bytes/(current-start))
            last_output = current
            
        previous = current
        
    finish = previous
    f.close()
    elapsed = finish-start
    
    average = bytes / elapsed
    #print "done: " + str(average)
    
    out = open('log.txt','a')
    out.write(str(average)+'\n')
    out.close()
    
    