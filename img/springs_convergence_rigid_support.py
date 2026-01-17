import matplotlib.pyplot as plt
import numpy as np
import sympy

from sympy.abc import E, I, L, P, a, x

from symbeam import beam


# Solve with symbeam
new_beam = beam(L)
new_beam.set_young(0, L, E)
new_beam.set_inertia(0, L, I)
new_beam.add_point_load(L, P)
new_beam.add_transverse_spring(0, a * E * I / L**3)
new_beam.add_rotational_spring(0, a * E * I / L)
new_beam.solve()
deflection = new_beam.segments[0].deflection

# Analytical solution
analyical_solution = P / (6 * E * I) * (3 * L * x**2 - x**3)
deflection_ratio = sympy.simplify(deflection / analyical_solution).subs({x: x * L})
deflection_ratio = sympy.simplify(sympy.cancel(deflection_ratio))

a_values = [1e1, 1e2, 1e3, 1e4, 1e5, 1e6]
fig, ax = plt.subplots(num=1, figsize=(7, 5))
x_num = np.linspace(L / 1000, L, 100) / L
colors = plt.cm.cividis(np.linspace(0, 1, len(a_values)))[::-1]
for i, a_val in enumerate(a_values):
    deflection_ratio_subs = deflection_ratio.subs({a: a_val})
    y_num = [deflection_ratio_subs.subs({x: xi}).evalf() for xi in x_num]
    plt.plot(x_num, y_num, label=rf"$a={a_val:1.0e}$", color=colors[i], linewidth=1.5)

ax.set_xlim(0, 1)
ax.set_ylim(0, 4)
ax.set_xlabel(r"x/L")
ax.set_ylabel(r"Deflection Ratio, $v_{spring}/v_{rigid}$")

plt.tight_layout()
plt.legend(fancybox=False, loc="upper right", edgecolor="none", fontsize=10, framealpha=0)

plt.savefig(__file__.split(".py")[0] + ".svg")
