import ply.yacc as yacc

from exceptions.missing_parameter_function_argument_exception import MissingParameterFunctionArgumentException
from core.tokenizer import tokens
from exceptions.duplicate_state_exception import DuplicateStateException
from exceptions.variable_undefined_exception import VariableUndefinedException

precedence = (
    ('left', 'IF'),
    ('left', 'THEN'),
    ('left', 'ELSEIF'),
    ('left', 'COLONEQ'),
    ('left', 'COLON'),
    ('left', 'OUTPUT'),
    ('left', 'OID'),
    ('nonassoc', 'GREATEREQUAL', 'LESSEQUAL'),
)

states = []


def make_3_elements_list(comparison):
    n = len(comparison)
    i = iter(comparison)

    return [[next(i) for _ in range(size)] for size in [3] * (n // 3)]


# Program : Block Program
def p_program(p):
    """program : block program"""
    p[0] = p[1], p[2]


# Program : Block
def p_program_1(p):
    """program : block"""
    p[0] = p[1]


def p_state(p):
    """
        STATE : LPAREN SID COMMA Rnumber COMMA Rnumber RPAREN
                    | LPAREN SID COLON NONINPUT  COMMA Rnumber COMMA Rnumber RPAREN
                    | LPAREN SID COMMA Rnumber COMMA Rnumber COMMA Rnumber COMMA Rnumber RPAREN
                    | LPAREN SID COLON NONINPUT  COMMA Rnumber COMMA Rnumber COMMA Rnumber COMMA Rnumber RPAREN
    """
    if p[2] in states:
        raise DuplicateStateException('Duplicate State Found!')
    states.append(p[2])

    captured = []

    for i in range(1, len(p)):
        captured.append(p[i])

    p[0] = captured


# Block : STATE COLON Statement
def p_block(p):
    """block : STATE COLON Statement"""

    p[0] = p[1], p[2], p[3]


def p_comparison_binop(p):
    """comparison : INSAMPLE GREATEREQUAL VARIABLE
                   | INSAMPLE LESSEQUAL VARIABLE
                   | INSAMPLE LESS VARIABLE
                   | INSAMPLE GREATER VARIABLE"""

    if p[3] not in variables:
        raise VariableUndefinedException(f'Undefined variable: {p[3]}')

    p[0] = p[1], p[2], p[3]


def p_comparison_binop_recursive(p):
    """comparison : comparison AND comparison"""

    p[0] = *p[1], *p[3]


def p_statement_if_block(p):
    """IfBlock : IF LPAREN comparison RPAREN THEN BStatement"""
    p[0] = p[1], p[2], make_3_elements_list(p[3]), p[4], p[5], p[6]


def p_statement_if(p):
    """Statement : IfBlock"""
    p[0] = ('ifBlock', p[1]),


def p_statement_else_block(p):
    """ElseBlock : ELSEIF LPAREN comparison RPAREN THEN BStatement"""
    p[0] = p[1], p[2], make_3_elements_list(p[3]), p[4], p[5], p[6]


def p_statement_else_recursive(p):
    """ElseBlock : ElseBlock ElseBlock"""

    if p[2][0][0] == 'elseif':
        p[0] = p[1], *p[2]
    else:
        p[0] = p[1], p[2]


def p_statement_if_and_else_block(p):
    """Statement : IfBlock ElseBlock"""
    else_block = p[2]
    if p[2][0] == 'elseif':
        else_block = (else_block,)
    p[0] = ('ifBlock', p[1]), ('elseBlock', else_block)


# Statement : BStatement
def p_statement_2(p):
    """Statement : BStatement"""
    p[0] = p[1]


# OutputValue
def p_output_value(p):
    """
    OutputValue : OID
                | INSAMPLE
                | INSAMPLEPRIME
    """

    if p[1] == "insampleprime" and len(p.stack[1].value) < 10:
        raise MissingParameterFunctionArgumentException("Unable to find d' and mean'")

    p[0] = p[1]


variables = {}


# OutputStatement : OUTPUT OutputValue
def p_output(p):
    """OutputStatement : OUTPUT OutputValue"""
    p[0] = p[1], p[2]


# GotoStatement : GOTO SID
def p_goto(p):
    """GotoStatement : GOTO SID"""
    p[0] = p[1], p[2]


# AssignmentStatement: VARIABLE COLONEQ INSAMPLE
def p_assignment(p):
    """AssignmentStatement : VARIABLE COLONEQ INSAMPLE"""

    variables[p[1]] = True
    p[0] = p[1]


def p_assignment_recursive(p):
    """AssignmentStatement : AssignmentStatement COMMA AssignmentStatement"""

    if type(p[3]) != str:
        p[0] = p[1], *p[3]
    else:
        p[0] = p[1], p[3]


def p_bstatement_with_assignment(p):
    """
    BStatement : AssignmentStatement SEMICOLON OutputStatement SEMICOLON GotoStatement
    """
    new_p_1 = p[1]
    if isinstance(new_p_1, str):
        new_p_1 = (new_p_1,)

    p[0] = ('assignment', list(new_p_1)), p[3], p[5]


def p_bstatement_without_assignment(p):
    """
    BStatement : OutputStatement SEMICOLON GotoStatement
    """

    p[0] = p[1], p[3]


# Rnumber: NUMBER
def p_rnumber(p):
    """Rnumber : NUMBER"""
    p[0] = p[1]


# Rnumber: NUMBER SLASH NUMBER
def p_rnumber_1(p):
    """Rnumber : NUMBER SLASH NUMBER"""
    p[0] = p[1], p[2], p[3]


def p_lap(p):
    """Rnumber : LAP LPAREN NUMBER COMMA NUMBER RPAREN"""

    p[0] = 1.3


# handle parsing errors
def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))


def make_parser():
    parser = yacc.yacc()
    return parser
