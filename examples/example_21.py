# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2025
# Features: 1. Isolated transverse spring
#           2. Isolated rotational spring
#           3. Combined transverse and rotational springs
#           4. Pin combined with rotational spring
#           5. Roller combined with rotational spring
#           6. Hinges with spring
#           7. Numerical calculation

import matplotlib.pyplot as plt

from symbeam import beam


L = 1.0
E = 1.0
I = 1.0
q = 1.0
k_theta = 100.0
k_v = 100.0
M = 0.2
P = -0.4
test_beam = beam(L, x0=0)
test_beam.set_young(0, L, E)
test_beam.set_inertia(0, L, I)
test_beam.add_support(0, "pin")
test_beam.add_support(L / 4, "hinge")
test_beam.add_support(L / 2, "roller")
test_beam.add_support(3 * L / 4, "hinge")
test_beam.add_rotational_spring(0, k_theta)
test_beam.add_rotational_spring(L / 2, k_theta)
test_beam.add_transverse_spring(3 * L / 4, k_v)
test_beam.add_transverse_spring(L / 8, k_v)
test_beam.add_rotational_spring(7 * L / 8, k_theta)
test_beam.add_transverse_spring(5 * L / 8, k_v)
test_beam.add_rotational_spring(5 * L / 8, k_theta)
test_beam.add_point_moment(L, M)
test_beam.add_point_load(3 * L / 8, P)
test_beam.add_distributed_load(L / 16, 15 * L / 16, "-2*(x + x**2)")

test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
