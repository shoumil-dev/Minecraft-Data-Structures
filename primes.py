"""
This file contains the Largest Prime Iterator class which generates the largest prime number lesser than a given upper bound
"""

from __future__ import annotations

__author__ = 'Andrew Miller Prince (32795467) and Arrtish Suthan (32896786)'
__docformat__ = 'reStructuredText'

class LargestPrimeIterator():
    """
        LargestPrimeIterator.

        attributes:
            upper_bound: the limit to find a prime number lesser than
            factor: a factor to increase the upper bound
    """
    def __init__(self, upper_bound, factor) -> None:
        """ Iterator initialiser. """

        self.upper_bound = upper_bound
        self.factor = factor

    def __iter__(self) -> LargestPrimeIterator:
        """ Standard __iter__() method for initialisers. Returns itself. """

        return self

    def __next__(self) -> int:
        """ The main body of the iterator.
            Returns the largest prime number lesser than the upper bound
        """

        p_max = self.upper_bound - 1
        p = self.max_prime(p_max)
        self.upper_bound = p * self.factor
        return p

    def is_prime(self, n):
        """
            Checks if the inputted value is a prime number
            :complexity: O(n)
        """
        for i in range(2, n):
            if (n % i) == 0:
                return False
        return True

    def max_prime(self, check) -> int:
        """
            Gets the largest prime number lesser than the upper bound
            :complexity: O(n) ~ The function calls itself 'n' times to calculate the prime number
        """
        if self.is_prime(check):
            return check
        else:
            check -= 1
            return self.max_prime(check)
