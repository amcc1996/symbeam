# Import modules
# --------------
# Symbolic Python Package SymPy
import sympy as sym
# Global symbolic variables used within symbeam
from symbeam import x, E, I
# Beam supports classes
from symbeam.point import pin
# Loads classes
from symbeam.load import distributed_load, point_load
# ===================================================================================== beam
class beam:
    """Beam main class.
    """
    def __init__(self, length, x0=0):
        """Beam constructor.
        """
        # Initialise the length and startig point of the beam.
        self.length = sym.sympify(length)
        self.x0 = sym.sympify(x0)

        # Check the consitency of the input. Only one symbol is permitted for the geometry
        # definition, in order to facilitate the creation of the segments.
        # If the beam starts at zero it's fine.
        starts_at_zero = self.x0 == sym.sympify(0)
        if len(self.length.free_symbols) != len(self.x0.free_symbols) and not(starts_at_zero):
            raise RuntimeError("The number of symbols set for the length and initial"
                               + " beam coordinate is distinct. Only one symbol is"
                               + " allowed for the definition of the geometry")

        # Make sure the initial position and length use the same symbol.
        if len(self.length.free_symbols) == 1 and not(starts_at_zero):
            if next(iter(self.length.free_symbols)) != next(iter(self.x0.free_symbols)):
                raise RuntimeError("The length and initial coordinate of the beam have"
                                   + " been defined with distinct symbols.")

        # Initialise the list storing all the input information for the beam
        self.support_list = []
        self.distributed_load_list = []
        self.point_load_list = []
        self.young_segment_list = [property_segment(self.x0, self.x0 + self.length, E)]
        self.inertia_segment_list = [property_segment(self.x0, self.x0 + self.length, E)]
        self.segment_list = []
        self.loads_list = []
    # -------------------------------------------------------------------------- add_support
    def add_support(self, x_coord, type):
        """Appends a new support to the list of input supports.
        """
        if type.lower() == 'pin':
            new_point = pin(x_coord)

        for point in self.support_list:
            if point.x_coord == new_point.x_coord:
                raise RuntimeError("Repeated support for x = {0}.".format(new_point.x_coord))

        self.support_list.append(new_point)
    # ----------------------------------------------------------------- add_distributed_load
    def add_distributed_load(self, x_start, x_end, expression):
        """Appends a new distributed load to the list of input distributed loads.
        """
        new_load = distributed_load(x_start, x_end, expression)
        self.distributed_load_list.append(new_load)
    # ----------------------------------------------------------------------- add_point_load
    def add_point_load(self, x_coord, value):
        """Appends a new point load to the list of input point loads.
        """
        new_load = point_load(x_coord, value)
        self.point_load_list.append(new_load)
    # ---------------------------------------------------------------------------- set_young
    def set_young(self, x_start, x_end, value):
        """Sets the young modulus of a portion of the beam.
        """
        new_young = property_segment(x_start, x_end, value)
        self.young_segment_list.append(new_young)
    # -------------------------------------------------------------------------- set_inertia
    def set_inertia(self, x_start, x_end, value):
        """Sets the second moment of area of a portion of the beam.
        """
        new_inertia = property_segment(x_start, x_end, value)
        self.inertia_segment_list.append(new_inertia)
    # ------------------------------------------------------------------------- set_segments
    def set_segments(self):
        pass

    def solve_reactions(self):
        pass

    def solve_internal_loads(self):
        pass

    def solve_deflection(self):
        pass

    def plot(self):
        pass

class property_segment:
    def __init__(self, x_start, x_end, value):
        self.x_start = sym.sympify(x_start)
        self.x_end = sym.sympify(x_end)
        self.value = sym.sympify(value)

class segment:
    def __init__(self, x_start, x_end, distributed_load, young, inertia):
        pass
