from src.models import Node
from src.enums.algoChoices import AlgoChoices

class NodesManager:
    def __init__(self, algo:str, NombreNoeuds: int, k: int, alpha: float, beta: int):
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
        self.set_algo_to_use(algo)


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
        for node in self.nodes:
            if not hasattr(node, self.algo_name):
                raise AttributeError(f"L'algorithme '{self.algo_name}' n'est pas défini dans la classe Node.")
            
            # Appelle dynamiquement la méthode correspondant à l'algorithme
            getattr(node, self.algo_name)(nodesManager=self, k=self.K, alpha=self.ALPHA, beta=self.BETA)
