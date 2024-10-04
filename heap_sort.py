def left(i):
    return 2 * i + 1  # Calculate left child index

def right(i):
    return 2 * i + 2  # Calculate right child index

def heap_size(A):
    return len(A) - 1

def max_heapify(A, i):
    l = left(i)  # Get left child index
    r = right(i)  # Get right child index

    if l <= heap_size(A) and A[l] > A[i]:
        largest = l
    else:
        largest = i

    if r <= heap_size(A) and A[r] > A[largest]:
        largest = r

    if largest != i:
        A[i], A[largest] = A[largest], A[i]  # Exchange A[i] <-> A[largest]
        max_heapify(A, largest)  # Recursively heapify the affected subtree

def build_max_heap(A):
    heap_size = len(A) - 1  # Set heap size (0-indexed)
    for i in range(heap_size // 2, -1, -1):
        max_heapify(A, i)

# Example usage
if __name__ == "__main__":
    array = [3, 1, 6, 5, 2, 4]
    build_max_heap(array)
    print("Max Heap:", array)
