from __future__ import annotations
import random
from typing import List

from src.enums.colors import Colors

class Node:

    def __init__(self):
        self.color = random.choice(list(Colors))
        self.observers = []

    def set_color(self, color: Colors):
        self.color = color
        self.notify_observers()

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

    def sample(self, nodesManger: 'NodesManager', k: int):
        """
        Retourne un échantillon de k noeuds parmi le tableau donné.
        :param nodes: Liste des noeuds disponibles.
        :param k: Nombre de noeuds à échantillonner.
        :return: Liste des noeuds échantillonnés.
        """
        filtered_nodes = [node for node in nodesManger.nodes if node != self]

        if k > len(filtered_nodes):
            raise ValueError("k ne peut pas être supérieur au nombre de noeuds disponibles.")
        sampled_nodes = random.sample(filtered_nodes, k)
        print(f"Nœuds échantillonnés ({k} sur {len(filtered_nodes)}) : {[node.get_color() for node in sampled_nodes]}")
        return sampled_nodes


    def query_all_nodes(self, nodes) -> List[Colors]:
        """
        Utilise la fonction query sur l'ensemble des noeuds de la liste !
        """
        colors = [node.on_query(self) for node in nodes]
        print(f"Couleurs obtenues après interrogation : {colors}")
        return colors

    # *************** Observers
    def add_observer(self, observer: 'NodeView'):
        """Ajoute une vue à la liste des observateurs."""
        self.observers.append(observer)

    def notify_observers(self):
        """Notifie toutes les vues de la mise à jour de la couleur."""
        for observer in self.observers:
            observer.update_color(self.color)


