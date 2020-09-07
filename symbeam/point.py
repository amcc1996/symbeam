"""Point module.

Provides the point class, reponsible for handling point forces and moments,
reactions and supports. A point is defined by an abstract class with all attributes and
methods associated with point features. Concrete implementations, for instance, for
distinct supports types, are realised by concrete class implementations.

These classes are used internally by SymBeam thus, they shall not be used directly by the
user, in a general scenario. In fact, SymBeam instanciates the points on the beam by
the data coming from the user, accounting for the existance of supports, point forces and
moments and changes of beam properties.

..module:: point
  :synopsis: Point class

..moduleauthor:: A. M. Couto Carneiro <amcc@fe.up.pt>
"""
from abc import ABC, abstractmethod

import matplotlib.patches as patches
import sympy as sym

from sympy.abc import x


# Set numerical tolerance
tol = 1e-6
# ==================================================================================== point
class point(ABC):
    """Abstract definition of a beam point."""

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
        """Returns the point type descriptor.

        Returns
        -------
        name : str
          Name of the support
        """

    # ------------------------------------------------------------------- has_reaction_force
    @abstractmethod
    def has_reaction_force(self):
        """Flags if the current point support reactions forces.

        Returns
        -------
        flag : bool
          Flags if the point supports exterior reaction forces
        """

    # ------------------------------------------------------------------ has_reaction_moment
    @abstractmethod
    def has_reaction_moment(self):
        """Flags if the current point support reactions moments.


        Returns
        -------
        flag : bool
          Flags if the point supports exterior reaction moments
        """

    # ---------------------------------------------------- get_deflection_boundary_condition
    @abstractmethod
    def get_deflection_boundary_condition(self, list_deflection):
        """Establishes the deflection boundary condition on the current point.

        Parameters
        ----------
        list_deflection : list of SymPy expressions
          List of the deflection expressions associated with a point as function of x and
          the integration constants

        Returns
        -------
        equations : list of SymPy expressions
          List of equations setting the deflection boundary condition at the point that
          allow the determination of the integration constants
        """

    # ------------------------------------------------------ get_rotation_boundary_condition
    @abstractmethod
    def get_rotation_boundary_condition(self, list_rotation):
        """Establishes the rotation boundary condition on the current point.

        Parameters
        ----------
        list_rotation : list of SymPy expressions
          List of the rotation expressions associated with a point as function of x and
          the integration constants

        Returns
        -------
        equations : list of SymPy expressions
          List of equations setting the rotation boundary condition at the point that
          allow the determination of the integration constants
        """

    # ---------------------------------------------------------- get_fixed_degree_of_freedom
    @abstractmethod
    def get_fixed_degree_of_freedom(self):
        """Returns the number of fixed degrees of freedom in a support.

        Retunrs
        -------
        number_fixed : int
          Number of fixed degrees of freedom at the point
        """

    # --------------------------------------------------------------------------- draw_point
    @abstractmethod
    def draw_point(self, ax):
        """Draws the point in the given axis.

        Parameters
        ----------
        ax : Matplotlib axis object
          Axis where to draw the point
        """

    # ------------------------------------------------------------- has_deflection_condition
    def has_deflection_condition(self):
        """Flags if the current point enforces some boundary condition on the deflection.

        Returns
        -------
        flag : bool
          Flags if the current support sets a deflection boundary condition
        """
        return not (self.is_method_empty(self.get_deflection_boundary_condition))

    # --------------------------------------------------------------- has_rotation_condition
    def has_rotation_condition(self):
        """Flags if the current point enforces some boundary condition on the rotation.

        Returns
        -------
        flag : bool
          Flags if the current support sets a rotation boundary condition
        """
        return not (self.is_method_empty(self.get_rotation_boundary_condition))

    # ---------------------------------------------------- set_geometric_boundary_conditions
    def set_geometric_boundary_conditions(self, list_rotation, list_deflection, equations):
        """Sets the geometric boundary conditions on the global system of equations.

        Parameters
        ----------
        list_rotation : list of SymPy expressions
          List of the rotation expressions associated with a point as function of x and
          the integration constants
        list_deflection : list of SymPy expressions
          List of the deflection expressions associated with a point as function of x and
          the integration constants
        equations : list of SymPy expressions
          List of global geometric boundary condition equations
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

        Parameters
        ----------
        func : Python function
          Function to check
        """

        def empty_func():
            pass

        def empty_func_with_doc():
            """Empty function with docstring."""
            pass

        return (
            func.__code__.co_code == empty_func.__code__.co_code
            or func.__code__.co_code == empty_func_with_doc.__code__.co_code
        )

    # --------------------------------------------------------------- get_numeric_coordinate
    def get_numeric_coordinate(self, input_substitution={}):
        """Returns the coordinate of the point, by substituting all present symbols byb 1.

        Parameters
        ----------
        input_substitution : dictionary
          User-specified symbols substitution for the symbolic expressions

        Returns
        -------
        x_coord_plot : SymPy float
          Numerical value of point coordinate
        """
        x_coord_plot = self.x_coord
        input_substitution.pop("x", None)
        x_coord_plot = x_coord_plot.subs(input_substitution)
        for ivariable in x_coord_plot.free_symbols:
            x_coord_plot = x_coord_plot.subs({ivariable: 1})

        return x_coord_plot

    # ------------------------------------------------------------------------- draw_support
    def draw_support(self, ax, input_substitution={}):
        """Draws the point in the axis.

        Parameters
        ----------
        ax : Matplotlib axis object
          Axis where to draw the point
        """
        x_coord_plot = self.get_numeric_coordinate(input_substitution=input_substitution)
        self.draw_point(x_coord_plot, ax)

    # --------------------------------------------------------------------------- draw_force
    def draw_force(self, ax, length, input_substitution={}):
        """Draws a point force in the axis.

        Parameters
        ----------
        ax : Matplotlib axis object
          Axis where to draw the point force
        length : float
          Length of the force in the figure
        """
        x_coord_plot = self.get_numeric_coordinate(input_substitution=input_substitution)
        # Set the geometry scale (heuristic).
        scale_x = ax.get_xlim()[1] - ax.get_xlim()[0]
        scale_y = ax.get_ylim()[1] - ax.get_ylim()[0]
        width = 0.002
        head_width = width * 7 * scale_x
        head_length = width * 35 * scale_y
        color = "seagreen"

        # Draw the vector.
        ax.arrow(
            x_coord_plot,
            -length,
            0,
            length,
            clip_on=False,
            color=color,
            width=width,
            head_width=head_width,
            head_length=head_length,
            overhang=0,
            length_includes_head=True,
        )

    # -------------------------------------------------------------------------- draw_moment
    def draw_moment(self, ax, value, input_substitution={}):
        """Draws a point moment in the axis.

        Parameters
        ----------
        ax : Matplotlib axis object
          Axis where to draw the point moment
        value : float
          Relative absolute value the moment, relative to all present moments in the beam
        """
        x_coord_plot = self.get_numeric_coordinate(input_substitution=input_substitution)
        color = "firebrick"
        # Get the limits of the x- and y-axis
        xlim = ax.get_xlim()
        xmin = xlim[0]
        xmax = xlim[1]
        xspan = xmax - xmin

        ylim = ax.get_ylim()
        ymin = ylim[0]
        ymax = ylim[1]
        yspan = ymax - ymin

        # Set the starting and ending angles of the arc.
        diameter = xspan / 25
        if value > 0:
            start_angle = 105
            end_angle = 90
        else:
            start_angle = 90
            end_angle = 75

        # In order to draw an approximately circular arc, get the aspect ratio associated
        # with the data and the figure/axis itself, and scale the diameter.
        bbox = ax.get_window_extent()
        width, height = bbox.width, bbox.height

        data_scale = yspan / xspan
        axis_scale = width / height

        angle = 0
        diameterx = diameter
        diametery = diameter * data_scale * axis_scale

        linewidth = 1 + abs(value) * 1
        markersize = 3 + abs(value) * 4

        # Draw the arc.
        arc = patches.Arc(
            [x_coord_plot, 0],
            diameterx,
            diametery,
            angle=angle,
            theta1=start_angle,
            theta2=end_angle,
            zorder=1000,
            linewidth=linewidth,
            color=color,
            clip_on=False,
        )
        ax.add_patch(arc)

        # Plot the arrow head (marker) and the center of the arc.
        ax.plot(
            x_coord_plot,
            0,
            marker="+",
            clip_on=False,
            markersize=8,
            markerfacecolor=color,
            markeredgecolor=color,
        )
        if value > 0:
            ax.plot(
                x_coord_plot,
                diametery / 2,
                marker="<",
                clip_on=False,
                markersize=markersize,
                markerfacecolor=color,
                markeredgewidth=0,
                markeredgecolor=color,
            )
        else:
            ax.plot(
                x_coord_plot,
                diametery / 2,
                marker=">",
                clip_on=False,
                markersize=markersize,
                markerfacecolor=color,
                markeredgewidth=0,
                markeredgecolor=color,
            )


# ====================================================================================== pin
class pin(point):
    """Concrete implementation of a pinned support."""

    @staticmethod
    def get_name():
        return "Pinned Support"

    # --------------------------------------------------------------------------------------
    def has_reaction_force(self):
        return True

    # --------------------------------------------------------------------------------------
    def has_reaction_moment(self):
        return False

    # --------------------------------------------------------------------------------------
    def get_fixed_degree_of_freedom(self):
        return 2

    # --------------------------------------------------------------------------------------
    def get_deflection_boundary_condition(self, list_deflection):
        fixed_equation = list_deflection[0].subs({x: self.x_coord})
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs(
                {x: self.x_coord}
            ) - list_deflection[1].subs({x: self.x_coord})
            equations = [fixed_equation, deflection_continuous]
        else:
            equations = [fixed_equation]

        return equations

    # --------------------------------------------------------------------------------------
    def get_rotation_boundary_condition(self, list_rotation):
        if len(list_rotation) == 2:
            rotation_continuous = list_rotation[0].subs({x: self.x_coord}) - list_rotation[
                1
            ].subs({x: self.x_coord})
            equations = [rotation_continuous]
        else:
            equations = []

        return equations

    # --------------------------------------------------------------------------------------
    def draw_point(self, x_coord_plot, ax):
        # Get the limits of the x- and y-axis
        xlim = ax.get_xlim()
        xmin = xlim[0]
        xmax = xlim[1]
        xspan = xmax - xmin

        ylim = ax.get_ylim()
        ymin = ylim[0]
        ymax = ylim[1]
        yspan = ymax - ymin
        ymid = (ymax + ymin) / 2

        # Draw the triangle.
        length_bottom_line = xspan / 20
        ax.plot(
            x_coord_plot,
            ymid - yspan / 11,
            marker="^",
            clip_on=False,
            markersize=20,
            markerfacecolor="silver",
            markeredgewidth=1,
            markeredgecolor="black",
        )

        # Draw the final line.
        ax.plot(
            [x_coord_plot - length_bottom_line / 2, x_coord_plot + length_bottom_line / 2],
            [ymid - yspan / 5, ymid - yspan / 5],
            color="silver",
            linewidth=5,
            clip_on=False,
            solid_capstyle="butt",
        )
        ax.plot(
            [x_coord_plot - length_bottom_line / 2, x_coord_plot + length_bottom_line / 2],
            [ymid - yspan / 5.5, ymid - yspan / 5.5],
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="butt",
        )


# =================================================================================== roller
class roller(point):
    """Concrete implementation of a roller support (same as pin if there are no axial
    loads on the beam).
    """

    @staticmethod
    def get_name():
        return "Roller"

    def has_reaction_force(self):
        return True

    def has_reaction_moment(self):
        return False

    def get_fixed_degree_of_freedom(self):
        return 1

    def get_deflection_boundary_condition(self, list_deflection):
        fixed_equation = list_deflection[0].subs({x: self.x_coord})
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs(
                {x: self.x_coord}
            ) - list_deflection[1].subs({x: self.x_coord})
            equations = [fixed_equation, deflection_continuous]
        else:
            equations = [fixed_equation]

        return equations

    def get_rotation_boundary_condition(self, list_rotation):
        if len(list_rotation) == 2:
            rotation_continuous = list_rotation[0].subs({x: self.x_coord}) - list_rotation[
                1
            ].subs({x: self.x_coord})
            equations = [rotation_continuous]
        else:
            equations = []

        return equations

    def draw_point(self, x_coord_plot, ax):
        # Get the limits of the x- and y-axis
        xlim = ax.get_xlim()
        xmin = xlim[0]
        xmax = xlim[1]
        xspan = xmax - xmin

        ylim = ax.get_ylim()
        ymin = ylim[0]
        ymax = ylim[1]
        yspan = ymax - ymin

        # Draw the triangle.
        length_bottom_line = xspan / 20
        ax.plot(
            x_coord_plot,
            -yspan / 15.5,
            marker="^",
            clip_on=False,
            markersize=15,
            markerfacecolor="silver",
            markeredgewidth=1,
            markeredgecolor="black",
        )

        # Draw the circles.
        ax.plot(
            x_coord_plot + xspan / 100,
            -yspan / 6.8,
            marker="o",
            clip_on=False,
            markersize=6,
            markerfacecolor="black",
            markeredgewidth=0,
            markeredgecolor="black",
        )
        ax.plot(
            x_coord_plot - xspan / 100,
            -yspan / 6.8,
            marker="o",
            clip_on=False,
            markersize=6,
            markerfacecolor="black",
            markeredgewidth=0,
            markeredgecolor="black",
        )

        # Draw the final line.
        ax.plot(
            [x_coord_plot - length_bottom_line / 2, x_coord_plot + length_bottom_line / 2],
            [-yspan / 5, -yspan / 5],
            color="silver",
            linewidth=5,
            clip_on=False,
            solid_capstyle="butt",
        )
        ax.plot(
            [x_coord_plot - length_bottom_line / 2, x_coord_plot + length_bottom_line / 2],
            [-yspan / 5.5, -yspan / 5.5],
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="butt",
        )


# =============================================================================== continuity
class continuity(point):
    """Concrete implementation of a continuity point in a beam."""

    @staticmethod
    def get_name():
        return "Continuity point"

    def has_reaction_force(self):
        return False

    def has_reaction_moment(self):
        return False

    def get_fixed_degree_of_freedom(self):
        return 0

    def get_deflection_boundary_condition(self, list_deflection):
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs(
                {x: self.x_coord}
            ) - list_deflection[1].subs({x: self.x_coord})
            equations = [deflection_continuous]
        else:
            equations = []

        return equations

    def get_rotation_boundary_condition(self, list_rotation):
        if len(list_rotation) == 2:
            rotation_continuous = list_rotation[0].subs({x: self.x_coord}) - list_rotation[
                1
            ].subs({x: self.x_coord})
            equations = [rotation_continuous]
        else:
            equations = []

        return equations

    def draw_point(self, x_coord_plot, ax):
        pass


# ==================================================================================== fixed
class fixed(point):
    """Concrete implementation of a fixed/clamped support."""

    @staticmethod
    def get_name():
        return "Fixed"

    def has_reaction_force(self):
        return True

    def has_reaction_moment(self):
        return True

    def get_fixed_degree_of_freedom(self):
        return 3

    def get_deflection_boundary_condition(self, list_deflection):
        fixed_equation = list_deflection[0].subs({x: self.x_coord})
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs(
                {x: self.x_coord}
            ) - list_deflection[1].subs({x: self.x_coord})
            equations = [fixed_equation, deflection_continuous]
        else:
            equations = [fixed_equation]

        return equations

    def get_rotation_boundary_condition(self, list_rotation):
        fixed_equation = list_rotation[0].subs({x: self.x_coord})
        if len(list_rotation) == 2:
            rotation_continuous = list_rotation[0].subs({x: self.x_coord}) - list_rotation[
                1
            ].subs({x: self.x_coord})
            equations = [fixed_equation, rotation_continuous]
        else:
            equations = [fixed_equation]

        return equations

    def draw_point(self, x_coord_plot, ax):
        # Get the limits of the x- and y-axis
        xlim = ax.get_xlim()
        xmin = xlim[0]
        xmax = xlim[1]
        xspan = xmax - xmin

        ylim = ax.get_ylim()
        ymin = ylim[0]
        ymax = ylim[1]
        yspan = ymax - ymin

        # Draw the triangle.
        if abs(x_coord_plot - xmin) < tol:
            ax.plot(
                [x_coord_plot - xspan / 150, x_coord_plot - xspan / 150],
                [-yspan / 15.5, yspan / 15.5],
                color="silver",
                linewidth=5,
                clip_on=False,
                solid_capstyle="butt",
            )
            ax.plot(
                [x_coord_plot, x_coord_plot],
                [-yspan / 15.5, yspan / 15.5],
                color="black",
                linewidth=1.5,
                clip_on=False,
                solid_capstyle="butt",
            )
        elif abs(x_coord_plot - xmin) > tol:
            ax.plot(
                [x_coord_plot + xspan / 150, x_coord_plot + xspan / 150],
                [-yspan / 15.5, yspan / 15.5],
                color="silver",
                linewidth=5,
                clip_on=False,
                solid_capstyle="butt",
            )
            ax.plot(
                [x_coord_plot, x_coord_plot],
                [-yspan / 15.5, yspan / 15.5],
                color="black",
                linewidth=1.5,
                clip_on=False,
                solid_capstyle="butt",
            )
        else:
            ax.plot(
                [x_coord_plot, x_coord_plot],
                [-yspan / 15.5, yspan / 15.5],
                color="silver",
                linewidth=5,
                clip_on=False,
                solid_capstyle="butt",
            )
            ax.plot(
                [x_coord_plot - xspan / 150, x_coord_plot - xspan / 150],
                [-yspan / 15.5, yspan / 15.5],
                color="black",
                linewidth=1.5,
                clip_on=False,
                solid_capstyle="butt",
            )
            ax.plot(
                [x_coord_plot + xspan / 150, x_coord_plot + xspan / 150],
                [-yspan / 15.5, yspan / 15.5],
                color="black",
                linewidth=1.5,
                clip_on=False,
                solid_capstyle="butt",
            )


# ==================================================================================== hinge
class hinge(point):
    """Concrete implementation of a hinge."""

    @staticmethod
    def get_name():
        return "Hinge"

    def has_reaction_force(self):
        return False

    def has_reaction_moment(self):
        return False

    def get_fixed_degree_of_freedom(self):
        return 0

    def get_deflection_boundary_condition(self, list_deflection):
        if len(list_deflection) == 2:
            deflection_continuous = list_deflection[0].subs(
                {x: self.x_coord}
            ) - list_deflection[1].subs({x: self.x_coord})
            equations = [deflection_continuous]
        else:
            equations = []

        return equations

    def get_rotation_boundary_condition(self, list_rotation):
        pass

    def draw_point(self, x_coord_plot, ax):
        ax.plot(
            x_coord_plot,
            0,
            marker="o",
            clip_on=False,
            markersize=8,
            markerfacecolor="white",
            markeredgewidth=1.5,
            markeredgecolor="black",
        )


# ==========================================================================================
