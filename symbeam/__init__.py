from sympy.abc import x


def check_x_variable(expr):
    """Checks if the independent x-variable is present on a given expression.

    Parameters
    ----------
    expr : SymPy object
    Expression to be verified

    Raises
    ------
    RuntimeError
    If the independent x-variable is found on some coordinate/expression
    """
    if x in expr.free_symbols:
        raise RuntimeError(
            "The independent x-variable must not be contained in the "
            + "definition of a point coordinate."
        )
