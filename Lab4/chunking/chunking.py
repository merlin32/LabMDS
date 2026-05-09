def chunk(lst, n):
    list_len = len(lst)
    chunks = list_len // n
    chunking = []
    if list_len % n:
        chunks = chunks + 1;
    chunks_index = 0 
    while(chunks_index < chunks):
        current_pos = chunks_index * n
        chunking.append(lst[current_pos : current_pos + n])
        chunks_index = chunks_index + 1
    return chunking

def flatten(lst_of_lsts):
    result = []
    for i in range (0, len(lst_of_lsts)):
        temp = lst_of_lsts[i]
        for j in range (0, len(temp)):
            result.append(temp[j])
    return result
