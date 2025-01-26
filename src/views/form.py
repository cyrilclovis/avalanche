import tkinter as tk

from src.config.algoParameters import AlgoParametersManager
from src.views.nodesManagerView import NodesManagerView

BACKGROUND = "Grey95"
FOREGROUND = "Black"
FONT = ('Bahnschrift Light SemiCondensed', 15)

class Form(object):
    """Gère l'interface utilisateur pour demander les paramètres nécessaires à l'algorithme et au terrain."""

    def __init__(self, racine: tk.Tk):
        """Le constructeur crée la racine et appelle la méthode interface."""
        self.racine = racine
        self.algo_manager = AlgoParametersManager()
        self.racine.title("Paramètres pour l'algorithme")
        self.racine["bg"] = BACKGROUND
        self.bouttons = {}  # Stocke les champs d'entrée pour récupérer les valeurs
        self.creation_interface()
        self.nodes_manager_view = NodesManagerView(racine)

    def creation_interface(self):
        """Crée l'interface utilisateur pour demander les paramètres."""
        self.ligne = 0
        self.colonne = 0
        self.interface(self.algo_manager.map_field_parameters())

        # Bouton pour valider
        valider = tk.Button(
            self.racine,
            text="Valider",
            font=FONT,
            command=self.valider_parametres
        )
        valider.grid(column=0, row=self.ligne, columnspan=2)

    def interface(self, information):
        """Ajoute les champs de saisie pour chaque paramètre."""
        for cle, valeur_defaut in information.items():
            label = tk.Label(
                self.racine,
                text=cle,
                bg=BACKGROUND,
                fg=FOREGROUND,
                font=FONT
            )
            label.grid(column=0, row=self.ligne, sticky="w", padx=10, pady=5)

            entree = tk.Entry(
                self.racine,
                font=FONT,
                justify="center"
            )
            entree.insert(0, valeur_defaut)  # Valeur par défaut
            entree.grid(column=1, row=self.ligne, padx=10, pady=5)

            self.bouttons[cle] = entree
            self.ligne += 1


    def valider_parametres(self):
        """Récupère les valeurs saisies et les met à jour dans le gestionnaire."""
        for cle, val in self.bouttons.items():
            valeur = val.get()
            # Convertit en float ou int selon la saisie
            valeur_convertie = float(valeur) if '.' in valeur else int(valeur)
            self.algo_manager.set(cle, valeur_convertie)
        
        self.nodes_manager_view.update(self.get_all_parameters())


    def get_all_parameters(self):
        """Renvoie les valeurs des paramètres après validation."""
        return self.algo_manager.get_all_parameters()
