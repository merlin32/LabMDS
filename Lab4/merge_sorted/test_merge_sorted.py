import merge_sorted
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

def test_merge_sorted_static():
    assert merge_sorted.merge_sorted([1, 2], [5, 6]) == [1, 2, 5, 6]
    assert merge_sorted.merge_sorted([1, 5], [2, 6]) == [1, 2, 5, 6]
    assert merge_sorted.merge_sorted([], [1, 2]) == [1, 2]
    assert merge_sorted.merge_sorted([], []) == []

@given(
    st.lists(st.integers()).map(sorted), 
    st.lists(st.integers()).map(sorted)
)
def test_merge_sorted_stability(a, b):
    result = merge_sorted.merge_sorted(a, b)
    expected = sorted(a + b)
    assert result == expected
    
def test_kill_mutant_7():
    a = [1.0]
    b = [1]
    result = merge_sorted.merge_sorted(a, b)

    assert result == [1.0, 1]
    assert isinstance(result[0], float)
