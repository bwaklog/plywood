from contextlib import contextmanager
from ply.src.ply import yacc
from bash_lex import tokens

def p_start(p):
    """start : assignment_word
    | echo_command
    | condition
    | if_command
    | arithmetic_expression
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
    | arithmetic_expr"""
    p[0] = p[1]

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

def p_compare_operator(p):
    """compare_operator : GREATER
    | EQUAL_TO
    | LESSER
    | GREATEREQUAL
    | LESSEREQUAL
    | NOTEQUAL"""
    p[0] = p[1]

def p_condition(p):
    """condition : CONDITIONAL_CONST_OPEN IDENTIFIER compare_operator IDENTIFIER CONDITIONAL_CONST_CLOSE
    | CONDITIONAL_CONST_OPEN NUMBER compare_operator NUMBER CONDITIONAL_CONST_CLOSE
    | CONDITIONAL_CONST_OPEN IDENTIFIER compare_operator NUMBER CONDITIONAL_CONST_CLOSE
    | CONDITIONAL_CONST_OPEN NUMBER compare_operator IDENTIFIER CONDITIONAL_CONST_CLOSE"""
    p[0] = {
        "type": "condition",
        "left": p[2],
        "operator": p[3],
        "right": p[4],
    }

def p_if_command(p): 
    """if_command : IF condition THEN FI"""
    p[0] = {
        "type": "if_command",
        "condition": p[2],
    }

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
    | term TIMES factor
    | term DIVIDE factor
    |term MODULUS factor"""

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


# <SIMPLE-COMMAND-ELEMENT> ::= <WORD>
#                           |  <ASSIGNMENT-WORD>
#                           |  <REDIRECTION>
# def p_simple_command_element(p):
#     """simple_command_element : IDENTIFIER
#     | assignment_word
#     | echo_command"""
#     p[0] = p[1]

# # <SIMPLE-COMMAND> ::=  <SIMPLE-COMMAND-ELEMENT>
# #                    |  <SIMPLE-COMMAND> <SIMPLE-COMMAND-ELEMENT>
# def p_simple_command(p):
#     """simple_command : simple_command_element
#     | simple_command simple_command_element"""
#     p[0] = {
#         "type": "simple_command",
#         "elements": p[1] if len(p) == 2 else p[1] + [p[2]],
#     }

# # <COMMAND> ::=  <SIMPLE-COMMAND>
# #             |  <SHELL-COMMAND>
# #             |  <SHELL-COMMAND> <REDIRECTION-LIST>
# def p_command(p):
#     """command : simple_command"""
#     p[0] = p[1]

# # <SHELL-COMMAND> ::=  <FOR-COMMAND>
# #                   |  <CASE-COMMAND>
# #                   |  while <COMPOUND-LIST> do <COMPOUND-LIST> done
# #                   |  until <COMPOUND-LIST> do <COMPOUND-LIST> done
# #                   |  <SELECT-COMMAND>
# #                   |  <IF-COMMAND>
# #                   |  <SUBSHELL>
# #                   |  <GROUP-COMMAND>
# #                   |  <FUNCTION-DEF>
# def p_shell_command(p):
#     """shell_command : if_command"""
#     p[0] = p[1]

# def p_pipeline(p):
#     """pipeline : pipeline PIPELINE newline pipeline
#     | command"""

# # <PIPELINE-COMMAND> ::= <PIPELINE>
# #                     |  '!' <PIPELINE>
# #                     |  <TIMESPEC> <PIPELINE>
# #                     |  <TIMESPEC> '!' <PIPELINE>
# #                     |  '!' <TIMESPEC> <PIPELINE>
# def p_pipeline_command(p):
#     """pipeline_command : pipeline
#     | NOT pipeline"""
#     p[0] = {
#         "type": "pipeline_command",
#         "negated": len(p) == 3,
#         "pipeline": p[2] if len(p) == 3 else p[1],
#     }

# """
# AND-OR Lists is a sequence of one or more pipelines separated
# by operators `&&` and `||` (equal precedence)

# A list is a sequence of one or more AND-OR lists separated by
# the operators `;` and `&`

# A `;` separator or <newline> cause the preceding AND-OR list to be
# executed sequentially; an `&` separator causes asynchronous execution
# of the preceding AND-OR list.

# false && echo foo || echo bar 
# true || echo foo && echo bar

# The term `compound-list` -> sequence of lists separated by <newline>
# characters that can be preceded or followed by an arbitrary number of 
# <newline> characters
# """


# def p_newline(p):
#     """newline : NEWLINE
#     | NEWLINE newline"""
#     p[0] = p[1]

# # <LIST1> ::=   <LIST1> '&&' <NEWLINE-LIST> <LIST1>
# #            |  <LIST1> '||' <NEWLINE-LIST> <LIST1>
# #            |  <LIST1> '&' <NEWLINE-LIST> <LIST1>
# #            |  <LIST1> ';' <NEWLINE-LIST> <LIST1>
# #            |  <LIST1> '\n' <NEWLINE-LIST> <LIST1>
# #            |  <PIPELINE-COMMAND>
# def p_list_1(p):
#     """list1 : list1 AND newline list1
#     | list1 OR newline list1
#     | list1 SINGLE_AND newline list1
#     | list1 SEMICOLON newline list1
#     | list1 NEWLINE newline list1
#     | pipeline_command"""
#     p[0] = {
#         "type": "list1",
#         "left": p[1],
#         "operator": p[2],
#         "right": p[4],
#     }

# # <LIST0> ::=   <LIST1> '\n' <NEWLINE-LIST>
# #            |  <LIST1> '&' <NEWLINE-LIST>
# #            |  <LIST1> ';' <NEWLINE-LIST>
# def p_list_0(p):
#     """list : list1 NEWLINE newline
#     | list1 SINGLE_AND newline
#     | list1 SEMICOLON newline"""
#     p[0] = {
#         "type": "list_0",
#         "left": p[1],
#         "operator": p[2],
#         "right": p[3],
#     }

# # <LIST> ::=   <NEWLINE-LIST> <LIST0>
# def p_list(p):
#     """list : newline list"""
#     p[0] = {
#         "type": "list",
#         "left": p[1],
#         "right": p[2],
#     }

# # <COMPOUND-LIST> ::=  <LIST>
# #                   |  <NEWLINE-LIST> <LIST1>
# def p_compound_list(p):
#     """compound_list : list
#     | newline list"""
#     p[0] = {
#         "type": "compound_list",
#         "left": p[1],
#         "right": p[2] if len(p) > 2 else None,
#     }

# # <ELIF-CLAUSE> ::= elif <COMPOUND-LIST> then <COMPOUND-LIST>
# #            | elif <COMPOUND-LIST> then <COMPOUND-LIST> else <COMPOUND-LIST>
# #            | elif <COMPOUND-LIST> then <COMPOUND-LIST> <ELIF-CLAUSE>
# def p_elif_caluse(p):
#     """elif_clause : ELIF compound_list THEN compound_list
#     | ELIF compound_list THEN compound_list ELSE compound_list
#     | ELIF compound_list THEN compound_list elif_clause"""
#     p[0] = {
#         "type": "elif_clause",
#         "condition": p[2],
#         "then": p[4],
#         "else": p[6] if len(p) > 5 else None,
#     }

# # <IF-COMMAND> ::= if <COMPOUND-LIST> then <COMPOUND-LIST> fi
# #           | if <COMPOUND-LIST> then <COMPOUND-LIST> else <COMPOUND-LIST> fi
# #           | if <COMPOUND-LIST> then <COMPOUND-LIST> <ELIF-CLAUSE> fi
# def p_if_command(p):
#     """if_command : IF compound_list THEN compound_list FI
#     | IF compound_list THEN compound_list ELSE compound_list FI
#     | IF compound_list THEN compound_list elif_clause FI"""
#     p[0] = {
#         "type": "if_command",
#         "condition": p[2],
#         "then": p[4],
#         "else": p[6] if len(p) > 5 else None,
#     }

def p_error(p):
    if p:
        print("Syntax error at: ", p.value)
    else:
        print("Syntax error at EOF")

# sample input for if
# if true; then echo "true"; fi

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
