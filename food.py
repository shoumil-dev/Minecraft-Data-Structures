from __future__ import annotations

from random_gen import RandomGen

"""
Modified by: Avinash Rvan (32717792)

"""

# List of food names from https://github.com/vectorwing/FarmersDelight/tree/1.18.2/src/main/resources/assets/farmersdelight/textures/item
FOOD_NAMES = [
    "Apple Cider",
    "Apple Pie",
    "Apple Pie Slice",
    "Bacon",
    "Bacon And Eggs",
    "Bacon Sandwich",
    "Baked Cod Stew",
    "Barbecue Stick",
    "Beef Patty",
    "Beef Stew",
    "Cabbage",
    "Cabbage Leaf",
    "Cabbage Rolls",
    "Cabbage Seeds",
    "Cake Slice",
    "Chicken Cuts",
    "Chicken Sandwich",
    "Chicken Soup",
    "Chocolate Pie",
    "Chocolate Pie Slice",
    "Cod Slice",
    "Cooked Bacon",
    "Cooked Chicken Cuts",
    "Cooked Cod Slice",
    "Cooked Mutton Chops",
    "Cooked Rice",
    "Cooked Salmon Slice",
    "Dog Food",
    "Dumplings",
    "Egg Sandwich",
    "Fish Stew",
    "Fried Egg",
    "Fried Rice",
    "Fruit Salad",
    "Grilled Salmon",
    "Ham",
    "Hamburger",
    "Honey Cookie",
    "Honey Glazed Ham",
    "Honey Glazed Ham Block",
    "Horse Feed",
    "Hot Cocoa",
    "Melon Juice",
    "Melon Popsicle",
    "Milk Bottle",
    "Minced Beef",
    "Mixed Salad",
    "Mutton Chops",
    "Mutton Wrap",
    "Nether Salad",
    "Noodle Soup",
    "Onion",
    "Pasta With Meatballs",
    "Pasta With Mutton Chop",
    "Pie Crust",
    "Pumpkin Pie Slice",
    "Pumpkin Slice",
    "Pumpkin Soup",
    "Ratatouille",
    "Raw Pasta",
    "Rice",
    "Rice Panicle",
    "Roast Chicken",
    "Roast Chicken Block",
    "Roasted Mutton Chops",
    "Rotten Tomato",
    "Salmon Slice",
    "Shepherds Pie",
    "Shepherds Pie Block",
    "Smoked Ham",
    "Squid Ink Pasta",
    "Steak And Potatoes",
    "Stuffed Potato",
    "Stuffed Pumpkin",
    "Stuffed Pumpkin Block",
    "Sweet Berry Cheesecake",
    "Sweet Berry Cheesecake Slice",
    "Sweet Berry Cookie",
    "Tomato",
    "Tomato Sauce",
    "Tomato Seeds",
    "Vegetable Noodles",
    "Vegetable Soup",
]

RANDOM_PRICE_MIN = 1
RANDOM_PRICE_MAX = 50
RANDOM_HUNGER_MIN = 1
RANDOM_HUNGER_MAX = 100

class Food:
    """
    This class contains information for the food objects in the game

        attributes:
            name: the name of the food
            hunger_bars -  An integer stating how many hunger bars this food provides
            price - An integer containing the buying price of this food
    
    """
    def __init__(self, name: str, hunger_bars: int, price: int) -> None:
        """
            Initialises a Food Object

            @Param: name - A string containing Cave name
            @Param: hunger_bars -  An integer stating how many hunger bars this food provides
            @Param: price - An integer containing the buying price of this food
            @Return: None
        """
        self.name = name
        self.hunger_bars = hunger_bars
        self.price = price
    
    def __str__(self) -> str:
        """
            Creates a string to display the food item, showing the name of the food, price, and 
            the hunger bars it provides

            @Return: a descriptive string
        
        """
        print_string = "[{}: {}💰 for {}🍗]".format(self.name, self.price, self.hunger_bars)
        return print_string

    def get_price(self) -> int:
        """
            Retruns the price of the food
        """
        return self.price

    def get_hunger_bars(self) -> float:
        """
            returns the number of hunger bars
        """
        return self.hunger_bars

    @classmethod
    def random_food(cls) -> Food:
        """
            Creates an instance of a random Food with random name, price and hunger bars

            @Return: A random instance of Food
        """
        random_food= RandomGen.random_choice(FOOD_NAMES)
        random_price= RandomGen.randint(RANDOM_PRICE_MIN, RANDOM_PRICE_MAX)
        random_hunger_bars = RandomGen.randint(RANDOM_HUNGER_MIN, RANDOM_HUNGER_MAX)
        return Food(random_food, random_hunger_bars, random_price)

if __name__ == "__main__":
    print(Food.random_food())
