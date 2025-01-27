from __future__ import annotations
import random
from typing import List

from src.enums.colors import Colors

class Node:

    def __init__(self, is_bizantin=False):
        self.is_bizantin = is_bizantin
        self.color = random.choice([Colors.BLUE, Colors.RED, Colors.NULL]) if not self.is_bizantin else Colors.PURPLE
        self.color_observers = []
        self.color_history = [self.color]

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
        return self.color if not self.is_bizantin else Colors.PURPLE
    
    
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
    
    
    def snowflakeLoop(self, nodesManager: 'NodesManager', k: int, alpha: int, beta: int, iter_max: int = 50):
        # Initialisation
        color = random.choice(list(Colors))
        cpt = 0
        undecided = True
        iterations = 0

        # Déroulement de l'algorithme
        while (undecided or iterations <= iter_max):  # On souhiate aller jusqu'à itermax pour faire le record de la couleur !!!

            self.record_color()
            iterations += 1
            if iterations > iter_max:
                #print(f"Le noeud {self} a atteint le nombre d'itération maximal {iter_max} ")
                return

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


    def snowballLoop(self, nodesManager: 'NodesManager', k: int, alpha: float, beta: int, iter_max: int = 50):
        # Initialisation
        color = random.choice(list(Colors))
        lastColor = random.choice(list(Colors))
        cpt = 0
        d = {
            Colors.RED: 0,
            Colors.BLUE: 0,
            Colors.PURPLE: 0,
        }
        undecided = True
        iterations = 0

        # Déroulement de l'algorithme
        while (undecided or iterations <= iter_max):

            self.record_color()
            iterations += 1
            if iterations > iter_max:
                #print(f"Le noeud {self} a atteint le nombre d'itération maximal {iter_max} ")
                return
        
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
                            undecided = False

