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
test_beam.solve()
fig, ax = test_beam.plot()

plt.show()
