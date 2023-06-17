from random_gen import RandomGen

# Material names taken from https://minecraft-archive.fandom.com/wiki/Items
RANDOM_MATERIAL_NAMES = [
    "Arrow",
    "Axe",
    "Bow",
    "Bucket",
    "Carrot on a Stick",
    "Clock",
    "Compass",
    "Crossbow",
    "Exploration Map",
    "Fire Charge",
    "Fishing Rod",
    "Flint and Steel",
    "Glass Bottle",
    "Dragon's Breath",
    "Hoe",
    "Lead",
    "Map",
    "Pickaxe",
    "Shears",
    "Shield",
    "Shovel",
    "Sword",
    "Saddle",
    "Spyglass",
    "Totem of Undying",
    "Blaze Powder",
    "Blaze Rod",
    "Bone",
    "Bone meal",
    "Book",
    "Book and Quill",
    "Enchanted Book",
    "Bowl",
    "Brick",
    "Clay",
    "Coal",
    "Charcoal",
    "Cocoa Beans",
    "Copper Ingot",
    "Diamond",
    "Dyes",
    "Ender Pearl",
    "Eye of Ender",
    "Feather",
    "Spider Eye",
    "Fermented Spider Eye",
    "Flint",
    "Ghast Tear",
    "Glistering Melon",
    "Glowstone Dust",
    "Gold Ingot",
    "Gold Nugget",
    "Gunpowder",
    "Ink Sac",
    "Iron Ingot",
    "Iron Nugget",
    "Lapis Lazuli",
    "Leather",
    "Magma Cream",
    "Music Disc",
    "Name Tag",
    "Nether Bricks",
    "Paper",
    "Popped Chorus Fruit",
    "Prismarine Crystal",
    "Prismarine Shard",
    "Rabbit's Foot",
    "Rabbit Hide",
    "Redstone",
    "Seeds",
    "Beetroot Seeds",
    "Nether Wart Seeds",
    "Pumpkin Seeds",
    "Wheat Seeds",
    "Slimeball",
    "Snowball",
    "Spawn Egg",
    "Stick",
    "String",
    "Wheat",
    "Netherite Ingot",
]

RANDOM_MINING_RATE_MULTIPLIER = 30

class Material:
    """
        This class contains the methods and attributes needed for the Material class

        attributes:
            name: name of the material
            mining_rate: the number of hunger bars needed to mine 1 unit of this material

    """
    
    def __init__(self, name: str, mining_rate: float) -> None:
        """ Initaliser """
        self.name = name
        self.mining_rate = mining_rate
    
    def __str__(self) -> str:
        """ 
            Creates a descriptive string representation of the Material including the name and 
            mining rate of the Material

                @Returns: a string
        """
        print_string = "[{}: {}🍗/💎]".format(self.name, round(self.mining_rate, 2))
        return print_string

    def get_material_name(self) -> str:
        """
            Getter for the material name

            @Returns: the name of the material as a string
        
        """
        return self.name

    def get_name(self) -> str:
        """
            Getter for the material name

            @Returns: the name of the material as a string
        
        """
        return self.name

    def get_mining_rate(self) -> float:
        """
            Getter for the material mining_rate

            @Returns: the mining_rate of the material as a float
        
        """
        return self.mining_rate

    @classmethod
    def random_material(cls):
        """
            Creates a random instance of the Material with random attributes and returns it.

            @Returns: a random instance of a Material object
        
        """
        random_material = RandomGen.random_choice(RANDOM_MATERIAL_NAMES)
        random_mining_rate = RandomGen.random_float()*RANDOM_MINING_RATE_MULTIPLIER
        return Material(random_material, random_mining_rate)

if __name__ == "__main__":
    print(Material.random_material())
