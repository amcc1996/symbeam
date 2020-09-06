# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Numeric length
#           2. Roller
#           3. Hinge
#           4. Fixed
#           5. Numeric distributed constant load
#           6. Numeric distributed quadratic load

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam(4, x0=0)
test_beam.add_support(0, "roller")
test_beam.add_support(1, "hinge")
test_beam.add_support(4, "fixed")
test_beam.add_distributed_load(0, 2, "-5")
test_beam.add_distributed_load(2, 4, "-(4*x**2 - 24 *x + 37)")
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
