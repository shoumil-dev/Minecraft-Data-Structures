""" Array-based implementation of SortedList ADT. """

from referential_array import ArrayR
from AbstractSortedList import SortedList, T
from constants import EPSILON
from cave import Cave


class ArraySortedList_Game(SortedList[T]):
    """ SortedList ADT implemented with arrays. 
    This will be used to calculate and store the best option for mining in multiplayer game. 
    
    Each element is a tuple:
    (Cave, Quantity_mined, Earnings)
    """
    MIN_CAPACITY = 1

    def __init__(self, max_capacity: int) -> None:
        """ ArraySortedList object initialiser. """

        # first, calling the basic initialiser
        SortedList.__init__(self)

        # initialising the internal array
        size = max(self.MIN_CAPACITY, max_capacity)
        self.array = ArrayR(size)

    def reset(self):
        """ Reset the list. """
        SortedList.__init__(self)

    def __getitem__(self, index: int) -> T:
        """ Magic method. Return the element at a given position. """
        return self.array[index]

    def __setitem__(self, index: int, value: tuple) -> None:
        """ Magic method. Insert the item at a given position,
            if possible (!). Shift the following elements to the right.
        """
        if self.is_full():
            self._resize()

        self._shuffle_right(index)
        self.array[index] = value


    def __contains__(self, item):
        """ Checks if item is in the list. """
        for i in range(len(self)):
            if self.array[i] == item:
                return True
        return False

    def _shuffle_right(self, index: int) -> None:
        """ Shuffle items to the right up to a given position. """
        for i in range(len(self), index, -1):
            self.array[i] = self.array[i - 1]

    def _shuffle_left(self, index: int) -> None:
        """ Shuffle items starting at a given position to the left. """
        for i in range(index, len(self)):
            self.array[i] = self.array[i + 1]

    def _resize(self) -> None:
        """ Resize the list. """
        # doubling the size of our list
        new_array = ArrayR(2 * len(self.array))

        # copying the contents
        for i in range(self.length):
            new_array[i] = self.array[i]

        # referring to the new array
        self.array = new_array

    def delete_at_index(self, index: int) -> T:
        """ Delete item at a given position. (Will first check if the number options is 0) """
        item = self.array[index]
        cave = item[0]
        quantity = item[1]
        earning = item[2]
        num_append = item[3]-1
        
        item = (cave, quantity, earning, num_append)
        self.array[index] = item
        
        if item[3] <= 0:
            self.length -= 1
            self._shuffle_left(index)
            return item
        

    def index(self, item: T) -> int:
        """ Find the position of a given item in the list. """
        pos = self._index_to_add(item)
        if pos < len(self) and self[pos] == item:
            return pos
        raise ValueError('item not in list')

    def is_full(self):
        """ Check if the list is full. """
        return len(self) >= len(self.array)

    def add(self, item: tuple[Cave, float, float, int]) -> None: #(Cave, Quantity, Earning, number of options)
        """ Add new element to the list. 
                complexity: O(log(n))
        """
        if self.is_full():
            self._resize()

        # find where to place it
        position = self._index_to_add(item)

        self[position] = item
        self.length += 1

    def _index_to_add(self, item: tuple) -> int:
        """ Find the position where the new item should be placed. 
                complexity: O(log(n)) because this uses binary search
        """
        low = 0
        high = len(self)
        while low < high:
            mid = low + (high-low) // 2
            if self[mid][2] < item[2]-EPSILON:
                low = mid + 1
            elif self[mid][2]-EPSILON > item[2]:
                high = mid
            else:
                return mid
        return low