from math import ceil, sqrt
import tkinter as tk
import random as rd

from src.models.nodesManager import NodesManager
from src.views.nodeView import NodeView


class NodesManagerView(object):
    """Modélise un terrain réprésentant l'évolution des noeuds"""

    SIDE_SIZE = 15

    def __init__(self, racine, nodesManager: NodesManager):
        """Génère le terrain"""
        self.nodesManager = nodesManager

        # Propriétés de la grille
        self.NODES_NUMBER = len(nodesManager.nodes)
        self.SIDE_NUMBER  = ceil(sqrt(self.NODES_NUMBER))
        self.WIDTH = self.SIDE_NUMBER * self.SIDE_SIZE
        self.HEIGHT = self.WIDTH

        # Initialisation de la vue
        self.racine = racine
        self.racine.title("Terrain de jeu")
        self.create_field()

        # Ajout du bouton
        self.lauch_algo_btn()   

    def create_field(self):
        """Crée le terrain de base puis y applique les règles"""
        self.canvas = tk.Canvas(self.racine, width=self.WIDTH, height=self.HEIGHT)
        self.init_field()
        self.canvas.grid(column=0, row=0)


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


    def lauch_algo_btn(self):
        """Ajoute un bouton pour lancer l'algorithme"""
        bouton_lancer = tk.Button(
            self.racine,
            text="Lancer l'algorithme",
            command=self.lauch_algorithm
        )
        # Placer le bouton en dessous de la grille
        bouton_lancer.grid(column=0, row=1, pady=10)


    def lauch_algorithm(self):
        """Appelle la méthode lauch_algorithm avec des paramètres prédéfinis"""
        # Paramètres à ajuster selon vos besoins
        k = 3   # Taille de l'échantillon
        alpha = 0.8
        beta = 3

        print(f"Lancement de l'algorithme avec k={k}, alpha={alpha}, beta={beta}")
        self.nodesManager.lauch_algorithm(k, alpha, beta)
