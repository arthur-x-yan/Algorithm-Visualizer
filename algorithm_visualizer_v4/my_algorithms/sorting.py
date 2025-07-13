def bubble_sort(arr):
    """Yield (array, highlight_indices)"""
    a = arr[:]                 # copy
    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            yield a, (j, j + 1)
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                yield a, (j, j + 1)
    yield a, ()                # finished

def insertion_sort(arr):
    """Yield (snapshot, red_index, key_index)"""
    a = arr[:]                                # copy
    for i in range(1, len(a)):
        key_val = a[i]
        key_idx = i
        yield a[:], None, key_idx             # show chosen key

        j = i - 1
        while j >= 0 and a[j] > key_val:
            # compare & shift
            red_idx = j                       # red bar
            a[j + 1] = a[j]                   # shift right  (height change)
            yield a[:], red_idx, key_idx      # after shift
            j -= 1


        a[j + 1] = key_val
        yield a[:], None, j + 1               

    yield a[:], None, None                    # finished

def selection_sort(arr):
    """Yield (array, highlight, dest, min)"""
    a = arr[:]                 # copy
    for i in range(len(a)):
        min_idx = i
        for j in range(i + 1, len(a)):
            yield a, j, i, min_idx
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            yield a, i, i, min_idx
    yield a, None, None, None             # finished

def merge_sort(arr):
    """Yield (full_array_snapshot, current_merge_segment, highlight_indices)"""
    def sort(subarr, offset):
        if len(subarr) <= 1:
            yield arr[:], subarr[:], ()
            return subarr[:]

        mid = len(subarr) // 2
        left = yield from sort(subarr[:mid], offset)
        right = yield from sort(subarr[mid:], offset + mid)

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            # Replace values in main array
            arr[offset:offset+len(merged)] = merged
            yield arr[:], merged + left[i:] + right[j:], (offset + i, offset + mid + j)

        merged.extend(left[i:])
        merged.extend(right[j:])
        arr[offset:offset+len(merged)] = merged
        yield arr[:], merged[:], ()
        return merged

    yield from sort(arr[:], 0)

def quick_sort(arr):
    """Yield (array, highlights)"""
    a = arr[:]

    def _quick_sort(lo, hi):
        if lo < hi:
            pivot_idx, states = partition(lo, hi)
            for state in states:
                yield state
            yield from _quick_sort(lo, pivot_idx - 1)
            yield from _quick_sort(pivot_idx + 1, hi)

    def partition(lo, hi):
        pivot = a[hi]
        i = lo
        steps = []

        for j in range(lo, hi):
            steps.append((a[:], (j, hi)))  
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                steps.append((a[:], (i, j)))  # swap
                i += 1

        a[i], a[hi] = a[hi], a[i]
        steps.append((a[:], (i, hi)))  # final pivot swap
        return i, steps

    yield from _quick_sort(0, len(a) - 1)
    yield a[:], ()  # finished

def counting_sort(arr):
    """Yield (array_snapshot, freq_snapshot, info_dict)"""
    a = arr[:]
    if not a:
        yield a, [], {}
        return

    k = max(a) + 1
    freq = [0] * k

    # count phase
    for i, v in enumerate(a):
        freq[v] += 1
        yield a[:], freq[:], {"phase": "count", "idx": i, "val": v}

    # write phase
    out = 0
    for val, cnt in enumerate(freq):
        while cnt:
            a[out] = val
            cnt   -= 1
            freq[val] = cnt        
            yield a[:], freq[:], {"phase": "write", "idx": out, "val": val}
            out += 1

    yield a[:], freq[:], {"phase": "done"}