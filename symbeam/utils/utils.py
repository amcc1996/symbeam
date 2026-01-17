"""Utility functions for tests, namely, Euler-Bernoulli stiffness matrix, Hermite
polynomials, and computation of rotation, bending moment, and shear force.

..module:: utils.utils
  :synopsis: Utility functions for tests

..moduleauthor:: A. M. Couto Carneiro <amcc@fe.up.pt>
"""

from typing import List

import sympy


x = sympy.symbols("x")


def hermite_polynomials(
    x: sympy.Symbol, x0: sympy.Symbol, L: sympy.Symbol
) -> List[sympy.Expr]:
    """Returns the cubic Hermite polynomials.

    Parameters
    ----------
    x : sympy.Symbol
        Independent variable.
    x0 : sympy.Symbol
        Element initial coordinate.
    L : sympy.Symbol
        Element length.

    Returns
    -------
    N : List[sympy.Expr]
        List of cubic Hermite polynomials.
    """
    N1 = 1 - 3 * ((x - x0) / L) ** 2 + 2 * ((x - x0) / L) ** 3
    N2 = (x - x0) - 2 * ((x - x0) ** 2) / L + ((x - x0) ** 3) / (L**2)
    N3 = 3 * ((x - x0) / L) ** 2 - 2 * ((x - x0) / L) ** 3
    N4 = -((x - x0) ** 2) / L + ((x - x0) ** 3) / (L**2)

    return [N1, N2, N3, N4]


def euler_bernoulli_stiff_matrix(
    E: sympy.Symbol, I: sympy.Symbol, L: sympy.Symbol
) -> sympy.Matrix:
    """Returns the Euler-Bernoulli beam element stiffness matrix.

    Parameters
    ----------
    E : sympy.Symbol
        Young's modulus.
    I : sympy.Symbol
        Second moment of area.
    L : sympy.Symbol
        Element length.

    Returns
    -------
    k : sympy.Matrix
        Element stiffness matrix.
    """
    k = (
        (E * I)
        / (L**3)
        * sympy.Matrix(
            [
                [12, 6 * L, -12, 6 * L],
                [6 * L, 4 * L**2, -6 * L, 2 * L**2],
                [-12, -6 * L, 12, -6 * L],
                [6 * L, 2 * L**2, -6 * L, 4 * L**2],
            ]
        )
    )

    return k


def compute_rotation(displacement: sympy.Expr, x: sympy.Symbol) -> sympy.Expr:
    """Computes the rotation as the first derivative of the displacement.

    Parameters
    ----------
    displacement : sympy.Expr
        Displacement expression.
    x : sympy.Symbol
        Independent variable.

    Returns
    -------
    rotation : sympy.Expr
        Rotation expression.
    """
    rotation = sympy.diff(displacement, x)

    return rotation


def compute_bending_moment(
    displacement: sympy.Expr, E: sympy.Symbol, I: sympy.Symbol, x: sympy.Symbol
) -> sympy.Expr:
    """Computes the bending moment as the second derivative of the displacement times EI.

    Parameters
    ----------
    displacement : sympy.Expr
        Displacement expression.
    E : sympy.Symbol
        Young's modulus.
    I : sympy.Symbol
        Second moment of area.
    x : sympy.Symbol
        Independent variable.

    Returns
    -------
    bending_moment : sympy.Expr
        Bending moment expression.
    """
    bending_moment = E * I * sympy.diff(displacement, x, 2)

    return bending_moment


def computes_shear_force(bending_moment: sympy.Expr, x: sympy.Symbol) -> sympy.Expr:
    """Computes the shear force as the third derivative of the displacement times EI.

    Parameters
    ----------
    bending_moment : sympy.Expr
        Bending moment expression.
    x : sympy.Symbol
        Independent variable.

    Returns
    -------
    shear_force : sympy.Expr
        Shear force expression.
    """
    shear_force = -sympy.diff(bending_moment, x)

    return shear_force
