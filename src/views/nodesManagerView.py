from math import ceil, sqrt
import tkinter as tk
import random as rd
import threading

from src.models.nodesManager import NodesManager
from src.views.nodeView import NodeView
from src.config.algoParameters import AlgoParametersManager

class NodesManagerView(object):
    """Modélise un terrain réprésentant l'évolution des noeuds"""

    SIDE_SIZE = 15

    def __init__(self, racine):
        """Génère le terrain"""
        self.racine = racine
        self.racine.title("Terrain de jeu")
        self.update()
        

    def create_field(self):
        """Crée le terrain de base puis y applique les règles"""
        self.canvas = tk.Canvas(self.racine, width=self.WIDTH, height=self.HEIGHT)
        self.init_field()
        self.canvas.grid(column=2, row=0, rowspan=4)
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
        if params_tuple:
            N, K, ALPHA, BETA = params_tuple
        else:
            N, K, ALPHA, BETA = AlgoParametersManager().get_all_parameters()
        self.nodesManager = NodesManager(N, K, ALPHA, BETA)


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
        bouton_lancer.grid(column=2, row=4, pady=10)


    def lauch_algorithm(self):
        """Appelle la méthode lauch_algorithm avec des paramètres prédéfinis dans un thread séparé"""

        def algorithm_thread():
            """Fonction exécutée dans un thread séparé permet de ne pas bloquer la GUI !"""
            self.nodesManager.lauch_algorithm()

        # Création et démarrage du thread
        thread = threading.Thread(target=algorithm_thread)
        thread.daemon = True  # Permet au programme de se terminer même si le thread tourne encore
        thread.start()

