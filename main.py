import random
from src.nodeHandler.nodesManager import NodesManager
from src.enums.colors import Colors

def afficher_distribution_couleurs(legend: str, nodes_manager: NodesManager):
    """
    Affiche la distribution des couleurs des nœuds gérés par un NodesManager.
    :param nodes_manager: Instance de NodesManager contenant les nœuds.
    """
    final_colors = [node.get_color() for node in nodes_manager.nodes]
    rouge_count = final_colors.count(Colors.RED)
    bleu_count = final_colors.count(Colors.BLUE)
    none_count = final_colors.count(Colors.NULL)

    # Affichage de la distribution finale des couleurs
    print(legend)
    print(f"Rouge: {rouge_count}")
    print(f"Bleu: {bleu_count}")
    print(f"Indéterminé : {none_count}")

# Paramètres principaux
N = 600  # Nombre total de nœuds
k = 3   # Taille de l'échantillon
alpha = 0.8
beta = 5  # Ajout d'un paramètre beta pour le seuil de stabilisation

# Initialisation du gestionnaire de nœuds
nodes_manager = NodesManager(N)

afficher_distribution_couleurs("Au début", nodes_manager)



afficher_distribution_couleurs("A la fin", nodes_manager)
