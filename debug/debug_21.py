from symbeam.beam import beam
import matplotlib.pyplot as plt

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

test_beam = beam('L', x0=0)
test_beam.add_support(0, 'fixed')
test_beam.add_point_load('L', '-P')
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
