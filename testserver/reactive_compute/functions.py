##File with all computational functions


def add(args):
    """
    Addition Function.
    """
    return sum(args)


def sub(args):
    """
    Subtraction Function.
    """
    return (args[0] - args[1])


def mul(args):
    """
    Multiplication function.
    """
    prod = 1
    for arg in args:
        prod *= arg
    return prod


class Functions(object):
    """
    Class to store mapping between function name and function
    implementation.
    """

    mapping = {
        'ADD': add,
        'SUB': sub,
        'MUL': mul
        }
