import gc
import os

def df():
    s = os.statvfs('/')
    print(s)
    print('Disk space: {0} kB free out of {1}'.format(s[0]*s[3]/1024,s[0]*s[2]/1024))

def free(full=False):
    gc.collect()    
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = '{0:.2f}%'.format(100-F/T*100)
    print('Ram memory: {0} Bytes free out of {1} ({2} in use)'.format(F,T,P))
    
df()
free()
