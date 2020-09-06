# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Numeric length
#           2. Pin
#           3. Roller
#           4. Numeric point force
#           5. Classical pinned beam problem with half-span force

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam("l", x0=0)
test_beam.add_support(0, "pin")
test_beam.add_support("l", "roller")
test_beam.add_point_load("l/2", "-P")
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
