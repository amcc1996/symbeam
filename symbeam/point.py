"""Point module.

Provides the point class, responsible for handling point forces and moments,
reactions and supports. A point is defined by an abstract class with all attributes and
methods associated with point features. Concrete implementations, for instance, for
distinct supports types, are realised by concrete class implementations.

These classes are used internally by SymBeam thus, they shall not be used directly by the
user, in a general scenario. In fact, SymBeam instantiates the points on the beam by
the data coming from the user, accounting for the existence of supports, point forces and
moments and changes of beam properties.

..module:: point
  :synopsis: Point class

..moduleauthor:: A. M. Couto Carneiro <amcc@fe.up.pt>
"""

from abc import ABC, abstractmethod

import matplotlib.patches as patches
import numpy as np
import sympy as sym

from sympy.abc import x

from symbeam.spring import rotational_spring, transverse_spring


# Set numerical tolerance
tol = 1e-6


# ==================================================================================== point
class point(ABC):
    """Abstract definition of a beam point."""

    def __init__(self, x_coord, **kwargs):
        self.x_coord = sym.sympify(x_coord)
        self.reaction_force = sym.sympify(0)
        self.reaction_moment = sym.sympify(0)
        self.external_force = sym.sympify(0)
        self.external_moment = sym.sympify(0)
        self.deflection_left = sym.sympify(0)
        self.deflection_right = sym.sympify(0)
        self.rotation_left = sym.sympify(0)
        self.rotation_right = sym.sympify(0)
        self.transverse_spring_stiffness = sym.sympify(0)
        self.rotational_spring_stiffness = sym.sympify(0)
        self.transverse_spring_force = sym.sympify(0)
        self.rotational_spring_moment = sym.sympify(0)

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

        Returns
        -------
        number_fixed : int
          Number of fixed degrees of freedom at the point
        """

    # --------------------------------------------------------------------------- draw_point
    @abstractmethod
    def draw_point(self, ax, x_start, y_stat, xmin, xmid, xspan, ymin, ymid, yspan):
        """Draws the point in the given axis.

        Parameters
        ----------
        ax : Matplotlib axis object
          Axis where to draw the point
        x_start : float
          X-coordinate where to start drawing the point
        y_stat : float
          Y-coordinate where to draw the point
        xmin : float
            Minimum X value of the axis
        xmid : float
            Midpoint of the x-axis
        xspan : float
            Span of the x-axis
        ymin : float
            Minimum Y value of the axis
        ymid : float
            Midpoint of the y-axis
        yspan : float
            Span of the y-axis
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

    # ---------------------------------------------------------------- has_transverse_spring
    def has_transverse_spring(self):
        """Flags if the current point has a transverse spring.

        Returns
        -------
        flag : bool
          Flags if the current point has a transverse spring
        """
        return self.transverse_spring_stiffness != sym.sympify(0)

    # ---------------------------------------------------------------- has_rotational_spring
    def has_rotational_spring(self):
        """Flags if the current point has a rotational spring.

        Returns
        -------
        flag : bool
          Flags if the current point has a rotational spring
        """
        return self.rotational_spring_stiffness != sym.sympify(0)

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
        input_substitution : dictionary
          User-specified symbols substitution for the symbolic expressions
        """
        # Get the limits of the x- and y-axis
        xlim = ax.get_xlim()
        xmin = xlim[0]
        xmax = xlim[1]
        xspan = xmax - xmin
        xmid = (xmax + xmin) / 2

        ylim = ax.get_ylim()
        ymin = ylim[0]
        ymax = ylim[1]
        yspan = ymax - ymin
        ymid = (ymax + ymin) / 2

        # Set ground drawing parameters
        y_ground = ymid - yspan / 5.5
        y_below_ground = ymid - yspan / 5
        ground_length = xspan / 20

        # Get the numeric coordinate for plotting
        x_coord_plot = self.get_numeric_coordinate(input_substitution=input_substitution)

        # Draw the springs if any
        has_springs = self.has_transverse_spring() or self.has_rotational_spring()
        if has_springs:
            self.draw_springs(ax, x_coord_plot, y_ground, xspan, yspan, xmax, ymid)

        # Draw the support point
        self.draw_point(ax, x_coord_plot, y_ground, xmin, xmid, xspan, ymin, ymid, yspan)

        # Draw the ground lines if needed
        needs_ground = False
        if type(self) in [pin, roller]:
            needs_ground = True
        elif has_springs:
            needs_ground = True

        if needs_ground:
            self.draw_ground(
                ax,
                x_coord_plot,
                y_ground=y_ground,
                y_below_ground=y_below_ground,
                ground_length=ground_length,
            )

    # -------------------------------------------------------------------------- draw_ground
    def draw_ground(
        self,
        ax,
        x_coord_plot,
        y_ground,
        y_below_ground,
        ground_length,
        x_offset=0,
        xspan=None,
        yspan=None,
        xmid=None,
        ymid=None,
    ):
        """Draws the ground lines.

        Parameters
        ----------
        ax : Matplotlib axis object
          Axis where to draw the ground line
        x_coord_plot : float
          X-coordinate where to draw the ground line
        y_ground : float
            Y-coordinate of the ground line
        y_below_ground : float
            Y-coordinate below the ground line
        ground_length : float
            Length of the ground line
        x_offset : float
            X-offset of the ground line
        xspan : float
            Span of the x-axis
        yspan : float
            Span of the y-axis
        xmid : float
            Midpoint of the x-axis
        ymid : float
            Midpoint of the y-axis
        """
        ax.plot(
            [
                x_coord_plot - ground_length / 2 + x_offset,
                x_coord_plot + ground_length / 2 + x_offset,
            ],
            [y_below_ground, y_below_ground],
            color="silver",
            linewidth=5,
            clip_on=False,
            solid_capstyle="butt",
        )
        ax.plot(
            [
                x_coord_plot - ground_length / 2 + x_offset,
                x_coord_plot + ground_length / 2 + x_offset,
            ],
            [y_ground, y_ground],
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="butt",
        )

    # ------------------------------------------------------------------------- draw_springs
    def draw_springs(self, ax, x_start, y_start, xspan, yspan, xmax, ymid):
        """Draws the springs at a point.

        Parameters
        ----------
        ax : Matplotlib axis object
          Axis where to draw the point
        x_start : float
            X-coordinate where to start drawing the springs
        y_start : float
            Y-coordinate where to start drawing the springs
        xspan : float
            X-axis span of the axis
        yspan : float
            Y-axis span of the axis
        xmax : float
            Maximum X value of the axis
        ymid : float
            Midpoint of the y-axis
        """
        if self.has_transverse_spring() and not (self.has_rotational_spring()):
            ystart_transverse = y_start
            spring_length_transverse = ymid - y_start
            n_coils_transverse = 6
            coil_width_transverse = xspan / 100
            include_ending_transverse = True

        elif not (self.has_transverse_spring()) and self.has_rotational_spring():
            ystart_rotational = y_start
            spring_height_rotational = abs(ymid - y_start)
            spring_radius_rotational = (ymid - y_start) / 2
            n_coils_rotational = 3
            include_ending_rotational = True
            if type(self) in [pin, roller]:
                include_ending_rotational = False
                ending = "support"
            else:
                ending = "center"

        elif self.has_transverse_spring() and self.has_rotational_spring():
            ystart_transverse = y_start
            spring_length_transverse = ymid - y_start
            n_coils_transverse = 6
            coil_width_transverse = xspan / 100
            include_ending_transverse = True

            ystart_rotational = y_start
            spring_height_rotational = abs(ymid - y_start)
            spring_radius_rotational = (ymid - y_start) / 2
            n_coils_rotational = 3
            ending = "side"
            include_ending_rotational = True

        if self.has_transverse_spring():
            transverse_spring(x_start, self.transverse_spring_stiffness).draw(
                ax,
                x_start,
                ystart_transverse,
                spring_length=spring_length_transverse,
                n_coils=n_coils_transverse,
                coil_width=coil_width_transverse,
                include_end_length=include_ending_transverse,
            )

        if self.has_rotational_spring():
            rotational_spring(x_start, self.rotational_spring_stiffness).draw(
                ax,
                x_start,
                ystart_rotational,
                spring_radius=spring_radius_rotational,
                spring_height=spring_height_rotational,
                n_coils=n_coils_rotational,
                xspan=xspan,
                yspan=yspan,
                xmax=xmax,
                ending=ending,
                include_end_length=include_ending_rotational,
            )

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
    def draw_point(self, ax, x_start, y_start, xmin, xmid, xspan, ymin, ymid, yspan):
        length_base = xspan / 20
        x = np.array(
            [x_start - length_base / 2, x_start, x_start + length_base / 2], dtype=float
        )
        y1 = np.array([y_start, ymid, y_start], dtype=float)
        y2 = np.array([y_start, y_start, y_start], dtype=float)
        # Draw the triangle.
        ax.fill_between(x, y2, y1, clip_on=False, edgecolor="none", facecolor="silver")
        ax.plot(
            x,
            y2,
            color="black",
            linewidth=1.0,
            clip_on=False,
            solid_capstyle="round",
        )
        ax.plot(
            x,
            y1,
            color="black",
            linewidth=1.0,
            clip_on=False,
            solid_capstyle="round",
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

    def draw_point(self, ax, x_start, y_start, xmin, xmid, xspan, ymin, ymid, yspan):
        size_factor = 0.7
        length_base = xspan / 20 * size_factor
        height_triangle = abs(ymid - y_start) * size_factor
        radius = (ymid - y_start) - height_triangle
        y_start_tri = y_start + (ymid - y_start) - height_triangle
        x = np.array(
            [x_start - length_base / 2, x_start, x_start + length_base / 2], dtype=float
        )
        y1 = np.array([y_start_tri, ymid, y_start_tri], dtype=float)
        y2 = np.array([y_start_tri, y_start_tri, y_start_tri], dtype=float)
        # Draw the triangle.
        ax.fill_between(x, y2, y1, clip_on=False, edgecolor="none", facecolor="silver")
        ax.plot(
            x,
            y2,
            color="black",
            linewidth=1.0,
            clip_on=False,
            solid_capstyle="round",
        )
        ax.plot(
            x,
            y1,
            color="black",
            linewidth=1.0,
            clip_on=False,
            solid_capstyle="round",
        )
        # Draw the wheels
        y1_circle = y_start + radius / 2
        y2_circle = y_start + radius / 2
        x1_circle = x_start - xspan / 100
        x2_circle = x_start + xspan / 100
        ax.plot(
            [x1_circle],
            [y1_circle],
            marker="o",
            markersize=6,
            color="black",
            markeredgewidth=0,
            clip_on=False,
        )
        ax.plot(
            [x2_circle],
            [y2_circle],
            marker="o",
            markersize=6,
            color="black",
            markeredgewidth=0,
            clip_on=False,
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

    def draw_point(self, ax, x_start, y_start, xmin, xmid, xspan, ymin, ymid, yspan):
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

    def draw_point(self, ax, x_start, y_start, xmin, xmid, xspan, ymin, ymid, yspan):
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
        if abs(x_start - xmin) < tol:
            ax.plot(
                [x_start - xspan / 150, x_start - xspan / 150],
                [-yspan / 15.5, yspan / 15.5],
                color="silver",
                linewidth=5,
                clip_on=False,
                solid_capstyle="butt",
            )
            ax.plot(
                [x_start, x_start],
                [-yspan / 15.5, yspan / 15.5],
                color="black",
                linewidth=1.5,
                clip_on=False,
                solid_capstyle="butt",
            )
        elif abs(x_start - xmin) > tol:
            ax.plot(
                [x_start + xspan / 150, x_start + xspan / 150],
                [-yspan / 15.5, yspan / 15.5],
                color="silver",
                linewidth=5,
                clip_on=False,
                solid_capstyle="butt",
            )
            ax.plot(
                [x_start, x_start],
                [-yspan / 15.5, yspan / 15.5],
                color="black",
                linewidth=1.5,
                clip_on=False,
                solid_capstyle="butt",
            )
        else:
            ax.plot(
                [x_start, x_start],
                [-yspan / 15.5, yspan / 15.5],
                color="silver",
                linewidth=5,
                clip_on=False,
                solid_capstyle="butt",
            )
            ax.plot(
                [x_start - xspan / 150, x_start - xspan / 150],
                [-yspan / 15.5, yspan / 15.5],
                color="black",
                linewidth=1.5,
                clip_on=False,
                solid_capstyle="butt",
            )
            ax.plot(
                [x_start + xspan / 150, x_start + xspan / 150],
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

    def draw_point(self, ax, x_start, y_start, xmin, xmid, xspan, ymin, ymid, yspan):
        ax.plot(
            x_start,
            0,
            marker="o",
            clip_on=False,
            markersize=8,
            markerfacecolor="white",
            markeredgewidth=1.5,
            markeredgecolor="black",
        )


# ==========================================================================================
