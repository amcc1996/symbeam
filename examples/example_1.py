# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Symbolic length
#           2. Roller
#           3. Pin
#           4. Symbolic distributed linear load
#           5. Symbolic distributed constant load

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam("l", x0=0)
test_beam.add_support(0, "roller")
test_beam.add_support("l", "pin")
test_beam.add_distributed_load(0, "l/2", "-2 * q / l * x")
test_beam.add_distributed_load("l/2", "l", "-q")
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
