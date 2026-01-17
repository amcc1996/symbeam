from contextlib import redirect_stdout

import sympy

from sympy.abc import E, I, L, k

from symbeam import beam


def baseline_output_symbolic():
    """Generate baseline output for symbolic beam example."""
    test_beam = beam("l", x0=0)
    test_beam.add_support(0, "roller")
    test_beam.add_support("l", "pin")
    test_beam.add_distributed_load(0, "l/2", "-2 * q / l * x")
    test_beam.add_distributed_load("l/2", "l", "-q")
    test_beam.solve()


def baseline_output_numeric():
    """Generate baseline output for numeric beam example."""
    test_beam = beam(6, x0=0)
    test_beam.add_support(0, "fixed")
    test_beam.add_support(2, "hinge")
    test_beam.add_support(4, "roller")
    test_beam.add_distributed_load(0, 4, "-5/4 * x")
    test_beam.add_distributed_load(4, 6, -5)
    test_beam.add_point_moment(4, 20)
    test_beam.solve()


def baseline_output_springs_numeric():
    """Generate baseline output for beam with springs numeric example."""
    L = 1.0
    E = 1.0
    I = 1.0
    P = -1.0
    k_theta = 100.0
    k_v = 100.0
    test_beam = beam(L, x0=0)
    test_beam.set_young(0, L, E)
    test_beam.set_inertia(0, L, I)
    test_beam.add_support(0, "fixed")
    test_beam.add_point_load(L, P)
    test_beam.add_rotational_spring(L / 4, k_theta)
    test_beam.add_transverse_spring(L / 2, k_v)
    test_beam.add_rotational_spring(3 * L / 4, k_theta)
    test_beam.add_transverse_spring(3 * L / 4, k_v)
    test_beam.solve()


def baseline_output_springs_symbolic():
    """Generate baseline output for beam with springs symbolic example."""
    test_beam = beam(L, x0=0)
    test_beam.set_young(0, L, E)
    test_beam.set_inertia(0, L, I)
    test_beam.add_support(0, "pin")
    test_beam.add_support(L, "roller")
    test_beam.add_rotational_spring(0, k)
    test_beam.add_rotational_spring(L, k)
    test_beam.add_distributed_load(0, L, sympy.sympify("q*x*(x-L)-q"))
    test_beam.solve()


if __name__ == "__main__":
    func_list = [
        baseline_output_symbolic,
        baseline_output_numeric,
        baseline_output_springs_numeric,
        baseline_output_springs_symbolic,
    ]
    file_names = [
        "baseline_output_symbolic.txt",
        "baseline_output_numeric.txt",
        "baseline_output_springs_numeric.txt",
        "baseline_output_springs_symbolic.txt",
    ]
    for i in range(len(func_list)):
        with open(f"tests/output_baseline/{file_names[i]}", "w") as f:
            with redirect_stdout(f):
                func_list[i]()
