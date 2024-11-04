from typing import Callable
import pprint
from contextlib import contextmanager
from ply.src.ply import yacc
from bash_lex import tokens, lexer

def p_start(p):
    """start : command_list"""
    p[0] = p[1]

def p_empty(p):
    """empty :"""
    pass

def p_any_space(p):
    """any_space : empty
    | any_space SPACE"""
    pass

def p_no_space(p):
    """no_space : empty"""
    pass

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
    | condition_chain
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
    """echo_command : ECHO SPACE NUMBER
    | ECHO SPACE IDENTIFIER
    | ECHO SPACE STRING"""
    p[0] = {
        "type": "echo_command",
        "value": p[3],
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


# [ ]
def p_simple_condition(p):
    """simple_condition : BASIC_COND_OPEN SPACE operands SPACE compare_operator SPACE operands SPACE BASIC_COND_CLOSE"""
    p[0] = {
        "type": "basic_condition",
        "left": p[3],
        "operator": p[5],
        "right": p[7],
    }

# [[ ]]
def p_extended_condition(p):
    """extended_condition : CONDITIONAL_CONST_OPEN SPACE operands SPACE compare_operator SPACE operands SPACE CONDITIONAL_CONST_CLOSE"""
    p[0] = {
        "type": "extended_condition",
        "left": p[3],
        "operator": p[5],
        "right": p[7],
    }

def p_condition(p):
    """condition : simple_condition
    | extended_condition"""
    p[0] = p[1]

# def p_newline_list(p):
#     """newline_list : empty
#     | newline_list NEWLINE"""
#     p[0] = p[1] if len(p) == 2 else []

def p_command_list(p):
    """command_list : command
    | command_list SPACE AND SPACE command_list
    | command_list SPACE OR SPACE command_list"""
    p[0] = {
        "type": "command_list",
        "left_command": p[1],
    }
    if len(p) == 6:
        p[0]["list_join"] = p[3]
        p[0]["right_command"] = p[5]

def p_condition_chain(p):
    """condition_chain : condition_chain SPACE AND SPACE condition_chain
    | condition_chain SPACE OR SPACE condition_chain 
    | condition"""
    if len(p) == 6:
        p[0] = {
            "type": "condition_chain",
            "left_condition": p[1],
            "condition_join": p[3],
            "condition_right": p[5],
        }
    else:
        p[0] = {
            "type": "condition_chain",
            "condition": p[1],
        }

def p_else_command(p):
    """else_command : ELSE SPACE command"""
    p[0] = {
        "type": "else_command",
        "command": p[3],
    }

def p_elif_command(p):
    """elif_command : ELIF SPACE condition_chain SEMICOLON SPACE THEN SPACE command"""
    p[0] = {
        "type": "elif_command",
        "condition": p[3],
        "then_command": p[8],
    }
    # if len(p) == 5:
    #     pass
    # else:
    #     # There is another elif condition
    #     p[0]["elif_command"] = p[6]

# if [ 10 -eq 10 ]; then echo "hi"; else echo "byte"; fi
def p_if_command(p):
    """if_command : IF SPACE condition_chain SEMICOLON SPACE THEN SPACE command_list SEMICOLON SPACE FI
    | IF SPACE condition_chain SEMICOLON SPACE THEN SPACE command SEMICOLON SPACE else_command SEMICOLON SPACE FI
    | IF SPACE condition_chain SEMICOLON SPACE THEN SPACE command SEMICOLON SPACE elif_command SEMICOLON SPACE FI
    | IF SPACE condition_chain SEMICOLON SPACE THEN SPACE command SEMICOLON SPACE elif_command SEMICOLON SPACE else_command SEMICOLON SPACE FI"""
    if (len(p) == 12):
        p[0] = {
            "type": "if_command",
            "condition": p[3],
            "then_command": p[8],
        }
    elif (len(p) == 15) and type(p[11]) == dict:
        p[0] = {
            "type": "if_else_elif_command" if p[11]["type"] == "elif_command" else "if_else_command",
            "condition": p[3],
            "then_command": p[8],
        }
        # "else_command": p[7],
        if p[11]["type"] == "elif_command":
            p[0]["elif_command"] = p[11]
        elif p[11]["type"] == "else_command":
            p[0]["else_command"] = p[11]
    else:
        p[0] = {
            "type": "if_elif_else_command",
            "condition": p[3],
            "then_command": p[8],
            "elif_command": p[11],
            "else_command": p[14],
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

def get_commands(file: str) -> list[str]:
    return list(
        map(
            CLEAN_LINE,
            filter(IGNORE_LINE, open(file, "r").readlines()[1:])
        )
    )

def generate_tokens(command: str) -> list[dict]:
    tokens = []
    lexer.input(command)
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append({
            "type": tok.type,
            "value": tok.value,
            "lineno": tok.lineno,
            "lexpos": tok.lexpos
        })
    return tokens


if __name__=="__main__":
    commands = get_commands(file="test.sh")
    for command in commands:
        parsed_output = parser.parse(command)
        pprint.pp({
            # "tokens": generate_tokens(command),
            "parsed_output": parsed_output if parsed_output != None else "[ERROR] Failed to parse"
        })