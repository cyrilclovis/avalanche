from math import ceil, sqrt
import tkinter as tk
import random as rd
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import Counter

from src.models.nodesManager import NodesManager
from src.views.nodeView import NodeView
from src.config.algoParameters import AlgoParametersManager
from src.enums.colors import Colors

class NodesManagerView(object):
    """Modélise un terrain réprésentant l'évolution des noeuds"""

    SIDE_SIZE = 15
    GRID_ROW_SPAN = 7

    def __init__(self, racine):
        """Génère le terrain"""
        self.racine = racine
        self.racine.title("Terrain de jeu")
        self.update()
        

    def create_field(self):
        """Crée le terrain de base puis y applique les règles"""
        self.canvas = tk.Canvas(self.racine, width=self.WIDTH, height=self.HEIGHT)
        self.init_field()
        self.canvas.grid(column=2, row=0, rowspan=self.GRID_ROW_SPAN)
        # Ajout du bouton
        self.lauch_algo_btn()


    def init_field(self):
        """La fonction crée la grille composé de carré bleus (eau)
        avec une probabilité p et marrons si cette proba n'est pas
        vérifiée.
        """
        cpt = 0
        for i in range(self.SIDE_NUMBER):
            for j in range(self.SIDE_NUMBER):
                if cpt >= self.NODES_NUMBER:
                    return
                NodeView(self.nodesManager.nodes[cpt], self.canvas, i*self.SIDE_SIZE, j*self.SIDE_SIZE, self.SIDE_SIZE)
                cpt += 1


    def update(self, params_tuple=None):
        self.update_model(params_tuple)
        self.update_view()


    def update_model(self, params_tuple=None):
        print(params_tuple)
        if params_tuple:
            ALGO, N, K, ALPHA, BETA, BIZANTINS_PERCENT, PANNES = params_tuple
        else:
            ALGO, N, K, ALPHA, BETA, BIZANTINS_PERCENT, PANNES = AlgoParametersManager().get_all_parameters()
        self.nodesManager = NodesManager(ALGO, N, K, ALPHA, BETA, BIZANTINS_PERCENT)


    def update_view(self):
        """Redessine la vue en effaçant et recréant la grille avec les nouveaux paramètres."""
        # Effacer l'ancien terrain
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.delete("all")
        
        # Réinitialiser les propriétés de la grille
        self.NODES_NUMBER = len(self.nodesManager.nodes)
        self.SIDE_NUMBER  = ceil(sqrt(self.NODES_NUMBER))
        self.WIDTH = self.SIDE_NUMBER * self.SIDE_SIZE
        self.HEIGHT = self.WIDTH
        
        # Re-créer le terrain avec la nouvelle configuration
        self.create_field()


    def lauch_algo_btn(self):
        """Ajoute un bouton pour lancer l'algorithme"""
        bouton_lancer = tk.Button(
            self.racine,
            text="Lancer l'algorithme",
            command=self.lauch_algorithm
        )
        # Placer le bouton en dessous de la grille
        bouton_lancer.grid(column=2, row=self.GRID_ROW_SPAN, pady=10)


    def lauch_algorithm(self):
        """Appelle la méthode lauch_algorithm avec des paramètres prédéfinis dans un thread séparé"""

        def algorithm_thread():
            """Fonction exécutée dans un thread séparé permet de ne pas bloquer la GUI !"""
            self.nodesManager.launch_algorithm()
            self.plot_graph()

        # Création et démarrage du thread
        thread = threading.Thread(target=algorithm_thread)
        thread.daemon = True  # Permet au programme de se terminer même si le thread tourne encore
        thread.start()


    def plot_graph(self):
        """Affiche le graphique dans l'interface Tkinter"""
        # Collecter les historiques de couleurs des noeuds
        iterations = max(len(node.color_history) for node in self.nodesManager.nodes)    # Comme les noeuds peuvent avoir un nombre d'itérations différents, on prend l'iter max
        color_counts = {color: [0] * iterations for color in Colors}

        for node in self.nodesManager.nodes:
            for i, color in enumerate(node.color_history):
                color_counts[color][i] += 1

        # Créer la figure Matplotlib
        fig, ax = plt.subplots()
        for color, counts in color_counts.items():
            if (sum(counts) != 0): 
                ax.plot(range(iterations), counts, label=color.value, color=color.value)

        ax.set_xlabel('Itérations')
        ax.set_ylabel('Nombre de noeuds')
        ax.set_title('Évolution des couleurs des nœuds au fil des itérations')
        ax.legend()

        # Intégrer la figure dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.racine)  # Associer la figure à la fenêtre Tkinter
        canvas.draw()
        canvas.get_tk_widget().grid(column=3, row=0, rowspan=self.GRID_ROW_SPAN)  # Placer le graphique sous la grille
