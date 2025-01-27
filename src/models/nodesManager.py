import random

from src.models import Node
from src.enums.algoChoices import AlgoChoices

class NodesManager:
    def __init__(self, algo:str, nombreNoeuds: int, k: int, alpha: float, beta: int, bizantinPercent: float):
        """
        Initialise un tableau de noeuds avec une couleur aléatoire.
        :param NombreNoeuds: Nombre total de noeuds à créer.
        """
        if nombreNoeuds <= 0:
            raise ValueError("Le nombre de noeuds doit être supérieur à 0.")
        self.nodes = self.create_nodes(nombreNoeuds, bizantinPercent)
        self.K = k
        self.ALPHA = alpha
        self.BETA = beta
        self.set_algo_to_use(algo)


    def create_nodes(self, NombreNoeuds: int, bizantinPercent: float):
        """
        Crée les nœuds avec un pourcentage de nœuds byzantins.
        :param NombreNoeuds: Nombre total de nœuds.
        :param bizantinPercent: Pourcentage de nœuds byzantins.
        :return: Liste de nœuds.
        """
        nodes = []
        num_bizantin_nodes = int(NombreNoeuds * bizantinPercent / 100)
        print(f"Il y a {num_bizantin_nodes} bizantins")

        # Crée les nœuds avec le bon pourcentage de nœuds byzantins
        for i in range(NombreNoeuds):
            is_bizantin = i < num_bizantin_nodes  # Les premiers `num_bizantin_nodes` seront byzantins
            nodes.append(Node(is_bizantin=is_bizantin))
        
        random.shuffle(nodes)  # Mélange les nœuds pour une distribution aléatoire
        return nodes


    def set_algo_to_use(self, algo: str):
        """
        Définit l'algorithme à utiliser pour les nœuds.
        :param algo: Nom de l'algorithme (par exemple "snowflakeLoop" ou "snowballLoop").
        """
        if algo not in [choice.value for choice in AlgoChoices]:
            raise ValueError(f"Algorithme non valide : {algo}. Les choix possibles sont : {[choice.value for choice in AlgoChoices]}.")
        
        self.algo_name = algo


    def launch_algorithm(self):
        """
        Lance l'algorithme configuré sur tous les nœuds.
        """
        for _ in range (50):
            for node in self.nodes:
                node.sequential_snowflake_iteration(nodesManager=self, k=self.K, alpha=self.ALPHA, beta=self.BETA)
