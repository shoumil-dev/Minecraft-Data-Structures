from __future__ import annotations
# from ast import Mult
# from tkinter import NONE
from ArraySortedList import ArraySortedList_Game
from aset import ASet
from hash_table import LinearProbeTable

from player import Player
from trader import RandomTrader, RangeTrader, Trader
from material import Material
from cave import Cave
from food import Food
from random_gen import RandomGen
from abc import abstractmethod, ABC
from constants import EPSILON

"""
This file will contain methods that are used to run the entire game. 
This includes two types of games, that is SoloGame and MultiplayerGame


Modified by: Avinash Rvan (32717792)
"""

class Game(ABC):
    """
    This is the abstract class for both the types of games available, that is SoloGame, and MultiplayerGame.
    All methods, unless stated otherwise, have a complexity of O(1)

        attributes:
            material_list: a list of all the materials avaialable in the game
            cave_list: a list of all the caves that the player would be able to visit
            trader_list: a list of all the traders that exist in the game
    
    """

    MIN_MATERIALS = 5
    MAX_MATERIALS = 10

    MIN_CAVES = 5
    MAX_CAVES = 10

    MIN_TRADERS = 4
    MAX_TRADERS = 8

    MIN_FOOD = 2
    MAX_FOOD = 5

    def __init__(self) -> None:
        """ Constructor for the base class """
        self.setup = True

    def initialise_game(self) -> None:
        """Initialise all game objects: Materials, Caves, Traders."""
        N_MATERIALS = RandomGen.randint(self.MIN_MATERIALS, self.MAX_MATERIALS)
        self.generate_random_materials(N_MATERIALS)
        print("Materials:\n\t", end="")
        print("\n\t".join(map(str, self.get_materials())))
        N_CAVES = RandomGen.randint(self.MIN_CAVES, self.MAX_CAVES)
        self.generate_random_caves(N_CAVES)
        print("Caves:\n\t", end="")
        print("\n\t".join(map(str, self.get_caves())))
        N_TRADERS = RandomGen.randint(self.MIN_TRADERS, self.MAX_TRADERS)
        self.generate_random_traders(N_TRADERS)
        print("Traders:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader]):
        """ Initialises the class given inputs passed in """
        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)

    def set_materials(self, mats: list[Material]) -> None:
        """ Sets the list of materials for the game """
        self.material_list = mats

    def set_caves(self, caves: list[Cave]) -> None:
        """ Sets the list of caves for the game """
        self.cave_list = caves

    def set_traders(self, traders: list[Trader]) -> None:
        """ Sets the list of traders for the game """
        self.trader_list = traders

    def get_materials(self) -> list[Material]:
        """ Gets the list of materials for the game """
        return self.material_list

    def get_caves(self) -> list[Cave]:
        """ Gets the list of materials for the game """
        return self.cave_list

    def get_traders(self) -> list[Trader]:
        """ Gets the list of materials for the game """
        return self.trader_list

    def _amount_check(self, amount) -> bool:
        """ Checks if the amount input is a positive int """

        if type(amount)!=int or amount<=0:
            return False
        else:
            return True

    def _get_trading_list(self) -> LinearProbeTable:
        """ 
        Will return a dictionary with the material:highest buying price

            returns a material:price dictionary
            complexity: 
                best/worst: O(T) where T is the list of traders
        
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

    def _get_cave_materials(self) -> LinearProbeTable:
        """ 
        Will return a dictionary with the Cave:quantity of material

            returns a Cave:quantity dictionary
            complexity: 
                best/worst: O(C) where C is the list of caves
        
        """

        material_list = LinearProbeTable(len(self.get_caves()))

        for cave in self.get_caves():
            material_list.insert_custom(cave, cave.get_quantity())

        return material_list

    def generate_random_materials(self, amount):
        """
        Generates <amount> random materials using Material.random_material
        Generated materials must all have different names and different mining_rates.
        (You may have to call Material.random_material more than <amount> times.)
        """
        material_list = []
        name_list = []
        mining_rate_list = []

        # check that the amount entered is valid
        if not (self._amount_check(amount)):
            raise ValueError("The amount must be an integer more than 0")
        
        # iterate until the material_list has enough unique materials
        while len(material_list) < amount:
            newMaterial = Material.random_material()

            # check if the new random material has unique name and mining rate
            if (newMaterial.name not in name_list) and (newMaterial.mining_rate not in mining_rate_list) :

                # if it is unique, then add it to the final material list, and add its data into the other lists for checking later
                name_list.append(newMaterial.name)             
                mining_rate_list.append(newMaterial.mining_rate)   
                material_list.append(newMaterial)

        # set the materials using the setter method
        self.set_materials(material_list)
            
    def generate_random_caves(self, amount):
        """
        Generates <amount> random caves using Cave.random_cave
        Generated caves must all have different names
        (You may have to call Cave.random_cave more than <amount> times.)
        """
        cave_list = []
        name_list = []

        # check that the amount entered is valid
        if not (self._amount_check(amount)):
            raise ValueError("The amount must be an integer more than 0")
        
        # iterate until the cave_list has enough unique caves
        while len(cave_list) < amount:
            newCave = Cave.random_cave(self.get_materials())

            # check if the new random cave has unique name and mining rate
            if (newCave.name not in name_list) :

                # if it is unique, then add it to the final cave list, and add its name into the name list for checking later
                name_list.append(newCave.name)             
                cave_list.append(newCave)

        # set the caves using the setter method
        self.set_caves(cave_list)

    def generate_random_traders(self, amount):
        """
        Generates <amount> random traders by selecting a random trader class
        and then calling <TraderClass>.random_trader()
        and then calling set_all_materials with some subset of the already generated materials.
        Generated traders must all have different names
        (You may have to call <TraderClass>.random_trader() more than <amount> times.)
        """
        trader_list = []
        name_list = []

        # check that the amount entered is valid
        if not (self._amount_check(amount)):
            raise ValueError("The amount must be an integer more than 0")
        
        # iterate until the trader_list has enough unique traders
        while len(trader_list) < amount:
            # this will automatically choose a random type of trader as well
            newtrader = Trader.random_trader()

            # check if the new random trader has unique name and mining rate
            if (newtrader.name not in name_list) :

                # create a random subset of the existing materials and set the trader's materials
                material_list = self.get_materials()
                lowBound = RandomGen.randint(0, len(material_list)//2)
                upperBound = RandomGen.randint(lowBound+1, len(material_list))
                material_subset = material_list[lowBound:upperBound]

                newtrader.set_all_materials(material_subset)

                # if it is unique, then add it to the final trader list, and add its name into the name list for checking later
                name_list.append(newtrader.name)             
                trader_list.append(newtrader)

        # set the traders using the setter method
        self.set_traders(trader_list)

    def finish_day(self):
        """
        DO NOT CHANGE
        Affects test results.
        """
        for cave in self.get_caves():
            if cave.quantity > 0 and RandomGen.random_chance(0.2):
                cave.remove_quantity(RandomGen.random_float() * cave.quantity)
            else:
                cave.add_quantity(round(RandomGen.random_float() * 10, 2))
            cave.quantity = round(cave.quantity, 2)


class SoloGame(Game):
    """
    This is the class for the SoloGame. In this game mode, there is only one player who has multiple Food options and can visit multiple Caves in a day.
    All methods, unless stated otherwise, have a complexity of O(1)

        attributes:
            material_list: a list of all the materials avaialable in the game
            cave_list: a list of all the caves that the player would be able to visit
            trader_list: a list of all the traders that exist in the game
    
    """

    def initialise_game(self) -> None:
        """ Initialises the game with random materials, caves, and traders """

        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        """ Initalises the game with passed in inputs """
        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def simulate_day(self):
        """ 
            Simulates a day for the SoloGame by doing the following:
            1) get the trader deals
            2) get the foods offered to the player
            3) get the player's decision
            4) carry out verification and update the quantities of materials

            complexity:
                best: O(1) -> this is the case if there are no traders, foods and caves
                worst: O(T + F + C + F*C) -> this is the case where none of the attributes are empty and the functions run for as long as possible
        
        """

        # 1. Traders make deals
        trader_list = self.get_traders()

        for traders in trader_list:
            traders.generate_deal()

        # save this new updated trader list
        self.set_traders(trader_list)

        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        food_num = RandomGen.randint(self.MIN_FOOD, self.MAX_FOOD)
        foods = []
        for _ in range(food_num):
            foods.append(Food.random_food())
        print("\nFoods:\n\t", end="")
        print("\n\t".join(map(str, foods)))
        self.player.set_foods(foods)
        # 3. Select one food item to purchase
        food, balance, caves = self.player.select_food_and_caves()
        print(food, balance, caves)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(food, balance, caves)


    def verify_output_and_update_quantities(self, food: Food | None, balance: float, caves: list[tuple[Cave, float]]) -> None:
        """
            Verifies that all the inputs are logical, the balances are correct, and the quantities left in the cave are sufficient for the player
            to mine the materials as inputted

                params: 
                    @food -> the food purchased by the player
                    @balance -> the balance of emeralds in the player after buying food, mining and selling the material
                    @caves -> a list of tuples where each tuple contains the Cave visited and the quantity of material mined

                complexity:
                    best: O(1) -> this is case when there are no trader or caves, thus there is nothing to check
                    worst: O(T + C) -> where T is the size of list of traders and C is the size of list of caves
        """


            # 1. Check for basic logic checks 
        
        # check that the balance is a non-negative float
        if type(balance) not in [float, int] or (balance < 0):
            raise ValueError("The balance must be a non-negative float")

        # check that if the food is none, then the list of caves must also be none
        if food==None and caves!=None:
            raise ValueError("The player cannot visit caves without eating any food")

        # check that the food can be purchased and the player has funds to purchase it
        if (food!=None):
            if (food not in self.player.get_foods()) or (food.get_price()- EPSILON > self.player.get_balance()):
                raise ValueError("This food cannot be purchased")


            # 2. Check that all the caves have at least the amount required, and there is a trader who wants to buy the material

        # create a dictionary of the traders and the buying price 
        """ This will be O(T) complexity """
        trading_list=self._get_trading_list()
        
        # go through all the caves and check that there are enough materials 
        # and accumalate the total hunger bars required to mine all the materials listed
        # and accumalate the money earned by mining each cave
        total_hunger_bars = 0
        emeralds_earned = 0

        if caves!=None:
            """ This will be O(C) complexity"""
            for items in caves:
                cave = items[0]
                quantity = items[1]
                material = cave.get_material()

                # first check that there are enough materials in the cave
                quantity_check = (quantity < cave.get_quantity() - EPSILON) or (quantity-cave.get_quantity()<EPSILON)

                # next check if there is a trader willing to trade this material
                try: 
                    trading_list.get_custom(material) # this will check the Hash Table for this material key, and if it is not present, it will raise an error
                                                      # this method of checking has O(1) complexity instead of using material in trading_list.keys() which would be O(T) complexity
                    trader_check=True
                except:
                    trader_check =False

                if not(quantity_check and trader_check):
                    raise ValueError("The quantity of materials in the cave is less than required or there are no traders to trade this material")

                # accumalate the hunger bars needed 
                total_hunger_bars += (material.get_mining_rate() * quantity)

                # accumalate the money earned
                emeralds_earned += (quantity * trading_list.get_custom(material))

            
            # 3. Now check that after carrying out all the purchasing and mining, the final balance is the same as the input

        # first check that the player has enough hunger bars
        if (food!=None):
            if (total_hunger_bars- EPSILON > food.get_hunger_bars() ):
                raise ValueError("The mining requires more hunger bars than the player has")

        # now carry out all the purchase and mining
        current_balance = self.player.get_balance()
        if (food!=None):
            current_balance -= food.get_price()
        current_balance += emeralds_earned

        # now check that the final balance is the same
        if (abs(current_balance - balance) > EPSILON ):
            raise ValueError("The final balance is not the same as the input")
        

            # 4. Now that all the checks have passed, update the balance of the player, and update the quantities in each cave

        self.player.set_balance(balance)

        if (caves!=None):
            for items in caves:
                cave = items[0]
                quantity = items[1]
                
                cave.remove_quantity(quantity)


class MultiplayerGame(Game):
    """
    This is the class for the MultiplayerGame. In this game mode, there are multiple players who will play in order. 
    All methods, unless stated otherwise, have a complexity of O(1)

        attributes:
            material_list: a list of all the materials avaialable in the game
            cave_list: a list of all the caves that the player would be able to visit
            trader_list: a list of all the traders that exist in the game
            players: the list of all the players who are in the game
    
    """

    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        """ Initalises an empty list for the list of players in the game """
        super().__init__()
        self.players = []

    def initialise_game(self) -> None:
        """
            Initialises the game with random materials, players, caves, and traders
        """

        super().initialise_game()
        N_PLAYERS = RandomGen.randint(self.MIN_PLAYERS, self.MAX_PLAYERS)
        self.generate_random_players(N_PLAYERS)
        for player in self.players:
            player.set_materials(self.get_materials())
            player.set_caves(self.get_caves())
            player.set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def generate_random_players(self, amount) -> None:
        """Generate <amount> random players. Don't need anything unique, but you can do so if you'd like."""
        player_list = []
        name_list = []

        # check that the amount entered is valid
        if not (self._amount_check(amount)):
            raise ValueError("The amount must be an integer more than 0")

        while len(player_list) < amount:
            new_player = Player.random_player()
            new_player_name = new_player.name

            # check if the name already exists, and if not then add the player in 
            if new_player_name not in name_list:
                player_list.append(new_player)
                name_list.append(new_player_name)

        # once the length needed is reached, set the player list
        self.set_players(player_list)
    
    def set_players(self, players: list[Player]):
        """ Sets the list of players for the game """
        self.players = players

    def get_players(self):
        """     returns the list of players for the game    """
        return self.players

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        """
            Initialises the game with passed in inpus
        """
        super().initialise_with_data(materials, caves, traders)
        for player, emerald in zip(player_names, emerald_info):
            self.players.append(Player(player, emeralds=emerald))
            self.players[-1].set_materials(self.get_materials())
            self.players[-1].set_caves(self.get_caves())
            self.players[-1].set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def simulate_day(self):
        """
            Simulates a day in the game where the following will occur:
            1) the traders will generate their deals
            2) ONE random food will be offered to all the player's
            3) the players will choose which cave and how much material to mine 
            4) the decisions of all the players are verified and the quantities are updated

            complexity:
                best: O(1) -> where there are no foods offered, or no caves to visit 
                worst: O(T + P + C*log(C)) -> this is if there is at least one food, and one cave for the players to visit
        """

        # 1. Traders make deals
        trader_list = self.get_traders()

        for traders in trader_list:
            traders.generate_deal()

        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        offered_food = Food.random_food()
        print(f"\nFoods:\n\t{offered_food}")
        # 3. Each player selects a cave - The game does this instead.
        foods, balances, caves = self.select_for_players(offered_food)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(foods, balances, caves)        
    
    def _get_best_mining_choice(self, food: Food) -> list[tuple[Cave, float, float, int]]:
        """
            Helper function will iterate through the list of caves and keep creating tuple options of which cave, how much is 
            mined, and how much is earned. This data is added to a sorted list to be used later.

            This is done by first iterating through all the caves in the game. If the cave does not have a tradeable material, then it is ignored.
            Then, the quantity of materials in the cave is obtained and the maximum quantity of materials that can be mined by the player is calculated using the 
            hunger_bars of the food divided by the mining_rate of the material. 

            If the quantity the player can mine is more than what is in the cave, the num_append** is set to 0. 
            
            **The num_append is considered to be the number of players who can mine that same amount of material from the same cave before it runs out. 
            For example, if the amount a player can mine is 2, and the cave has 21 material, then the num_append is 10 because 10 players can mine 2 material each 
            from this cave before it gets too little. 

            If the quantity mineable by the player is less than what's in the cave, then the num_append is calculated by taking the quantity_in_the_cave/quantity_mineable_by_player.
            This num_append is added to the tuple which will be stored in the ArraySortedList.

            Finally, the balance material leftover in the cave after the multiple players mine the same amount is also added as an option to the sorted list.

            In the end, the sorted list will contain tuples sorted by their earning potential. Each tuple will contain the following information, in that order:
            (The cave being mined, How much is the maximum material that can be mined per player, How much is earned from this cave, How many players can mine this cave with this quantity)
            
                pre:
                    player has enough money to buy the food 

                params: 
                    food -> the food bought by the player
                
                return:
                    list[tuple[Cave, float, float, int]] -> the cave that is mined, the quantity of material mined, the earning from this mining, and the number of players that can mine this cave for this quantity

                complexity:
                    best: O(1) -> this is when there are no traders and caves, thus the code will not have any iterations
                    worst: O(T + C*log(C)) -> where C is the size of the list of Caves in the game and T is the size of the list of Traders in the game, this is when there is a list of caves and traders with more
                                              than 1 item. And, every iteration of adding an item to the sorted list is added at either the last or first index
        """

        # get the hunger bar for the food
        hunger_bars = food.get_hunger_bars()

        # create a sorted list to store all the options
        options_list = ArraySortedList_Game(len(self.get_caves()))

        """ This will have O(T) complexity """
        trading_list = self._get_trading_list()

        # add options to the list while there are not enough options
        """ we will consider this outer block to have a complexity of O(C) since it iterates through for all the caves """
        for cave in self.get_caves():
            # iterate through the caves
            material = cave.get_material()
            
            # check if the material is tradeable
            try:
                """ This check is O(1) complexity since the getter for HashTables is assumed to be O(1) complexity """
                price = trading_list.get_custom(material)
                mining_rate = material.get_mining_rate()

                quantity_in_cave = cave.get_quantity()
                
                quantity_mineable_player = hunger_bars/mining_rate
                
                if(quantity_mineable_player-EPSILON>quantity_in_cave): # this means that the player can mine the entirety of the content in the cave
                    num_append=0
                else:
                    num_append = int(quantity_in_cave // quantity_mineable_player) # this is the number of times a player can maximally mine in this cave

                if num_append==0:
                    # if the num_append is 0, then the player can mine more than what is in the cave
                    earning = price*quantity_in_cave
                    """ 
                        This function has O(log(C)) worst case beacause the add function uses binary search which will half the search elements each iteration
                    """
                    options_list.add((cave, quantity_in_cave, earning, 1))

                elif num_append>0:
                    # this means that the player can mine less than what is in the cave
                    earning = price*quantity_mineable_player

                    """ 
                        This function has O(log(C)) worst case beacause the add function uses binary search which will half the search elements each iteration
                    """
                    options_list.add((cave, quantity_mineable_player, earning, num_append))

                    if num_append<len(self.get_players()):
                        # this means that for this cave, there are less mining options than there are players, 
                        # and there is still some balance material in the cave, so add this option to the list
                        balance_in_cave = quantity_in_cave-(quantity_mineable_player*num_append)
                        earning = price*balance_in_cave

                        """ 
                        This function has O(log(C)) worst case beacause the add function uses binary search which will half the search elements each iteration
                        """
                        options_list.add((cave, balance_in_cave, earning, 1))
                    
            except:
                # this means that the material is not tradeable as the key is not in the HashTable
                pass


        return options_list


    def select_for_players(self, food: Food) -> tuple[list[Food|None], list[float], list[tuple[Cave, float]|None]]:
        """
        This method will run through each player in the order that of the player list, and choose a cave for them to mine as well as the quantity of material to mine from 
        that cave. The method will also take into account if the player has insufficient money to buy food, or if mining is not worth it. The design for the code is explained as follows:

            - Firstly, the empty variables are instantiated
            - Next, the helper function, _get_best_mining_choice is called. @see _get_best_mining_choice function for the full details on how it works. This function will return
              a sorted list of the best "options" for players to mine. Each option is in the form of tuple containing the following information:
              (Cave to mine, quantity to mine, earnings from mining this cave, how many players can mine this cave for this quantity)
            - This method of creating all the options is done first to ensure that it will not be placed within another for loop, which would increase the complexity exponentially. For example, the
              approach we first used is by placing a nested for loop within the player loop to iterate through all the caves and find the best material to mine. However, this would make the complexity
              O(P*C) which would make the code run for a much longer time when using larger data sets
            - Then, the code will iterate through all the players in the game currently
            - For each player, the next best option for mining is obatained from the sorted list that was created previously. Then, the outcome of this mining is checked to see if it is worth mining.
              This is checked by seeing if the money earned from mining the material is more than the cost of the food (with an error margin of EPSILON since floating point numbers are used). 
            - If the mining is worth it, then this mining option is removed from the sorted list using the delete_at_index function** and the other information are added to the lists as required
              **the delete_at_index function is modified in this scenario. the function will first decrement the num_append element in the tuple as this variable is the indication of how many players
                can still choose this option. then, if the variable is 0 or less, that means no other player can select this option anymore and it will be removed from the list
            - If the mining is not worth it, then None are appended to the lists as required

            - Essentially, this design was chosen to ensure that any for loops that need to be written are separated as much as possible. Without separating them, the complexity would increase
              exponentially which would lead to undesirable side effects. 

            - EXAMPLE: For a proper worked example, please see the worked_example function, and then RUN this file

            params:
                food -> the food offered to the players for the day

            returns:
                tuple containing a list for each of the following:
                    Food -> either the food bought by player or None if Food was not purchased
                    float -> the emerald balance of the players
                    tuple[Cave, float] -> the Cave visited by each player and the quantity of material mined by the player

            complexity:
                best: O(1) -> this will occur when there are no players in the game
                worst: 
                    O(T + P + C*log(C)) ---> this complexity is less than the bound of O(M + T + C + P*log C), as this function does not take into account the M materials list size 
                        -> this complexity will occur if there are non-zero number of traders, players, and caves in the game. 
        """

        # initalise some variables
        food_list = []
        balance_list = []
        cave_list = []
        food_price = food.get_price()

        # get a sorted list of the best options for the player to choose
        """ This line has a complexity of O(T + C*log(C)), the full details of this function are written in the function header of the _get_best_mining_choice function """
        options_list = self._get_best_mining_choice(food)

        # iterate through each player 
        """ This for loop has a complexity of O(P) """
        for player in self.get_players():
            current_balance = player.get_balance()
            
            # first check if the player can purchase food
            if (food_price < current_balance - EPSILON):
                # if the player has hunger bars, check which cave is the most worth to go to
                if len(options_list)>0:
                    cave, quantity, earning, _ = options_list[len(options_list)-1]
                else:
                    # this means there are no options left (the caves have no more material)
                    earning=0
                    cave=None
                    quantity=None
                
                # check that the earning is more than 0
                if ((earning - food_price)> EPSILON):
                    # update the balance for the player
                    current_balance -= food_price
                    current_balance += earning

                    # append the needed info to the return lists
                    food_list.append(food)
                    balance_list.append(current_balance)

                    tuple = (cave, quantity)
                    cave_list.append(tuple)

                    # remove this option from the list
                    """ This is O(1) since always deleting the last index only """
                    options_list.delete_at_index(len(options_list)-1)

                else:
                    # this means that it was not worth to buy the food
                    food_list.append(None)
                    balance_list.append(current_balance)
                    cave_list.append(None)

            else:
                # this means that the player could not afford the food
                food_list.append(None)
                balance_list.append(current_balance)
                cave_list.append(None)


        return (food_list, balance_list, cave_list)
        
    def worked_example(self):
        """
            This function is written as a way to show a written and worked example of how the select_for_player function works.
            Please fully read the docstrings below for a written example on the expected output given this set of food, materials, traders, and caves.
            Once you have read the explanation, please RUN this file to see the output based on calling the actual function
        """


        """
            Defining example food offered to the players for the day:
                -   Food("Cooked Chicken Cuts", 424, 19),
            Defining example materials:
                -   gold = Material("Gold Nugget", 27.24)
                -   netherite = Material("Netherite Ingot", 20.95)
                -   fishing_rod = Material("Fishing Rod", 26.93)
                -   ender_pearl = Material("Ender Pearl", 13.91)
                -   prismarine = Material("Prismarine Crystal", 11.48)

            Defining example Players:
                -   Johnny
                    - starting emerald balance: 20
                -   Papa
                    - starting emerald balance: 12
                
            Defining example caves:
                -   Boulderfall Cave
                        -   Conatains: Prismarine Crystal, Quantity: 10 
                -   Castle Karstaag Ruins
                        -   Conatains: Netherite Ingot, Quantity: 4 
                -   Glacial Cave
                        -   Conatains: Gold Nugget, Quantity: 47
                        
            Defining example traders:
                - Waldo Morgan
                    - Trade Item:
                        -Item: Fishing Rod, Selling Price: 7.44
                - Orson Hoover
                    - Trade Item:
                        -Item: Gold Nugget, Selling Price: 7.70
                - Ruby Goodman
                    - Trade Item:
                        -Item: Netherite Ingot, Selling Price: 9.78
                - Mable Hodge
                    - Trade Item:
                        -Item: Gold Nugget, Selling Price: 5.40

            Once the select_for_player is called, the following will occur:
             
                -> _get_best_mining_choice(food) is called:
                    -> this will obtain a trading_list which contains a key:value pair of Material:Selling Price
                    -> it will set the hunger bars of the input food as the hunger bars available, in this case it is 424 hunger bars
                    -> it will iterate through the caves one by one
                    -> for Boulderfall Cave, the material it contains is not being bought by traders, so the code will skip it
                    -> for Castle Karstaag Ruins, the material is being traded so the following is checked:
                        -> the code will check if the player can mine all the Netherite Ingot from the cave. 
                        -> in this case, the player can mine 20.24 (calculated using 424/20.95) Netherite Ingot. Since that is more than what is in the cave, the earninings are calculated for 
                           mining this 4 units from the cave, which is 39.12 emeralds (4*9.78 trading price)
                        -> then, following mining option tuple is added to the sorted list: (Castle Karstaag Ruins, 4, 39.12, 0)
                    -> next, for Glacial Cave, the material is being traded so the following is checked:
                        -> the code will calculate the quantity the player can mine of the Gold Nugget, which is 15.57 units (calculated using 424/27.24)
                        -> the code will check if the player can mine all the Gold Nugget from the cave. 
                        -> the player cannot, so the code will check how many times the player can mine 15.57 units from the cave, which is 3 times
                        -> the earning for this quantity is calculated, which is 119.889 emeralds calculated using (15.57*7.7 trading price)
                        -> following mining option tuple is added to the sorted list: (Glacial Cave, 15.57, 119.889, 3)
                    -> this sorted list of mining option tuples is returned
                    -> the list would have the following items in that order:
                        [(Castle Karstaag Ruins, 4, 39.12, 0), (Glacial Cave, 15.57, 119.889, 3)] **it is in reverse order so that when an item is deleted, it is O(1) complexity

                -> the code will now iterate through each player
                    -> for Johnny, the code will check if he has enough emeralds to purchase the food, Cooked Chicken Cuts for 19 emeralds. Johnny has 20 emeralds so he can purchase it.
                    -> so, Johnny will choose the first option in the options_list obtained earlier. 
                    -> if the profit for this option is more than 0 (i.e. the earning is more than the price of the food), then the balance of Johnny is updated and appended to the return list
                    -> in this case, the earnings is 119.889 and the food price is 19, so the profit is more than 0
                    -> this option is "deleted" from the list which will result in the following list:
                        [(Castle Karstaag Ruins, 4, 39.12, 0), (Glacial Cave, 15.57, 119.889, 2)] **thus, another 2 players can mine the same amount from the same cave as Johnny
                    -> -> thus, the cave list has the following tuple appended (Glacial Cave, 15.57), the value 120.889 is appended to the balance list, and Cooked Chicken Cuts is appended to the food list
                    -> next, the code will check if Papa has enough emeralds to buy the food, however Papa only has 12 emeralds. 
                    -> so, the code will just append None to the cave list and the food list
                    -> the 12 emeralds current balance is appended to the list of balances 
                
                -> finally, the code will return the tuple of all 3 lists (food_list, balance_list, cave_list)
                    -> food_list in this case will be [Cooked Chicken Cuts, None]
                    -> balance_list in this case will be [120.889, 12]
                    -> cave_list in this case will be [(Glacial Cave, 15.57), None]
        """
        # create the food object
        food = Food("Cooked Chicken Cuts", 424, 19)
        food_list = [food]

        # create the materials needed and make a list of it
        gold = Material("Gold Nugget", 27.24)
        netherite = Material("Netherite Ingot", 20.95)
        fishing_rod = Material("Fishing Rod", 26.93)
        ender_pearl = Material("Ender Pearl", 13.91)
        prismarine = Material("Prismarine Crystal", 11.48)
        material_list = [gold, netherite, fishing_rod, ender_pearl, prismarine]

        # make a list of the player names and the emerald balances 
        player_names = ["Johnny", "Papa"]
        player_emeralds = [20, 12]

        # create a list of the caves 
        boulderfall = Cave("Boulderfall cave", prismarine, 10)
        castle_karstaag = Cave("Castle Karstaag Ruins", netherite, 4)
        glacial = Cave("Glacial Cave", gold, 47)
        cave_list = [boulderfall, castle_karstaag, glacial]

        # create the traders and create a list
        waldo = RandomTrader("Waldo Morgan")
        waldo.active_deal = (fishing_rod, 7.44)

        orson = RandomTrader("Orson Hoover")
        orson.active_deal = (gold, 7.7)

        ruby = RandomTrader("Ruby Goodman")
        ruby.active_deal = (netherite, 9.78)

        mable = RandomTrader("Mable Hodge")
        mable.active_deal = (gold, 5.40)
        trader_list = [waldo, orson, ruby, mable]

        self.initialise_with_data(material_list, cave_list, trader_list, player_names, player_emeralds)

        # check that the trader_list only gets the maximum selling value for a material
        # in this case, check that the gold price is 7.7
        print("===============================================")
        print("Checking that the trader_list only contains maximum selling price")
        print("Price of Gold Nugget in the list is (options are 7.7 by Orson or 5.40 by Mable): ", self._get_trading_list().get_custom(gold))

        # get the list of sorted options and check that it is the same as the written example
        options_list = self._get_best_mining_choice(food)
        # it should be as follows:
        # [(Castle Karstaag Ruins, 4, 39.12, 0), (Glacial Cave, 15.57, 119.889, 3)]
        print("===============================================")
        print("Checking that both the mining options are appended to the list in the correct order: ")
        string = "["
        for i in range(len(options_list)):
            string += "("
            item = options_list[i]
            cave = item[0]
            quantity = item[1]
            earning = item[2]
            num = item[3]
            string+=cave.get_name()
            string+=", "
            string+=str(quantity)
            string+=", "
            string+=str(earning)
            string+=", "
            string+=str(num)
            if i ==len(options_list)-1:
                string+=")"
            else:
                string+="), "
        string+="]"
        print(string)

        # now run the select_for_player function and check that the final result is the same as dicussed
        tuple = self.select_for_players(food)
        food_list = tuple[0]
        balance_list = tuple[1]
        cave_list = tuple[2]

        print("===============================================")
        print("The final output after running the select function:")
        food_str = "["
        balance_str="["
        cave_str="["
        for i in range(len(food_list)):
            if food_list[i]==None:
                food_str+="None"
            else:
                food_str += food_list[i].name
            balance_str += str(balance_list[i])
            if cave_list[i]==None:
                cave_str+="None"
            else:
                cave_str += "(" + cave_list[i][0].get_name() + ", " + str(cave_list[i][1]) + ")"
            
            if i==len(food_list)-1:
                pass
            else:
                food_str+=", "
                balance_str+=", "
                cave_str+=", "

        food_str+="]"
        balance_str+="]"
        cave_str+="]"

        # print out all the final lists returned by the function
        # the expected output is given in the explanation above
        # *** please note that the discrepancy in the float numbers is because all calculations in the explanation was done by rounding off the numbers to 2 d.p.
        #     for simplicity which is not done in the actual function
        print("The food list expected== [Cooked Chicken Cuts, None]")
        print("The ACTUAL food list returned == ", food_str)
        print("The food list expected== [120.889, 12]")
        print("The ACTUAL balance list returned == ", balance_str)
        print("The food list expected== [(Glacial Cave, 15.57), None]")
        print("The ACTUAL cave list returned == ", cave_str)

    def verify_output_and_update_quantities(self, foods: list[Food | None], balances: list[float], caves: list[tuple[Cave, float]|None]) -> None:
        """
            Verifies that all the inputs are logical, the balances are correct, and the quantities left in the cave are sufficient for the players
            to mine the materials as inputted

                params: 
                    foods -> the foods purchased by each player
                    balances -> the balances of emeralds in each player after buying food, mining and selling the material
                    caves -> a list of tuples where each tuple contains the Cave visited and the quantity of material mined by each player

                complexity:
                    best: O(1) -> where there are no food, caves or players to check 
                    O(T + P + C) -> where T is the size of list of traders and C is the size of list of caves, when there are non-zero number of food, players and caves to check
        """
            # 1. Check for basic logic checks 

        # check that the length of all the input lists are the same
        if not (len(foods)==len(balances)==len(caves)==len(self.get_players())):
            raise ValueError("The input lists must be the same length")
        
        # check that all the balances are a non-negative float
        for balance in balances:
            if type(balance) not in [float, int] or(balance < 0-EPSILON):
                raise ValueError("The balance must be a non-negative float")

        # check that if the food is none, then the list of caves must also be none
        for food, cave in zip(foods, caves):
            if food==None and cave!=None:
                raise ValueError("The player cannot visit caves without eating any food")

        # check that the food can be purchased and the player has funds to purchase it
        for player, food in zip(self.get_players(), foods):
            if food!=None and (food.get_price()- EPSILON > player.get_balance() ):
                raise ValueError("This food cannot be purchased")   

        


            # 2. Check that all the caves have at least the amount required, and there is a trader who wants to buy the material

        # create a dictionary of the traders and the buying price 
        """ O(T) complexity to get the list of all traders """
        trading_list=self._get_trading_list()

        """ O(C) complexity to get the list of all caves """
        cave_list=self._get_cave_materials()
        trader_check=True
        quantity_check=True

        """ O(P) complexity since it iterates through for all the caves that the players visit (1 cave per player) """
        # go through all the caves and check that there are enough materials 
        for items in caves:
            if items!=None:
                cave = items[0]
                quantity = items[1]
                material = cave.get_material()

                # update the materials taken from this cave
                new_quantity = cave_list.get_custom(cave) - quantity
                cave_list.insert_custom(cave, new_quantity)

                # next check if there is a trader willing to trade this material
                try: 
                    trading_list.get_custom(material)
                except:
                    trader_check=False

        """ O(C) complexity since it iterates through all the caves """
        for cave in cave_list.keys():
            if cave_list[cave] < 0 - EPSILON:
                quantity_check=False

        if not(quantity_check and trader_check):
            raise ValueError("The quantity of materials in the cave is less than required or there are no traders to trade this material")

            
            # 3. Now check that after carrying out all the purchasing and mining, check the final balance is the same as the input

        # first check that the player has enough hunger bars and the final balance is the same
        """ O(P) complexity since all the lists have the same length as the player list """
        for player, food, balance, cave_dig in zip(self.get_players(), foods, balances, caves):
            if food!=None and cave_dig!=None:
                cave = cave_dig[0]
                material = cave.get_material()
                quantity = cave_dig[1]

                # first check the hunger bars needed is less than food bars
                if (food.get_hunger_bars() < (material.get_mining_rate()*quantity) - EPSILON):
                    raise ValueError("The hunger bars required to mine this material is more than available")

                # then check the balance
                current_balance = player.get_balance()
                current_balance -= food.get_price()
                current_balance += (quantity*trading_list.get_custom(material))

                # now check that the final balance is the same
                if (abs(current_balance - balance) > EPSILON ):
                    raise ValueError("The final balance is not the same as the input")

                    # 4. Now that all the checks have passed, update the balance of the player, and update the quantities in each cave
                cave.remove_quantity(quantity)
            
            # set the player balance regardles of whether or not they bought food
            player.set_balance(balance)



if __name__ == "__main__":

    # r = RandomGen.seed # Change this to set a fixed seed.
    # RandomGen.set_seed(r)
    # print(r)

    # g = MultiplayerGame()
    # g.initialise_game()

    # g.simulate_day()
    # g.finish_day()

    # g.simulate_day()
    # g.finish_day()

    """
        This will run the code to show the worked example of how the select_for_player function workes
    """
    g = MultiplayerGame()
    g.worked_example()

