# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Numeric length
#           2. Pin
#           3. Roller
#           4. Symbolic point load

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam(3, x0=0)
test_beam.add_support(0.5, "pin")
test_beam.add_support(2.5, "roller")
test_beam.add_point_load(0, "-P")
test_beam.add_point_load(3, "-P")
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
