from src.models import Node

class NodesManager:
    def __init__(self, NombreNoeuds: int, k: int, alpha: float, beta: int):
        """
        Initialise un tableau de noeuds avec une couleur aléatoire.
        :param NombreNoeuds: Nombre total de noeuds à créer.
        """
        if NombreNoeuds <= 0:
            raise ValueError("Le nombre de noeuds doit être supérieur à 0.")
        self.nodes = [Node() for _ in range(NombreNoeuds)]
        self.K = k
        self.ALPHA = alpha
        self.BETA = beta

    
    def lauch_algorithm(self):
        for node in self.nodes:
            node.snowflakeLoop(self, k=self.K, alpha=self.ALPHA, beta=self.BETA)
