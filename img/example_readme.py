import matplotlib.pyplot as plt

from sympy.abc import E, I, L, M, P, q, x

from symbeam import beam


new_beam = beam(L)

# new_beam.set_young(x_start, x_end, value)
new_beam.set_young(0, L / 2, E)
new_beam.set_young(L / 2, L, E / 10)

# new_beam.set_inertia(x_start, x_end, value)
new_beam.set_inertia(0, L / 2, I)
new_beam.set_inertia(L / 2, L, I / 2)

# new_beam.add_support(x_coord, type)
new_beam.add_support(0, "fixed")
new_beam.add_support(L, "roller")
new_beam.add_support(3 * L / 4, "hinge")

new_beam.add_point_load(3 * L / 4, -P)
new_beam.add_point_moment(L, M)
new_beam.add_distributed_load(0, L / 2, -q * x)

new_beam.solve()

new_beam.plot(subs={"P": 1000, "q": 5000, "L": 2, "M": 1000})

plt.savefig(__file__.split(".py")[0] + ".svg")
