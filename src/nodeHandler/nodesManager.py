import random
from typing import List

from src.enums.colors import Colors
from src.nodeHandler import Node

class NodesManager:
    def __init__(self, NombreNoeuds: int):
        """
        Initialise un tableau de noeuds avec une couleur aléatoire.
        :param NombreNoeuds: Nombre total de noeuds à créer.
        """
        if NombreNoeuds <= 0:
            raise ValueError("Le nombre de noeuds doit être supérieur à 0.")
        self.nodes = [Node() for _ in range(NombreNoeuds)]

    def count(self, nodesColor: List[Colors], selectedColor: Colors) -> int:
        counter = 0
        for color in nodesColor:
            if color == selectedColor:
                counter += 1
        return counter


    def snowflakeLoop(self, u: Node, k: int, alpha: int, beta: int):
        # Initialisation
        color = random.choice(list(Colors))
        cpt = 0
        undecided = True

        # Déroulement de l'algorithme
        while (undecided):
            if color == Colors.NULL:
                continue
            K = u.sample(self, k)
            P = u.query_all_nodes(K)

            colorPrime = [Colors.RED, Colors.BLUE]
            for currentPrimeColor in colorPrime:
                if self.count(P, currentPrimeColor) >= alpha * k:
                    if currentPrimeColor != color:
                        color = currentPrimeColor
                        cpt = 0
                    else:
                        cpt += 1
                        if cpt > beta:
                            u.set_color(color)
                            undecided = False

    def snowballLoop(self, u: Node, k: int, alpha: int, beta: int):
        # Initialisation
        color = random.choice(list(Colors))
        lastColor = random.choice(list(Colors))
        cpt = 0
        d = {
            Colors.RED: 0,
            Colors.BLUE: 0,
        }

        undecided = False

        # Déroulement de l'algorithme
        while (undecided):
            if color == Colors.NULL:
                continue
            K = u.sample(self, k)
            P = u.query_all_nodes(K)

            colorPrime = [Colors.RED, Colors.BLUE]
            for currentPrimeColor in colorPrime:
                if self.count(P, currentPrimeColor) >= alpha * k:
                    d[currentPrimeColor] += 1

                    if d[currentPrimeColor] > d[color]:
                        color = currentPrimeColor
                        
                    if currentPrimeColor != lastColor:
                        lastColor = currentPrimeColor
                        cpt = 0
                    else:
                        cpt += 1
                        if cpt > beta:
                            u.set_color(color)