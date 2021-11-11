# regex for the builtin sentences
# this allows for translation of the sentences to other languages
import common.typeregex as typeregex

print = {
    "str": f'print (?P<str>{typeregex.string})',
    "num": f'print (?P<num>{typeregex.number})',
    "empty": f'print$',
    "var": f'print (?P<var>{typeregex.name})',
    "nothing": f'print {typeregex.nothing}'
}
let_be = f'let (?P<name>{typeregex.name}) be (?P<value>.*)'
increase_by = f'increase (?P<name>{typeregex.name}) by (?P<value>.*)'
decrease_by = f'decrease (?P<name>{typeregex.name}) by (?P<value>.*)'

# french
"""print = {
    "str": f'afficher (?P<str>{typeregex.string})',
    "num": f'afficher (?P<num>{typeregex.number})',
    "empty": f'afficher$',
    "var": f'afficher (?P<var>{typeregex.name})',
    "nothing": f'print {typeregex.nothing}'
}
let_be = f'soit (?P<name>{typeregex.name}) (?P<value>.*)'
increase_by = f'augmenter (?P<name>{typeregex.name}) de (?P<value>.*)'
decrease_by = f'diminuer (?P<name>{typeregex.name}) de (?P<value>.*)'"""