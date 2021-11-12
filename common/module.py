# module system
import common.typeregex as typeregex

class Module:
    def __init__(self, mode):
        self.mode = mode # mode is a string ('sentence_pack')
        self.methods = {} # dictionary of methods (sentences paired with functions)
        self.typeregex = typeregex # importing the typeregex module

    def method(self, sentence, function):
        # decorator that adds a method to the module
        self.methods[sentence] = function
        return function

    def setup(self, interpreter):
        # setup the module
        # this is called when the module is loaded using "using python <module>".

        # add the methods to the interpreter IF mode == 'sentence_pack'
        if self.mode == 'sentence_pack':
            for sentence, function in self.methods.items():
                interpreter.methods[sentence] = function
        pass