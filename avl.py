""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev, with edits by Jackson Goerner, modified by Shoumil Guha (32700660)'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic, List
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)
        self.range_counter = 0
        self.range_sorted_list = list()

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            
        """
        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')

        # get the height of the longest subtree and add 1 to account for the current node
        current.height = 1 + max(self.get_height(current.right), self.get_height(current.left))
        current = self.rebalance(current)
        return current

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                current.height -= 1
                return current.right
            elif current.right is None:
                current.height -= 1
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        return self.rebalance(current)

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """

        child = current.right  # save the child node in a variable
        center = child.left  # save the center node in a variable
        child.left = current  # current node is now to the left of the new root node, child
        current.right = center  # move center to the right of the current node

        # update heights for the trees
        # get the height of the longest subtree and add 1 to account for the current node
        current.height = 1 + max(self.get_height(current.right), self.get_height(current.left))
        child.height = 1 + max(self.get_height(child.right), self.get_height(child.left))
        return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """

        child = current.left  # save the child node in a variable
        center = child.right  # save the center node in a variable
        child.right = current  # current node is now to the right of the new root node, child
        current.left = center  # move center to the left of the current node

        # update heights for the trees
        # get the height of the longest subtree and add 1 to account for the current node
        current.height = 1 + max(self.get_height(current.right), self.get_height(current.left))
        child.height = 1 + max(self.get_height(child.right), self.get_height(child.left))
        return child

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def range_between_aux(self, current: AVLTreeNode, i: int, j: int):
        """
        Custom function that utilises recursion to traverse the AVLTree to
        find nodes between the indexes of i and j, inclusive.
        Found nodes are added to a global list variable.

            Params:
                current (AVLTreeNode): The current node of the AVLTree.
                i (int): The lower index.
                j (int): The higher index.

            :complexity: O(j - i + log(N))
                Where N is the number of nodes in the AVLTree
        """
        if current is not None:  # if not a base case
            self.range_between_aux(current.left, i, j)
            self.range_counter += 1
            if i + 1 <= self.range_counter <= j + 1:
                self.range_sorted_list.append(current.item)
            self.range_between_aux(current.right, i, j)

    def range_between(self, i: int, j: int) -> List:
        """
        Returns a sorted list of all elements in the tree between the ith and jth indices, inclusive.
        
        :complexity: O(j - i + log(N))
            The complexity here is due to the range_between_aux function called inside
            this method. Otherwise, all other lines together are O(1).
        """
        self.range_sorted_list = list()  # clear the list from previous calls on this method.
        self.range_between_aux(self.root, i, j)
        self.range_counter = 0
        return self.range_sorted_list
