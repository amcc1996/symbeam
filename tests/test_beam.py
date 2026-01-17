import io

from contextlib import redirect_stdout

import pytest
import sympy as sym

from sympy.abc import E, I, L, M, P, x

from symbeam.beam import beam
from symbeam.utils import (
    baseline_output_numeric,
    baseline_output_springs_numeric,
    baseline_output_springs_symbolic,
    baseline_output_symbolic,
    compute_bending_moment,
    compute_rotation,
    computes_shear_force,
    euler_bernoulli_stiff_matrix,
    hermite_polynomials,
)


def test_beam_two_symbols():
    """Test if an error is raised if more than one symbols is used to initialise
    the beam.
    """
    with pytest.raises(RuntimeError):
        a = beam("L * a", x0=0)  # noqa: F841


def test_beam_distinct_symbols():
    """Test if an error is raised if the symbols used for the initial position and length
    are distinct.
    """
    with pytest.raises(RuntimeError):
        a = beam("L * a", x0="b")  # noqa: F841


def test_beam_numeric_length():
    """Test if a numeric length is accepted for the beam."""
    a = beam(1)
    assert a.length == 1


def test_beam_symbolic_length():
    """Test if a symbolic length is accepted for the beam."""
    a = beam("l")
    assert a.length == sym.sympify("l")


def test_repeated_support():
    """Test if an error is raised when a repeated support is specified."""
    with pytest.raises(RuntimeError):
        a = beam("l")
        a.add_support(0, "fixed")
        a.add_support(0, "pin")


def test_support_inside_beam():
    """Test if an error is raised when the supports lies outside the beam."""
    with pytest.raises(RuntimeError):
        a = beam("l")
        a.add_support("2*l", "fixed")


def test_point_load_inside_beam():
    """Test if an error is raised when the point load lies outside the beam."""
    with pytest.raises(RuntimeError):
        a = beam("l")
        a.add_point_load("2*l", "P")


def test_point_moment_inside_beam():
    """Test if an error is raised when the point moment lies outside the beam."""
    with pytest.raises(RuntimeError):
        a = beam("l")
        a.add_point_moment("2*l", "M")


def test_distributed_load_coordinates():
    """Test if the coordinates of the distributed load are consistent."""
    with pytest.raises(RuntimeError):
        a = beam(1)
        a.add_distributed_load(1, 0.5, "q")


def test_young_specification_missing():
    """Test if the Young modulus is specified in all lengths."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.set_young(0, "l/2", E)
        a.solve(output=False)


def test_young_specification_overlap():
    """Test if the Young modulus is specified in all lengths."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.set_young(0, "l/2", E)
        a.set_young("l/2", "3*l/4", 4 * E)
        a.solve(output=False)


def test_inertia_specification_missing():
    """Test if the inertia is specified in all lengths."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.set_inertia(0, "l/2", I)
        a.solve(output=False)


def test_inertia_specification_overlap():
    """Test if the inertia is specified in all lengths."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.set_inertia(0, "l/2", "I")
        a.set_inertia("l/2", "3*l/4", 4 * I)
        a.solve(output=False)


def test_hyperstatic_1():
    """Test if hyperstatic beams are detected."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.add_support(0, "pin")
        a.add_support("l", "pin")
        a.solve(output=False)


def test_hyperstatic_2():
    """Test if hyperstatic beams are detected."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.add_support(0, "fixed")
        a.add_support("l", "roller")
        a.solve(output=False)


def test_invalid_symbol_load():
    """Test if errors are raised when the coordinate of a load include the x variable."""
    with pytest.raises(RuntimeError):
        a = beam("l")
        a.add_point_load("2*x", 1)


def test_cantilever_point():
    """Test classical cantilever beam with point load."""
    a = beam("L", x0=0)
    a.add_support(0, "fixed")
    a.add_point_load(L, -P)
    a.solve(output=False)

    errors = []
    length_points = len(a.points) == 2
    length_segments = len(a.segments) == 1

    x0_coord = a.points[0].x_coord == sym.sympify(0)
    xl_coord = a.points[1].x_coord == L

    x_start_coord = a.segments[0].x_start == sym.sympify(0)
    x_end_coord = a.segments[0].x_end == L
    young = a.segments[0].young == E
    inertia = a.segments[0].inertia == I

    reaction_force = (a.points[0].reaction_force == P) and (
        a.points[1].reaction_force == sym.sympify(0)
    )
    reaction_moment = (a.points[0].reaction_moment == P * L) and (
        a.points[1].reaction_moment == sym.sympify(0)
    )

    shear_force = a.segments[0].shear_force == -P
    bending_moment = a.segments[0].bending_moment == -L * P + P * x

    deflection = a.segments[0].deflection == -L * P * x**2 / (2 * E * I) + P * x**3 / (
        6 * E * I
    )
    rotation = a.segments[0].rotation == -L * P * x / (E * I) + P * x**2 / (2 * E * I)

    if not (length_points):
        errors.append("Error in the length of the list of points.")
    if not (length_segments):
        errors.append("Error in the length if the list of segments.")
    if not (x0_coord) or not (xl_coord):
        errors.append("Error in point coordinates.")
    if not (x_start_coord) or not (x_end_coord):
        errors.append("Error in the segment coordinates.")
    if not (young) or not (inertia):
        errors.append("Error in the segment properties.")
    if not (reaction_force):
        errors.append("Error in reaction force computation.")
    if not (reaction_moment):
        errors.append("Error in reaction moment computation.")
    if not (shear_force):
        errors.append("Error in shear force diagram.")
    if not (bending_moment):
        errors.append("Error in bending moment diagram.")
    if not (deflection):
        errors.append("Error in deflection.")
    if not (rotation):
        errors.append("Error in rotation.")

    # An empty list is False for Python
    assert not errors, "The following errors occurred:\n{}".format("\n".join(errors))


def test_cantilever_moment():
    """Test classical cantilever beam with point moment."""
    a = beam("L", x0=0)
    a.add_support(0, "fixed")
    a.add_point_moment(L, M)
    a.solve(output=False)

    errors = []
    length_points = len(a.points) == 2
    length_segments = len(a.segments) == 1

    x0_coord = a.points[0].x_coord == sym.sympify(0)
    xl_coord = a.points[1].x_coord == L

    x_start_coord = a.segments[0].x_start == sym.sympify(0)
    x_end_coord = a.segments[0].x_end == L
    young = a.segments[0].young == E
    inertia = a.segments[0].inertia == I

    reaction_force = a.points[0].reaction_force == sym.sympify(0) and a.points[
        1
    ].reaction_force == sym.sympify(0)
    reaction_moment = a.points[0].reaction_moment == -M and a.points[
        1
    ].reaction_moment == sym.sympify(0)

    shear_force = a.segments[0].shear_force == sym.sympify(0)
    bending_moment = a.segments[0].bending_moment == M

    deflection = a.segments[0].deflection == M * x**2 / (2 * E * I)
    rotation = a.segments[0].rotation == M * x / (E * I)

    if not (length_points):
        errors.append("Error in the length of the list of points.")
    if not (length_segments):
        errors.append("Error in the length if the list of segments.")
    if not (x0_coord) or not (xl_coord):
        errors.append("Error in point coordinates.")
    if not (x_start_coord) or not (x_end_coord):
        errors.append("Error in the segment coordinates.")
    if not (young) or not (inertia):
        errors.append("Error in the segment properties.")
    if not (reaction_force):
        errors.append("Error in reaction force computation.")
    if not (reaction_moment):
        errors.append("Error in reaction moment computation.")
    if not (shear_force):
        errors.append("Error in shear force diagram.")
    if not (bending_moment):
        errors.append("Error in bending moment diagram.")
    if not (deflection):
        errors.append("Error in deflection.")
    if not (rotation):
        errors.append("Error in rotation.")

    # An empty list is False for Python
    assert not errors, "The following errors occurred:\n{}".format("\n".join(errors))


def test_half_span_force():
    """Test classical problem of pin-roller beam with half-span point force."""
    a = beam("L", x0=0)
    a.add_support(0, "pin")
    a.add_support("L", "roller")
    a.add_point_load("L/2", "-P")
    a.solve(output=False)

    errors = []
    length_points = len(a.points) == 3
    length_segments = len(a.segments) == 2

    x_coord = (
        a.points[0].x_coord == sym.sympify(0)
        and a.points[1].x_coord == L / 2
        and a.points[2].x_coord == L
    )

    x_start_coord = (
        a.segments[0].x_start == sym.sympify(0) and a.segments[1].x_start == L / 2
    )
    x_end_coord = a.segments[0].x_end == L / 2 and a.segments[0].x_end == L
    young = a.segments[0].young == E and a.segments[1].young == E
    inertia = a.segments[0].inertia == I and a.segments[1].inertia == I

    reaction_force = (
        a.points[0].reaction_force == P / 2
        and a.points[1].reaction_force == sym.sympify(0)
        and a.points[2].reaction_force == P / 2
    )
    reaction_moment = (
        a.points[0].reaction_moment == sym.sympify(0)
        and a.points[1].reaction_moment == sym.sympify(0)
        and a.points[2].reaction_moment == sym.sympify(0)
    )

    shear_force = a.segments[0].shear_force == -P / 2 and a.segments[1].shear_force == P / 2
    bending_moment = (
        a.segments[0].bending_moment == P * x / 2
        and a.segments[1].bending_moment == P * L / 2 - P * x / 2
    )

    deflection_1 = -P * L**2 * x / (16 * E * I) + P * x**3 / (12 * E * I)
    deflection_2 = (
        P * L**3 / (48 * E * I)
        - 3 * P * L**2 * x / (16 * E * I)
        + P * L * x**2 / (4 * E * I)
        - P * x**3 / (12 * E * I)
    )
    rotation_1 = -P * L**2 / (16 * E * I) + P * x**2 / (4 * E * I)
    rotation_2 = (
        -3 * P * L**2 / (16 * E * I) + P * L * x / (2 * E * I) - P * x**2 / (4 * E * I)
    )
    deflection = (
        a.segments[0].deflection == deflection_1
        and a.segments[1].deflection == deflection_2
    )
    rotation = a.segments[0].rotation == rotation_1 and a.segments[1].rotation == rotation_2

    if not (length_points):
        errors.append("Error in the length of the list of points.")
    if not (length_segments):
        errors.append("Error in the length if the list of segments.")
    if not (x_coord):
        errors.append("Error in point coordinates.")
    if not (x_start_coord or x_end_coord):
        errors.append("Error in the segment coordinates.")
    if not (young) or not (inertia):
        errors.append("Error in the segment properties.")
    if not (reaction_force):
        errors.append("Error in reaction force computation.")
    if not (reaction_moment):
        errors.append("Error in reaction moment computation.")
    if not (shear_force):
        errors.append("Error in shear force diagram.")
    if not (bending_moment):
        errors.append("Error in bending moment diagram.")
    if not (deflection):
        errors.append("Error in deflection.")
    if not (rotation):
        errors.append("Error in rotation.")

    # An empty list is False for Python
    assert not errors, "The following errors occurred:\n{}".format("\n".join(errors))


def test_complex_beam_hinge():
    """Test a complex structure with distributed loadings and hinges."""
    a = beam(6, x0=0)
    a.add_support(0, "fixed")
    a.add_support(4, "hinge")
    a.add_support(6, "roller")
    a.add_point_moment(6, 20)
    a.add_distributed_load(0, 2, "-5*x")
    a.add_distributed_load(2, 4, "-(20-5*x)")
    a.solve(output=False)

    errors = []
    length_points = len(a.points) == 4
    length_segments = len(a.segments) == 3

    x_coord = (
        a.points[0].x_coord == sym.sympify(0)
        and a.points[1].x_coord == sym.sympify(2)
        and a.points[2].x_coord == sym.sympify(4)
        and a.points[3].x_coord == sym.sympify(6)
    )

    x_start_coord = (
        a.segments[0].x_start == sym.sympify(0)
        and a.segments[1].x_start == sym.sympify(2)
        and a.segments[2].x_start == sym.sympify(4)
    )
    x_end_coord = (
        a.segments[0].x_end == sym.sympify(2)
        and a.segments[1].x_end == sym.sympify(4)
        and a.segments[2].x_end == sym.sympify(6)
    )
    young = (
        a.segments[0].young == E and a.segments[1].young == E and a.segments[2].young == E
    )
    inertia = (
        a.segments[0].inertia == I
        and a.segments[1].inertia == I
        and a.segments[2].inertia == I
    )

    reaction_force = (
        a.points[0].reaction_force == sym.sympify(30)
        and a.points[1].reaction_force == sym.sympify(0)
        and a.points[3].reaction_force == sym.sympify(-10)
    )
    reaction_moment = (
        a.points[0].reaction_moment == sym.sympify(80)
        and a.points[1].reaction_moment == sym.sympify(0)
        and a.points[2].reaction_moment == sym.sympify(0)
    )

    shear_force1 = sym.sympify(5 * x**2 / 2 - 30)
    shear_force2 = sym.sympify(-5 * x**2 / 2 + 20 * x - 50)
    shear_force3 = sym.sympify(-10)
    shear_force = (
        a.segments[0].shear_force == shear_force1
        and a.segments[1].shear_force == shear_force2
        and a.segments[2].shear_force == shear_force3
    )
    bending_moment1 = sym.sympify("-5*x**3/6 + 30*x - 80")
    bending_moment2 = sym.sympify("5*x**3/6 - 10*x**2 + 50*x - 280/3")
    bending_moment3 = sym.sympify("10*x - 40")
    bending_moment = (
        a.segments[0].bending_moment == bending_moment1
        and a.segments[1].bending_moment == bending_moment2
        and a.segments[2].bending_moment == bending_moment3
    )

    deflection_1 = -(x**5) / (24 * E * I) + 5 * x**3 / (E * I) - 40 * x**2 / (E * I)
    deflection_2 = (
        x**5 / (24 * E * I)
        - 5 * x**4 / (6 * E * I)
        + 25 * x**3 / (3 * E * I)
        - 140 * x**2 / (3 * E * I)
        + 20 * x / (3 * E * I)
        - 8 / (3 * E * I)
    )
    deflection_3 = (
        5 * x**3 / (3 * E * I)
        - 20 * x**2 / (E * I)
        + 760 * x / (3 * E * I)
        - 1160 / (E * I)
    )
    deflection = (
        a.segments[0].deflection == deflection_1
        and a.segments[1].deflection == deflection_2
        and a.segments[2].deflection == deflection_3
    )
    rotation_1 = -5 * x**4 / (24 * E * I) + 15 * x**2 / (E * I) - 80 * x / (E * I)
    rotation_2 = (
        5 * x**4 / (24 * E * I)
        - 10 * x**3 / (3 * E * I)
        + 25 * x**2 / (E * I)
        - 280 * x / (3 * E * I)
        + 20 / (3 * E * I)
    )
    rotation_3 = 5 * x**2 / (E * I) - 40 * x / (E * I) + 760 / (3 * E * I)
    rotation = (
        a.segments[0].rotation == rotation_1
        and a.segments[1].rotation == rotation_2
        and a.segments[2].rotation == rotation_3
    )

    if not (length_points):
        errors.append("Error in the length of the list of points.")
    if not (length_segments):
        errors.append("Error in the length if the list of segments.")
    if not (x_coord):
        errors.append("Error in point coordinates.")
    if not (x_start_coord or x_end_coord):
        errors.append("Error in the segment coordinates.")
    if not (young) or not (inertia):
        errors.append("Error in the segment properties.")
    if not (reaction_force):
        errors.append("Error in reaction force computation.")
    if not (reaction_moment):
        errors.append("Error in reaction moment computation.")
    if not (shear_force):
        errors.append("Error in shear force diagram.")
    if not (bending_moment):
        errors.append("Error in bending moment diagram.")
    if not (deflection):
        errors.append("Error in deflection.")
    if not (rotation):
        errors.append("Error in rotation.")

    # An empty list is False for Python
    assert not errors, "The following errors occurred:\n{}".format("\n".join(errors))


def test_discontinuous_properties():
    """Test a beam with discontinuous inertia and Young modulus."""

    a = beam(3, x0=0)
    a.add_support(0.5, "pin")
    a.add_support(2.5, "roller")
    a.add_point_load(0, "-P")
    a.add_point_load(3, "-P")
    a.set_young(0, 1.5, E / 1000)
    a.set_young(1.5, 3, E)
    a.set_inertia(0, 1, I)
    a.set_inertia(1, 3, 100 * I)
    a.solve(output=False)

    errors = []
    length_points = len(a.points) == 6
    length_segments = len(a.segments) == 5

    x_coord = (
        a.points[0].x_coord == sym.sympify(0)
        and a.points[1].x_coord == sym.sympify(0.5)
        and a.points[2].x_coord == sym.sympify(1)
        and a.points[3].x_coord == sym.sympify(1.5)
        and a.points[4].x_coord == sym.sympify(2.5)
        and a.points[5].x_coord == sym.sympify(3)
    )

    x_start_coord = (
        a.segments[0].x_start == sym.sympify(0)
        and a.segments[1].x_start == sym.sympify(0.5)
        and a.segments[2].x_start == sym.sympify(1)
        and a.segments[3].x_start == sym.sympify(1.5)
        and a.segments[4].x_start == sym.sympify(2.5)
    )
    x_end_coord = (
        a.segments[0].x_end == sym.sympify(0.5)
        and a.segments[1].x_end == sym.sympify(1)
        and a.segments[2].x_end == sym.sympify(1.5)
        and a.segments[3].x_end == sym.sympify(2.5)
        and a.segments[4].x_end == sym.sympify(3)
    )
    young = (
        a.segments[0].young == E / 1000
        and a.segments[1].young == E / 1000
        and a.segments[2].young == E / 1000
        and a.segments[3].young == E
        and a.segments[4].young == E
    )
    inertia = (
        a.segments[0].inertia == I
        and a.segments[1].inertia == I
        and a.segments[2].inertia == I * 100
        and a.segments[3].inertia == I * 100
        and a.segments[4].inertia == I * 100
    )

    reaction_force = (
        a.points[0].reaction_force == sym.sympify(0)
        and a.points[1].reaction_force == P
        and a.points[2].reaction_force == sym.sympify(0)
        and a.points[3].reaction_force == sym.sympify(0)
        and a.points[4].reaction_force == P
        and a.points[5].reaction_force == sym.sympify(0)
    )
    reaction_moment = (
        a.points[0].reaction_moment == sym.sympify(0)
        and a.points[1].reaction_moment == sym.sympify(0)
        and a.points[2].reaction_moment == sym.sympify(0)
        and a.points[3].reaction_moment == sym.sympify(0)
        and a.points[4].reaction_moment == sym.sympify(0)
        and a.points[5].reaction_moment == sym.sympify(0)
        and a.points[5].reaction_moment == sym.sympify(0)
    )

    shear_force1 = P
    shear_force2 = sym.sympify(0)
    shear_force3 = -P
    shear_force = (
        (a.segments[0].shear_force - shear_force1).is_zero
        and (a.segments[1].shear_force - shear_force2).is_zero
        and (a.segments[2].shear_force - shear_force2).is_zero
        and (a.segments[3].shear_force - shear_force2).is_zero
        and (a.segments[4].shear_force - shear_force3).is_zero
    )
    bending_moment1 = -P * x
    bending_moment2 = -0.5 * P
    bending_moment3 = P * x - 3.0 * P
    bending_moment = (
        a.segments[0].bending_moment == bending_moment1
        and a.segments[1].bending_moment == bending_moment2
        and a.segments[2].bending_moment == bending_moment2
        and a.segments[3].bending_moment == bending_moment2
        and a.segments[4].bending_moment == bending_moment3
    )

    deflection_1 = (
        -500 * P * x**3 / (3 * E * I)
        + 345.31375 * P * x / (E * I)
        - 151.823541666667 * P / (E * I)
    )
    deflection_2 = (
        -250.0 * P * x**2 / (E * I) + 470.31375 * P * x / (E * I) - 172.656875 * P / (E * I)
    )
    deflection_3 = (
        -2.5 * P * x**2 / (E * I) - 24.68625 * P * x / (E * I) + 74.843125 * P / (E * I)
    )
    deflection_4 = (
        -0.0025 * P * x**2 / (E * I) - 32.17875 * P * x / (E * I) + 80.4625 * P / (E * I)
    )
    deflection_5 = (
        0.0016666666666666 * P * x**3 / (E * I)
        - 0.015 * P * x**2 / (E * I)
        - 32.1475 * P * x / (E * I)
        + 80.4364583333333 * P / (E * I)
    )
    deflection = (
        a.segments[0].deflection.evalf(10) == deflection_1.evalf(10)
        and a.segments[1].deflection == deflection_2
        and a.segments[2].deflection == deflection_3
        and a.segments[3].deflection == deflection_4
        and a.segments[4].deflection.evalf(10) == deflection_5.evalf(10)
    )
    rotation_1 = -500 * P * x**2 / (E * I) + 345.31375 * P / (E * I)
    rotation_2 = -500.0 * P * x / (E * I) + 470.31375 * P / (E * I)
    rotation_3 = -5.0 * P * x / (E * I) - 24.68625 * P / (E * I)
    rotation_4 = -0.005 * P * x / (E * I) - 32.17875 * P / (E * I)
    rotation_5 = 0.005 * P * x**2 / (E * I) - 0.03 * P * x / (E * I) - 32.1475 * P / (E * I)
    rotation = (
        (a.segments[0].rotation - rotation_1).is_zero
        and (a.segments[1].rotation - rotation_2).is_zero
        and (a.segments[2].rotation - rotation_3).is_zero
        and (a.segments[3].rotation - rotation_4).is_zero
        and (a.segments[4].rotation - rotation_5).is_zero
    )

    if not (length_points):
        errors.append("Error in the length of the list of points.")
    if not (length_segments):
        errors.append("Error in the length if the list of segments.")
    if not (x_coord):
        errors.append("Error in point coordinates.")
    if not (x_start_coord or x_end_coord):
        errors.append("Error in the segment coordinates.")
    if not (young) or not (inertia):
        errors.append("Error in the segment properties.")
    if not (reaction_force):
        errors.append("Error in reaction force computation.")
    if not (reaction_moment):
        errors.append("Error in reaction moment computation.")
    if not (shear_force):
        errors.append("Error in shear force diagram.")
    if not (bending_moment):
        errors.append("Error in bending moment diagram.")
    if not (deflection):
        errors.append("Error in deflection.")
    if not (rotation):
        errors.append("Error in rotation.")

    # An empty list is False for Python
    assert not errors, "The following errors occurred:\n{}".format("\n".join(errors))


def test_output_symbolic(capsys):
    """Test if the output with symbolic variables works."""
    with capsys.disabled():
        with io.StringIO() as buf, redirect_stdout(buf):
            output_baseline = open(
                "tests/output_baseline/baseline_output_symbolic.txt"
            ).read()
            baseline_output_symbolic()
            assert output_baseline == buf.getvalue()


def test_output_numeric(capsys):
    """Test if the output with numeric variables works."""
    with capsys.disabled():
        with io.StringIO() as buf, redirect_stdout(buf):
            output_baseline = open(
                "tests/output_baseline/baseline_output_numeric.txt"
            ).read()
            baseline_output_numeric()
            assert output_baseline == buf.getvalue()


def test_output_springs_numeric(capsys):
    """Test if the output with springs and numeric variables works."""
    with capsys.disabled():
        with io.StringIO() as buf, redirect_stdout(buf):
            output_baseline = open(
                "tests/output_baseline/baseline_output_springs_numeric.txt"
            ).read()
            baseline_output_springs_numeric()
            assert output_baseline == buf.getvalue()


def test_output_springs_symbolic(capsys):
    """Test if the output with springs and symbolic variables works."""
    with capsys.disabled():
        with io.StringIO() as buf, redirect_stdout(buf):
            output_baseline = open(
                "tests/output_baseline/baseline_output_springs_symbolic.txt"
            ).read()
            baseline_output_springs_symbolic()
            assert output_baseline == buf.getvalue()


def test_cantilever_beam_with_endpoint_springs():
    """Test a beam with endpoint springs."""
    # Solve the problem with Euler-Bernoulli finite elements
    L = sym.symbols("L")
    P = sym.symbols("P")
    M = sym.symbols("M")
    k_theta = sym.symbols("k_theta")
    k_v = sym.symbols("k_v")
    E = sym.symbols("E")
    I = sym.symbols("I")

    v1 = sym.symbols("v1")
    theta1 = sym.symbols("theta1")
    v2 = sym.symbols("v2")
    theta2 = sym.symbols("theta2")
    v1 = sym.sympify(0)
    theta1 = sym.sympify(0)

    k = euler_bernoulli_stiff_matrix(E, I, L)
    equations = [
        k[2, 2] * v2 + k[2, 3] * theta2 + k_v * v2 - P,
        k[3, 2] * v2 + k[3, 3] * theta2 + k_theta * theta2 - M,
    ]
    solutions = sym.solve(equations, (v2, theta2))
    v2 = solutions[v2]
    theta2 = solutions[theta2]

    N = hermite_polynomials(x, 0, L)
    displacement = N[0] * v1 + N[1] * theta1 + N[2] * v2 + N[3] * theta2
    rotation = compute_rotation(displacement, x)
    bending_moment = compute_bending_moment(displacement, E, I, x)
    shear_force = computes_shear_force(bending_moment, x)

    # Solve the problem with SymBeam
    test_beam = beam("L", x0=0)
    test_beam.add_support(0, "fixed")
    test_beam.add_point_load("L", "P")
    test_beam.add_point_moment("L", "M")
    test_beam.add_rotational_spring("L", "k_theta")
    test_beam.add_transverse_spring("L", "k_v")
    test_beam.solve(output=False)

    # Compare results
    disp_comp = (sym.simplify(test_beam.segments[0].deflection - displacement)).is_zero
    rot_comp = (sym.simplify(test_beam.segments[0].rotation - rotation)).is_zero
    bend_comp = (
        sym.simplify(test_beam.segments[0].bending_moment - bending_moment)
    ).is_zero
    shear_comp = (sym.simplify(test_beam.segments[0].shear_force - shear_force)).is_zero

    errors = []
    if not (disp_comp):
        errors.append("Error in the deflection.")
    if not (rot_comp):
        errors.append("Error in the rotation.")
    if not (bend_comp):
        errors.append("Error in the bending moment.")
    if not (shear_comp):
        errors.append("Error in the shear force.")

    assert not errors, "The following errors occurred:\n{}".format("\n".join(errors))


def test_cantilever_beam_with_midpoint_springs():
    """Test a beam with midpoint springs."""
    # Solve the problem with Euler-Bernoulli finite elements
    L = sym.symbols("L")
    P = sym.symbols("P")
    M = sym.symbols("M")
    k_theta = sym.symbols("k_theta")
    k_v = sym.symbols("k_v")
    E = sym.symbols("E")
    I = sym.symbols("I")

    v1 = sym.symbols("v1")
    theta1 = sym.symbols("theta1")
    v2 = sym.symbols("v2")
    theta2 = sym.symbols("theta2")
    v3 = sym.symbols("v3")
    theta3 = sym.symbols("theta3")
    v1 = sym.sympify(0)
    theta1 = sym.sympify(0)

    k = euler_bernoulli_stiff_matrix(E, I, L / 2)
    equations = [
        (k[2, 2] + k[0, 0]) * v2
        + (k[2, 3] + k[0, 1]) * theta2
        + k[0, 2] * v3
        + k[0, 3] * theta3
        + k_v * v2,
        (k[3, 2] + k[1, 0]) * v2
        + (k[3, 3] + k[1, 1]) * theta2
        + k[1, 2] * v3
        + k[1, 3] * theta3
        + k_theta * theta2,
        k[2, 0] * v2 + k[2, 1] * theta2 + k[2, 2] * v3 + k[2, 3] * theta3 - P,
        k[3, 0] * v2 + k[3, 1] * theta2 + k[3, 2] * v3 + k[3, 3] * theta3 - M,
    ]
    solutions = sym.solve(equations, (v2, theta2, v3, theta3))
    v2 = solutions[v2]
    theta2 = solutions[theta2]
    v3 = solutions[v3]
    theta3 = solutions[theta3]

    N = hermite_polynomials(x, 0, L / 2)
    displacement_1 = N[0] * v1 + N[1] * theta1 + N[2] * v2 + N[3] * theta2
    rotation_1 = compute_rotation(displacement_1, x)
    bending_moment_1 = compute_bending_moment(displacement_1, E, I, x)
    shear_force_1 = computes_shear_force(bending_moment_1, x)

    N = hermite_polynomials(x, L / 2, L / 2)
    displacement_2 = N[0] * v2 + N[1] * theta2 + N[2] * v3 + N[3] * theta3
    rotation_2 = compute_rotation(displacement_2, x)
    bending_moment_2 = compute_bending_moment(displacement_2, E, I, x)
    shear_force_2 = computes_shear_force(bending_moment_2, x)

    # Solve the problem with SymBeam
    test_beam = beam("L", x0=0)
    test_beam.add_support(0, "fixed")
    test_beam.add_point_load("L", "P")
    test_beam.add_point_moment("L", "M")
    test_beam.add_rotational_spring("L/2", "k_theta")
    test_beam.add_transverse_spring("L/2", "k_v")
    test_beam.solve(output=False)

    # Compare results
    disp_comp = (
        sym.simplify(test_beam.segments[0].deflection - displacement_1)
    ).is_zero and (sym.simplify(test_beam.segments[1].deflection - displacement_2)).is_zero
    rot_comp = (sym.simplify(test_beam.segments[0].rotation - rotation_1)).is_zero and (
        sym.simplify(test_beam.segments[1].rotation - rotation_2)
    ).is_zero
    bend_comp = (
        sym.simplify(test_beam.segments[0].bending_moment - bending_moment_1)
    ).is_zero and (
        sym.simplify(test_beam.segments[1].bending_moment - bending_moment_2)
    ).is_zero
    shear_comp = (
        sym.simplify(test_beam.segments[0].shear_force - shear_force_1)
    ).is_zero and (sym.simplify(test_beam.segments[1].shear_force - shear_force_2)).is_zero

    errors = []
    if not (disp_comp):
        errors.append("Error in the deflection.")
    if not (rot_comp):
        errors.append("Error in the rotation.")
    if not (bend_comp):
        errors.append("Error in the bending moment.")
    if not (shear_comp):
        errors.append("Error in the shear force.")

    assert not errors, "The following errors occurred:\n{}".format("\n".join(errors))


def test_complex_beam_with_springs_and_hinge():
    """Test a beam with midpoint springs."""
    # Solve the problem with Euler-Bernoulli finite elements
    L = sym.symbols("L")
    P = sym.symbols("P")
    M = sym.symbols("M")
    k_theta = sym.symbols("k_theta")
    k_v = sym.symbols("k_v")
    E = sym.symbols("E")
    I = sym.symbols("I")

    v1 = sym.symbols("v1")
    theta1 = sym.symbols("theta1")
    v2 = sym.symbols("v2")
    theta2 = sym.symbols("theta2")
    v3 = sym.symbols("v3")
    theta3 = sym.symbols("theta3")
    v4 = sym.symbols("v4")
    theta4l = sym.symbols("theta4l")
    theta4r = sym.symbols("theta4r")
    v5 = sym.symbols("v5")
    theta5 = sym.symbols("theta5")
    v6 = sym.symbols("v6")
    theta6 = sym.symbols("theta6")
    v7 = sym.symbols("v7")
    theta7 = sym.symbols("theta7")

    v1 = sym.sympify(0)
    theta1 = sym.sympify(0)
    v7 = sym.sympify(0)

    k = euler_bernoulli_stiff_matrix(E, I, L / 6)
    equations = [sym.sympify(0) for _i in range(12)]
    map_eldof_glbdof = {
        1: [v1, theta1, v2, theta2],
        2: [v2, theta2, v3, theta3],
        3: [v3, theta3, v4, theta4l],
        4: [v4, theta4r, v5, theta5],
        5: [v5, theta5, v6, theta6],
        6: [v6, theta6, v7, theta7],
    }
    map_glbdof_equation_index = {
        v1: -1,
        theta1: -1,
        v2: 0,
        theta2: 1,
        v3: 2,
        theta3: 3,
        v4: 4,
        theta4l: 5,
        theta4r: 6,
        v5: 7,
        theta5: 8,
        v6: 9,
        theta6: 10,
        v7: -1,
        theta7: 11,
    }
    for el in map_eldof_glbdof:
        eldofs = map_eldof_glbdof[el]
        for i in range(len(eldofs)):
            equation_index = map_glbdof_equation_index[eldofs[i]]
            if equation_index == -1:
                continue
            for j in range(len(eldofs)):
                equations[equation_index] += k[i, j] * eldofs[j]
                if equation_index == -1:
                    continue

    equations[map_glbdof_equation_index[v2]] -= P
    equations[map_glbdof_equation_index[theta5]] -= M
    equations[map_glbdof_equation_index[v3]] += k_v * v3
    equations[map_glbdof_equation_index[theta6]] += k_theta * theta6
    solutions = sym.solve(
        equations,
        (v2, theta2, v3, theta3, v4, theta4l, theta4r, v5, theta5, v6, theta6, v7, theta7),
    )

    v2 = solutions[v2]
    theta2 = solutions[theta2]
    v3 = solutions[v3]
    theta3 = solutions[theta3]
    v4 = solutions[v4]
    theta4l = solutions[theta4l]
    theta4r = solutions[theta4r]
    v5 = solutions[v5]
    theta5 = solutions[theta5]
    v6 = solutions[v6]
    theta6 = solutions[theta6]
    theta7 = solutions[theta7]
    map_eldof_glbdof = {
        1: [v1, theta1, v2, theta2],
        2: [v2, theta2, v3, theta3],
        3: [v3, theta3, v4, theta4l],
        4: [v4, theta4r, v5, theta5],
        5: [v5, theta5, v6, theta6],
        6: [v6, theta6, v7, theta7],
    }

    displacement = []
    rotation = []
    bending_moment = []
    shear_force = []

    for iel in map_eldof_glbdof:
        eldofs = map_eldof_glbdof[iel]
        x0 = (iel - 1) * L / 6
        N = hermite_polynomials(x, x0, L / 6)
        disp_iel = N[0] * eldofs[0] + N[1] * eldofs[1] + N[2] * eldofs[2] + N[3] * eldofs[3]
        rot_iel = compute_rotation(disp_iel, x)
        bend_iel = compute_bending_moment(disp_iel, E, I, x)
        shear_iel = computes_shear_force(bend_iel, x)

        displacement.append(disp_iel)
        rotation.append(rot_iel)
        bending_moment.append(bend_iel)
        shear_force.append(shear_iel)

    # Solve the problem with SymBeam
    test_beam = beam("L", x0=0)
    test_beam.add_support(0, "fixed")
    test_beam.add_support("L", "roller")
    test_beam.add_support("L/2", "hinge")
    test_beam.add_point_load("L/6", "P")
    test_beam.add_point_moment("4*L/6", "M")
    test_beam.add_rotational_spring("5*L/6", "k_theta")
    test_beam.add_transverse_spring("2*L/6", "k_v")
    test_beam.solve(output=False)

    # Compare results
    disp_comp = all(
        [
            (sym.simplify(test_beam.segments[i].deflection - displacement[i])).is_zero
            for i in range(len(test_beam.segments))
        ]
    )
    rot_comp = all(
        [
            (sym.simplify(test_beam.segments[i].rotation - rotation[i])).is_zero
            for i in range(len(test_beam.segments))
        ]
    )
    bend_comp = all(
        [
            (sym.simplify(test_beam.segments[i].bending_moment - bending_moment[i])).is_zero
            for i in range(len(test_beam.segments))
        ]
    )
    shear_comp = all(
        [
            (sym.simplify(test_beam.segments[i].shear_force - shear_force[i])).is_zero
            for i in range(len(test_beam.segments))
        ]
    )

    errors = []
    if not (disp_comp):
        errors.append("Error in the deflection.")
    if not (rot_comp):
        errors.append("Error in the rotation.")
    if not (bend_comp):
        errors.append("Error in the bending moment.")
    if not (shear_comp):
        errors.append("Error in the shear force.")

    assert not errors, "The following errors occurred:\n{}".format("\n".join(errors))


def test_rotational_spring_on_hinge():
    """Test that a rotational spring cannot be added on a hinge."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.add_support(0, "fixed")
        a.add_support("l", "roller")
        a.add_support("l/2", "hinge")
        a.add_point_load("l/2", "P")
        a.add_rotational_spring("l/2", "k_theta")
        a.solve(output=False)


def test_rotational_spring_on_fixed():
    """Test that a rotational spring cannot be added on a fixed support."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.add_support(0, "fixed")
        a.add_support("l", "roller")
        a.add_support("l/2", "hinge")
        a.add_point_load("l/2", "P")
        a.add_rotational_spring(0, "k_theta")
        a.solve(output=False)


def test_transverse_spring_on_pin():
    """Test that a transverse spring cannot be added on a pin support."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.add_support(0, "pin")
        a.add_support("l", "roller")
        a.add_point_load("l/2", "P")
        a.add_transverse_spring(0, "k_v")
        a.solve(output=False)


def test_transverse_spring_on_roller():
    """Test that a transverse spring cannot be added on a roller support."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.add_support(0, "fixed")
        a.add_support("l", "roller")
        a.add_support("l/2", "hinge")
        a.add_point_load("l/2", "P")
        a.add_transverse_spring("l", "k_v")
        a.solve(output=False)


def test_transverse_spring_on_fixed():
    """Test that a transverse spring cannot be added on fixed support"""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.add_support(0, "fixed")
        a.add_support("l", "roller")
        a.add_support("l/2", "hinge")
        a.add_point_load("l/2", "P")
        a.add_transverse_spring(0, "k_v")
        a.solve(output=False)


def test_monolithic_not_unique_solution():
    """Test that an error is raised when a beam with springs (monolithic solver) has not a
    unique solution."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.add_transverse_spring(0, "k_v")
        a.add_point_moment("l", "M")
        a.solve(output=False)


def test_monolithic_hyperstatic():
    """Test that an error is raised when a beam with springs (monolithic solver) is
    hyperstatic."""
    with pytest.raises(RuntimeError):
        a = beam("l", x0=0)
        a.add_support(0, "fixed")
        a.add_support("l", "roller")
        a.add_transverse_spring("l/2", "k_v")
        a.add_point_load("l/2", "P")
        a.solve(output=True)


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True, tolerance=0.1)
def test_plot_point_loads():
    """Test the plotting function for pins, rollers, hinges  and point forces and moments.
    The figures generated with the current version are compared against reference files.
    """
    a = beam(L)
    a.add_support(0, "pin")
    a.add_support(L / 4, "roller")
    a.add_support(L / 2, "hinge")
    a.add_support(L, "roller")
    a.add_point_load(L / 4, -P)
    a.add_point_load(3 * L / 4, P / 2)
    a.add_point_moment(L / 8, M)
    a.add_point_moment(7 * L / 8, -M / 2)
    a.solve()
    fig, ax = a.plot(subs={"P": 1000, "L": 2, "M": 1000})
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True, tolerance=0.1)
def test_plot_distributed_loads_fixed_left():
    """Test the plotting function for distributed loads and fixed support on the left.
    Additionally, test plotting of continuity points.
    """
    a = beam(L)
    a.add_support(0, "fixed")
    a.add_distributed_load(0, L / 2, "-q * x")
    a.add_distributed_load(L / 2, L, "q * (L - x)")
    a.solve()
    fig, ax = a.plot(subs={"q": 1000})
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True, tolerance=0.1)
def test_plot_distributed_loads_fixed_right():
    """Test the plotting function for distributed loads and fixed support on the right."""
    a = beam(L)
    a.add_support(L, "fixed")
    a.add_distributed_load(0, L / 2, "-q * x")
    a.add_distributed_load(L / 2, L, "q * (L - x)")
    a.solve()
    fig, ax = a.plot(subs={"q": 1000})
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True, tolerance=0.1)
def test_plot_beam_with_springs():
    """Test the plotting function for a beam with springs."""
    L = 1.0
    M = 1.0
    P = 1.0
    I = 1.0
    E = 1.0
    kv = 100.0
    ktheta = 100.0
    a = beam(L, x0=0)
    a.set_inertia(0, L, I)
    a.set_young(0, L, E)
    a.add_support(0, "pin")
    a.add_support(0.25 * L, "hinge")
    a.add_support(0.5 * L, "roller")
    a.add_support(L, "roller")
    a.add_transverse_spring(0.125 * L, kv)
    a.add_rotational_spring(0, ktheta)
    a.add_rotational_spring(0.5 * L, ktheta)
    a.add_transverse_spring(0.25 * L, kv)
    a.add_transverse_spring(0.75 * L, kv)
    a.add_rotational_spring(0.75 * L, ktheta)
    a.add_rotational_spring(0.875 * L, ktheta)
    a.add_point_moment(L, M)
    a.add_point_load(L / 3, -P)
    a.add_distributed_load(L / 7, 5 * L / 7, "-(2 - 2*x**2)")
    a.solve()
    fig, ax = a.plot()
    return fig
