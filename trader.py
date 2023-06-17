from __future__ import annotations
from abc import abstractmethod, ABC
from array_list import ArrayList
from avl import AVLTree
from heap import MaxHeap
from material import Material
from random_gen import RandomGen
"""
This file contains all the classes and methods for the trader functionality of the game.
"""

__author__ = 'Modified by: Shoumil Guha (32700660)'

# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]


class Trader(ABC):
    """
    The Trader class extends the ABC and abstractmethod classes in order to
    implement the abstract base class functionality.
    It contains attributes and methods shared by all the extending trader classes.

    :complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1).
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.material_list = ArrayList(0)
        self.active_deal = None

    @classmethod
    def random_trader(cls) -> Trader:
        """
        Gives a random type of trader.

            Returns: (Trader) A trader object of either one of the three trader types.
        """
        trader_name = RandomGen.random_choice(TRADER_NAMES)
        random_int = RandomGen.randint(1, 3)
        if random_int == 1:
            return RandomTrader(trader_name)
        if random_int == 2:
            return RangeTrader(trader_name)
        if random_int == 3:
            return HardTrader(trader_name)

    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Clears the list of materials from the trader's inventory and puts in the list
        of materials passed in through the list.

            Params:
                mats (list[Material]):  A list of materials you want the trader to sell.

            :complexity:
                best/worst: O(N)
                    Appending to an ArrayList is always O(1) complexity hence appending all elements
                    from the given list is O(N).
        """
        self.material_list = ArrayList(0)
        for material in mats:
            self.material_list.append(material)

    def add_material(self, mat: Material) -> None:
        """
        Adds a material to the trader's material list.

            Params:
                mat (Material): The material to be added.
        """
        self.material_list.append(mat)

    def remove_material(self, mat: Material) -> None:
        """
        Removes a material to the trader's material list.

            Params:
                mat (Material): The material to be removed.
        """
        self.material_list.remove(mat)

    def is_currently_selling(self) -> bool:
        """
        Checks if the trader has a deal currently active.

            Returns: (bool) True, if the trader is currently selling something.
        """
        if self.active_deal:
            return True
        return False

    def current_deal(self) -> tuple[Material, float]:
        """
        Gives the currently active deal of the trader.

            Returns: (tuple) The active deal which has the material and its buying price.
        """
        if not self.active_deal:
            raise ValueError("No active deal!")
        return self.active_deal

    @abstractmethod
    def generate_deal(self) -> None:
        raise NotImplementedError()

    def stop_deal(self) -> None:
        """
        Clears the active deal of the trader.
        """
        self.active_deal = None

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns: (str) A string describing the type of trader,
        material being sold, and its buying price.
        """
        raise NotImplementedError()


class RandomTrader(Trader):
    """
    Extends the base Trader class and implements its own version of generate_deal.
    Trader's active deal is generated at random.
    """
    def __init__(self, name: str) -> None:
        Trader.__init__(self, name)

    def generate_deal(self) -> None:
        """
        Generates a deal with a random material (from the list of materials)
        and a random buy price.
        """
        random_material = RandomGen.random_choice(self.material_list)
        buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        self.active_deal = (random_material, buy_price)

    def __str__(self) -> str:
        if self.active_deal is not None:
            current_deal = self.current_deal()
        else:
            current_deal = (None, None)
        print_string = "<RandomTrader: {} buying {} for {}💰>".format(self.name, current_deal[0], current_deal[1])
        return print_string


class RangeTrader(Trader):
    """
    Extends the base Trader class and implements its own version of generate_deal.
    Trader's active deal is generated based on a range of materials chosen based on difficulty.
    """
    def __init__(self, name: str) -> None:
        Trader.__init__(self, name)

    def materials_between(self, i: int, j: int) -> list[Material]:
        """
        A special helper method which returns a list containing the materials
        which are somewhere between the ith and jth easiest to mine.

            Params:
                i (int): Index of the lower end of the easiest to mine.
                j (int): Index of the higher end of the easiest to mine.

            Returns: (list) A list containing the materials.

        :complexity:
            best/worst: O(N)
                Where N is the size of the list of materials in the trader's inventory.
        """
        avl_tree = AVLTree()
        for material in self.material_list:
            if material is not None:
                avl_tree[material.mining_rate] = material
        easy_materials = avl_tree.range_between(i, j)
        return easy_materials

    def generate_deal(self) -> None:
        """
        Generates a deal with a random material in the materials list that
        lies between the ith and jth easiest to mine, inclusive.
        A random buy price is selected.

        :complexity:
            best/worst: O(N)
                Where N is the size of the list of materials in the trader's inventory.
        """
        i = RandomGen.randint(0, len(self.material_list) - 1)
        j = RandomGen.randint(i, len(self.material_list) - 1)
        random_material = RandomGen.random_choice(self.materials_between(i, j))
        buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        self.active_deal = (random_material, buy_price)

    def __str__(self) -> str:
        if self.active_deal is not None:
            current_deal = self.current_deal()
        else:
            current_deal = (None, None)
        print_string = "<RangeTrader: {} buying {} for {}💰>".format(self.name, current_deal[0], current_deal[1])
        return print_string


class HardTrader(Trader):
    """
    Extends the base Trader class and implements its own version of generate_deal.
    Trader's active deal is generated based on the hardest to mine material in their inventory.
    """
    def __init__(self, name: str) -> None:
        Trader.__init__(self, name)

    def generate_deal(self) -> None:
        """
        Generates a deal with the hardest to mine material and removes
        it from the trader's inventory.
        A random buy price is selected.

        :complexity:
            best/worst: O(N)
                Where N is the size of the list of materials in the trader's inventory.
        """
        material_heap = MaxHeap(len(self.material_list))
        for material in self.material_list:
            if material is not None:
                material_heap.add((material, material.mining_rate))
        hardest_to_mine = material_heap.get_max()

        buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        self.active_deal = (hardest_to_mine[0], buy_price)

    def __str__(self) -> str:
        if self.active_deal is not None:
            current_deal = self.current_deal()
        else:
            current_deal = (None, None)

        print_string = "<HardTrader: {} buying {} for {}💰>".format(self.name, current_deal[0], current_deal[1])
        return print_string


if __name__ == "__main__":
    trader = RangeTrader("Jackson")
    print(trader)
    trader.set_all_materials([
        Material("Coal", 4.5),
        Material("Diamonds", 3),
        Material("Redstone", 20),
    ])
    trader.generate_deal()
    print(trader)
    trader.stop_deal()
    print(trader)
