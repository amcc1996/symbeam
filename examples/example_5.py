# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Numeric length
#           2. Pin
#           3. Two rollers
#           4. Numeric distributed constant load
#           5. Numeric distributed quadratic load

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam(6, x0=0)
test_beam.add_support(0, "roller")
test_beam.add_support(2, "roller")
test_beam.add_support(6, "pin")
test_beam.add_support(4, "hinge")
test_beam.add_distributed_load(0, 4, -5)
test_beam.add_distributed_load(4, 6, "-(-3*(x-5)**2 + 8)")
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
