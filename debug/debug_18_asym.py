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
test_beam.check_beam_properties()
test_beam.set_segments()
test_beam.print_points()
test_beam.print_segments()
test_beam.solve_reactions()
test_beam.print_reactions()
test_beam.solve_internal_loads()
test_beam.print_internal_loads()
test_beam.solve_deflection()
test_beam.print_deflections()
fig, ax = test_beam.plot()

plt.show()
