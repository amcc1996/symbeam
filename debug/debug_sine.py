from symbeam.beam import beam
import matplotlib.pyplot as plt

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

test_beam = beam(1, x0=0)
test_beam.add_support(0, 'pin')
test_beam.add_support(1, 'roller')
test_beam.add_distributed_load(0, 1, 'sin(20 * x)')
test_beam.solve()
fig, ax = test_beam.plot()

plt.show()
