# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2025
# Features: 1. Combined transverse and rotational springs as flexible supports
#           3. Symbolic calculation

import matplotlib.pyplot as plt
import sympy

from sympy.abc import E, I, L, k

from symbeam import beam


test_beam = beam(L, x0=0)
test_beam.set_young(0, L, E)
test_beam.set_inertia(0, L, I)
test_beam.add_rotational_spring(0, k)
test_beam.add_rotational_spring(L, k)
test_beam.add_transverse_spring(0, k)
test_beam.add_transverse_spring(L, k)
test_beam.add_distributed_load(0, L, sympy.sympify("q"))
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
