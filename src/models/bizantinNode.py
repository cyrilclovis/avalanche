from src.enums.colors import Colors
from src.models.node import Node
import random

class ByzantineNode(Node):
    # Par défaut, le byzantin renvoie toujours la couleur violette !

    def __init__(self):
        super().__init__(random.choice([Colors.BLUE, Colors.RED]))

    # *************** Gestion des requetes
    def on_query(self, otherNode) -> Colors:
        """Le byzantin renvoie une couleur aléatoire"""
        if (self.color_is_null()):
            self.set_color(otherNode.color)
        return random.choice([Colors.BLUE, Colors.RED])
