# RegII, a Regular Instruction Interpreter (aka a regular expression-based programming language)
# Copyleft (C) 2021, by Mizu
# it's dumb, but it works
# and it's funny because it's not really a language, it's just a bunch of regular expressions that can be used to do stuff

import re
import sys
import os
import time
import random
import math
import common.typeregex as typeregex

class RegII:
    def __init__(self, source=""):
        self.__version__ = "0.0.1"
        self.__author__ = "Mizu"
        self.__copyright__ = "Copyleft (C) 2021, by Mizu"
        self.__license__ = "GNU General Public License v3.0"
        self.__source__ = source
        self.variables = {}

    def SentenceMatchError(self, index, line):
        return f'RegII | SentenceMatchError ({self.__source__} : {index+1})\n    > | {line}\n    ! | Didn\'t find any matching sentence'
    
    def TypeError(self, index, line, expected_types, actual_type):
        return f'RegII | TypeError ({self.__source__} : {index+1})\n    > | {line}\n    ! | TypeError: Expected type(s) {expected_types if type(expected_types) == str else ", ".join(expected_types)} but got {actual_type}'
    
    def TypeMismatchError(self, index, line, expected_types, actual_type):
        return f'RegII | AssignTypeError ({self.__source__} : {index+1})\n    > | {line}\n    ! | TypeMismatchError: Attempted to match type(s) {expected_types if type(expected_types) == str else ", ".join(expected_types)} with type {actual_type}'
        
    def process_string_escape(self, string):
        return string.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").replace("\\\"", "\"")

    def tostring(self, value):
        if type(value) == str:
            return value
        elif type(value) == int:
            return str(value)
        elif type(value) == float:
            return str(value)
        elif type(value) == bool:
            return typeregex.bools[value]
        elif value == None:
            return typeregex.nothing

    def interpret(self, code):
        # Interpret the code
        # code is a string
        lines = code.split("\n")
        lines = [line.lstrip() for line in lines] # remove whitespace from the beginning of each line
        lines = [line.rstrip() for line in lines] # remove whitespace from the end of each line
        lines = [line for line in lines if line != ""] # remove empty lines
        lines = [line for line in lines if not line.startswith("//")] # remove comments at the beginning of each line
        # TODO: remove comments at the end of each line

        import sentences.builtins

        _i = 0
        tree = []
        return_stack = [True]

        while _i < len(lines):
            # interpret the line
            line = lines[_i]
            #print(return_stack)
            if re.match(sentences.builtins.print, line):
                # print
                args = re.search(sentences.builtins.print, line)

                if re.match(typeregex.string, args['input']):
                    print(self.process_string_escape(args['input'][1:-1])) # print string without quotes
                elif re.match(typeregex.number, args['input']):
                    print(args['input'])
                elif re.match(typeregex.boolean, args['input']):
                    print(typeregex.bools[args['input']])
                elif re.match(typeregex.nothing, args['input']):
                    print(typeregex.nothing)
                elif re.match(typeregex.expression, args['input']):
                    result = self.interpret(args['input'][1:-1])
                    #print(result)
                    print(result[6].pop()) # expression result (recursive)
                elif re.match(args['input'], typeregex.name):
                    print(self.variables[args['input']])
                else:
                    return False, self, lines, _i, line, self.TypeError(_i, line, ["string", "integer", "float", "boolean", "nothing", "name", "expression"], 'undefined'), return_stack
            elif re.match(sentences.builtins.let_be, line):
                # variable assignment (let name be value)
                args = re.search(sentences.builtins.let_be, line)
                if args['value'][0] == '"' and args['value'][-1] == '"':
                    self.variables[args['name']] = self.process_string_escape(args['value'][1:-1]) # string
                elif args['value'].isdigit():
                    self.variables[args['name']] = int(args['value']) # integer
                elif args['value'].replace('.', '', 1).isdigit():
                    self.variables[args['name']] = float(args['value']) # float
                elif re.match(typeregex.boolean, args['value']):
                    self.variables[args['name']] = typeregex.bools[args['value']] # boolean
                elif re.match(typeregex.nothing, args['value']):
                    self.variables[args['name']] = None # nothing
                elif re.match(typeregex.name, args['value']):
                    self.variables[args['name']] = self.variables[args['value']] # variable
                elif re.match(typeregex.expression, args['value']):
                    result = self.interpret(args['value'][1:-1])
                    #print(result)
                    self.variables[args['name']] = result[6].pop() # expression result (recursive)
                else:
                    # unknown type error
                    return False, self, lines, _i, line, self.TypeError(_i, line, ["string", "integer", "float", "boolean", "nothing", "name"], 'undefined'), return_stack
                # TODO: more types (list, dict, etc.)
            elif re.match(sentences.builtins.increase_by, line):
                # variable increase (increase name by value)
                args = re.search(sentences.builtins.increase_by, line)
                # only integer and float are supported
                if type(self.variables[args['name']]) == int or type(self.variables[args['name']]) == float:
                    if args['value'].isdigit():
                        self.variables[args['name']] += int(args['value'])
                    elif args['value'].replace('.', '', 1).isdigit():
                        self.variables[args['name']] += float(args['value'])
                    else:
                        return False, self, lines, _i, line, self.TypeMismatchError(_i, line, ['int', 'float'], type(self.variables[args['name']])), return_stack
                else:
                    return False, self, lines, _i, line, self.TypeError(_i, line, ['int', 'float'], type(self.variables[args['name']])), return_stack
            elif re.match(sentences.builtins.decrease_by, line):
                # variable decrease (decrease name by value)
                args = re.search(sentences.builtins.decrease_by, line)
                # only integer and float are supported
                if type(self.variables[args['name']]) == int or type(self.variables[args['name']]) == float:
                    if args['value'].isdigit():
                        self.variables[args['name']] -= int(args['value'])
                    elif args['value'].replace('.', '', 1).isdigit():
                        self.variables[args['name']] -= float(args['value'])
                    else:
                        return False, self, lines, _i, self.TypeMismatchError(_i, line, ['int', 'float'], type(self.variables[args['name']])), return_stack
                else:
                    return False, self, lines, _i, line, self.TypeError(_i, line, ['int', 'float'], type(self.variables[args['name']])), return_stack
            elif re.match(f'(?P<term_a>({typeregex.number}|{typeregex.expression}))\s*\+\s*(?P<term_b>({typeregex.number}|{typeregex.expression}))', line):
                # addition
                args = re.search(f'(?P<term_a>({typeregex.number}|{typeregex.expression}))\s*\+\s*(?P<term_b>({typeregex.number}|{typeregex.expression}))', line)
                if args['term_a'].isdigit():
                    term_a = int(args['term_a'])
                elif args['term_a'].replace('.', '', 1).isdigit():
                    term_a = float(args['term_a'])
                elif re.match(typeregex.expression, args['term_a']):
                    result = self.interpret(args['term_a'][1:-1])
                    #print(result)
                    term_a = result[6].pop() # expression result (recursive)
                
                if args['term_b'].isdigit():
                    term_b = int(args['term_b'])
                elif args['term_b'].replace('.', '', 1).isdigit():
                    term_b = float(args['term_b'])
                elif re.match(typeregex.expression, args['term_b']):
                    result = self.interpret(args['term_b'][1:-1])
                    #print(result)
                    term_b = result[6].pop()
                
                return_stack.append(term_a + term_b)
            elif re.match(f'(?P<term_a>({typeregex.number}|{typeregex.expression}))\s*-\s*(?P<term_b>({typeregex.number}|{typeregex.expression}))', line):
                # substraction
                args = re.search(f'(?P<term_a>({typeregex.number}|{typeregex.expression}))\s*-\s*(?P<term_b>({typeregex.number}|{typeregex.expression}))', line)
                if args['term_a'].isdigit():
                    term_a = int(args['term_a'])
                elif args['term_a'].replace('.', '', 1).isdigit():
                    term_a = float(args['term_a'])
                elif re.match(typeregex.expression, args['term_a']):
                    result = self.interpret(args['term_a'][1:-1])
                    #print(result)
                    term_a = result[6].pop() # expression result (recursive)
                
                if args['term_b'].isdigit():
                    term_b = int(args['term_b'])
                elif args['term_b'].replace('.', '', 1).isdigit():
                    term_b = float(args['term_b'])
                elif re.match(typeregex.expression, args['term_b']):
                    result = self.interpret(args['term_b'][1:-1])
                    #print(result)
                    term_b = result[6].pop()
                
                return_stack.append(term_a - term_b)
            elif re.match(f'(?P<term_a>({typeregex.number}|{typeregex.expression}))\s*/\s*(?P<term_b>({typeregex.number}|{typeregex.expression}))', line):
                # division
                args = re.search(f'(?P<term_a>({typeregex.number}|{typeregex.expression}))\s*/\s*(?P<term_b>({typeregex.number}|{typeregex.expression}))', line)
                if args['term_a'].isdigit():
                    term_a = int(args['term_a'])
                elif args['term_a'].replace('.', '', 1).isdigit():
                    term_a = float(args['term_a'])
                elif re.match(typeregex.expression, args['term_a']):
                    result = self.interpret(args['term_a'][1:-1])
                    #print(result)
                    term_a = result[6].pop() # expression result (recursive)
                
                if args['term_b'].isdigit():
                    term_b = int(args['term_b'])
                elif args['term_b'].replace('.', '', 1).isdigit():
                    term_b = float(args['term_b'])
                elif re.match(typeregex.expression, args['term_b']):
                    result = self.interpret(args['term_b'][1:-1])
                    #print(result)
                    term_b = result[6].pop()
                
                return_stack.append(term_a / term_b)
            elif re.match(f'(?P<term_a>({typeregex.number}|{typeregex.expression}))\s*\*\s*(?P<term_b>({typeregex.number}|{typeregex.expression}))', line):
                # multiplication
                args = re.search(f'(?P<term_a>({typeregex.number}|{typeregex.expression}))\s*\*\s*(?P<term_b>({typeregex.number}|{typeregex.expression}))', line)
                if args['term_a'].isdigit():
                    term_a = int(args['term_a'])
                elif args['term_a'].replace('.', '', 1).isdigit():
                    term_a = float(args['term_a'])
                elif re.match(typeregex.expression, args['term_a']):
                    result = self.interpret(args['term_a'][1:-1])
                    #print(result)
                    term_a = result[6].pop() # expression result (recursive)
                
                if args['term_b'].isdigit():
                    term_b = int(args['term_b'])
                elif args['term_b'].replace('.', '', 1).isdigit():
                    term_b = float(args['term_b'])
                elif re.match(typeregex.expression, args['term_b']):
                    result = self.interpret(args['term_b'][1:-1])
                    #print(result)
                    term_b = result[6].pop()
                
                return_stack.append(term_a * term_b)
            else:
                # print("Error: Unknown command: " + line) # temporary until we have a proper error system
                return False, self, lines, _i, line, self.SentenceMatchError(_i, line), return_stack
            
            _i += 1
            
        return True, self, lines, _i, line, None, return_stack # Success, self, lines, index, line, error, return stack