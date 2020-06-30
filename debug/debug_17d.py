from symbeam.beam import beam
import matplotlib.pyplot as plt

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

test_beam = beam(6, x0=0)
test_beam.add_support(0, 'roller')
test_beam.add_support(2, 'roller')
test_beam.add_support(6, 'pin')
test_beam.add_support(4, 'hinge')
test_beam.add_distributed_load(0, 4, -5)
test_beam.add_distributed_load(4, 6, '-(-3*(x-5)**2 + 8)')
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
