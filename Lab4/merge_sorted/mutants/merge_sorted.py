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
def merge_sorted(a, b):
    args = [a, b]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_merge_sorted__mutmut_orig, x_merge_sorted__mutmut_mutants, args, kwargs, None)
def x_merge_sorted__mutmut_orig(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_1(a, b):
    result = None
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_2(a, b):
    result = []
    i, j = None
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_3(a, b):
    result = []
    i, j = 1, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_4(a, b):
    result = []
    i, j = 0, 1
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_5(a, b):
    result = []
    i, j = 0, 0
    max_steps = None
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_6(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) - len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_7(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(None):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_8(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) or j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_9(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i <= len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_10(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j <= len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_11(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] < b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_12(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(None)
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_13(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i = 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_14(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i -= 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_15(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 2
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_16(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(None)
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_17(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j = 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_18(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j -= 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_19(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 2
        else:
            break
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_20(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            return
            
    result.extend(a[i:])
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_21(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(None)
    result.extend(b[j:])
    return result
def x_merge_sorted__mutmut_22(a, b):
    result = []
    i, j = 0, 0
    max_steps = len(a) + len(b)
    
    for _ in range(max_steps):
        if i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        else:
            break
            
    result.extend(a[i:])
    result.extend(None)
    return result

x_merge_sorted__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_merge_sorted__mutmut_1': x_merge_sorted__mutmut_1, 
    'x_merge_sorted__mutmut_2': x_merge_sorted__mutmut_2, 
    'x_merge_sorted__mutmut_3': x_merge_sorted__mutmut_3, 
    'x_merge_sorted__mutmut_4': x_merge_sorted__mutmut_4, 
    'x_merge_sorted__mutmut_5': x_merge_sorted__mutmut_5, 
    'x_merge_sorted__mutmut_6': x_merge_sorted__mutmut_6, 
    'x_merge_sorted__mutmut_7': x_merge_sorted__mutmut_7, 
    'x_merge_sorted__mutmut_8': x_merge_sorted__mutmut_8, 
    'x_merge_sorted__mutmut_9': x_merge_sorted__mutmut_9, 
    'x_merge_sorted__mutmut_10': x_merge_sorted__mutmut_10, 
    'x_merge_sorted__mutmut_11': x_merge_sorted__mutmut_11, 
    'x_merge_sorted__mutmut_12': x_merge_sorted__mutmut_12, 
    'x_merge_sorted__mutmut_13': x_merge_sorted__mutmut_13, 
    'x_merge_sorted__mutmut_14': x_merge_sorted__mutmut_14, 
    'x_merge_sorted__mutmut_15': x_merge_sorted__mutmut_15, 
    'x_merge_sorted__mutmut_16': x_merge_sorted__mutmut_16, 
    'x_merge_sorted__mutmut_17': x_merge_sorted__mutmut_17, 
    'x_merge_sorted__mutmut_18': x_merge_sorted__mutmut_18, 
    'x_merge_sorted__mutmut_19': x_merge_sorted__mutmut_19, 
    'x_merge_sorted__mutmut_20': x_merge_sorted__mutmut_20, 
    'x_merge_sorted__mutmut_21': x_merge_sorted__mutmut_21, 
    'x_merge_sorted__mutmut_22': x_merge_sorted__mutmut_22
}
x_merge_sorted__mutmut_orig.__name__ = 'x_merge_sorted'
