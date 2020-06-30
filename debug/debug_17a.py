from symbeam.beam import beam
import matplotlib.pyplot as plt

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

test_beam = beam('l', x0=0)
test_beam.add_support(0, 'roller')
test_beam.add_support('l', 'pin')
test_beam.add_distributed_load(0, 'l/2', '-2 * q / l * x')
test_beam.add_distributed_load('l/2', 'l', '-q')
test_beam.solve()
fig, ax = test_beam.plot()

plt.show()
