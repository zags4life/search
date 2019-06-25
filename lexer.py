import logging
import re

from .conditions import *

logger = logging.getLogger(__name__)


from functools import wraps

def print_name(func):
    @wraps(func)
    def wrapper(t):
        print('{}({})'.format(func.__name__, str(t)))
        return func(t)
    return wrapper

expression_map = {
    '=': EqualityExpression,
    '<': LessThanExpression,
    '>': GreaterThanExpression,
    'like': LikeExpression,
    '>=': GreaterThanOrEqualExpression,
    '<=': LessThanOrEqualExpression
}

literals = ['=', '>', '<', '!', '(', ')']

tokens = (
    'KEY_VALUE',
    'AND',
    'OR',
    'NOT',
)

# Tokens
t_KEY_VALUE = r'(?P<field>[a-zA-Z0-9_.*-]+)\s*(?P<operand>([<>=]{1,2}|((?i)\slike\s)))\s*(?P<value>[a-zA-Z0-9_\\.*\-\+\^\$/\|]*)'
t_AND = r'(?i)and'
t_OR = r'(?i)or'
t_NOT = r'(?i)not'

# Ignored characters
t_ignore = " \t"

has_error = False

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    logger.debug("Illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)

    global has_error
    has_error = True

# Build the lexer
from .ply import lex, yacc

# Precedence rules for the arithmetic operators
precedence = (
    # ('like', 'LIKE', 'KEY_VALUE'),
    ('left', 'AND', 'OR'),
    ('left', 'NOT', '!'),
)

def p_expression_token(p):
    '''expression : KEY_VALUE'''
    tokens = re.search(t_KEY_VALUE, p[1])
    if not tokens:
        return

    tokens = tokens.groupdict()

    # Create the expression object
    lhs = tokens['field']
    rhs = tokens['value']
    operand = tokens['operand']

    if not rhs:
        logger.warning('bad')
        return
        # logger.warning("Expression '{}' has an empty rhs value.  Implicitly converting to '{} like .*'".format(p[1], lhs))
        # operand = 'like'
        # rhs = '.*'

    operand = operand.strip().lower()

    if operand == '><':
        return
    if operand == '<>':
        p[0] = NotCondition(expression_map['='](lhs=lhs, rhs=rhs))
    else:
        p[0] = expression_map[operand](lhs=lhs, rhs=rhs)

def p_expression_expr(p):
    'expression : expression expression'
    p[0] = AndCondition(p[1], p[2])

def p_expression_and(p):
    'expression : expression AND expression'
    p[0] = AndCondition(p[1], p[3])

def p_expression_or(p):
    'expression : expression OR expression'
    p[0] = OrCondition(p[1], p[3])

def p_expression_not(p):
    '''expression : NOT expression
                  | "!" expression'''
    p[0] = NotCondition(p[2])

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_error(p):
    if p:
        logger.warning("Syntax error at '{}'".format(p.value))
    else:
        logger.warning('An error occurred... not sure what')

    global has_error
    has_error = True

def compile(query):
    global has_error
    try:
        lex.lex()
        compiled_cond = yacc.yacc().parse(query)
        return compiled_cond if not has_error else None
    finally:
        has_error = False

if __name__ == '__main__':
    import sys
    if sys.version_info[0] >= 3:
        raw_input = input

    lex.lex()
    yacc.yacc()

    while True:
        try:
            s = input('search > ')   # use input() on Python 3
        except EOFError:
            break
        result = yacc.parse(s)
        print(result)