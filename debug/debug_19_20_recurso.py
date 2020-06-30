from symbeam.beam import beam
import matplotlib.pyplot as plt

print("\n ============================================================================= ")
print(" Debuggin script for Symbeam")
print(" ============================================================================= ")

test_beam = beam(4, x0=0)
test_beam.add_support(2, 'roller')
test_beam.add_support(4, 'pin')
test_beam.add_distributed_load(0, 2, '-5*x')
test_beam.add_distributed_load(2, 4, '-(4*x**2-24*x+42)')
test_beam.set_inertia(0, 4, 2.051e-5)
test_beam.set_young(0, 4, 210e9)
test_beam.solve()
fig, ax = test_beam.plot()

plt.show()
