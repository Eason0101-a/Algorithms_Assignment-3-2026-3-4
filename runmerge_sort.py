from __future__ import annotations

from dataclasses import dataclass
from random import randint
from time import perf_counter
from typing import List, Sequence


@dataclass
class SortStats:
    comparisons: int = 0
    moves: int = 0


class RunMergeSorter:
    """
    RunMerge Sort (custom hybrid sort)

    Idea:
    1. Detect natural runs in data.
    2. Extend short runs with binary insertion sort.
    3. Merge runs bottom-up.

    Inspired by natural merge sort and insertion-based run boosting.
    """

    def __init__(self, min_run: int = 32) -> None:
        if min_run < 2:
            raise ValueError("min_run must be >= 2")
        self.min_run = min_run
        self.stats = SortStats()

    def sort(self, data: Sequence[int]) -> List[int]:
        arr = list(data)
        n = len(arr)
        if n <= 1:
            return arr

        runs = self._detect_runs(arr)
        runs = self._boost_small_runs(arr, runs)
        self._merge_all_runs(arr, runs)
        return arr

    def _compare(self, a: int, b: int) -> int:
        self.stats.comparisons += 1
        if a < b:
            return -1
        if a > b:
            return 1
        return 0

    def _detect_runs(self, arr: List[int]) -> List[tuple[int, int]]:
        n = len(arr)
        runs: List[tuple[int, int]] = []
        i = 0

        while i < n:
            start = i
            i += 1
            if i == n:
                runs.append((start, i))
                break

            if self._compare(arr[i - 1], arr[i]) <= 0:
                while i < n and self._compare(arr[i - 1], arr[i]) <= 0:
                    i += 1
            else:
                while i < n and self._compare(arr[i - 1], arr[i]) > 0:
                    i += 1
                arr[start:i] = reversed(arr[start:i])
                self.stats.moves += i - start

            runs.append((start, i))

        return runs

    def _binary_search_pos(self, arr: List[int], left: int, right: int, key: int) -> int:
        while left < right:
            mid = (left + right) // 2
            if self._compare(arr[mid], key) <= 0:
                left = mid + 1
            else:
                right = mid
        return left

    def _binary_insertion_sort(self, arr: List[int], left: int, right: int) -> None:
        for i in range(left + 1, right):
            key = arr[i]
            pos = self._binary_search_pos(arr, left, i, key)
            j = i
            while j > pos:
                arr[j] = arr[j - 1]
                self.stats.moves += 1
                j -= 1
            arr[pos] = key
            self.stats.moves += 1

    def _boost_small_runs(self, arr: List[int], runs: List[tuple[int, int]]) -> List[tuple[int, int]]:
        if not runs:
            return runs

        boosted: List[tuple[int, int]] = []
        n = len(arr)
        idx = 0

        while idx < len(runs):
            start = runs[idx][0]
            end = runs[idx][1]

            while end - start < self.min_run and end < n:
                next_idx = idx + 1
                if next_idx < len(runs) and runs[next_idx][0] == end:
                    end = runs[next_idx][1]
                    idx = next_idx
                else:
                    end = min(start + self.min_run, n)
                    break

            self._binary_insertion_sort(arr, start, end)
            boosted.append((start, end))
            idx += 1

        return boosted

    def _merge(self, arr: List[int], left: int, mid: int, right: int) -> None:
        left_part = arr[left:mid]
        right_part = arr[mid:right]

        i = 0
        j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            if self._compare(left_part[i], right_part[j]) <= 0:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            self.stats.moves += 1
            k += 1

        while i < len(left_part):
            arr[k] = left_part[i]
            self.stats.moves += 1
            i += 1
            k += 1

        while j < len(right_part):
            arr[k] = right_part[j]
            self.stats.moves += 1
            j += 1
            k += 1

    def _merge_all_runs(self, arr: List[int], runs: List[tuple[int, int]]) -> None:
        current = runs
        while len(current) > 1:
            merged: List[tuple[int, int]] = []
            i = 0
            while i < len(current):
                if i + 1 == len(current):
                    merged.append(current[i])
                    break

                left_start, left_end = current[i]
                right_start, right_end = current[i + 1]
                self._merge(arr, left_start, right_start, right_end)
                merged.append((left_start, right_end))
                i += 2

            current = merged


def benchmark() -> None:
    datasets = {
        "sorted": list(range(2000)),
        "reversed": list(range(1999, -1, -1)),
        "random": [randint(0, 10_000) for _ in range(2000)],
    }

    print("RunMerge Sort Benchmark (n=2000)")
    for name, data in datasets.items():
        sorter = RunMergeSorter(min_run=32)
        t0 = perf_counter()
        result = sorter.sort(data)
        elapsed = perf_counter() - t0
        is_sorted = all(result[i] <= result[i + 1] for i in range(len(result) - 1))
        print(
            f"{name:8s} | time={elapsed:.6f}s | comparisons={sorter.stats.comparisons:7d} | "
            f"moves={sorter.stats.moves:7d} | sorted={is_sorted}"
        )


if __name__ == "__main__":
    benchmark()
