##Examples
Here you can find a comprehensive but by no means exhaustive list of examples exploring the capabilities of SymBeam. In each example, you will find a hyperlink to the associated file in the repository, the respective source code and output: both console and plot.

##[example_14.py](./example_14.py)
1. Numeric length
2. Pin
3. Roller
4. Numeric point force
5. Classical pinned beam problem without mid-length force

```python
from symbeam.beam import beam
import matplotlib.pyplot as plt

test_beam = beam('l', x0=0)
test_beam.add_support(0, 'pin')
test_beam.add_support('l', 'roller')
test_beam.add_point_load('l/2', '-P')
test_beam.solve()
fig, ax = test_beam.plot()
```
<img src='./example_14.svg', alt='./example_14.svg' width='60%'/>

                                    Beam points                                    
===================================================================================
     Coordinate              Type                 Load                Moment       
-----------------------------------------------------------------------------------
         0              Pinned Support             0                    0          
        l/2            Continuity point            -P                   0          
         l                  Roller                 0                    0          
===================================================================================


                                   Beam segments                                   
===================================================================================
        Span            Young modulus           Inertia          Distributed load  
-----------------------------------------------------------------------------------
 [   0   -  l/2  ]            E                    I                    0          
 [  l/2  -   l   ]            E                    I                    0          
===================================================================================


                                Exterior Reactions                                 
===================================================================================
           Point                       Type                        Value           
-----------------------------------------------------------------------------------
             0                         Force                        P/2            
             l                         Force                        P/2            
===================================================================================


                                  Internal Loads                                   
===================================================================================
        Span          Diagram                       Expression                    
-----------------------------------------------------------------------------------
 [   0   -  l/2  ]      V(x)                           -P/2                       
 [   0   -  l/2  ]      M(x)                          P*x/2                       
-----------------------------------------------------------------------------------
 [  l/2  -   l   ]      V(x)                           P/2                        
 [  l/2  -   l   ]      M(x)                      P*l/2 - P*x/2                   
===================================================================================


                              Rotation and deflection                              
===================================================================================
        Span          Variable                      Expression                    
-----------------------------------------------------------------------------------
 [   0   -  l/2  ]      v(x)           -P*l**2*x/(16*E*I) + P*x**3/(12*E*I)       
 [   0   -  l/2  ]    dv/dx(x)          -P*l**2/(16*E*I) + P*x**2/(4*E*I)         
-----------------------------------------------------------------------------------
 [  l/2  -   l   ]      v(x)    P*l**3/(48*E*I) - 3*P*l**2*x/(16*E*I) + P*l*x**2/(4*E*I) - P*x**3/(12*E*I)
 [  l/2  -   l   ]    dv/dx(x)  -3*P*l**2/(16*E*I) + P*l*x/(2*E*I) - P*x**2/(4*E*I)
===================================================================================


##[example_3.py](./example_3.py)
1. Symbolic length
2. Fixed
3. Hinge
4. Symbolic contstant linear load
5. Symbolic point load

```python
from symbeam.beam import beam
import matplotlib.pyplot as plt

test_beam = beam('l', x0=0)
test_beam.add_support(0, 'fixed')
test_beam.add_support('l/2', 'hinge')
test_beam.add_support('l', 'roller')
test_beam.add_distributed_load('l/2', 'l', '-q')
test_beam.add_point_load('l/4', '-q*l')
test_beam.solve()
fig, ax = test_beam.plot()
```
<img src='./example_3.svg', alt='./example_3.svg' width='60%'/>

                                    Beam points                                    
===================================================================================
     Coordinate              Type                 Load                Moment       
-----------------------------------------------------------------------------------
         0                  Fixed                  0                    0          
        l/4            Continuity point           -l*q                  0          
        l/2                 Hinge                  0                    0          
         l                  Roller                 0                    0          
===================================================================================


                                   Beam segments                                   
===================================================================================
        Span            Young modulus           Inertia          Distributed load  
-----------------------------------------------------------------------------------
 [   0   -  l/4  ]            E                    I                    0          
 [  l/4  -  l/2  ]            E                    I                    0          
 [  l/2  -   l   ]            E                    I                    -q         
===================================================================================


                                Exterior Reactions                                 
===================================================================================
           Point                       Type                        Value           
-----------------------------------------------------------------------------------
             0                         Force                      5*l*q/4          
             0                        Moment                    3*l**2*q/8         
             l                         Force                       l*q/4           
===================================================================================


                                  Internal Loads                                   
===================================================================================
        Span          Diagram                       Expression                    
-----------------------------------------------------------------------------------
 [   0   -  l/4  ]      V(x)                         -5*l*q/4                     
 [   0   -  l/4  ]      M(x)                 -3*l**2*q/8 + 5*l*q*x/4              
-----------------------------------------------------------------------------------
 [  l/4  -  l/2  ]      V(x)                          -l*q/4                      
 [  l/4  -  l/2  ]      M(x)                   -l**2*q/8 + l*q*x/4                
-----------------------------------------------------------------------------------
 [  l/2  -   l   ]      V(x)                      -3*l*q/4 + q*x                  
 [  l/2  -   l   ]      M(x)             -l**2*q/4 + 3*l*q*x/4 - q*x**2/2         
===================================================================================


                              Rotation and deflection                              
===================================================================================
        Span          Variable                      Expression                    
-----------------------------------------------------------------------------------
 [   0   -  l/4  ]      v(x)      -3*l**2*q*x**2/(16*E*I) + 5*l*q*x**3/(24*E*I)   
 [   0   -  l/4  ]    dv/dx(x)       -3*l**2*q*x/(8*E*I) + 5*l*q*x**2/(8*E*I)     
-----------------------------------------------------------------------------------
 [  l/4  -  l/2  ]      v(x)    l**4*q/(384*E*I) - l**3*q*x/(32*E*I) - l**2*q*x**2/(16*E*I) + l*q*x**3/(24*E*I)
 [  l/4  -  l/2  ]    dv/dx(x)  -l**3*q/(32*E*I) - l**2*q*x/(8*E*I) + l*q*x**2/(8*E*I)
-----------------------------------------------------------------------------------
 [  l/2  -   l   ]      v(x)    -5*l**4*q/(96*E*I) + 3*l**3*q*x/(32*E*I) - l**2*q*x**2/(8*E*I) + l*q*x**3/(8*E*I) - q*x**4/(24*E*I)
 [  l/2  -   l   ]    dv/dx(x)  3*l**3*q/(32*E*I) - l**2*q*x/(4*E*I) + 3*l*q*x**2/(8*E*I) - q*x**3/(6*E*I)
===================================================================================
