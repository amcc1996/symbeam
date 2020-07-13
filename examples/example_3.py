# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Symbolic length
#           2. Fixed
#           3. Hinge
#           4. Symbolic contstant linear load
#           5. Symbolic point load

from symbeam.beam import beam
import matplotlib.pyplot as plt

test_beam = beam('l', x0=0)
test_beam.add_support(0, 'fixed')
test_beam.add_support('l/2', 'hinge')
test_beam.add_support('l', 'roller')
test_beam.add_distributed_load('l/2', 'l', '-q')
test_beam.add_point_load('l/4', '-q*l')
test_beam.solve()
fig, ax = test_beam.plot()

plt.savefig(__file__.split('.py')[0]+'.svg')

plt.show()
