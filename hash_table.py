""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
"""
from __future__ import annotations
from random_gen import RandomGen
__author__ = 'Brendon Taylor. Modified by Graeme Gange, Alexey Ignatiev, Jackson Goerner, and Avinash Rvan (32717792)'
__docformat__ = 'reStructuredText'
__modified__ = '26/10/2022'


from referential_array import ArrayR
from primes import LargestPrimeIterator
from typing import TypeVar, Generic
T = TypeVar('T')
from trader import TRADER_NAMES

from material import Material
from cave import Cave

class LinearProbeTable(Generic[T]):
    """
        Linear Probe Table.

        attributes:
            count: number of elements in the hash table
            table: used to represent our internal array
            tablesize: current size of the hash table
            conflict_count: the number of conflicts encountered throughout using the Hash Table
            probe_total: the number of probes done throughout using the Hash Table
            probe_max: the maximum probe chain length throughout using the Hash Table
            rehash_count: the number of rehashes the table has done throughout using the Hash Table
    """

    def __init__(self, expected_size: int, tablesize_override: int = -1) -> None:
        """
            Initialiser.
        """

        # check if the user wants to override the auto table size 
        if(tablesize_override==-1):
            # create the initial estimate of table size (which is 2.5 times the expected size)
            tablesize=round(2.5*(expected_size))

            # create a prime generator based on the estimate tablesize and set the step factor to 2 (to always double the size)
            self.primeGenerator = LargestPrimeIterator(tablesize, 2)
            tablesize = next(self.primeGenerator)
        else:
            tablesize=tablesize_override

            # create a prime generator based on the initial tablesize and set the step factor to 2 (to always double the size)
            self.primeGenerator = LargestPrimeIterator(tablesize, 2)
            next(self.primeGenerator)

        
        # set the intial count to 0
        self.count=0
        self.table=ArrayR(tablesize)

        # initalise the statistics variables
        self.conflict_count = 0
        self.probe_total = 0
        self.probe_max = 0
        self.rehash_count = 0

    def hash(self, key: str) -> int:
        """
            Hash a key for insertion into the hashtable. 
            This is done using a prime base which changes pseudorandomly for every input.

                return: 
                    the hash key for a given input
                complexity: 
                    O(n) where n is the number of characters of input string
        """

        # initalise the hash
        value = 0

        # create a base value which is prime to allow the hash to be as unique as possible
        base = 5333
        baseGen = 7919

        for char in key:
            value = ((value*base) + ord(char)% len(self.table)) % len(self.table)

            # keep changing the base value pseudorandomly to ensure more spread out hash keys
            base = (base * baseGen) % len(self.table)

        return value


    def statistics(self) -> tuple:
        """
            Returns a tuple containing conflict_count, total probes, maximum probe chain length, number of rehashes
        """
        returnTuple = (self.conflict_count, self.probe_total, self.probe_max, self.rehash_count)
        return returnTuple

    def __len__(self) -> int:
        """
            Returns number of elements in the hash table
            :complexity: O(1)
        """
        return self.count

    def _linear_probe(self, key: str, is_insert: bool) -> int:
        """
            Find the correct position for this key in the hash table using linear probing
            :complexity best: O(K) first position is empty
                            where K is the size of the key
            :complexity worst: O(K + N) when we've searched the entire table
                            where N is the tablesize
            :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash

        if is_insert and (self.count > (len(self.table)/2)):
            # if the table is more than half full, then rehash the whole table
            self._rehash()
        elif is_insert and self.is_full():
            raise KeyError(key)
        
        # set a flag to ensure that the conflict counter is only incremented once
        increment_flag = True
        probe_count=0

        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is something but not the key, try next by probing
                position = (position + 1) % len(self.table)

                # increment the probe count and check if it is the max
                probe_count+=1

                if(probe_count>self.probe_max):
                    self.probe_max=probe_count
                
                # increment all the variables needed for statistics
                if increment_flag and is_insert:
                    self.conflict_count+=1
                    increment_flag = False

                self.probe_total+=1

        raise KeyError(key)

    def keys(self) -> list[str]:
        """
            Returns all keys in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][0])
        return res

    def values(self) -> list[T]:
        """
            Returns all values in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][1])
        return res

    def __contains__(self, key: str) -> bool:
        """
            Checks to see if the given key is in the Hash Table
            :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
            Get the item at a certain key
            :see: #self._linear_probe(key: str, is_insert: bool)
            :raises KeyError: when the item doesn't exist
        """
        position = self._linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
            Set an (key, data) pair in our hash table
            :see: #self._linear_probe(key: str, is_insert: bool)
            :see: #self.__contains__(key: str)
        """

        position = self._linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1

        self.table[position] = (key, data)

    def is_empty(self):
        """
            Returns whether the hash table is empty
            :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
            Returns whether the hash table is full
            :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
            Utility method to call our setitem method
            :see: #__setitem__(self, key: str, data: T)
        """
        self[key] = data

    def insert_custom(self, key: Material|Cave, data: float) -> None:
        """
            Custom method used to insert either a Material or Cave object into the Hash Table by passing in the instance 
            of the object. This method will use the name of the object as the key for hashing

                params:
                    @key -> an object of either Material or Cave instance
                    @data -> a float
        """
        key_string = key.get_name()
        self[key_string] = data
    
    def get_custom(self, key: Material|Cave) -> float:
        """
            Custom method used to return the value given a key of either Material or Cave instance

                params:
                    @key Material or Cave instance

                returns:
                    a float
        """
        key_string = key.get_name()
        return self.__getitem__(key_string)

    def _rehash(self) -> None:
        """
            Need to resize table and reinsert all values
            :complexity: O(n)
        """
        # set the new table size by taking the largest prime which is less than twice of the previous size
        newTableSize = next(self.primeGenerator)

        # copy the old table
        oldTable = self.table

        # create a new table and reset the count
        self._clear(newTableSize)

        for pos in range(len(oldTable)):
            item = oldTable[pos]

            if item is not None:
                (key, value) = item

                # insert the key and value into the new table
                self.insert(key, value)

        # increment the rehash count
        self.rehash_count+=1


    def _clear(self, newTableSize) -> None:
        """
            Clears the entire Hash Table  
        """
        self.table = ArrayR(newTableSize)
        self.count = 0

    def __str__(self) -> str:
        """
            Returns all they key/value pairs in our hash table (no particular
            order).
            :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result


