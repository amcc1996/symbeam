# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Numeric length
#           2. Fixed
#           3. Hinge
#           4. Roller
#           5. Numeric point moment
#           6. Two numeric distributed linear loads

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam(6, x0=0)
test_beam.add_support(0, "fixed")
test_beam.add_support(4, "hinge")
test_beam.add_support(6, "roller")
test_beam.add_point_moment(6, 20)
test_beam.add_distributed_load(0, 2, "-5*x")
test_beam.add_distributed_load(2, 4, "-(20-5*x)")
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
