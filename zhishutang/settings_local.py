#! /usr/sbin/python2.7
# __*__ coding: utf-8 __*__


import string, random


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
