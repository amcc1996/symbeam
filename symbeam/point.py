from abc import ABC, abstractmethod
import sympy as sym
from symbeam import x

class point(ABC):
    def __init__(self, x_coord):
        self.x_coord = sym.sympify(x_coord)
        self.reaction_force = sym.sympify(0)
        self.reaction_moment = sym.sympify(0)
        self.external_force = sym.sympify(0)
        self.external_moment = sym.sympify(0)

    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def has_reaction_force(self):
        pass

    @abstractmethod
    def has_reaction_moment(self):
        pass

    @abstractmethod
    def get_deflection_boundary_condition(self, list_deflection):
        pass

    @abstractmethod
    def get_rotation_boundary_condition(self, list_rotation):
        pass

    def has_deflection_condition(self):
        return self.is_method_empty(self.get_deflection_boundary_condition)

    def has_rotation_condition(self):
        return self.is_method_empty(self.get_rotation_boundary_condition)

    def set_geometric_boundary_conditions(self, list_rotation, list_deflection, equations):
        if self.has_rotation_condition():
            condition_equation = self.get_rotation_boundary_condition(self, list_rotation)
            equations.extend(condition_equation)

        elif self.has_deflection_condition():
            condition_equation = self.get_deflection_boundary_condition(self, list_deflection)
            equations.extend(condition_equation)


    @staticmethod
    def is_method_empty(func):
        """Detect if a method is empty by comparing the bytecode instructions with an
        empty function with and without docstring documentation.
        """
        def empty_func():
            pass

        def empty_func_with_doc():
            """Empty function with docstring."""
            pass

        return func.__code__.co_code == empty_func.__code__.co_code or \
            func.__code__.co_code == empty_func_with_doc.__code__.co_code

class pin(point):

    @staticmethod
    def get_name():
        return "Pinned Support"

    def has_reaction_force(self):
        return True

    def has_reaction_moment(self):
        return False

    def get_deflection_boundary_condition(self, list_deflection):
        fixed_equation = list_deflection[0].subs({x : self.x0})
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs({x : self.x0}) - list_deflection[1].subs({x : self.x0})
            equations = (fixed_equation, deflection_continuous)
        else:
            equations = (fixed_equation)

    def get_rotation_boundary_condition(self, list_rotation):
        if len(list_rotation) == 2:
            rotation_continuous = list_rotation[0].subs({x : self.x0}) - list_rotation[1].subs({x : self.x0})
            equations = (rotation_continuous)
        else:
            equations = ()

class continuity(point):

    @staticmethod
    def get_name():
        return "Continuity point"

    def has_reaction_force(self):
        return False

    def has_reaction_moment(self):
        return False

    def get_deflection_boundary_condition(self, list_deflection):
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs({x : self.x0}) - list_deflection[1].subs({x : self.x0})
            equations = (deflection_continuous)
        else:
            equations = ()

    def get_rotation_boundary_condition(self, list_rotation):
        if len(list_rotation) == 2:
            rotation_continuous = list_rotation[0].subs({x : self.x0}) - list_rotation[1].subs({x : self.x0})
            equations = (rotation_continuous)
        else:
            equations = ()
