import math
import sys

class Heap:
    """
    Heap class implementing a fixed-size binary heap.

    Supports:
    - Max-heap (default) or min-heap according to is_max
    - Insertion with push() respecting priority
    - Extraction of the priority value with pop()

    The structure is implemented on a linear array representing a complete binary tree.
    """
    def __init__(self, length: int, is_max: bool = True):
        """
        Initializes a fixed-size heap.

        Parameters:
        length (int): Maximum capacity of the heap.
        is_max (bool): True for max-heap, False for min-heap.
        """
        if length < 1:
            raise Exception("LEN_INVALID")
        
        self.length = 0
        self.is_max = is_max
        self.__set_height(length)
        self.__set_weight()
        
        if self.is_max:
            min_inf = -sys.maxsize - 1
            self.arr = [min_inf] * self.weight
        else:
            self.arr = [sys.maxsize] * self.weight

    def __set_height(self, length: int) -> None:
        """Calculates the maximum height of a complete heap given its capacity."""
        max_height = math.ceil(math.log2(length + 1))
        self.height = max_height - 1

    def __set_weight(self) -> None:
        """Calculates the maximum number of nodes in a complete heap of height self.height."""
        self.weight = int(math.pow(2, self.height + 1) - 1)

    def __get_left_pos(self, parent_pos: int) -> int:
        """Returns the left child position in the array."""
        return (parent_pos * 2) + 1

    def __get_right_pos(self, parent_pos: int) -> int:
        """Returns the right child position in the array."""
        return 2 * (parent_pos + 1)

    def __get_father_pos(self, child_pos: int) -> int:
        """Returns the parent position of the given node in the array."""
        if child_pos % 2 == 0:
            return (child_pos // 2) - 1
        else:
            return (child_pos - 1) // 2

    def __is_priority(self, parent_val, child_val) -> bool:
        """Returns True if the child has higher priority than the parent."""
        return (child_val > parent_val) if self.is_max else (child_val < parent_val)

    def is_empty(self) -> bool:
        """Returns True if the heap has no elements."""
        return self.length == 0

    def is_full(self) -> bool:
        """Returns True if the heap has reached its maximum capacity."""
        return self.length == self.weight

    def push(self, value) -> None:
        """
        Inserts a value into the heap and maintains the priority property.

        Parameters:
        value: The value to be inserted into the heap.
        """
        if self.is_full():
            raise Exception("FULL_HEAP")

        pos = self.length
        self.arr[pos] = value

        while pos != 0:
            father_pos = self.__get_father_pos(pos)
            if not self.__is_priority(self.arr[father_pos], self.arr[pos]):
                break
            self.arr[pos], self.arr[father_pos] = self.arr[father_pos], self.arr[pos]
            pos = father_pos

        self.length += 1

    def pop(self):
        """
        Removes and returns the priority value from the heap (root).

        Returns:
        The highest priority value in a max-heap or the lowest in a min-heap.
        """
        if self.is_empty():
            raise Exception("EMPTY_HEAP")

        val = self.arr[0]

        self.length -= 1
        last_val = self.arr[self.length]
        self.arr[0] = last_val

        pos = 0

        while True:
            left_pos = self.__get_left_pos(pos)
            right_pos = self.__get_right_pos(pos)
            candidate = pos

            if left_pos < self.length and self.__is_priority(self.arr[candidate], self.arr[left_pos]):
                candidate = left_pos

            if right_pos < self.length and self.__is_priority(self.arr[candidate], self.arr[right_pos]):
                candidate = right_pos

            if candidate == pos:
                break

            self.arr[pos], self.arr[candidate] = self.arr[candidate], self.arr[pos]
            pos = candidate

        return val