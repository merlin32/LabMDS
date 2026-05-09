def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort()
    merged = [list(intervals[0])]
    for i in range(1, len(intervals)):
        last_interval = merged[-1]
        current_start, current_end = intervals[i]
        if current_start <= last_interval[1]:
            last_interval[1] = max(last_interval[1], current_end)
        else:
            merged.append(list(intervals[i]))
            
    return merged
