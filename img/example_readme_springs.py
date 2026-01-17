import matplotlib.pyplot as plt

from sympy.abc import x

from symbeam import beam


L = 1  # Length of the beam in m
E = 210e3  # Young's modulus in Pa
I = 1e-6  # Moment of inertia in m^4
P = 1000  # Point load in N
M = 200  # Point moment in Nm
q = 2000  # Distributed load in N/m
kv = 1e3  # Transverse spring stiffness in N/m
ktheta = 1e3  # Rotational spring stiffness in Nm/rad
new_beam = beam(L)

# new_beam.set_young(x_start, x_end, value)
new_beam.set_young(0, L, E)

# new_beam.set_inertia(x_start, x_end, value)
new_beam.set_inertia(0, L, I)

# new_beam.add_support(x_coord, type)
new_beam.add_support(0, "pin")
new_beam.add_support(L, "roller")

# new_beam.add_point_load(x_coord, magnitude)
# new_beam.add_point_moment(x_coord, magnitude)
# new_beam.add_distributed_load(x_start, x_end, expression)
new_beam.add_point_load(L / 3, -P)
new_beam.add_point_moment(2 * L / 3, M)
new_beam.add_distributed_load(0, L, -q * x / L)

# new_beam.add_transverse_spring(x_coord, k_v)
# new_beam.add_rotational_spring(x_coord, k_theta)
new_beam.add_rotational_spring(0, ktheta)
new_beam.add_transverse_spring(L / 2, kv)
new_beam.add_rotational_spring(L / 4, ktheta)
new_beam.add_transverse_spring(3 * L / 4, kv)
new_beam.add_rotational_spring(3 * L / 4, ktheta)
new_beam.add_rotational_spring(L, ktheta)

new_beam.solve()

new_beam.plot()

plt.savefig(__file__.split(".py")[0] + ".svg")
