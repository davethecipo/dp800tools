def create_channels():
    ch1 = {'v':[], 'i':[]}
    ch2 = {'v':[], 'i':[]}
    ch3 = {'v':[], 'i':[]}
    return ch1, ch2, ch3

def every_interval(stream, size, offset, n):
    '''Yield every size bytes on the stream, starting from offset, stopping after n number of times.'''
    for i in range(offset, size*n, size):
        #print('start from {}, up to {}, every {}'.format(offset, size*n, size))
        #print('i is now {}, i+size {}'.format(i, i+size))
        yield stream[i:i+size]  # [included:excluded], python starts indexing at 0


def convert_current_or_voltage(four_bytes):
    '''Returns time in seconds, voltage in Volts and current in Amperes.'''
    #return round(convert_int(four_bytes) / 10000, 3)
    return convert_int(four_bytes)/10000

def convert_int(four_bytes):
    return int.from_bytes(four_bytes, byteorder='little')
