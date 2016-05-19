from .common import\
    create_channels,\
    convert_current_or_voltage,\
    convert_int, every_interval


def create_time(file_content):
    time_interval = convert_int(file_content[16:20])
    print('time interval {}'.format(time_interval))
    number_points = convert_int(file_content[20:24])
    print('number points {}'.format(number_points))
    times = [time_interval*i for i in range(1, number_points+1)]
    return times


def convert_rof(file_content):
    '''Return (time, channel 1, channel 2, channel 3).'''
    time = create_time(file_content)
    ch1, ch2, ch3 = create_channels()
    for elem in every_interval(file_content, 4*6, 28, len(time)+1):
        ch1['v'].append(convert_current_or_voltage(elem[0:4]))
        ch1['i'].append(convert_current_or_voltage(elem[4:8]))
        ch2['v'].append(convert_current_or_voltage(elem[8:12]))
        ch2['i'].append(convert_current_or_voltage(elem[12:16]))
        ch3['v'].append(convert_current_or_voltage(elem[16:20]))
        ch3['i'].append(convert_current_or_voltage(elem[20:24]))
    return time, ch1, ch2, ch3


def to_csv_format(time, *channels, **kwargs):
    '''Return a string corresponding to the csv format.

    Args:
        time (list): list of integers representing the time in seconds when
         the measurement is taken
        *channels (dict): variable length list of channels. Each channel is
         a dict with two lists, one for voltage in Volts and one for current
          in Amperes, i.e {'v': [1, 2, 3], 'i': [2, 4, 6]}.
           The order in which channels are passed is conserved in the output
        TODO spiegare kwargs
        separator (str): the separator between values
        header(bool): if False, only numbers are written, i.e the header is
         skipped.
        units_second_row(bool): if True, the measurement unit symbol is put
         on the second line

    Returns:
        str: the text as it will appear on the csv file

    Examples:
        >>> time = [0, 2, 4]
        >>> channel1 = {'v': [0, 1, 2], 'i': [0, 1, 2]}
        >>> channel2 = {'v': [5, 6, 7], 'i': [0.1, 0.2, 0.3]}

        Use the predefined separator (comma), write the header in one single
         line
        >>> result = to_csv_format(time, channel1, channel2)

        Use space as separator, skip header
        >>> result = to_csv_format(time, channel1, separator=" ", header=False)

        Write units on the second row
        >>> result = to_csv_format(time, channel1, units_second_row=True)
    '''
    # the following three lines are needed for backward compatibility with
    # python 2.7, see http://goo.gl/pnUyyt
    separator = kwargs.pop('separator', ',')
    header = kwargs.pop('header', True)
    units_second_row = kwargs.pop('units_second_row', False)
    return False


def to_hdf5_format(time, *channels, **kwargs):
    units_metadata = kwargs.pop('units_metadata', False)
    return False
