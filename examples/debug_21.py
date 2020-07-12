from symbeam.beam import beam
import matplotlib.pyplot as plt

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

test_beam = beam('L', x0=0)
test_beam.add_support(0, 'fixed')
test_beam.add_point_load('L', '-P')
test_beam.solve()
fig, ax = test_beam.plot()

plt.show()
