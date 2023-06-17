from __future__ import annotations
from array_sorted_list import ArraySortedList
from cave import Cave
from hash_table import LinearProbeTable
from material import Material
from sorted_list import ListItem
from trader import Trader, RandomTrader
from food import Food
from random_gen import RandomGen
from constants import EPSILON

"""
This file contains the Player class that will be used to create Player instances to be used in Game generation

Modified by: Arrtish Suthan (32896786), Andrew Miller Prince (32795467) and Avinash Rvan (32717792)

"""

# List taken from https://minecraft.fandom.com/wiki/Mob
PLAYER_NAMES = [
    "Steve",
    "Alex",
    "ɘᴎiɿdoɿɘH",
    "Allay",
    "Axolotl",
    "Bat",
    "Cat",
    "Chicken",
    "Cod",
    "Cow",
    "Donkey",
    "Fox",
    "Frog",
    "Glow Squid",
    "Horse",
    "Mooshroom",
    "Mule",
    "Ocelot",
    "Parrot",
    "Pig",
    "Pufferfish",
    "Rabbit",
    "Salmon",
    "Sheep",
    "Skeleton Horse",
    "Snow Golem",
    "Squid",
    "Strider",
    "Tadpole",
    "Tropical Fish",
    "Turtle",
    "Villager",
    "Wandering Trader",
    "Bee",
    "Cave Spider",
    "Dolphin",
    "Enderman",
    "Goat",
    "Iron Golem",
    "Llama",
    "Panda",
    "Piglin",
    "Polar Bear",
    "Spider",
    "Trader Llama",
    "Wolf",
    "Zombified Piglin",
    "Blaze",
    "Chicken Jockey",
    "Creeper",
    "Drowned",
    "Elder Guardian",
    "Endermite",
    "Evoker",
    "Ghast",
    "Guardian",
    "Hoglin",
    "Husk",
    "Magma Cube",
    "Phantom",
    "Piglin Brute",
    "Pillager",
    "Ravager",
    "Shulker",
    "Silverfish",
    "Skeleton",
    "Skeleton Horseman",
    "Slime",
    "Spider Jockey",
    "Stray",
    "Vex",
    "Vindicator",
    "Warden",
    "Witch",
    "Wither Skeleton",
    "Zoglin",
    "Zombie",
    "Zombie Villager",
    "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
]


class Player():
    """
    This class contains information for the player objects in the game

    attributes:
            name: the name of the player
            balance: the emerald balance of the player
            traders_list: list of traders player can trade with
            foods_list: list of foods player can buy
            materials_list: list of materials player can potentially mine
            caves_list: list of caves player can visit
    """
    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        """ Player class initialiser. """

        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.traders_list = None
        self.foods_list = None
        self.materials_list = None
        self.caves_list = None


    def set_traders(self, traders_list: list[Trader]) -> None:
        """
            Sets the list of traders
            :param
                -> traders_list: a list of traders
        """

        self.traders_list = traders_list

    def get_traders(self) -> list[Trader]:
        """
            Gets the list of traders
            :returns
                -> traders_list: a list of traders
        """

        return self.traders_list

    def set_caves(self, caves_list: list[Cave]) -> None:
        """
            Sets the list of caves
            :param
                -> caves_list: a list of caves
        """

        self.caves_list = caves_list

    def get_caves(self) -> list[Cave]:
        """
            Gets the list of caves
            :returns
                -> caves_list: a list of caves
        """

        return self.caves_list

    def set_foods(self, foods_list: list[Food]) -> None:
        """
            Sets the list of foods
            :param
                -> foods_list: a list of foods
        """

        self.foods_list = foods_list

    def get_foods(self) -> list[Food]:
        """
            Gets the list of foods
            :returns
                -> foods_list: a list of foods
        """

        return self.foods_list

    def get_balance(self) -> float:
        """
            Gets the emerald balance of player
            :returns
                -> balance: emerald balance of player
        """

        return self.balance

    def set_balance(self, new_balance: float) -> None:
        """
            Sets the emerald balance of player
            :param
                -> new_balance: emerald balance of player
        """

        self.balance = new_balance

    @classmethod
    def random_player(self) -> Player:
        """
            Generates a random player by using random name and emerald balance
            :returns
                -> an instance of player
        """

        random_name = RandomGen.random_choice(PLAYER_NAMES)
        random_emeralds = RandomGen.randint(self.MIN_EMERALDS, self.MAX_EMERALDS)
        return Player(random_name, random_emeralds)

    def set_materials(self, materials_list: list[Material]) -> None:
        """
            Gets the list of materials
            :returns
                -> materials_list: a list of materials
        """

        self.materials_list = materials_list

    def _get_trading_list(self) -> LinearProbeTable:
        """ 
        Will return a dictionary with the material:highest buying price

            returns a material:price dictionary
            complexity: O(T) where T is the list of traders
        
        """

        trading_list = LinearProbeTable(len(self.get_traders()))
        for traders in self.get_traders():
            material = traders.current_deal()[0]
            buying_price = traders.current_deal()[1]

            try:
                # if there is already a trader for this material, then ignore the trader with lower buying price
                if(buying_price > trading_list.get_custom(material)):
                    trading_list.insert_custom(material, buying_price)
            except:
                # if not then there is no exisitng trader for this material yet
                trading_list.insert_custom(material, buying_price)

        return trading_list

    def __str__(self) -> str:
        """
            Converts the player contains to a string
            :returns
                -> String containing player name and player's emeralds

        """
        return "Player Name: {pname}, Emeralds: {emeralds}".format(pname=self.name, emeralds=self.balance)

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        """
        This method is used by the player AI to determine the best course of actions to take in the game per day.
        Firstly, we iterate through the list of caves and compare their materials to the available trades the player
        can make via traders. The selected caves are placed in an array sorted list. Then, by iterating through each
        food trade available, we use the balance of the player and the hunger bars obtained to calculate the quantity
        of materials mined from each cave in the array sorted list and calculate the possible profit and new balance
        of the player after mining and trading in a day. The most optimal choice made by the player in the end will
        be the food option that provides the most food, without reducing the initial player balance as well provide
        enough food for the player to obtain large profit balance after trading and mining thought the selected caves.

        The method returns the following:
            tuple containing a list for each of the following:
                Food -> either the food bought by player or None if Food was not purchased
                float -> the emerald balance of the players
                tuple[Cave, float] -> the Cave visited by each player and the quantity of material mined by the player

            complexity:
                O(T+C+F*C) -> T is the list of traders, C is the list of caves, F is the list of foods
                The method has a complexity less than of O(M+T+F*C*LogC)

        ** In depth example is provided at the bottom of the method
        """
        # stores the current emeralds balance of player
        current_balance = self.get_balance()
        # gets the list of trade price
        """ This line has a complexity of O(T), the full details of this function are written in the function header of the _get_trading_list function """
        trader_list = self._get_trading_list()
        # creates a ArraySortedList to store caves and it's efficiency
        efficiency_sorted_list = ArraySortedList(len(self.get_caves()))

        # This particular for loop checks through each available caves, to see if there is a trader for the material the cave contains and adds that cave and it's efficiency to the ArraySortedList
        """ The loop has a complexity of O(C) ~ as all the caves in the cave list has to be looped. hence, the best and worst case complexity is O(C) """
        for cave in self.get_caves():
            try:
                material = cave.get_material()
                # check if there is a trader for this material, if not then skip this cave
                selling_price = trader_list.get_custom(material)
                mining_rate = material.get_mining_rate()
                efficiency = selling_price/mining_rate
                # stores the cave as the value and efficiency as the key
                efficiency_sorted_list.add(ListItem(cave, efficiency), True)
            except:
                pass

        # Empty variables are instantiated
        current_max_profits = 0
        max_cave_list = None
        best_food = None

        # This particular for loop checks through each available food and compares it with the profit from caves to select the optimum emeralds erarned as well as the cave list and food
        """ The loop has a complexity of O(F) ~ as all the foods in the foods list has to be looped. hence, the best and worst case complexity is O(F)
            Combining with the while loop below the overall complexity is O(F*C) 
        """
        for food in self.get_foods():
            # checks if player has enough emeralds to buy any of the foods from the list and gives a value to the variable current_hunger accordingly
            if current_balance-EPSILON > food.get_price():
                current_hunger = food.get_hunger_bars()
            else:
                current_hunger = -1

            # initialise a stop flag and the index
            index = 0

            # initialise a list for the caves visited
            current_cave_list = []
            earnings = 0

            # This particular while loop calculates the  profit from a particular food and generates a tuple of caves visited by player and quantity mined  for the same food item
            """ The loop has a Worst case complexity of O(C) when the player is able to visit every cave and mine materials. Best case is when player cannot afford food so it does not enter the while loop, giving it O(1) complexity"""
            while current_hunger-EPSILON > 0 and index < len(efficiency_sorted_list):
                item = efficiency_sorted_list[index]  # gets each element of the efficiency_sorted_list
                cave = item.value  # retrieves the element's cave
                material = cave.get_material()  # retrieves the cave's material
                mining_rate = material.get_mining_rate()

                quantity_in_cave = cave.get_quantity()  # gets the quantity of the material is in the cave
                quantity_mineable_player = (current_hunger/mining_rate)  # calculates how much the player can mine with the hunger_bars given by the current food

                # check how much can be mined
                quantity_mined = min(quantity_mineable_player, quantity_in_cave)  # if the quantity mineable by the player is larger than cave's quantity, then cave's quantity is mined

                # update the current_hunger
                current_hunger -= (quantity_mined * mining_rate)

                # update the cave_list
                tuple = (cave, quantity_mined)  # tuple of caves visited by player and quantity mined
                current_cave_list.append(tuple)

                # update the earning for this food 
                earnings += trader_list.get_custom(material) * quantity_mined

                # increment list index
                index += 1

            # after going through all the caves possible, check the final profits
            profit = earnings-food.get_price()

            # gets the cave list and food according to the highest profit generated by that particular food
            if (current_max_profits < profit - EPSILON):
                current_max_profits = profit
                max_cave_list = current_cave_list
                best_food = food

        # finally, get the most optimum food to purchase and the most optimum caves and materials to mine
        current_max_profits = max(current_max_profits, 0)  # do this just in case the max profit was negative
        current_balance += current_max_profits

        to_return = (best_food, current_balance, max_cave_list)
        return to_return


        """

        Example for method select_food_and_caves
        
        For this example the player has a intial balance of 50 emeralds
         
           Defining example foods:
                -   Food
                    -   Cabbage Seeds, 
                            - Hunger Bars: 106, Price: 30
                    - Cooked Chicken Cuts
                            - Hunger Bars: 424, Price: 19

            Defining example materials:
                - Gold Nugget
                    - Mining Rate: 27.24
                - Netherite Ingot
                    - Mining Rate: 20.95
                - Fishing Rod
                    - Mining Rate: 26.93
                - Ender Pearl
                    - Mining Rate: 13.91
                - Prismarine Crystal
                    - Mining Rate: 11.48

            Defining example caves:
                -   Castle Karstaag Ruins
                        -   Contains: Netherite Ingot, Quantity: 4 
                -   Glacial Cave
                        -   Contains: Gold Nugget, Quantity: 3
                -   Red Eagle Redoubt
                        -   Contains: Fishing Rod, Quantity: 3 

            Defining example traders:
                - Waldo Morgan
                    - Trade Item:
                        -Item: Fishing Rod, Selling Price: 7.44
                - Orson Hoover
                    - Trade Item:
                        -Item: Gold Nugget, Selling Price: 7.70
                - Lea Carpenter
                    - Trade Item:
                        -Item: Prismarine Crystal, Selling Price: 7.63
                - Ruby Goodman
                    - Trade Item:
                        -Item: Netherite Ingot, Selling Price: 9.78
                - Mable Hodge
                    - Trade Item:
                        -Item: Gold Nugget, Selling Price: 5.40

So, the method will run the set of data accordingly to this example.

Firstly, we will need to select the available list of caves and order them. Available caves are caves that possess a 
material that can be traded with a trader. Per the example caves we have, the array sorted list made from the 
available caves are: 

        Defining example caves:
        -   Castle Karstaag Ruins
                -   Conatains: Netherite Ingot, Quantity: 4 
        -   Glacial Cave
                -   Conatains: Gold Nugget, Quantity: 3
        -   Red Eagle Redoubt
                -   Conatains: Fishing Rod, Quantity: 3 

The array sorted list contains the Cave objects as values, and the efficiency per cave, calculated by dividing the
highest trading price available by the mining rate of that cave

Now we move on to the calculations to determine the best food option and the overall profits garnered.  For each for 
trade available, the initial check ensures that the player has enough emerald initially in their balance to buy the 
trade option, else the entire iteration of the loop for that food option is skipped. If lets say, we have the food option 
chosen and the player can buy them, this is how the calculations would proceed: 

    food chosen = Cabbage Seeds
    current hunger = 106
    earnings = 0

    The overall earnings are zero and we iterate through each cave to find the profit from visiting all the caves.
        -   Castle Karstaag Ruins
            -   Contains: Netherite Ingot, Quantity: 4 

                mining rate = 20.95
                cave quantity = 4
                trading rate = 9.78

                quantity that the player can mine overall = total food / mining rate 
                = 106/20.95 = 5.060

                minium of previous two quantities = 4

                current hunger = current hunger - minimum quantity * mining rate
                current hunger = 106 - 4 * 20.95 = 22.2

                earnings = earnings + minimum quantity * trading rate   
                earnings =  0 +  4 * 9.78 = 29.76

        -   Glacial Cave
            -   Contains: Gold Nugget, Quantity: 3

                mining rate = 27.24
                cave quantity = 3
                trading rate = 7.70

                quantity that the player can mine overall = total food / mining rate 
                = 22.2/27.24 = 0.815

                minium of previous two quantities = 0.815

                current hunger = current hunger - minimum quantity * mining rate
                current hunger = 22.2 - 0.815 * 27.24 = 0

                earnings = earnings + minimum quantity * trading rate   
                earnings = 29.76 +  0.815 * 7.70 = 36.04

        -   Red Eagle Redoubt
            -   Contains: Fishing Rod, Quantity: 3 

                mining rate = 26.93
                cave quantity = 3
                trading rate = 7.44

                quantity that the player can mine overall = total food / mining rate 
                = 0/26.93 = 0

                minium of previous two quantities = 0

                current hunger = current hunger - minimum quantity * mining rate
                current hunger = 0 - 0 * 26.93 = 0

                earnings = earnings + minimum quantity * trading rate   
                earnings =  0 +  0 * 7.44  = 0


    The final values obtained are:
        - earnings = 36.06
        - current hunger = 0
        - list of caves = 

            -   Castle Karstaag Ruins
                -   Conatains: Netherite Ingot, Quantity Mined: 4 
            -   Glacial Cave
                -   Conatains: Gold Nugget, Quantity Mined: 0.815

        - player balance = initial amount + earnings - food trade price
        - player balance = 50 + 36.06 - 30 = 56.06


Now we repeat for food item 2:

    food chosen = Cooked Chicken Cuts
    current hunger = 424
    earnings = 0

    The overall earnings are zero and we iterate through each cave to find the profit from visiting all the caves.
        -   Castle Karstaag Ruins
            -   Contains: Netherite Ingot, Quantity: 4 

                mining rate = 20.95
                cave quantity = 4
                trading rate = 9.78

                quantity that the player can mine overall = total food / mining rate 
                = 424/20.95 = 20.24

                minium of previous two quantities = 4

                current hunger = current hunger - minimum quantity * mining rate
                current hunger = 424 - 4 * 20.95 = 340.2

                earnings = earnings + minimum quantity * trading rate   
                earnings =  0 +  4 * 9.78 = 29.76

        -   Glacial Cave
            -   Contains: Gold Nugget, Quantity: 3

                mining rate = 27.24
                cave quantity = 3
                trading rate = 7.70

                quantity that the player can mine overall = total food / mining rate 
                = 340.2/27.24 = 12.49

                minium of previous two quantities = 3

                current hunger = current hunger - minimum quantity * mining rate
                current hunger = 340.2 - 3 * 27.24 = 258.48

                earnings = earnings + minimum quantity * trading rate   
                earnings = 29.76 + 3 * 7.70 = 52.86

        -   Red Eagle Redoubt
            -   Contains: Fishing Rod, Quantity: 3 

                mining rate = 26.93
                cave quantity = 3
                trading rate = 7.44

                quantity that the player can mine overall = total food / mining rate 
                = 258.48/26.93 = 9.598

                minium of previous two quantities = 3

                current hunger = current hunger - minimum quantity * mining rate
                current hunger = 258.48 - 3 * 26.93 = 177.69

                earnings = earnings + minimum quantity * trading rate   
                earnings =  52.86 +  3 * 7.44  = 75.18


    The final values obtained are:
        - earnings = 75.18
        - current hunger = 177.69
        - list of caves = 

            -   Castle Karstaag Ruins
                -   Contains: Netherite Ingot, Quantity Mined: 4 
            -   Glacial Cave
                -   Contains: Gold Nugget, Quantity Mined: 3
            -   Red Eagle Redoubt
                -   Contains: Fishing Rod, Quantity Mined: 3

        - player balance = initial amount + earnings - food trade price
        - player balance = 50 + 75.18 - 19 = 106.18


Thus via both the iterations of the loop per food, we can determine that the Cooked Chicken Cuts are a more 
profitable food option for the player top select to mine and trade in order to obtain the highest player balance at 
the end of the day 

        """


if __name__ == "__main__":
    print(Player("Steve"))
    print(Player("Alex", emeralds=1000))
