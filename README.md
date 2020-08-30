<p align="center">
  <a href=""><img alt="symbeam" src="img/symbeam_logo.svg" width="60%"></a>
  <p align="center">A pedagogical package for beam beanding.</p>
</p>

`symbeam` is a pedagogical software package, written in Python, targeted at Mechanical, Civil and Industrial Engineering students learning the fundamentals of bending of beams, namely, bending diagrams and beam deflections.

The modular object-oriented-based design of `symbeam` combined with the excelent symbolic engine [SymPy](https://www.sympy.org/pt/index.html), on which `symbeam` relies heavily, provides an unique computational learning environemnt for student grasping these concepts for the first time.
`symbeam` can be exploited to quickly assess the solutions of exercises for a wide variety of bending loadings and supports while allowing to easily modify the parameters of the problem fostering physical intuition and improving the students' understanding of the phenomena.

Conversely, `symbeam` can also be used by teachers to create and validate new problems for classes and exams, faccilitating this sometimes cumbersome task.

## Installation

### Installing from source
Clone this reposityory into your system
```
git clone git@github.com:amcc1996/symbeam.git
```
and install the Python package with `pip3`, running the following command inside `symbeam` root directory, where the `setup.py` is located
```
pip3 install .
```
At this point, `symbeam` can be imported into your Python scripts and modules the usual Python-way
```python
import symbeam
```

## Usage
Virtually all useful features of `symbeam` can be accessed through the `beam` class. `beam` objects, this is, concrete instances of the `beam` class, are initially defined by the starting point (0 by default) and the beam length. The beam supports, material and section properties and loadings are set by calling a specific set of methods on the beam object.

In the following sections, a thorough description of an exemplar application of `symbeam` is given. It should be noted beforehand that most (if not all) values characterising the problem can se set either using numerical input (e.g. 100) or a literal expression (100 * x + 100). In any case, this input is `sympified` using `SymPy` facilities, allowing to handle input of distinct types out-of-the-box.

> :warning: The `x` symbol is used by `symbeam` as the independent variable for the position along the beam. This variable must be used to specify any variation along the length of the beam and for nothing else. 

### Creating a beam
The fundamental tool for a bending analysis with `symbeam` is a `beam` object, as emphasised above. To create a new beam, import the `beam` class from the `symbeam` package. Then, simply call the `beam` constructor by passing the length of the beam and, if needed, a starting point. For instance, a beam with length equal to 1 and starting at 0 can be created by

```python
from symbeam import beam

new_beam = beam(1, x0=0)
```

As claimed before, one can create a beam with both numeric and symbolic input. A list of the distinct alternatives for instantiating a beam follows (the optional initial position `x0` is omitted here, for simplicity). Note that these alternatives also apply to any input data that can be given to `beam` methods, for instance, for specifying supports, loads and properties.

1. Numeric input
```python
from symbeam import beam

new_beam = beam(1)
```

2. Numeric input from string
```python
from symbeam import beam

new_beam = beam("1")
```

3. Symbolic input from string

```python
from symbeam import beam

new_beam = beam("L")
```

4. Symbolic input from a symbolic variable created with SymPy
```python
from symbeam import beam
import sympy

L = sympy.symbols("L")
new_beam = beam(L)
```

5. Symbolic input from a symbolic variable provided by SymPy
```python
from symbeam import beam
from sympy.abc import L

new_beam = beam(L)
```

### Setting beam properties: Young modulus and second moment of area
A beam must be associated with some distribution of material propertiy and section geometry along its length, namely, the Young modulus of the material and the second moment of area of the section. While these are not required for finding the bending diagramas, as these results simply from equilibirum considerations, they are mandatory for computing the deflections of the beam.

In `symbeam`, these properties can be set in individual segments along the beam, such that the set of segments for each property must encompass all the beam span and not be overlapping at any region. For example, considering a beam of length `L`, the Young modulus and second moment of area are set by passing the stating and ending coordinate and the value to the methods `set_young()` and `set_inertia()` as follows
```python
from symbeam import beam
from sympy.abc import L, E, I, P, M, q, x

new_beam = beam(L)

# new_beam.set_young(x_start, x_end, value)
new_beam.set_young(0, L/2, E)
new_beam.set_young(L/2, L, E/10)

# new_beam.set_inertia(x_start, x_end, value)
new_beam.set_inertia(0, L/2, I)
new_beam.set_inertia(L/2, L, I/2)
```
By default, if the properties are not explicitely set by the user, `symbeam` considers constant values `E` and `I` along the span of the beam, this is, the property setting methods do not need to be evoked. If any segment is explicitely set, the user must then specify all segments in a consistent manner. 

> :warning: **Our beloved symbols E and I**: Be careful when specifying symbolic Young modulus and second moment of area via a string, for instance, with "E" and "I". SymPy parses the string in the expression and will interpret "E" as the Nepper number and "I" as the imaginary operator. Prioritise using the variables directly imported from `sympy.abc` or create the variables explicitely with `sympy.symbols()`.

### Adding supports
The beam must be connected to the exterior via a set of supports, which materialise the geometric boundary conditions of the problem. Currently, `symbeam` can only solve statically determinate beams, therefore, redundant supports cannot be handled. A support can be added to the beam by specifying the coordinate and the type of support. Exemplarily, this is accomplished by calling the method `add_support()`

```python
# new_beam.add_support(x_coord, type)
new_beam.add_support(0, 'fixed')
new_beam.add_support(L, 'roller')
new_beam.add_support(3*L/4, 'hinge')
```
The types of support availbe in `symbeam` are
* `roller` : a roller, fixed in transverse direction and allows rotations in the bending plane
* `pin` : a pinned support, fixed in the axial and transverse directions and allows rotations in the bending plane
* `fixed` : a fixed/clamped support, all degrees of freedom are constrained (no displacements and no rotation)
* `hinge` : allows distinct rotations on the left and right of the point, but does no fix the beam in any direction

### Adding loads
The applied external loads are the missing item for completely defining the beam bending problem. These can be of point-type, namely, transverse point loads/forces and moments or segment-type loads, this is, transverse forces distributed along the span of the beam.

Point loads and moments are incorporated by calling the `add_point_load()` and `add_point_moment()` methods, which receive the coordinate of the point and the value of the load. Distributed loads are applied by calling the `add_distributed_load()` method, which takes the starting and ending point of the distributed load and the associated expression.

```python
new_beam.add_point_load(3*L/4, -P)
new_beam.add_point_moment(L, M)
new_beam.add_distributed_load(0, L/2, -q * x)
```

### Solving the problem
After specifying the beam properties, supports and loads, the problem can be solved by calling the method `solve()`. The program will proceed as follows
1. check if the input data is consistent
2. define the individual beam segments, such that the each one is associated with a continuous function of the Young modulus, second moment of area and distributed load: in sum, this subdivision must guarantee that the shear force and bending moment diagrams are continuous in each segment and piecewise continuous along the span of the beam
3. solve for the reaction forces and moments of the supports (equilibirum equations)
4. solve for internal loads (integrate the differential equations for beam equilibirum)
5. solve for deflections (integrate the elastic curve equation)
6. output the results (can be supressed if the optional argument `output=False`): identified segments, exterior reactions, shear force, bending moment, slope and deflection for each beam segment.

### Plotting the results
The results can be plotted with [matplotlib](https://matplotlib.org/) by calling the method `solve` on the beam object. The produced figure contains
1. a schematic representation of the problem
2. the shear force diagram
3. the bending moment diagram
4. the deformed shape of the beam.

At this stage, in order to the able to plot the expressions, all the parameters of the problem must be substituted by numerical values, with the natural exception of the `x` variable, since this is the independent variable. This is can be acomplished by passing the optional argument `subs` to the `plot` method. This must be a dictionary whose keys are the string representations of the variables and the values are the effective numerical values.

> :warning: Do not forget to call the method `show()` from `matplotlib` in order to plot the figure to the screen.

### Final script
Here you can find the complete script discussed on the previous sections.
```python
from symbeam import beam
from sympy.abc import L, E, I, P, M, q, x
import matplotlib.pyplot as plt

new_beam = beam(L)

# new_beam.set_young(x_start, x_end, value)
new_beam.set_young(0, L/2, E)
new_beam.set_young(L/2, L, E/10)

# new_beam.set_inertia(x_start, x_end, value)
new_beam.set_inertia(0, L/2, I)
new_beam.set_inertia(L/2, L, I/2)

# new_beam.add_support(x_coord, type)
new_beam.add_support(0, 'fixed')
new_beam.add_support(L, 'roller')
new_beam.add_support(3*L/4, 'hinge')

new_beam.add_point_load(3*L/4, -P)
new_beam.add_point_moment(L, M)
new_beam.add_distributed_load(0, L/2, -q * x)

new_beam.solve()

new_beam.plot(subs={'P':1000, 'q':5000, 'L':2})

plt.show()
```

