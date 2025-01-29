import tkinter as tk

from src.models.nodesManager import NodesManager
from src.views.form import Form
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


racine = tk.Tk()
Form(racine)
racine.mainloop()
