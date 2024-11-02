from contextlib import contextmanager
from ply.src.ply import yacc
from bash_lex import tokens


def p_assignment_word(p):
    """assignment_word : IDENTIFIER EQUALS IDENTIFIER
    | IDENTIFIER EQUALS NUMBER"""
    p[0] = {
        "type": "assignment_word",
        "name": p[1],
        "value": p[3],
    }


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input("inp >")
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
