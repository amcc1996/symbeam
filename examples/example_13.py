# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Symbolic length
#           2. Fixed
#           3. Symbolic point moment
#           4. Classical clamped beam problem

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam("L", x0=0)
test_beam.add_support(0, "fixed")
test_beam.add_point_moment("L", "M")
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
