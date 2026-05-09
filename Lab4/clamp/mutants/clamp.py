from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore
def clamp(x, lo, hi):
    args = [x, lo, hi]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_clamp__mutmut_orig, x_clamp__mutmut_mutants, args, kwargs, None)
def x_clamp__mutmut_orig(x, lo, hi):
    return max(lo, min(x, hi))
def x_clamp__mutmut_1(x, lo, hi):
    return max(None, min(x, hi))
def x_clamp__mutmut_2(x, lo, hi):
    return max(lo, None)
def x_clamp__mutmut_3(x, lo, hi):
    return max(min(x, hi))
def x_clamp__mutmut_4(x, lo, hi):
    return max(lo, )
def x_clamp__mutmut_5(x, lo, hi):
    return max(lo, min(None, hi))
def x_clamp__mutmut_6(x, lo, hi):
    return max(lo, min(x, None))
def x_clamp__mutmut_7(x, lo, hi):
    return max(lo, min(hi))
def x_clamp__mutmut_8(x, lo, hi):
    return max(lo, min(x, ))

x_clamp__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_clamp__mutmut_1': x_clamp__mutmut_1, 
    'x_clamp__mutmut_2': x_clamp__mutmut_2, 
    'x_clamp__mutmut_3': x_clamp__mutmut_3, 
    'x_clamp__mutmut_4': x_clamp__mutmut_4, 
    'x_clamp__mutmut_5': x_clamp__mutmut_5, 
    'x_clamp__mutmut_6': x_clamp__mutmut_6, 
    'x_clamp__mutmut_7': x_clamp__mutmut_7, 
    'x_clamp__mutmut_8': x_clamp__mutmut_8
}
x_clamp__mutmut_orig.__name__ = 'x_clamp'
