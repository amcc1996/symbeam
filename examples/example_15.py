# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Numeric length
#           2. Pin
#           3. Roller
#           4. Set of numeric point forces and moments

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam("l", x0=0)
test_beam.add_support(0, "pin")
test_beam.add_support("l", "roller")
test_beam.add_point_load("l/4", "P")
test_beam.add_point_moment("l/4", "P*l / 2")
test_beam.add_point_load("l/2", "-2*P")
test_beam.add_point_moment("7*l/8", "-P*l")
test_beam.add_point_load("3*l/4", "-3*P")
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
