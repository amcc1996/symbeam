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
test_beam.solve()
fig, ax = test_beam.plot()

plt.show()
