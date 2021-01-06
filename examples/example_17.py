# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
#
# Credit to Bernardo Ferreira (2020) for detecting the bug where SymBeam would fail when
# the length of the beam contains both numbers and symbols, like "3*l"
# Features: 1. Symbolic length scaled by number
#           2. Roller
#           3. Hinge
#           4. Fixed
#           4. Symbolic distributed linear load
#           4. Symbolic distributed quadratic load

import matplotlib.pyplot as plt

from symbeam import beam


test_beam = beam("3*l", x0=0)
test_beam.add_support("l", "roller")
test_beam.add_support("2*l", "hinge")
test_beam.add_support("3*l", "fixed")
test_beam.add_distributed_load(0, "l", "- q / l * x")
test_beam.add_distributed_load("2*l", "3*l", "q / l**2 * x**2 - 6*q*x/l + 9*q")
test_beam.solve()
fig, ax = test_beam.plot()
plt.savefig(__file__.split(".py")[0] + ".svg")
