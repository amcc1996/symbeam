import sympy as sym
from symbeam import x

class distributed_load:
    def __init__(self, x_start, x_end, expression):
        self.x_start = sym.sympify(x_start)
        self.x_end = sym.sympify(x_end)
        self.expression = sym.sympify(expression)
        
        self.equivalent_magnitude = sym.integrate(self.expression, (x, self.x_start, self.x_end))
        self.equivalent_coord = sym.integrate(self.expression * x, (x, self.x_start, self.x_end)) / self.equivalent_magnitude
        
class point_load:
    def __init__(self, x_coord, value):
        self.x_coord = sym.sympify(x_coord)
        self.value = sym.sympify(value)
