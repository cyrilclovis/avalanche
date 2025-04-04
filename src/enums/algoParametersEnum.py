from enum import Enum

class AlgoParameters(Enum):
    """Enum pour définir les clés des paramètres d'algorithme."""
    
    ALGO = "Algorithme à utiliser"
    M = "Nombre d'itérations (M)"
    N = "Nombre de nœuds (N)"
    K = "k (nombre de voisins à contacter)"
    ALPHA = "alpha"
    BETA = "beta"
    BIZANTIN = "Bizantins (en %)"
    PANNE = "Panne (en %)"