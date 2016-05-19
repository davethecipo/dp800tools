import struct


def create_channels():
    ch1 = {'v': [], 'i': []}
    ch2 = {'v': [], 'i': []}
    ch3 = {'v': [], 'i': []}
    return ch1, ch2, ch3


def every_interval(stream, size, offset, n):
    '''Yield every size bytes on the stream, starting from offset,
     stopping after n number of times.'''
    for i in range(offset, size*n, size):
        yield stream[i:i+size]  # [included:excluded]


def convert_current_or_voltage(four_bytes):
    '''Returns time in seconds, voltage in Volts and current in Amperes.'''
    return convert_int(four_bytes)/10000.0  # 10000.0 for python 2 division


def convert_int(four_bytes):
    return struct.unpack("<i", four_bytes)[0]  # 32 bit little endian
