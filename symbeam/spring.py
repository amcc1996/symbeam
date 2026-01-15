"""Spring module.

Defines the transverse and rotational spring classes.

..module:: spring
  :synopsis: Main spring class

..moduleauthor:: A. M. Couto Carneiro <amcc@fe.up.pt>
"""

import sympy as sym

import numpy as np

from sympy.abc import x


# ======================================================================== transverse_spring
class transverse_spring:
    """Transverse spring."""

    def __init__(self, x_coord, stiffness):
        self.x_coord = sym.sympify(x_coord)
        self.stiffness = sym.sympify(stiffness)

    # --------------------------------------------------------------------------------- draw
    def draw(self, ax, x_start, y_start, spring_length, n_coils, coil_width, length_bottom_line, xspan, yspan):
        """Draws a transverse spring in the axis.

        Parameters
        ----------
        ax : Matplotlib axis object
            Axis where to draw the transverse spring
        x_start : float
            X-coordinate where to start drawing the spring
        y_start : float
            Y-coordinate where to start drawing the spring
        spring_length : float
            Length of the spring
        n_coils : int
            Number of coils of the spring
        coil_width : float
            Width of the coils of the spring
        length_bottom_line : float
            Length of the bottom line of the spring
        xspan : float
            X-axis span of the axis
        yspan : float
            Y-axis span of the axis
        """
        coil_length = 0.5 * spring_length / n_coils
        end_length = (spring_length - n_coils * coil_length) / 2
        # Draw the first ending
        ax.plot(
            [x_start, x_start],
            [y_start, y_start + end_length],
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="butt",
        )
        # Draw the coils
        aux_y_start = y_start + end_length
        for i in range(n_coils):
            if i % 2 == 0:
                ax.plot(
                    [x_start, x_start + coil_width, x_start],
                    [aux_y_start, aux_y_start + coil_length/2, aux_y_start + coil_length],
                    color="black",
                    linewidth=1.5,
                    clip_on=False,
                    solid_capstyle="butt",
                )
                aux_y_start += coil_length
            else:
                ax.plot(
                    [x_start, x_start - coil_width, x_start],
                    [aux_y_start, aux_y_start + coil_length/2, aux_y_start + coil_length],
                    color="black",
                    linewidth=1.5,
                    clip_on=False,
                    solid_capstyle="butt",
                )
                aux_y_start += coil_length
        # Draw the last ending
        ax.plot(
            [x_start, x_start],
            [y_start + spring_length - end_length, y_start + spring_length],
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="butt",
        )
        # Draw the base line
        ax.plot(
            [
                x_start - length_bottom_line / 2,
                x_start + length_bottom_line / 2,
            ],
            [y_start - yspan / 55, y_start - yspan / 55],
            color="silver",
            linewidth=5,
            clip_on=False,
            solid_capstyle="butt",
        )
        ax.plot(
            [
                x_start - length_bottom_line / 2,
                x_start + length_bottom_line / 2,
            ],
            [y_start, y_start],
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="butt",
        )


# ======================================================================== rotational_spring
class rotational_spring:
    """Rotational spring."""

    def __init__(self, x_coord, stiffness):
        self.x_coord = sym.sympify(x_coord)
        self.stiffness = sym.sympify(stiffness)

# ------------------------------------------------------------------- draw_rotational_spring
    def draw(self, ax, x_start, y_start, spring_radius, n_coils, length_bottom_line, xspan, yspan, include_end_length=True):
        """Draws a rotational spring in the axis.

        Parameters
        ----------
        ax : Matplotlib axis object
            Axis where to draw the rotational spring
        x_start : float
            X-coordinate where to start drawing the spring
        y_start : float
            Y-coordinate where to start drawing the spring
        spring_radius : float
            Radius of the spring
        n_coils : int
            Number of coils of the spring
        length_bottom_line : float
            Length of the bottom line of the spring
        xspan : float
            X-axis span of the axis
        yspan : float
            Y-axis span of the axis
        """
        if not include_end_length:
            end_length = 0
        else:
            end_length = abs(abs(y_start) - spring_radius)
        # Get axis aspect ratio
        # Source: https://stackoverflow.com/questions/41597177/get-aspect-ratio-of-axes
        figW, figH = ax.get_figure().get_size_inches()
        _, _, w, h = ax.get_position().bounds
        disp_ratio = (figH * h) / (figW * w)
        data_ratio = yspan / xspan
        aspect_ratio = disp_ratio / data_ratio
        # Draw the first ending
        ax.plot(
            [x_start, x_start],
            [y_start, y_start + end_length],
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="butt",
        )
        # Draw the coils (spiral)
        theta_max = n_coils * 2 * np.pi
        spiral_parameter = spring_radius / theta_max
        n_points = 100
        theta = np.linspace(0, theta_max, n_points, endpoint=True)
        r = theta * spiral_parameter
        x_spiral = x_start + r * np.sin(theta) * aspect_ratio
        y_spiral = - r * np.cos(theta)
        ax.plot(
            x_spiral,
            y_spiral,
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="butt",
        )
        # Draw the base line
        ax.plot(
            [
                x_start - length_bottom_line / 2,
                x_start + length_bottom_line / 2,
            ],
            [y_start - yspan / 55, y_start - yspan / 55],
            color="silver",
            linewidth=5,
            clip_on=False,
            solid_capstyle="butt",
        )
        ax.plot(
            [
                x_start - length_bottom_line / 2,
                x_start + length_bottom_line / 2,
            ],
            [y_start, y_start],
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="butt",
        )

# ==========================================================================================
