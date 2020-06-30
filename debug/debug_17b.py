from symbeam.beam import beam
import matplotlib.pyplot as plt

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

test_beam = beam('l', x0=0)
test_beam.add_support(0, 'fixed')
test_beam.add_support('l/2', 'hinge')
test_beam.add_support('l', 'roller')
test_beam.add_distributed_load('l/2', 'l', '-q')
test_beam.add_point_load('l/4', '-q*l')
test_beam.solve()
fig, ax = test_beam.plot()

plt.show()
