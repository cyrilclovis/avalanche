import tkinter as tk
from tkinter import ttk, messagebox

from src.config.algoParameters import AlgoParametersManager
from src.views.nodesManagerView import NodesManagerView
from src.enums.algoParametersEnum import AlgoParameters
from src.enums.algoChoices import AlgoChoices

BACKGROUND = "Grey95"
FOREGROUND = "Black"
FONT = ('Bahnschrift Light SemiCondensed', 12)

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
        self.frame = ttk.LabelFrame(self.racine, text="Paramètres de l'algorithme", padding=10)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configuration de la grille principale
        self.racine.grid_rowconfigure(0, weight=1)
        self.racine.grid_columnconfigure(0, weight=1)

        self.interface(self.algo_manager.map_field_parameters())

        # Bouton pour valider, positionné après le cadre
        valider = ttk.Button(self.racine, text="Valider", command=self.valider_parametres)
        valider.grid(row=self.ligne, column=0, columnspan=2, pady=10)


    def interface(self, information):
        """Ajoute les champs de saisie pour chaque paramètre."""
        for cle, valeur_defaut in information.items():
            ttk.Label(self.frame, text=cle, font=FONT).grid(row=self.ligne, column=0, padx=5, pady=5, sticky="w")
            
            if cle == AlgoParameters.ALGO.value:
                combobox = ttk.Combobox(self.frame, values=[choice.value for choice in AlgoChoices], font=FONT)
                combobox.set(valeur_defaut)  # Valeur par défaut
                combobox.grid(row=self.ligne, column=1, padx=5, pady=5)
                self.bouttons[cle] = combobox
            else:
                entree = ttk.Entry(self.frame, font=FONT)
                entree.insert(0, valeur_defaut)  # Valeur par défaut
                entree.grid(row=self.ligne, column=1, padx=5, pady=5)
                self.bouttons[cle] = entree
            self.ligne += 1

        info_icon = ttk.Label(self.frame, text="ℹ", font=(FONT[0], 12, "bold"), foreground="blue", cursor="hand2")
        info_icon.grid(row=self.ligne, column=2, padx=5, pady=5, sticky="w")
        
        tooltip_text = (
            "Si vous renseignez P % pannes, alors à la fin des M itérations, (P/100) * NbNoeuds "
            "seront en panne. Les pannes sont réparties aléatoirement.\n\n"
            "Conseil : Pour bien observer l'effet des pannes sur l'algorithme :\n"
            "1. Exécutez sans panne et notez la convergence.\n"
            "2. Ensuite, choisissez M proche de ce nombre d'itérations.\n"
            "3. Ajouter des pannes, puis relancer"
        )

        def show_tooltip(event):
            messagebox.showinfo("Info - Pannes", tooltip_text)
        
        info_icon.bind("<Button-1>", show_tooltip)


    def valider_parametres(self):
        """Récupère les valeurs saisies et les met à jour dans le gestionnaire."""
        userForm = [(key, val.get()) for key, val in self.bouttons.items()]
        isValidForm, errors = self.algo_manager.set_parameters_if_correct_form(userForm)
        if isValidForm:
            self.nodes_manager_view.update(self.algo_manager.get_all_parameters())
        else:
            error_message = "\n".join(errors)
            messagebox.showerror("Erreur de validation", f"Les erreurs suivantes sont survenues :\n\n{error_message}")
