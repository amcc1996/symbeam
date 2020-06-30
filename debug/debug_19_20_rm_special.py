from symbeam.beam import beam
import matplotlib.pyplot as plt

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

test_beam = beam(4, x0=0)
test_beam.add_support(0, 'roller')
test_beam.add_support(1, 'hinge')
test_beam.add_support(4, 'fixed')
test_beam.add_distributed_load(0, 2, '-5')
test_beam.add_distributed_load(2, 4, '-(4*x**2 - 24 *x + 37)')
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
