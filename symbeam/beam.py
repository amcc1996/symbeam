# Import modules
# --------------
# Symbolic Python Package SymPy
import sympy as sym
# Global symbolic variables used within symbeam
from symbeam import x, E, I, tol
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
        self.point_moment_list = []
        self.young_segment_list = [property_segment(self.x0, self.x0 + self.length, E)]
        self.young_default = True
        self.inertia_segment_list = [property_segment(self.x0, self.x0 + self.length, E)]
        self.inertia_default = True
        self.segment_list = []
        self.loads_list = []
    # -------------------------------------------------------------------------- add_support
    def add_support(self, x_coord, type):
        """Appends a new support to the list of input supports.
        """
        self.check_inside_beam(x_coord)
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
        self.check_coordinates(x_start, x_end)
        new_load = distributed_load(x_start, x_end, expression)
        self.distributed_load_list.append(new_load)
    # ----------------------------------------------------------------------- add_point_load
    def add_point_load(self, x_coord, value):
        """Appends a new point load to the list of input point loads.
        """
        self.check_inside_beam(x_coord)
        new_load = point_load(x_coord, value)
        self.point_load_list.append(new_load)
    # --------------------------------------------------------------------- add_point_moment
    def add_point_moment(self, x_coord, value):
        """Appends a new point moment to the list of input point moments.
        """
        self.check_inside_beam(x_coord)
        new_moment = point_load(x_coord, value)
        self.point_moment_list.append(new_moment)
    # ---------------------------------------------------------------------------- set_young
    def set_young(self, x_start, x_end, value):
        """Sets the young modulus of a portion of the beam.
        """
        self.check_coordinates(x_start, x_end)
        # If the user specifies the property explicitely, reset the default values
        if self.young_default:
            self.young_default = False
            self.young_segment_list = []
        new_young = property_segment(x_start, x_end, value)
        self.young_segment_list.append(new_young)
    # -------------------------------------------------------------------------- set_inertia
    def set_inertia(self, x_start, x_end, value):
        """Sets the second moment of area of a portion of the beam.
        """
        self.check_coordinates(x_start, x_end)
        # If the user specifies the property explicitely, reset the default values
        if self.inertia_default:
            self.inertia_default = False
            self.inertia_segment_list = []
        new_inertia = property_segment(x_start, x_end, value)
        self.inertia_segment_list.append(new_inertia)
    # ---------------------------------------------------------------- check_beam_properties
    def check_beam_properties(self):
        """Verifies is the beam properties have been consistently set along the entire
        length of the beam.
        """
        # If the length is given as a variable, substitute by 1 for ease of comparison.
        length_numeric = self.length.subs({self.length : 1.0})
        x0_numeric = self.x0.subs({self.length : 1.0})
        young_x_start_numeric = [item.x_start.subs({self.length : 1.0}) for item in self.young_segment_list]
        young_x_end_numeric = [item.x_end.subs({self.length : 1.0}) for item in self.young_segment_list]
        inertia_x_start_numeric = [item.x_start.subs({self.length : 1.0}) for item in self.inertia_segment_list]
        inertia_x_end_numeric = [item.x_end.subs({self.length : 1.0}) for item in self.inertia_segment_list]

        length_young = 0.0
        length_inertia = 0.0

        # Quick check Young modulus specification.
        for i in range(len(self.young_segment_list)):
            if young_x_start_numeric[i] < x0_numeric:
                raise RuntimeError("Yound modulus specified for segment starting outside the beam.")
            elif young_x_end_numeric[i] > length_numeric + x0_numeric:
                raise RuntimeError("Young modulus specified for segment ending outside the beam.")
            else:
                length_young = length_young + young_x_end_numeric[i] - young_x_start_numeric[i]

        if abs(length_young - length_numeric) > tol:
            raise RuntimeError("Inconsistent specification of the Young modulus along the beam."
                               + " There are either repeated or missing segments of the beam.")

        # Now a more thorough verification.
        for i in range(len(self.young_segment_list)):
            for j in range(len(self.young_segment_list)):
                if j != i:
                    is_on_the_right = (young_x_end_numeric[j] < young_x_start_numeric[i] + tol)
                    is_on_the_left = (young_x_start_numeric[j] > young_x_end_numeric[i] - tol)
                    if not(is_on_the_left or is_on_the_right):
                        raise RuntimeError("Inconsistent specification of the Young modulus along the beam."
                                           + " There are either repeated or missing segments of the beam.")

        # Quick check secnod moment of area specification.
        for i in range(len(self.inertia_segment_list)):
            if inertia_x_start_numeric[i] < x0_numeric:
                raise RuntimeError("Moment of inertia specified for segment starting outside the beam.")
            elif inertia_x_end_numeric[i] > length_numeric + x0_numeric:
                raise RuntimeError("Moment of inertia specified for segment ending outside the beam.")
            else:
                length_inertia = length_inertia + inertia_x_end_numeric[i] - inertia_x_start_numeric[i]

        if abs(length_inertia - length_numeric) > tol:
            raise RuntimeError("Inconsistent specification of the moment of inertia along the beam."
                               + " There are either repeated or missing segments of the beam.")

        # Now a more thorough verification.
        for i in range(len(self.inertia_segment_list)):
            for j in range(len(self.inertia_segment_list)):
                if j != i:
                    is_on_the_right = (inertia_x_end_numeric[j] < inertia_x_start_numeric[i] + tol)
                    is_on_the_left = (inertia_x_start_numeric[j] > inertia_x_end_numeric[i] - tol)
                    if not(is_on_the_left or is_on_the_right):
                        raise RuntimeError("Inconsistent specification of the moment of inertia along the beam."
                                           + " There are either repeated or missing segments of the beam.")
    # -------------------------------------------------------------------- check_coordinates
    def check_coordinates(self, x_start, x_end):
        """Checks if the input segment coordinates are valid.
        """
        x_start_symbol = sym.sympify(x_start)
        x_end_symbol = sym.sympify(x_end)

        if len(x_start_symbol.free_symbols) > 1:
            raise RuntimeError("More than one symbol used for starting coordinate.")

        if len(x_end_symbol.free_symbols) > 1:
            raise RuntimeError("More than one symbol used for coordinate coordinate.")

        if len(x_start_symbol.free_symbols) == 1:
            if next(iter(x_start_symbol.free_symbols)) != self.length:
                raise RuntimeError("Distinct symbols have been used for coordinate along the"
                                   + " the beam and beam length.")

        if len(x_end_symbol.free_symbols) == 1:
            if next(iter(x_end_symbol.free_symbols)) != self.length:
                raise RuntimeError("Distinct symbols have been used for coordinate along the"
                                   + " the beam and beam length.")

        x_start_numeric = x_start_symbol.subs({self.length : 1})
        x_end_numeric = x_end_symbol.subs({self.length : 1})
        if abs(x_start_numeric - x_end_numeric) < tol:
            raise RuntimeError("The specified beam segment is too short. The poits are overlapping.")
        elif x_start_numeric > x_end_numeric:
            raise RuntimeError("The starting coordinate is greater than the ending coordinte.")
    # -------------------------------------------------------------------- check_inside_beam
    def check_inside_beam(self, x_coord):
        """Chekcs if a given coordinate is valid and lies inside the beam domain.
        """
        x_coord_symbol = sym.sympify(x_coord)

        if len(x_coord_symbol.free_symbols) > 1:
            raise RuntimeError("More than one symbol used for coordinate.")

        if len(x_coord_symbol.free_symbols) == 1:
            if next(iter(x_coord_symbol.free_symbols)) != self.length:
                raise RuntimeError("Distinct symbols have been used for coordinate along the"
                                   + " the beam and beam length.")

        x_coord_numeric = x_coord_symbol.subs({self.length : 1})
        length_numeric = self.length.subs({self.length : 1.0})
        x0_numeric = self.x0.subs({self.length : 1.0})
        if not(x0_numeric - tol <= x_coord_numeric <= x0_numeric + length_numeric + tol):
            raise RuntimeError("The specified coordinate lies outside the beam.")
    # ------------------------------------------------------------------------- set_segments
    def set_segments(self):
        """Create the beam segments, such that the properties and loads are piecewise
        continuous within each segments and, therefore, are properly setup for symbolic
        integration.
        """
        # Start by defining all numeric variables in order to be able sort the segments
        length_numeric = self.length.subs({self.length : 1.0})
        x0_numeric = self.x0.subs({self.length : 1.0})
        young_x_start_numeric = [item.x_start.subs({self.length : 1.0}) for item in self.young_segment_list]
        young_x_end_numeric = [item.x_end.subs({self.length : 1.0}) for item in self.young_segment_list]
        inertia_x_start_numeric = [item.x_start.subs({self.length : 1.0}) for item in self.inertia_segment_list]
        inertia_x_end_numeric = [item.x_end.subs({self.length : 1.0}) for item in self.inertia_segment_list]

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
        self.x_start = sym.sympify(x_start)
        self.x_end = sym.sympify(x_end)
        self.distributed_load = distributed_load
        self.young = sym.sympify(young)
        self.inertia = sym.sympify(inertia)
