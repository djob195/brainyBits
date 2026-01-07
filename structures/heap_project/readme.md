![Python Version](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)

# Fixed-Size Heap in Python

A Python implementation of a **fixed-size binary heap** (max-heap or min-heap) with unit tests. This repository is based on the data structures and algorithms featured in my [blog](https://djob195.github.io/posts/heap/).

## Features

- Supports **max-heap** and **min-heap**
- Fixed-size heap with capacity checks
- `push()` to insert elements while maintaining priority
- `pop()` to extract the element with highest priority
- Methods to check if the heap is **empty** or **full**
- Fully covered with **unit tests**

## Prerequisites

A `Python` environment is required to run this project.  
You can set it up by following the [tutorial](https://github.com/djob195/brainyBits/blob/master/readme.md) provided in the root of this repository.

## Project Setup

### 1. Navigate to the project’s root directory
```bash
cd structures/heap_project
```
### 2. Execute Unit Test
```bash
python -m unittest discover
```
This command will execute all tests for the heap implementation. If all tests pass successfully, you should see output similar to:
```plaintext
Ran 5 tests in 0.001s

OK
```

##  What the tests do
1. **Max-heap structure:** Inserts multiple numeric values into a max-heap and performs `pop()` operations. The test verifies that each `pop()` returns the correct maximum value until the heap is empty.
2. **Min-heap structure:** Similar to the first test, but for a min-heap. Ensures that pop() returns the minimum value in the correct order. 
3. **Empty Heap Exception:** Verifies that attempting to pop() from an empty heap raises the appropriate exception.. 
4. **Full heap scenario**. Fills the heap to its maximum capacity and attempts to insert an additional value. Checks that a full heap exception is raised, ensuring proper overflow handling.
5. **Heap Height and Weight Verification**: Confirms that the internal calculations for the heap’s maximum height and total number of nodes are correct for a heap of a given capacity.