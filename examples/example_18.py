# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2025
# Features: 1. Isolated transverse spring
#           2. Isolated rotational spring
#           3. Combined transverse and rotational springs
#           4. Numerical calculation

import matplotlib.pyplot as plt

from symbeam import beam


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
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
