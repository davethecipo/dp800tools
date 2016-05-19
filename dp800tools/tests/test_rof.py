import os
import pytest
from dp800tools.rof import convert_rof
from dp800tools.common import every_interval


def test_bytes_generator():
    content = b'\x0a\x00\x16\x0a\x0a\x00\x16\x0a\x0a\x00\x16\x0a'  # 12 bytes
    result = []
    for elem in every_interval(content, 4, 0, 2):
        result.append(elem)
    assert b''.join(result) == b'\x0a\x00\x16\x0a\x0a\x00\x16\x0a'


def test_every_interval():
    content = 'abcdefghijklmnopqrstuvwxz'
    expected = ['abcd', 'efgh', 'ijkl', 'mnop', 'qrst', 'uvwx']
    result = []
    for elem in every_interval(content, 4, 0, 6):
        result.append(elem)
    assert result == expected


def test_all_channels_and_times():
    time_1s = [e for e in range(1, 6)]
    time_2s = [e for e in range(2, 7, 2)]
    time_10s = [e for e in range(10, 70, 10)]

    # every 1 second
    ch1_1s = {'v': [0.09, 0.089, 0.089, 0.089, 0.089],
              'i': [0.002, 0.002, 0.002, 0.002, 0.002]}
    ch2_1s = {'v': [0.127, 0.126, 0.127, 0.126, 0.126],
              'i': [0.004, 0.004, 0.004, 0.004, 0.004]}
    ch3_1s = {'v': [0.489, 0.488, 0.488, 0.487, 0.487],
              'i': [0.007, 0.007, 0.007, 0.007, 0.007]}

    # every 2 seconds
    ch1_2s = {'v': [0.084, 0.084, 0.084], 'i': [0.002, 0.002, 0.002]}
    ch2_2s = {'v': [0.125, 0.125, 0.125], 'i': [0.004, 0.004, 0.004]}
    ch3_2s = {'v': [0.482, 0.482, 0.482], 'i': [0.007, 0.007, 0.007]}

    # every 10 seconds
    ch1_10s = {'v': [0.078, 0.077, 0.077, 0.077, 0.077, 0.076],
               'i': [0.002, 0.002, 0.002, 0.002, 0.002, 0.002]}
    ch2_10s = {'v': [0.124, 0.123, 0.124, 0.123, 0.123, 0.123],
               'i': [0.004, 0.004, 0.004, 0.004, 0.004, 0.004]}
    ch3_10s = {'v': [0.475, 0.475, 0.475, 0.475, 0.474, 0.474],
               'i': [0.006, 0.006, 0.006, 0.006, 0.006, 0.006]}

    all_samples = [(time_1s, ch1_1s, ch2_1s, ch3_1s, '1s.ROF'),
                   (time_2s, ch1_2s, ch2_2s, ch3_2s, '2s.ROF'),
                   (time_10s, ch1_10s, ch2_10s, ch3_10s, '10s.ROF')]
    for elem in all_samples:
        binary_content = binary_file_content(elem[4])
        result = convert_rof(binary_content)
        yield check_convert_one_channel, elem[1], result[1]
        yield check_convert_one_channel, elem[2], result[2]
        yield check_convert_one_channel, elem[3], result[3]
        yield check_convert_time, elem[0], result[0]


def binary_file_content(fname):
    '''Returns test file binary content'''
    dir = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(dir, fname)
    with open(fpath, 'rb') as f:
        content = f.read()
    return content


def check_convert_one_channel(expected, result, round_error=0.001):
    for result_v, result_i, expected_v, expected_i in zip(result['v'],
                                                          result['i'],
                                                          expected['v'],
                                                          expected['i']):
        assert abs(expected_v - result_v) < round_error
        assert abs(expected_i - result_i) < round_error


def check_convert_time(expected, result):
    assert expected == result
