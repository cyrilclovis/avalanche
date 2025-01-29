import random

from src.models import Node
from src.models.bizantinNode import ByzantineNode
from src.models.breakdownNode import BreakdownNode

class NodesManager:
    def __init__(self, algo:str,  m: int, nombreNoeuds: int, k: int, alpha: float, beta: int, bizantinPercent: float, breakdownPercent: float):
        """
        Initialise un tableau de noeuds avec une couleur aléatoire.
        :param NombreNoeuds: Nombre total de noeuds à créer.
        """
        if nombreNoeuds <= 0:
            raise ValueError("Le nombre de noeuds doit être supérieur à 0.")
        self.nodes = self.create_nodes(algo, nombreNoeuds, bizantinPercent, breakdownPercent)
        self.M = m
        self.K = k
        self.ALPHA = alpha
        self.BETA = beta

    def create_nodes(self, algo:str, nombreNoeuds: int, bizantinPercent: float, breakdownPercent: float):
        """
        Crée les nœuds avec un pourcentage de nœuds byzantins et de pannes.
        
        :param algo: Nom de l'algorithme à utiliser
        :param NombreNoeuds: Nombre total de nœuds.
        :param bizantinPercent: Pourcentage de nœuds byzantins.
        :param breakdownPercent: Pourcentage de nœuds en panne.
        :return: Liste de nœuds.
        """
        nodes = []
        num_bizantin_nodes = int(nombreNoeuds * bizantinPercent / 100)
        num_breakdown_nodes = int(nombreNoeuds * breakdownPercent / 100)

        for i in range(nombreNoeuds):
            if i < num_bizantin_nodes:
                nodes.append(ByzantineNode())  # Création d'un nœud byzantin
            elif i < num_bizantin_nodes + num_breakdown_nodes:
                nodes.append(BreakdownNode())  # Création d'un nœud en panne
            else:
                nodes.append(Node())  # Création d'un nœud normal
            nodes[-1].set_current_algorithm(algo)
        
        random.shuffle(nodes)  # Mélange des nœuds pour une distribution aléatoire
        return nodes



    def launch_algorithm(self):
        """
        Lance l'algorithme configuré sur tous les nœuds.
        """
        for _ in range (self.M):
            for node in self.nodes:
                node.execute_one_iteration(nodesManager=self, k=self.K, alpha=self.ALPHA, beta=self.BETA)

