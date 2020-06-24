# A function for generating a sex
import numpy
import names

def calcAge(mean,mu):
    return round(numpy.random.normal(mean, mu))
def calcSex():
    return 'M' if (round(numpy.random.random()) == 1) else 'F'
def calcName(sex):
    sexWord = 'male' if sex == 'M' else 'female'
    return names.get_full_name(gender=sexWord)