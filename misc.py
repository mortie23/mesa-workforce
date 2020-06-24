#!/usr/bin/python3

import numpy
import names

def randomAge():
    age = round(numpy.random.normal(45, 10))
    return age
#print(randomAge())

def randomSex():
    return 'M' if (round(numpy.random.random()) == 1) else 'F'
#print(randomSex())

def randomName(sex):
    return names.get_full_name(gender=sex)
print(randomName('M'))