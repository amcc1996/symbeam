# Examples
Here you can find a comprehensive but by no means exhaustive list of examples exploring the capabilities of SymBeam. In each example, you will find a hyperlink to the associated file in the repository, the respective source code and output: both console and plot.

## [example_1.py](./example_1.py)
1. Symbolic length
2. Roller
3. Pin
4. Symbolic distributed linear load
5. Symbolic contstant linear load

```python
from symbeam.beam import beam
import matplotlib.pyplot as plt

test_beam = beam('l', x0=0)
test_beam.add_support(0, 'roller')
test_beam.add_support('l', 'pin')
test_beam.add_distributed_load(0, 'l/2', '-2 * q / l * x')
test_beam.add_distributed_load('l/2', 'l', '-q')
test_beam.solve()
fig, ax = test_beam.plot()
```
<p align="center">
  <img src="./svg/./example_1.svg" width="50%">
</p>

```
                                    Beam points                                    
===================================================================================
     Coordinate              Type                 Load                Moment       
-----------------------------------------------------------------------------------
         0                  Roller                 0                    0          
        l/2            Continuity point            0                    0          
         l              Pinned Support             0                    0          
===================================================================================


                                   Beam segments                                   
===================================================================================
        Span            Young modulus           Inertia          Distributed load  
-----------------------------------------------------------------------------------
 [   0   -  l/2  ]            E                    I                 -2*q*x/l      
 [  l/2  -   l   ]            E                    I                    -q         
===================================================================================


                                Exterior Reactions                                 
===================================================================================
           Point                       Type                        Value           
-----------------------------------------------------------------------------------
             0                         Force                     7*l*q/24          
             l                         Force                     11*l*q/24         
===================================================================================


                                  Internal Loads                                   
===================================================================================
        Span          Diagram                       Expression                    
-----------------------------------------------------------------------------------
 [   0   -  l/2  ]      V(x)                   -7*l*q/24 + q*x**2/l               
 [   0   -  l/2  ]      M(x)                7*l*q*x/24 - q*x**3/(3*l)             
-----------------------------------------------------------------------------------
 [  l/2  -   l   ]      V(x)                     -13*l*q/24 + q*x                 
 [  l/2  -   l   ]      M(x)           -l**2*q/24 + 13*l*q*x/24 - q*x**2/2        
===================================================================================


                              Rotation and deflection                              
===================================================================================
        Span          Variable                      Expression                    
-----------------------------------------------------------------------------------
 [   0   -  l/2  ]      v(x)    -187*l**3*q*x/(5760*E*I) + 7*l*q*x**3/(144*E*I) - q*x**5/(60*E*I*l)
 [   0   -  l/2  ]    dv/dx(x)  -187*l**3*q/(5760*E*I) + 7*l*q*x**2/(48*E*I) - q*x**4/(12*E*I*l)
-----------------------------------------------------------------------------------
 [  l/2  -   l   ]      v(x)    -l**4*q/(1920*E*I) - 157*l**3*q*x/(5760*E*I) - l**2*q*x**2/(48*E*I) + 13*l*q*x**3/(144*E*I) - q*x**4/(24*E*I)
 [  l/2  -   l   ]    dv/dx(x)  -157*l**3*q/(5760*E*I) - l**2*q*x/(24*E*I) + 13*l*q*x**2/(48*E*I) - q*x**3/(6*E*I)
===================================================================================


```
## [example_2.py](./example_2.py)
1. Symbolic length
2. Roller
3. Pin
4. Symbolic distributed linear load
5. Symbolic contstant linear load
6. User-specified symbolic substitutions

```python
from symbeam.beam import beam
import matplotlib.pyplot as plt

test_beam = beam('l', x0=0)
test_beam.add_support(0, 'roller')
test_beam.add_support('l', 'pin')
test_beam.add_distributed_load(0, 'l/2', '-2 * q / l * x')
test_beam.add_distributed_load('l/2', 'l', '-q')
test_beam.solve()
fig, ax = test_beam.plot(subs={'q':2, 'l':2, 'x':10}) # 'x' is not substituted
```
<p align="center">
  <img src="./svg/./example_2.svg" width="50%">
</p>

```
                                    Beam points                                    
===================================================================================
     Coordinate              Type                 Load                Moment       
-----------------------------------------------------------------------------------
         0                  Roller                 0                    0          
        l/2            Continuity point            0                    0          
         l              Pinned Support             0                    0          
===================================================================================


                                   Beam segments                                   
===================================================================================
        Span            Young modulus           Inertia          Distributed load  
-----------------------------------------------------------------------------------
 [   0   -  l/2  ]            E                    I                 -2*q*x/l      
 [  l/2  -   l   ]            E                    I                    -q         
===================================================================================


                                Exterior Reactions                                 
===================================================================================
           Point                       Type                        Value           
-----------------------------------------------------------------------------------
             0                         Force                     7*l*q/24          
             l                         Force                     11*l*q/24         
===================================================================================


                                  Internal Loads                                   
===================================================================================
        Span          Diagram                       Expression                    
-----------------------------------------------------------------------------------
 [   0   -  l/2  ]      V(x)                   -7*l*q/24 + q*x**2/l               
 [   0   -  l/2  ]      M(x)                7*l*q*x/24 - q*x**3/(3*l)             
-----------------------------------------------------------------------------------
 [  l/2  -   l   ]      V(x)                     -13*l*q/24 + q*x                 
 [  l/2  -   l   ]      M(x)           -l**2*q/24 + 13*l*q*x/24 - q*x**2/2        
===================================================================================


                              Rotation and deflection                              
===================================================================================
        Span          Variable                      Expression                    
-----------------------------------------------------------------------------------
 [   0   -  l/2  ]      v(x)    -187*l**3*q*x/(5760*E*I) + 7*l*q*x**3/(144*E*I) - q*x**5/(60*E*I*l)
 [   0   -  l/2  ]    dv/dx(x)  -187*l**3*q/(5760*E*I) + 7*l*q*x**2/(48*E*I) - q*x**4/(12*E*I*l)
-----------------------------------------------------------------------------------
 [  l/2  -   l   ]      v(x)    -l**4*q/(1920*E*I) - 157*l**3*q*x/(5760*E*I) - l**2*q*x**2/(48*E*I) + 13*l*q*x**3/(144*E*I) - q*x**4/(24*E*I)
 [  l/2  -   l   ]    dv/dx(x)  -157*l**3*q/(5760*E*I) - l**2*q*x/(24*E*I) + 13*l*q*x**2/(48*E*I) - q*x**3/(6*E*I)
===================================================================================


```