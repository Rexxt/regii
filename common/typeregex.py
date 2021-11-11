# regular expressions for type checking
string='".*"'
number='\d+'
bools={
    True: 'true',
    False: 'false'
}
boolean=f'({bools[True]}|{bools[False]})'
name='[a-zA-Z_][a-zA-Z0-9_]*'
nothing='nothing'
expression='\(.*\)'
handled_by_function='.*'

# french
"""
bools={
    True: 'vrai',
    False: 'faux'
}
nothing='rien'
"""