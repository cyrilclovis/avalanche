from __future__ import annotations
import random
from typing import List

from src.enums.colors import Colors

class Node:

    def __init__(self):
        self.color = random.choice(list(Colors))

    def set_color(self, color: Colors):
        self.color = color

    def get_color(self) -> Colors:
        return self.color

    def color_is_null(self) -> bool:
        """Vérifie si la couleur du noeud est NULL."""
        return self.color == Colors.NULL

    def on_query(self, otherNode) -> Colors:
        """On renvoie la couleur du noeud actuelle"""
        if (self.color_is_null()):
            self.set_color(otherNode.color)
        return self.color
    
    def query_all_nodes(self, nodes) -> List[Colors]:
        """
        Utilise la fonction query sur l'ensemble des noeuds de la liste !
        """
        colors = [node.on_query(self) for node in nodes]
        #print(f"Couleurs obtenues après interrogation : {colors}")
        return colors

    def sample(self, nodesManager: 'NodesManager', k: int) -> List[Node]:
        """
        Retourne un échantillon de k noeuds parmi le tableau donné.
        :param nodes: Liste des noeuds disponibles.
        :param k: Nombre de noeuds à échantillonner.
        :return: Liste des noeuds échantillonnés.
        """
        filtered_nodes = [node for node in nodesManager.nodes if node != self]

        if k > len(filtered_nodes):
            raise ValueError("k ne peut pas être supérieur au nombre de noeuds disponibles.")
        sampled_nodes = random.sample(filtered_nodes, k)
        #print(f"Nœuds échantillonnés ({k} sur {len(filtered_nodes)}) : {[node.get_color() for node in sampled_nodes]}")
        return sampled_nodes    

    def count(self, nodesColor: List[Colors], selectedColor: Colors) -> int:
        counter = 0
        for color in nodesColor:
            if color == selectedColor:
                counter += 1
        return counter
    
    
    def snowflakeLoop(self, nodesManager: 'NodesManager', k: int, alpha: int, beta: int, iter_max: int = 10):
        # Initialisation
        color = random.choice(list(Colors))
        cpt = 0
        undecided = True
        iterations = 0

        # Déroulement de l'algorithme
        while (undecided):
            if color == Colors.NULL:
                continue
            K = self.sample(nodesManager, k)
            P = self.query_all_nodes(K)

            colorPrime = [Colors.RED, Colors.BLUE]
            for currentPrimeColor in colorPrime:
                if self.count(P, currentPrimeColor) >= alpha * k:
                    if currentPrimeColor != color:
                        color = currentPrimeColor
                        cpt = 0
                    else:
                        cpt += 1
                        if cpt > beta:
                            self.set_color(color)
                            undecided = False

                        iterations += 1
        
            if iterations >= iter_max:
                print(f"Le noeud {self} a atteint le nombre d'itération maximal {iter_max} ")
                undecided = False


    def snowballLoop(self, nodesManager: 'NodesManager', k: int, alpha: int, beta: int):
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
            K = self.sample(nodesManager, k)
            P = self.query_all_nodes(K)

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
                            self.set_color(color)
