import ply.lex as lex
import re

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'elseif': 'ELSEIF',
    'insample': 'INSAMPLE',
    'insampleprime': 'INSAMPLEPRIME',
    'goto': 'GOTO',
    'non-input': 'NONINPUT',
    'Lap': 'LAP',
    'output': 'OUTPUT'

}

tokens = [
    'NUMBER',
    'IF', 'THEN', 'ELSEIF', 'GOTO', 'SLASH',
    'LPAREN', 'RPAREN',
    'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL',
    'COLONEQ', 'COLON', 'SEMICOLON', 'COMMA',
    'INSAMPLE', 'INSAMPLEPRIME', 'SID', 'OID', 'OUTPUT', 'LAP',
    'NONINPUT', 'VARIABLE', 'AND'
]

t_NUMBER = r'[0-9][0-9]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LESS = r'<'
t_GREATER = r'>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_COLONEQ = r':='
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_IF = r'if'
t_THEN = r'then'
t_ELSEIF = r'elseif'
t_GOTO = r'goto'
t_SLASH = r'/'
t_AND = r'&&'
t_INSAMPLE = r'insample'
t_INSAMPLEPRIME = r'insample\''
t_LAP = r'Lap'
# t_NONINPUT = 'non-input'
t_OUTPUT = r'output'


def t_NONINPUT(t):
    r"non-input"
    t.type = "NONINPUT"
    return t


def t_SID(t):
    r"""q[a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'SID')
    return t


def t_OID(t):
    r"""o[a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'OID')
    return t


def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def make_lexer():
    return lex.lex()
