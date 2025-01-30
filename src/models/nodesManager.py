import random

from src.models import Node
from src.models.bizantinNode import ByzantineNode

class NodesManager:
    def __init__(self, algo:str,  m: int, nombreNoeuds: int, k: int, alpha: float, beta: int, bizantinPercent: float, breakdownPercent: float):
        """
        Initialise un tableau de noeuds avec une couleur aléatoire.
        :param NombreNoeuds: Nombre total de noeuds à créer.
        """
        if nombreNoeuds <= 0:
            raise ValueError("Le nombre de noeuds doit être supérieur à 0.")
        self.nodes = self.create_nodes(algo, nombreNoeuds, bizantinPercent)
        self.M = m
        self.K = k
        self.ALPHA = alpha
        self.BETA = beta
        self.BREAKDOWN_PERCENT = breakdownPercent/100

        self.schedule_breakdowns()

    def create_nodes(self, algo:str, nombreNoeuds: int, bizantinPercent: float):
        """
        Crée les nœuds avec un pourcentage de nœuds byzantins et de pannes.
        
        :param algo: Nom de l'algorithme à utiliser
        :param NombreNoeuds: Nombre total de nœuds.
        :param bizantinPercent: Pourcentage de nœuds byzantins.
        :return: Liste de nœuds.
        """
        nodes = []
        num_bizantin_nodes = int(nombreNoeuds * bizantinPercent / 100)

        for i in range(nombreNoeuds):
            if i < num_bizantin_nodes:
                nodes.append(ByzantineNode())  # Création d'un nœud byzantin
            else:
                nodes.append(Node())  # Création d'un nœud normal
            nodes[-1].set_current_algorithm(algo)
        
        random.shuffle(nodes)  # Mélange des nœuds pour une distribution aléatoire
        return nodes


    def schedule_breakdowns(self):
        """
        Planifie les pannes de sorte que le bon pourcentage de noeuds tombe en panne d'ici la fin des M itérations.
        """
        num_breakdowns = int(len(self.nodes) * self.BREAKDOWN_PERCENT)
        breakdown_nodes = random.sample(self.nodes, num_breakdowns)
        
        # Générer des moments où chaque nœud tombera en panne, répartis sur M itérations
        self.breakdown_schedule = {}
        breakdown_times = random.choices(range(1, self.M + 1), k=num_breakdowns)

        for node, t in zip(breakdown_nodes, breakdown_times):
            self.breakdown_schedule[node] = t


    def launch_algorithm(self):
        """
        Lance l'algorithme en répartissant uniformément les pannes sur toutes les itérations. L'utilisateur a donc intéret à estimer correctement le nombre d'itératioons !
        """
        for iteration in range(1, self.M + 1):
            for node in self.nodes:
                if node in self.breakdown_schedule and self.breakdown_schedule[node] == iteration:
                    self.nodes[self.nodes.index(node)].break_node_down()
                node.execute_one_iteration(nodesManager=self, k=self.K, alpha=self.ALPHA, beta=self.BETA)

