from symbeam.beam import beam
import matplotlib.pyplot as plt

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

test_beam = beam(6, x0=0)
test_beam.add_support(0, 'fixed')
test_beam.add_support(4, 'hinge')
test_beam.add_support(6, 'roller')
test_beam.add_point_moment(6, 20)
test_beam.add_distributed_load(0, 2, '-5*x')
test_beam.add_distributed_load(2, 4, '-(20-5*x)')
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
