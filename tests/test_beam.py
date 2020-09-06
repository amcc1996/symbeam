import pytest
import sympy as sym

from sympy.abc import E, I, L, M, P, q, x

from symbeam.beam import beam


def test_beam_two_symbols():
    """Test if an error is reaised if more than one symbols is used to initialise the beam."""
    with pytest.raises(RuntimeError):
        a = beam("L * a", x0=0)


def test_beam_distinct_symbols():
    """Test if an error is reaised if the symbols used for the inital position and length
    are distinct.
    """
    with pytest.raises(RuntimeError):
        a = beam("L * a", x0="b")


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

    deflection = a.segments[0].deflection == -L * P * x ** 2 / (2 * E * I) + P * x ** 3 / (
        6 * E * I
    )
    rotation = a.segments[0].rotation == -L * P * x / (E * I) + P * x ** 2 / (2 * E * I)

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
    assert not errors, "The following errors ocurred:\n{}".format("\n".join(errors))


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

    deflection = a.segments[0].deflection == M * x ** 2 / (2 * E * I)
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
    assert not errors, "The following errors ocurred:\n{}".format("\n".join(errors))


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

    deflection_1 = -P * L ** 2 * x / (16 * E * I) + P * x ** 3 / (12 * E * I)
    deflection_2 = (
        P * L ** 3 / (48 * E * I)
        - 3 * P * L ** 2 * x / (16 * E * I)
        + P * L * x ** 2 / (4 * E * I)
        - P * x ** 3 / (12 * E * I)
    )
    rotation_1 = -P * L ** 2 / (16 * E * I) + P * x ** 2 / (4 * E * I)
    rotation_2 = (
        -3 * P * L ** 2 / (16 * E * I) + P * L * x / (2 * E * I) - P * x ** 2 / (4 * E * I)
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
    assert not errors, "The following errors ocurred:\n{}".format("\n".join(errors))


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

    shear_force1 = sym.sympify(5 * x ** 2 / 2 - 30)
    shear_force2 = sym.sympify(-5 * x ** 2 / 2 + 20 * x - 50)
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

    deflection_1 = -(x ** 5) / (24 * E * I) + 5 * x ** 3 / (E * I) - 40 * x ** 2 / (E * I)
    deflection_2 = (
        x ** 5 / (24 * E * I)
        - 5 * x ** 4 / (6 * E * I)
        + 25 * x ** 3 / (3 * E * I)
        - 140 * x ** 2 / (3 * E * I)
        + 20 * x / (3 * E * I)
        - 8 / (3 * E * I)
    )
    deflection_3 = (
        5 * x ** 3 / (3 * E * I)
        - 20 * x ** 2 / (E * I)
        + 760 * x / (3 * E * I)
        - 1160 / (E * I)
    )
    deflection = (
        a.segments[0].deflection == deflection_1
        and a.segments[1].deflection == deflection_2
        and a.segments[2].deflection == deflection_3
    )
    rotation_1 = -5 * x ** 4 / (24 * E * I) + 15 * x ** 2 / (E * I) - 80 * x / (E * I)
    rotation_2 = (
        5 * x ** 4 / (24 * E * I)
        - 10 * x ** 3 / (3 * E * I)
        + 25 * x ** 2 / (E * I)
        - 280 * x / (3 * E * I)
        + 20 / (3 * E * I)
    )
    rotation_3 = 5 * x ** 2 / (E * I) - 40 * x / (E * I) + 760 / (3 * E * I)
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
    assert not errors, "The following errors ocurred:\n{}".format("\n".join(errors))


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
        a.segments[0].shear_force == shear_force1
        and a.segments[1].shear_force == shear_force2
        and a.segments[2].shear_force == shear_force2
        and a.segments[3].shear_force == shear_force2
        and a.segments[4].shear_force == shear_force3
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
        -500 * P * x ** 3 / (3 * E * I)
        + 345.31375 * P * x / (E * I)
        - 151.823541666667 * P / (E * I)
    )
    deflection_2 = (
        -250.0 * P * x ** 2 / (E * I)
        + 470.31375 * P * x / (E * I)
        - 172.656875 * P / (E * I)
    )
    deflection_3 = (
        -2.5 * P * x ** 2 / (E * I) - 24.68625 * P * x / (E * I) + 74.843125 * P / (E * I)
    )
    deflection_4 = (
        -0.0025 * P * x ** 2 / (E * I) - 32.17875 * P * x / (E * I) + 80.4625 * P / (E * I)
    )
    deflection_5 = (
        0.0016666666666666 * P * x ** 3 / (E * I)
        - 0.015 * P * x ** 2 / (E * I)
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
    rotation_1 = -500 * P * x ** 2 / (E * I) + 345.31375 * P / (E * I)
    rotation_2 = -500.0 * P * x / (E * I) + 470.31375 * P / (E * I)
    rotation_3 = -5.0 * P * x / (E * I) - 24.68625 * P / (E * I)
    rotation_4 = -0.005 * P * x / (E * I) - 32.17875 * P / (E * I)
    rotation_5 = (
        0.005 * P * x ** 2 / (E * I) - 0.03 * P * x / (E * I) - 32.1475 * P / (E * I)
    )
    rotation = (
        a.segments[0].rotation == rotation_1
        and a.segments[1].rotation == rotation_2
        and a.segments[2].rotation == rotation_3
        and a.segments[3].rotation == rotation_4
        and a.segments[4].rotation == rotation_5
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
    assert not errors, "The following errors ocurred:\n{}".format("\n".join(errors))


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
