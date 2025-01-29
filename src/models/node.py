from __future__ import annotations
import random
from typing import List

from src.enums.colors import Colors

class Node:

    def __init__(self, color=None):
        self.color = color if color else random.choice([Colors.BLUE, Colors.RED, Colors.NULL])
        self.color_observers = []
        self.color_history = [self.color]
        ##### Attributs pour le déroulement des algorithmes
        # --- Pour snowflake
        self.cpt = 0
        self.undecided = True
        self.iterations = 0
        # --- Pour snowball
        self.lastColor = self.color
        self.d = {color: 0 for color in (Colors.RED, Colors.BLUE)}

    # *************** Setters & getters

    def set_color(self, color: Colors):
        self.color = color
        self.notify_color_observers()

    def get_color(self) -> Colors:
        return self.color

    def color_is_null(self) -> bool:
        """Vérifie si la couleur du noeud est NULL."""
        return self.color == Colors.NULL
    
    def record_color(self):
        """Enregistre la couleur du noeud dans son historique."""
        self.color_history.append(self.get_color())
    
    def get_random_color(self, noneAllowed: bool = True):
        """Renvoie une couleur aléatoire"""
        return random.choice([Colors.BLUE, Colors.RED])

    # *************** Observers
    def add_color_observer(self, observer: 'NodeView'):
        """Ajoute une vue à la liste des observateurs."""
        self.color_observers.append(observer)

    def notify_color_observers(self):
        """Notifie toutes les vues de la mise à jour de la couleur."""
        for observer in self.color_observers:
            observer.update_color(self.color)


    # *************** Gestion des requetes
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

    # *************** Mise en place des algorithmes snowflakeLoop & snowballLoop

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
    
    
    def sequential_snowflake_iteration(self, nodesManager: 'NodesManager', k: int, alpha: int, beta: int):
        self.record_color()

        if not self.undecided: # J'ai déjà choisi
            return

        if self.color == Colors.NULL:
            return

        K = self.sample(nodesManager, k)
        P = self.query_all_nodes(K)

        colorPrime = [Colors.RED, Colors.BLUE] # Dans mon code, le bizantin doit toujours renvoyer violet, dois-je l'ajouter ici ?
        for currentPrimeColor in colorPrime:
            if self.count(P, currentPrimeColor) >= alpha * k:
                if currentPrimeColor != self.get_color():
                    self.set_color(currentPrimeColor)
                    self.cpt = 0
                else:
                    self.cpt += 1
                    if self.cpt > beta:
                        self.undecided = False


    def sequential_snowball_iteration(self, nodesManager: 'NodesManager', k: int, alpha: float, beta: int):
        self.record_color()

        if not self.undecided: # J'ai déjà choisi
            return

        if self.color == Colors.NULL:
            return
    
        K = self.sample(nodesManager, k)
        P = self.query_all_nodes(K)

        colorPrime = [Colors.RED, Colors.BLUE]
        for currentPrimeColor in colorPrime:
            if self.count(P, currentPrimeColor) >= alpha * k:
                self.d[currentPrimeColor] += 1

                if self.d[currentPrimeColor] > self.d[self.get_color()]:
                    self.set_color(currentPrimeColor)
                    
                if currentPrimeColor != self.lastColor:
                    self.lastColor = currentPrimeColor
                    cpt = 0
                else:
                    cpt += 1
                    if cpt > beta:
                        self.undecided = False

