import ply.lex as lex
import ply.yacc as yacc


reserved = {
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "while": "WHILE",
    "do": "DO",
    "for": "FOR",
    "to": "TO",
    "int": "INT",
    "float": "FLOAT",
    "bool": "BOOL",
    "true": "TRUE",
    "false": "FALSE",
}


tokens = [
    "INT",
    "FLOAT",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "POWER",
    "MOD",
    "EQUALS",
    "DOUBLE_EQUALS",
    "ID",
    "POSTFIX",
    "PREFIX",
]

t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_POWER = r"\^"
t_MOD = r"%"
t_EQUALS = r"="
t_DOUBLE_EQUALS = r"=="
t_ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
t_POSTFIX = r"postfix"
t_PREFIX = r"prefix"
t_ignore = " \t"

var_dict = {}
postfix = ""


def t_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_INT(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")


def p_assign(p):
    "assign : ID EQUALS expression"
    var_dict[p[1]] = p[3]


def p_expression(p):
    """assign : expression"""
    p[0] = p[1]


def p_double_equals(p):
    "expression : expression DOUBLE_EQUALS expression"
    if p[1] == p[3]:
        p[0] = "yes"
    else:
        p[0] = "no"


# E -> E + T
def p_expression_plus(p):
    """expression : expression PLUS term"""
    global postfix
    p[0] = p[1] + p[3]
    postfix = postfix + "+"


# E -> E - T
def p_expression_minus(p):
    """expression : expression MINUS term"""
    global postfix
    p[0] = p[1] - p[3]
    postfix = postfix + "-"


# E -> T
def p_expression_term(p):
    "expression : term"
    p[0] = p[1]


# T -> T * F
def p_term_times(p):
    """term : term TIMES factor"""
    global postfix
    p[0] = p[1] * p[3]
    postfix = postfix + "*"


# T -> T / F
def p_term_divide(p):
    "term : term DIVIDE factor"
    global postfix
    if p[3] == 0:
        print("Can't divide by 0")
        raise ZeroDivisionError("integer division by 0")
    p[0] = p[1] / p[3]
    postfix = postfix + "/"


# T -> F
def p_term_factor(p):
    "term : factor"
    p[0] = p[1]


# F -> F ^ F
def p_factor_power(p):
    "factor : factor POWER factor"
    global postfix
    p[0] = p[1] ** p[3]
    postfix = postfix + "^"


# F -> F % F
def p_factor_mod(p):
    "factor : factor MOD factor"
    global postfix
    p[0] = p[1] % p[3]
    postfix = postfix + "%"


# F -> -F
def p_factor_unary(p):
    "factor : MINUS factor"
    global postfix
    p[0] = -p[2]
    postfix = postfix + "-"


# F -> ID
def p_factor_id(p):
    "factor : ID"
    if p[1] not in var_dict:
        print("invalid input '%s'" % p[1])
        raise NameError("Undefined variable")
    p[0] = var_dict[p[1]]


# F -> INT
def p_factor_number(p):
    "factor : INT"
    global postfix
    p[0] = p[1]
    postfix = postfix + str(p[0])


# F -> FLOAT
def p_factor_float(p):
    "factor : FLOAT"
    global postfix
    p[0] = p[1]
    postfix = postfix + str(p[0])


# F -> (E)
def p_factor_expr(p):
    "factor : LPAREN expression RPAREN"
    p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error at '%s'" % p.value)
    quit()

lexer = lex.lex()
parser = yacc.yacc()

while True:
    postfix = ""
    try:
        s = input(">>> ")
    except EOFError:
        break
    try:
        if var_dict[s]:
            print(var_dict[s])
        continue
    except KeyError:
        pass

    temp = ""
    if s == "exit":
        print("Exiting...")
        break
    if "postfix" in s:
        temp = s
        s = s[8:-1]
    if "prefix" in s:
        temp = s
        s = s[7:-1]
        s = s[::-1]

    try:
        res = parser.parse(s)
        if res is not None:
            if "postfix" in temp:
                print(postfix)
            elif "prefix" in temp:
                print(postfix[::-1])
            else:
                print(res)
    except ZeroDivisionError:
        pass
    except NameError:
        pass
