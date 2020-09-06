# SymBeam examples suit
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020
# Features: 1. Numeric length
#           2. Pin
#           3. Rollers
#           4. Symbolic point load
#           5. Discontinuous distribution of Young modulus
#           6. Discontinuous distribution of second moment of area
#           7. `E` and `I` symbols created with SymPy
#           8. User-speficied substitution

import matplotlib.pyplot as plt
import sympy as sym

from symbeam import beam


E = sym.symbols("E")
I = sym.symbols("I")
test_beam = beam(3, x0=0)
test_beam.add_support(0.5, "pin")
test_beam.add_support(2.5, "roller")
test_beam.add_point_load(0, "-P")
test_beam.add_point_load(3, "-P")
test_beam.set_young(0, 1.5, E / 1000)
test_beam.set_young(1.5, 3, E)
test_beam.set_inertia(0, 1, I)
test_beam.set_inertia(1, 3, 100 * I)
test_beam.solve()
fig, ax = test_beam.plot(subs={"P": 1000})

plt.savefig(__file__.split(".py")[0] + ".svg")
