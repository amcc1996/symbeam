"""Load module.

Defines the point force and moment classes, which can fundamentally be interpreted as
strucutred variables with additional data verifications.

Also, it provides the distributed_load class. In contrast to the point counterpart,
distributed loads have a slightly more intricate structure, as they require the
computation of the net force and associated position along the beam, for the construction
of the equilibirum equations.

..module:: load
  :synopsis: Main load class

..moduleauthor:: A. M. Couto Carneiro <amcc@fe.up.pt>
"""
import sympy as sym

from sympy.abc import x


# ========================================================================= distributed_load
class distributed_load:
    """Distributed transverse load class."""

    def __init__(self, x_start, x_end, expression):
        self.x_start = sym.sympify(x_start)
        self.x_end = sym.sympify(x_end)
        self.expression = sym.sympify(expression)

        self.equivalent_magnitude = sym.integrate(
            self.expression, (x, self.x_start, self.x_end)
        )
        if self.equivalent_magnitude == sym.sympify(0):
            self.equivalent_coord = sym.sympify(0)
        else:
            self.equivalent_coord = (
                sym.integrate(self.expression * x, (x, self.x_start, self.x_end))
                / self.equivalent_magnitude
            )


# =============================================================================== point_load
class point_load:
    """Concentrated transverse point load."""

    def __init__(self, x_coord, value):
        self.x_coord = sym.sympify(x_coord)
        self.value = sym.sympify(value)


# ============================================================================= point_moment
class point_moment:
    """Concentrated point moment."""

    def __init__(self, x_coord, value):
        self.x_coord = sym.sympify(x_coord)
        self.value = sym.sympify(value)


# ==========================================================================================
