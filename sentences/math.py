# math methods for RegII
from common.module import Module
import math

module = Module('sentence_pack')

@module.method(f'square root of (?P<num>{module.typeregex.number})')
def square_root(self, args, return_stack):
    number = args['num']
    return math.sqrt(float(number))

def module_class():
    return module