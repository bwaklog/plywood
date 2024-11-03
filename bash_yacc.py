from typing import Callable
import pprint
from contextlib import contextmanager
from ply.src.ply import yacc
from bash_lex import tokens

def p_start(p):
    """start : assignment_word
    | echo_command
    | condition_chain
    | arithmetic_expression
    | if_command
    """
    p[0] = p[1]

def p_assignment_word(p):
    """assignment_word : IDENTIFIER EQUALS IDENTIFIER
    | IDENTIFIER EQUALS NUMBER"""
    p[0] = {
        "type": "assignment_word",
        "name": p[1],
        "value": p[3],
    }

def p_command(p):
    """command : assignment_word
    | echo_command
    | arithmetic_expression
    | if_command"""
    p[0] = p[1]

def p_newline_list(p):
    """newline_list :
    | newline_list NEWLINE"""
    p[0] = p[1] if len(p) == 2 else []

# def p_list_1(p):
#     """list_1 : list_1 AND newline_list list_1
#     | list_1 OR newline_list list_1
#     | list_1 SINGLE_AND newline_list list_1
#     | list_1 SEMICOLON newline_list list_1
#     | list_1 NEWLINE newline_list list_1
#     | command"""
#     p[0] = {
#         "type": "list_1",
#         "left": p[1],
#         "operator": p[2],
#         "right": p[4] if len(p) > 2 else None,
#     }

def p_echo_command(p):
    """echo_command : ECHO NUMBER
    | ECHO IDENTIFIER
    | ECHO STRING"""
    p[0] = {
        "type": "echo_command",
        "value": p[2],
    }

"""
condition : identifier compare_operator identifier
number compare_operator number
"""

def p_operands(p):
    """operands : IDENTIFIER
    | NUMBER"""
    p[0] = p[1]

def p_compare_operator(p):
    """compare_operator : GREATER
    | EQUAL_TO
    | LESSER
    | GREATEREQUAL
    | LESSEREQUAL
    | NOTEQUAL"""
    p[0] = p[1]

def p_empty(p):
    """empty :"""
    pass

# [ ]
def p_simple_condition(p):
    """simple_condition : BASIC_COND_OPEN operands compare_operator operands BASIC_COND_CLOSE"""
    p[0] = {
        "type": "basic_condition",
        "left": p[2],
        "operator": p[3],
        "right": p[4],
    }

# [[ ]]
def p_extended_condition(p):
    """extended_condition : CONDITIONAL_CONST_OPEN operands compare_operator operands CONDITIONAL_CONST_CLOSE"""
    p[0] = {
        "type": "extended_condition",
        "left": p[2],
        "operator": p[3],
        "right": p[4],
    }

def p_condition(p):
    """condition : simple_condition
    | extended_condition"""
    p[0] = p[1]

def p_newline_list(p):
    """newline_list : empty
    | newline_list NEWLINE"""
    p[0] = p[1] if len(p) == 2 else []

def command_list(p):
    """command_list : command
    | command_list newline_list command"""
    p[0] = {
        "type": "command_list",
        "left": p[1],
        "right": p[3] if len(p) > 2 else None,
    }

"""
if [ condition ] && [ condition ]; then
    echo "true"
fi

if [[ condition ]] && [[ condition ]]; then 
    echo "true"
fi

if [ condition ] && [ condition ]
then 
    echo "true"
fi
"""
def p_condition_chain(p):
    """condition_chain : condition AND condition
    | condition OR condition 
    | condition"""
    if len(p) == 4:
        p[0] = {
            "type": "condition_chain",
            "left_condition": p[1],
            "condition_join": p[2],
            "condition_right": p[3],
        }
    else:
        p[0] = {
            "type": "condition_chain",
            "condition": p[1],
        }

def p_else_command(p):
    """else_command : ELSE command"""
    p[0] = {
        "type": "else_command",
        "command": p[2],
    }

def p_elif_command(p):
    """elif_command : ELIF condition_chain SEMICOLON THEN command"""
    p[0] = {
        "type": "elif_command",
        "condition": p[2],
        "then_command": p[5],
    }
    # if len(p) == 5:
    #     pass
    # else:
    #     # There is another elif condition
    #     p[0]["elif_command"] = p[6]

# if [ 10 -eq 10 ]; then echo "hi"; else echo "byte"; fi
def p_if_command(p):
    """if_command : IF condition_chain SEMICOLON THEN command SEMICOLON FI
    | IF condition_chain SEMICOLON THEN command SEMICOLON else_command SEMICOLON FI
    | IF condition_chain SEMICOLON THEN command SEMICOLON elif_command SEMICOLON FI
    | IF condition_chain SEMICOLON THEN command SEMICOLON elif_command SEMICOLON else_command SEMICOLON FI"""
    if (len(p) == 8):
        p[0] = {
            "type": "if_command",
            "condition": p[2],
            "then_command": p[5],
        }
    elif (len(p) == 10) and type(p[7]) == dict:
        p[0] = {
            "type": "if_else_elif_command" if p[7]["type"] == "elif_command" else "if_else_command",
            "condition": p[2],
            "then_command": p[5],
        }
        # "else_command": p[7],
        if p[7]["type"] == "elif_command":
            p[0]["elif_command"] = p[7]
        elif p[7]["type"] == "else_command":
            p[0]["else_command"]
    else:
        p[0] = {
            "type": "if_elif_else_command",
            "condition": p[2],
            "then_command": p[5],
            "elif_command": p[7],
            "else_command": p[9],
        }

def p_compound_list(p):
    """compound_list : IDENTIFIER"""
    p[0] = p[1]


def p_arithmetic_expression(p):
    """arithmetic_expression : ARITHMETIC_EXP_START expression ARITHMETIC_EXP_END"""
    p[0] = {
        "type" : "arithmetic_expression",
        "value" : p[2]
    }

def p_expression(p):
    """expression : term
    | expression PLUS term
    | expression MINUS term"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {
            "type" : "binary_operation",
            "left" : p[1],
            "operator" : p[2],
            "right": p[3]
        }

def p_term(p):
    """term : factor
    | term MULTIPLY factor
    | term DIVIDE factor
    | term MODULUS factor"""

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {
            "type" : "binary_operation",
            "left" : p[1],
            "operator" : p[2],
            "right" : p[3]
        }

def p_factor(p):
    """factor : NUMBER
    | IDENTIFIER
    | LPAREN expression RPAREN
    | PLUS factor
    | MINUS factor"""
    if len(p) == 2:
        if isinstance(p[1], (int, float)):
            p[0] = {
                "type": "number",
                "value": p[1]
            }
        else:
            p[0] = {
                "type": "identifier",
                "value": p[1]
            }
    elif len(p) == 3:
        p[0] = {
            "type": "unary_operation",
            "operator": p[1],
            "operand": p[2]
        }
    else:
        p[0] = p[2]


def p_error(p):
    if p:
        print("Syntax error at: ", p.value)
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

def IGNORE_LINE(x: str) -> bool:
    if x == "\n":
        return False
    elif x.startswith("#"):
        return False
    else:
        return True

CLEAN_LINE: Callable[[str], str] = str.strip
# IGNORE_NEWLINE: Callable[[str], bool] = lambda x: x != "\n"

commands = list(
    map(
        CLEAN_LINE, 
        filter(IGNORE_LINE, open("test.sh", "r").readlines()[1:])
    )
)

for command in commands:
    pprint.pp(parser.parse(command))
