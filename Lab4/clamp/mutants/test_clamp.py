import clamp
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis import assume

def test_clamp():
    assert clamp.clamp(150, 0, 100) == 100
    assert clamp.clamp(-150, 0, 100) == 0
    assert clamp.clamp(0, 0, 100) == 0
    assert clamp.clamp(100, 0, 100) == 100
    assert clamp.clamp(40, 0, 100) == 40
    assert clamp.clamp(10, 5, 5) == 5
    assert clamp.clamp(5, 5, 5) == 5
    
@given(st.integers(), st.integers(), st.integers())
def test_clamp_always_within_bounds(x, a, b):
    lo, hi = sorted([a, b])
    result = clamp.clamp(x, lo, hi)
    assert lo <= result <= hi

@given(st.integers(), st.integers(), st.integers())
def test_clamp_logic_branches(x, a, b):
    lo, hi = sorted([a, b])
    result = clamp.clamp(x, lo, hi)
    
    if x < lo:
        assert result == lo
    elif x > hi:
        assert result == hi
    else:
        assert result == x

@given(st.integers(), st.integers(), st.integers())
def test_clamp_identity_inside_bounds(a, b, x):
    lo, hi = sorted([a, b])
    assume(lo <= x <= hi)
    assert clamp.clamp(x, lo, hi) == x

@given(st.integers(), st.integers())
def test_clamp_boundary_explicit(a, b):
    lo, hi = sorted([a, b])
    assert clamp.clamp(lo, lo, hi) == lo
    assert clamp.clamp(hi, lo, hi) == hi
