# External Sorting & K-Way Merge with Min-Heap

## 1. Problem Context & Asymptotics
When sorting datasets larger than available RAM (e.g. 100 GB log files on an 8 GB worker), External Merge Sort divides the data into $K$ sorted runs on disk, then performs a multi-way merge.

## 2. Min-Heap Optimal K-Way Merge
A direct sequential scan across $K$ files yields $O(N \cdot K)$ complexity. By maintaining a Min-Heap of size $K$:
- **Heap Element Tuple**: `(current_value, run_index)`
- **Initialization**: Insert the first element from each of the $K$ sorted runs: $O(K \log K)$.
- **Streaming Loop**:
  1. Pop the minimum value from the heap and write to output buffer.
  2. Read the next item from that specific `run_index` and push it to the heap ($O(\log K)$).
- **Total Time Complexity**: $O(N \log K)$, where $N$ is total elements across all runs.
- **Space Complexity**: $O(K)$ auxiliary memory in RAM.

## 3. High-Throughput Production Pattern
In Python, this is implemented natively via `heapq.merge(*iterables)` with generator expressions to avoid loading entire arrays into memory.

