import random
from typing import List

from src.enums.colors import Colors
from src.models.node import Node


class BreakdownNode(Node):
    # Le noeud en panne ne fait rien !

    def __init__(self):
        super().__init__(Colors.BLACK)

    # *************** Gestion des requetes
    def on_query(self, otherNode) -> Colors:
        """Le noeud ne réagit pas"""
        pass

    def query_all_nodes(self, nodes) -> List[Colors]:
        """Le noeud ne réagit pas"""
        pass
    
    # *************** Mise en place des algorithmes snowflakeLoop & snowballLoop

    def sequential_snowflake_iteration(self, nodesManager: 'NodesManager', k: int, alpha: int, beta: int):
        """Le noeud ne réagit pas, pour autant il ajoute sa couleur à la liste à chaque itération !"""
        self.record_color()
        pass


    def sequential_snowball_iteration(self, nodesManager: 'NodesManager', k: int, alpha: float, beta: int):
        """Le noeud ne réagit pas, pour autant il ajoute sa couleur à la liste à chaque itération !"""
        self.record_color()
        pass