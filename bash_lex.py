from ply.src.ply import lex

reserved = {
    # "!": "NOT",  # Pipelines
    # ":": "EXPANSION",
    # ".": "READ_FILE",
    # Conditional Constructs
    # "[[": "CONDITIONAL_CONST_OPEN",
    # "]]": "CONDITIONAL_CONST_CLOSE",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "elif": "ELIF",
    "fi": "FI",
    "select": "SELECT",
    "case": "CASE",
    "esac": "ESAC",
    # Command Grouping
    "{": "COMMAND_GROUPING_OPEN",
    "}": "COMMAND_GROUPING_CLOSE",
    # Looping Constructs
    "do": "DO",
    "done": "DONE",
    "while": "WHILE",
    "until": "UNTIL",
    "continue": "CONTINUE",
    # Shell functions
    "function": "FUNCTION",
    # Shell Commands
    "alias": "ALIAS",
    "bg": "BG",
    "bind": "BIND",
    "break": "BREAK",
    "builtin": "BUILTIN",
    "cd": "CD",
    "exit": "EXIT",
    "command": "COMMAND",
    "declare": "DECLARE",
    "dirs": "DIRS",
    "disown": "DISOWN",
    "echo": "ECHO",
    "exec": "EXEC",
    "enable": "ENABLE",
    "export": "EXPORT",
}

# Below are the list of tokens
tokens = (
    "IDENTIFIER",
    "STRING",
    "COMMENT",
    "LPAREN",
    "RPAREN",
    "CONDITIONAL_CONST_OPEN",
    "CONDITIONAL_CONST_CLOSE",
    "NOT",
    "EXPANSION",
    "READ_FILE",
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "GREATER",
    "LESSER",
    "NOTEQUAL",
    "EQUALS",
    "GREATEREQUAL",
    "LESSEREQUAL",
    "NUMBER",
) + tuple(reserved.values())

t_ignore = r" \t"

# Specifications of tokens written in regex
# t_ must match the exact name of the tokens
# specified above

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_CONDITIONAL_CONST_OPEN = r"\[\["
t_CONDITIONAL_CONST_CLOSE = r"\]\]"
t_NOT = r"!"
t_EXPANSION = r":"
t_READ_FILE = r"\."
t_EQUALS = r"="
t_PLUS = r"\+"
t_MINUS = r"\-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"/"
t_GREATER = r"-gt"
t_LESSER = r"-lt"
t_GREATEREQUAL = r"-ge"
t_LESSEREQUAL = r"-le"
t_NOTEQUAL = r"-ne"


def t_IDENTIFIER(t):
    # NOTE: idts this refex identifier is correct
    r"[a-zA-Z][a-zA-Z0-9\-]*"
    t.type = reserved.get(t.value, "IDENTIFIER")
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_STRING(t):
    r"(\"[^\"]*\"|\'[^\']*\')"
    return t


def t_COMMENT(t):
    r"\#.*"
    return t


def t_error(t):
    print(f"Illegal character at {t.value[0]!r}")
    t.lexer.skip(1)


lexer = lex.lex()

# if __name__ == "__main__":
#     test_input = """
# #This is a comment
# echo "hi"
# echo 'hi'
# a = 10
# if [[ 10 -eq 10]]; then
#     echo "hi"
# fi
# """
#     lexer.input(test_input)
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break
#         data = {
#             "type": tok.type,
#             "value": tok.value,
#             "lineno": tok.lineno,
#             "lexpos": tok.lexpos,
#         }
#         print(data)
