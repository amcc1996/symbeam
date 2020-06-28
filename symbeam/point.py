# Import modules
# --------------
# Abstract classes and methods
from abc import ABC, abstractmethod
# Symbolic Python Package, SymPy
import sympy as sym
# Global symbolic variables
from symbeam import x
# ==================================================================================== point
class point(ABC):
    """Abstract definition of a beam point.
    """
    def __init__(self, x_coord):
        self.x_coord = sym.sympify(x_coord)
        self.reaction_force = sym.sympify(0)
        self.reaction_moment = sym.sympify(0)
        self.external_force = sym.sympify(0)
        self.external_moment = sym.sympify(0)
    # ----------------------------------------------------------------------------- get_name
    @staticmethod
    @abstractmethod
    def get_name():
        """Returns the name of the type of point in question.
        """
        pass
    # ------------------------------------------------------------------- has_reaction_force
    @abstractmethod
    def has_reaction_force(self):
        """Flags if the current point support reactions forces.
        """
        pass
    # ------------------------------------------------------------------ has_reaction_moment
    @abstractmethod
    def has_reaction_moment(self):
        """Flags if the current point support reactions moments.
        """
        pass
    # ---------------------------------------------------- get_deflection_boundary_condition
    @abstractmethod
    def get_deflection_boundary_condition(self, list_deflection):
        """Establishes the deflection boundary condition on the current point.
        """
        pass
    # ------------------------------------------------------ get_rotation_boundary_condition
    @abstractmethod
    def get_rotation_boundary_condition(self, list_rotation):
        """Establishes the rotation boundary condition on the current point.
        """
        pass
    # ------------------------------------------------------------- has_deflection_condition
    def has_deflection_condition(self):
        """Flags if the current point enforces some boundary condition on the deflection.
        """
        return not(self.is_method_empty(self.get_deflection_boundary_condition))
    # --------------------------------------------------------------- has_rotation_condition
    def has_rotation_condition(self):
        """Flags if the current point enforces some boundary condition on the rotation.
        """
        return not(self.is_method_empty(self.get_rotation_boundary_condition))
    # ---------------------------------------------------- set_geometric_boundary_conditions
    def set_geometric_boundary_conditions(self, list_rotation, list_deflection, equations):
        """Sets the geometric boundary conditions on the global system of equations.
        """
        if self.has_rotation_condition():
            condition_equation = self.get_rotation_boundary_condition(list_rotation)
            equations.extend(condition_equation)

        if self.has_deflection_condition():
            condition_equation = self.get_deflection_boundary_condition(list_deflection)
            equations.extend(condition_equation)
    # ---------------------------------------------------------------------- is_method_empty
    @staticmethod
    def is_method_empty(func):
        """Detects if a method is empty by comparing the bytecode instructions with an
        empty function with and without docstring documentation.
        """
        def empty_func():
            pass

        def empty_func_with_doc():
            """Empty function with docstring."""
            pass

        return func.__code__.co_code == empty_func.__code__.co_code or \
            func.__code__.co_code == empty_func_with_doc.__code__.co_code
# ====================================================================================== pin
class pin(point):
    """Concrete implementation of a pinned support.
    """
    @staticmethod
    def get_name():
        return "Pinned Support"

    def has_reaction_force(self):
        return True

    def has_reaction_moment(self):
        return False

    def get_deflection_boundary_condition(self, list_deflection):
        fixed_equation = list_deflection[0].subs({x : self.x_coord})
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs({x : self.x_coord}) - list_deflection[1].subs({x : self.x_coord})
            equations = [fixed_equation, deflection_continuous]
        else:
            equations = [fixed_equation]

        return equations

    def get_rotation_boundary_condition(self, list_rotation):
        if len(list_rotation) == 2:
            rotation_continuous = list_rotation[0].subs({x : self.x_coord}) - list_rotation[1].subs({x : self.x_coord})
            equations = [rotation_continuous]
        else:
            equations = []

        return equations
# =============================================================================== continuity
class continuity(point):
    """Concrete implementation of a continuity point in a beam.
    """
    @staticmethod
    def get_name():
        return "Continuity point"

    def has_reaction_force(self):
        return False

    def has_reaction_moment(self):
        return False

    def get_deflection_boundary_condition(self, list_deflection):
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs({x : self.x_coord}) - list_deflection[1].subs({x : self.x_coord})
            equations = [deflection_continuous]
        else:
            equations = []

        return equations

    def get_rotation_boundary_condition(self, list_rotation):
        if len(list_rotation) == 2:
            rotation_continuous = list_rotation[0].subs({x : self.x_coord}) - list_rotation[1].subs({x : self.x_coord})
            equations = [rotation_continuous]
        else:
            equations = []

        return equations
# ==================================================================================== fixed
class fixed(point):
    """Concrete implementation of a fixed/clamped support.
    """
    @staticmethod
    def get_name():
        return "Fixed"

    def has_reaction_force(self):
        return True

    def has_reaction_moment(self):
        return True

    def get_deflection_boundary_condition(self, list_deflection):
        fixed_equation = list_deflection[0].subs({x : self.x_coord})
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs({x : self.x_coord}) - list_deflection[1].subs({x : self.x_coord})
            equations = [fixed_equation, deflection_continuous]
        else:
            equations = [fixed_equation]

        return equations

    def get_rotation_boundary_condition(self, list_rotation):
        fixed_equation = list_rotation[0].subs({x : self.x_coord})
        if len(list_rotation) == 2:
            rotation_continuous = list_rotation[0].subs({x : self.x_coord}) - list_rotation[1].subs({x : self.x_coord})
            equations = [fixed_equation, rotation_continuous]
        else:
            equations = [fixed_equation]

        return equations
# ==================================================================================== hinge
class hinge(point):
    """Concrete implementation of a hinge.
    """
    @staticmethod
    def get_name():
        return "Hinge"

    def has_reaction_force(self):
        return False

    def has_reaction_moment(self):
        return False

    def get_deflection_boundary_condition(self, list_deflection):
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs({x : self.x_coord}) - list_deflection[1].subs({x : self.x_coord})
            equations = [deflection_continuous]
        else:
            equations = []

        return equations

    def get_rotation_boundary_condition(self, list_rotation):
        pass
# ==========================================================================================
