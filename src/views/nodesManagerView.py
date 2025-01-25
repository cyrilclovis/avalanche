from math import ceil, sqrt
import tkinter as tk
import random as rd

from src.models.nodesManager import NodesManager
from src.views.nodeView import NodeView
from src.enums.colors import Colors


class NodesManagerView(object):
    """Modélise un terrain réprésentant l'évolution des noeuds"""

    SIDE_SIZE = 15

    def __init__(self, racine, nodesManager: NodesManager):
        """Génère le terrain"""
        # Propriétés de la grille
        self.NODES_NUMBER = len(nodesManager.nodes)
        self.SIDE_NUMBER  = ceil(sqrt(self.NODES_NUMBER))
        self.WIDTH = self.SIDE_NUMBER * self.SIDE_SIZE
        self.HEIGHT = self.WIDTH

        # Initialisation de la vue
        self.racine = racine
        self.racine.title("Terrain de jeu")
        self.creation_evolution_terrain()
        

    def creation_evolution_terrain(self):
        """Crée le terrain de base puis y applique les règles"""
        self.canvas = tk.Canvas(self.racine, width=self.WIDTH, height=self.HEIGHT)
        self.grille()
        self.canvas.grid(column=0, row=0)


    def grille(self):
        """La fonction crée la grille composé de carré bleus (eau)
        avec une probabilité p et marrons si cette proba n'est pas
        vérifiée.
        """
        cpt = 0
        for i in range(self.SIDE_NUMBER):
            for j in range(self.SIDE_NUMBER):
                if cpt >= self.NODES_NUMBER:
                    return
                NodeView(self.canvas, i*self.SIDE_SIZE, j*self.SIDE_SIZE, self.SIDE_SIZE, rd.choice(list(Colors)))
                cpt += 1
