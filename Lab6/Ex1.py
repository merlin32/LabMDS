import re

def tokenize(expr):
    """Split an expression into numbers and operators."""
    return re.findall(r'\d+|[+\-*()]', expr)

def parse_factor(tokens, pos):
    """Parse a number or parenthesized expression."""
    if tokens[pos] == '(':
        val, pos = parse_expr(tokens, pos + 1)
        return val, pos + 1  # skip ')'
    return int(tokens[pos]), pos + 1

def parse_term(tokens, pos):
    """Parse multiplication using a loop for left-associativity."""
    left, pos = parse_factor(tokens, pos)
    # Use a loop to keep consuming multiplication operators from left to right
    while pos < len(tokens) and tokens[pos] == '*':
        right, pos = parse_factor(tokens, pos + 1)
        left = left * right
    return left, pos

def parse_expr(tokens, pos):
    """Parse addition and subtraction using a loop for left-associativity."""
    left, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        op = tokens[pos]
        right, pos = parse_term(tokens, pos + 1)
        if op == '+':
            left = left + right
        else:
            left = left - right
    return left, pos

def evaluate(expr):
    tokens = tokenize(expr)
    if not tokens:
        return 0
    result, _ = parse_expr(tokens, 0)
    return result

# Verification tests
tests = [
    ("2 + 3",         5),
    ("2 * 3 + 1",     7),
    ("10 - 3 - 2",    5),
    ("(10 - 3) * 2",  14),
]

if __name__ == "__main__":
    for expr, expected in tests:
        result = evaluate(expr)
        status = "OK" if result == expected else "ERROR"
        print(f"{expr:>16} = {result:<4}  expected {expected:<4} [{status}]")
