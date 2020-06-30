from symbeam.beam import beam
import matplotlib.pyplot as plt
import sympy as sym

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

E = sym.symbols('E')
I = sym.symbols('I')
test_beam = beam(3, x0=0)
test_beam.add_support(0.5, 'pin')
test_beam.add_support(2.5, 'roller')
test_beam.add_point_load(0, '-P')
test_beam.add_point_load(3, '-P')
test_beam.set_young(0, 1.5, E)
test_beam.set_young(1.5, 3,  E)
test_beam.set_inertia(0, 1.5, I)
test_beam.set_inertia(1.5, 3,  10000*I)
test_beam.solve()
fig, ax = test_beam.plot()

plt.show()
