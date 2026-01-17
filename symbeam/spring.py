"""Spring module.

Defines the transverse and rotational spring classes.

..module:: spring
  :synopsis: Main spring class

..moduleauthor:: A. M. Couto Carneiro <amcc@fe.up.pt>
"""

import numpy as np
import sympy as sym


# ======================================================================== transverse_spring
class transverse_spring:
    """Transverse spring."""

    def __init__(self, x_coord, stiffness):
        self.x_coord = sym.sympify(x_coord)
        self.stiffness = sym.sympify(stiffness)

    # --------------------------------------------------------------------------------- draw
    def draw(
        self,
        ax,
        x_start,
        y_start,
        spring_length,
        n_coils,
        coil_width,
        include_end_length=True,
    ):
        """Draws a transverse spring in the axis.

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
        coil_width : float
            Width of the coils of the spring
        include_end_length : bool, optional
            Whether to include the end length in the drawing (default is True)
        """
        coil_length = 0.5 * spring_length / n_coils
        end_length = (spring_length - n_coils * coil_length) / 2
        if not include_end_length:
            end_length = 0
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
                    [aux_y_start, aux_y_start + coil_length / 2, aux_y_start + coil_length],
                    color="black",
                    linewidth=1.5,
                    clip_on=False,
                    solid_capstyle="round",
                )
                aux_y_start += coil_length
            else:
                ax.plot(
                    [x_start, x_start - coil_width, x_start],
                    [aux_y_start, aux_y_start + coil_length / 2, aux_y_start + coil_length],
                    color="black",
                    linewidth=1.5,
                    clip_on=False,
                    solid_capstyle="round",
                )
                aux_y_start += coil_length

        # Draw the last ending
        ax.plot(
            [x_start, x_start],
            [y_start + spring_length - end_length, y_start + spring_length],
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="round",
        )


# ======================================================================== rotational_spring
class rotational_spring:
    """Rotational spring."""

    def __init__(self, x_coord, stiffness):
        self.x_coord = sym.sympify(x_coord)
        self.stiffness = sym.sympify(stiffness)

    # --------------------------------------------------------------- draw_rotational_spring
    def draw(
        self,
        ax,
        x_start,
        y_start,
        spring_radius,
        spring_height,
        n_coils,
        xspan,
        yspan,
        xmax,
        ending="center",
        include_end_length=True,
    ):
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
        spring_height : float
            Height of the spring
        n_coils : int
            Number of coils of the spring
        xspan : float
            X-axis span of the axis
        yspan : float
            Y-axis span of the axis
        xmax : float
            Maximum X value of the axis
        ending : str, optional
            Type of ending to use: 'center', 'side', 'support'
        include_end_length : bool, optional
            Whether to include the end length in the drawing (default is True)
        """
        if not include_end_length:
            end_length = 0
        else:
            end_length = abs(spring_height - spring_radius)
        # Get axis aspect ratio
        # Source: https://stackoverflow.com/questions/41597177/get-aspect-ratio-of-axes
        figW, figH = ax.get_figure().get_size_inches()
        _, _, w, h = ax.get_position().bounds
        disp_ratio = (figH * h) / (figW * w)
        data_ratio = yspan / xspan
        aspect_ratio = disp_ratio / data_ratio

        # Draw the coils (spiral)
        theta_max = n_coils * 2 * np.pi
        spiral_parameter = spring_radius / theta_max
        n_points = 100
        if ending == "center":
            theta = np.linspace(0, theta_max, n_points, endpoint=True)
        elif ending == "side":
            theta = np.linspace(0, theta_max - np.pi / 4, n_points, endpoint=True)
        elif ending == "support":
            theta = np.linspace(0, theta_max - np.pi / 6, n_points, endpoint=True)

        r = theta * spiral_parameter
        x_aux = r * np.sin(theta) * aspect_ratio
        if x_start > xmax - xspan / 2000:
            x_spiral = x_start - x_aux
        else:
            x_spiral = x_start + x_aux
        y_spiral = y_start + spring_height - r * np.cos(theta)
        ax.plot(
            x_spiral,
            y_spiral,
            color="black",
            linewidth=1.5,
            clip_on=False,
            solid_capstyle="round",
        )

        # Draw the ending
        if ending == "center":
            ax.plot(
                [x_start, x_start],
                [y_start, y_start + end_length],
                color="black",
                linewidth=1.5,
                clip_on=False,
                solid_capstyle="round",
            )
        elif ending == "side":
            ax.plot(
                [x_spiral[-1], x_spiral[-1]],
                [y_start, y_spiral[-1]],
                color="black",
                linewidth=1.5,
                clip_on=False,
                solid_capstyle="round",
            )


# ==========================================================================================
