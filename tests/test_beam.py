import sympy as sym
from symbeam.beam import beam

def test_beam_two_symbols():
    """Test if an error is reaised if more tha one symbols is used to instatiate the beam.
    """
    a = beam('L * a', x0=0)

def test_beam_distinct_symbols():
    """Test if an error is reaised if the symbols used for the inital position and length
    are distinct.
    """
    a = beam('L * a', x0='b')
