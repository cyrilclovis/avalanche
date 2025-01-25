from src.models import Node

class NodesManager:
    def __init__(self, NombreNoeuds: int):
        """
        Initialise un tableau de noeuds avec une couleur aléatoire.
        :param NombreNoeuds: Nombre total de noeuds à créer.
        """
        if NombreNoeuds <= 0:
            raise ValueError("Le nombre de noeuds doit être supérieur à 0.")
        self.nodes = [Node() for _ in range(NombreNoeuds)]

    
    def lauch_algorithm(self, k: int, alpha: int, beta: int):
        for node in self.nodes:
            node.snowflakeLoop(self, k, alpha, beta)
