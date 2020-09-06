# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Numeric
#           2. Pin
#           3. Roller
#           4. Numeric sinusoidal distributed force

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam(1, x0=0)
test_beam.add_support(0, "pin")
test_beam.add_support(1, "roller")
test_beam.add_distributed_load(0, 1, "sin(20 * x)")
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
