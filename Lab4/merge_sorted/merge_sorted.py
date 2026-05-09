def merge_sorted(a, b):
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
