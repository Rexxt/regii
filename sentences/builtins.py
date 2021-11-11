# regex for the builtin sentences
# this allows for translation of the sentences to other languages
import common.typeregex as typeregex

print = f'print (?P<input>{typeregex.handled_by_function})'
let_be = f'let (?P<name>{typeregex.name}) be (?P<value>.*)'
increase_by = f'increase (?P<name>{typeregex.name}) by (?P<value>.*)'
decrease_by = f'decrease (?P<name>{typeregex.name}) by (?P<value>.*)'

# french
"""print = f'afficher (?P<input>{typeregex.handled_by_function})'
let_be = f'soit (?P<name>{typeregex.name}) (?P<value>.*)'
increase_by = f'augmenter (?P<name>{typeregex.name}) de (?P<value>.*)'
decrease_by = f'diminuer (?P<name>{typeregex.name}) de (?P<value>.*)'"""