from symbeam.beam import beam
import matplotlib.pyplot as plt

test_beam = beam(3, x0=0)
test_beam.add_support(0.5, 'pin')
test_beam.add_support(2.5, 'roller')
test_beam.add_point_load(0, '-P')
test_beam.add_point_load(3, '-P')
test_beam.solve()
fig, ax = test_beam.plot()

plt.show()
