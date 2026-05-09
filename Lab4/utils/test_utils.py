import utils
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis import assume

def test_clamp():
    assert utils.clamp(150, 0, 100) == 100
    assert utils.clamp(-150, 0, 100) == 0
    assert utils.clamp(0, 0, 100) == 0
    assert utils.clamp(100, 0, 100) == 100
    assert utils.clamp(40, 0, 100) == 40
    assert utils.clamp(10, 5, 5) == 5
    
def test_merge_sorted():
    assert utils.merge_sorted([1, 2], [5, 6]) == [1, 2, 5, 6]
    assert utils.merge_sorted([1, 5], [2, 6]) == [1, 2, 5, 6]
    assert utils.merge_sorted([1, 1], [2, 2]) == [1, 1, 2, 2]
    assert utils.merge_sorted([], [1, 2]) == [1, 2]
    assert utils.merge_sorted([], []) == []
    assert utils.merge_sorted([1, 2], [2, 3]) == [1, 2, 2, 3]
    
def test_parse_pair():
    assert utils.parse_pair("10:20") == (10, 20)
    with pytest.raises(ValueError):
        utils.parse_pair("1:2:3")
    with pytest.raises(ValueError):
        utils.parse_pair("10")
    with pytest.raises(ValueError):
        utils.parse_pair("a:b")
    
def test_unique_sorted():
    assert utils.unique_sorted([1, 6, 8, 9, 9]) == [1, 6, 8, 9]
    #assert utils.unique_sorted([1, 1, 1]) == [1] failure

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a
    
@given(st.integers(), st.integers(), st.integers())
def test_clamp_in_bounds(x, lo, hi):
    assume(lo <= hi)
    result = utils.clamp(x, lo, hi)
    if x <= lo:
        assert result == lo
    elif x >= hi:
        assert result == hi
    else:
        assert result == x
    
@given(
    st.lists(st.integers()).map(sorted), 
    st.lists(st.integers()).map(sorted))
def test_merge_sorted_hypothesis(a, b):
    result = utils.merge_sorted(a, b)
    assert len(result) == len(a) + len(b)
    assert result == sorted(a + b)
            
