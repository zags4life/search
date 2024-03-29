import logging
from ply import lex, yacc
import re

from .conditions import *

logger = logging.getLogger(__name__)

tokens = (
    'NAME',
    'EQUALS',
    'NOT_EQUALS',
    'LIKE', 'LT', 'GT', 'LTE', 'GTE',
    'AND', 'OR',
)

literals = ['!', '(', ')']

# Tokens
t_NAME      = r'(\(\?[a-z]\)\s*)?[a-zA-Z0-9_\\.*\-\+\^\$/\|\[\]\{\}\,\?,@,\'"]+'
t_LT        = r'\s*<\s*'
t_LTE       = r'\s*<=\s*'
t_GT        = r'\s*>\s*'
t_GTE       = r'\s*>=\s*'
t_EQUALS    = r'\s*=\s*'
t_NOT_EQUALS = r'\s*!=\s*'
t_AND       = r'((?i)\s+and\s+)|\s*&&\s*'
t_OR        = r'((?i)\s+or\s+)|\s*\|\|\s*'
t_LIKE      = r'(?i)\s+like\s+|\s*~\s*'


has_error = False

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    logger.debug("Illegal character '{}' at pos {}".format(
        t.value, t.lexpos+1))
    t.lexer.skip(1)

    global has_error
    has_error = True


# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'LT', 'GT', 'LTE', 'GTE'),
    ('left', 'EQUALS', 'LIKE', 'NOT_EQUALS'),
    ('left', 'AND', 'OR'),
    ('left', '(', ')'),
    ('right', 'NOT'),
)

def p_expression_eq(p):
    'expression : NAME EQUALS NAME'
    p[0] = EqualExpression(p[1], p[3])

def p_expression_ne(p):
    'expression : NAME NOT_EQUALS NAME'
    p[0] = NotEqualExpression(p[1], p[3])

def p_expression_like(p):
    'expression : NAME LIKE NAME'
    p[0] = LikeExpression(p[1], p[3])

def p_expression_lt(p):
    'expression : NAME LT NAME'
    p[0] = LessThanExpression(p[1], p[3])

def p_expression_lte(p):
    'expression : NAME LTE NAME'
    p[0] = LessThanOrEqualExpression(p[1], p[3])

def p_expression_gt(p):
    'expression : NAME GT NAME'
    p[0] = GreaterThanExpression(p[1], p[3])

def p_expression_gte(p):
    'expression : NAME GTE NAME'
    p[0] = GreaterThanOrEqualExpression(p[1], p[3])

def p_expression_name(p):
    'expression : NAME'
    p[0] = AnyExpression(p[1])

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_statement(p):
    'expression : statement'
    p[0] = p[1]

def p_statement_and(p):
    'statement : expression AND expression'
    p[0] = AndStatement(p[1], p[3])

def p_statement_or(p):
    'statement : expression OR expression'
    p[0] = OrStatement(p[1], p[3])

def p_statement_not(p):
    "statement : '!' expression %prec NOT"
    p[0] = NotStatement(p[2])

def p_statement_group(p):
    "statement : '(' statement ')'"
    p[0] = p[2]

def p_error(p):
    if p:
        logger.warning(
            "Syntax error at '{}' at pos {}".format(p.value, p.lexpos + 1)
        )
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
        if s.lower().strip() == 'quit':
            exit(0)
        result = yacc.parse(s)
        print(type(result))
        print(result)
