# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Numeric length
#           2. Fixed
#           3. Hinge
#           4. Numeric linear distributed load
#           5. Numeric contstant distributed load
#           6. Numeric point moment

from symbeam.beam import beam
import matplotlib.pyplot as plt

test_beam = beam(6, x0=0)
test_beam.add_support(0, 'fixed')
test_beam.add_support(2, 'hinge')
test_beam.add_support(4, 'roller')
test_beam.add_distributed_load(0, 4, '-5/4 * x')
test_beam.add_distributed_load(4, 6, -5)
test_beam.add_point_moment(4, 20)
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split('.py')[0]+'.svg')
