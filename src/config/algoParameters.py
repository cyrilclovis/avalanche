from src.enums.algoParametersEnum import AlgoParameters

class AlgoParametersManager:
    """Gestionnaire pour les paramètres de l'algorithme."""
    def __init__(self):
        self._parameters = {
            AlgoParameters.N.value: 600,
            AlgoParameters.K.value: 3,
            AlgoParameters.ALPHA.value: 0.5,
            AlgoParameters.BETA.value: 10
        }

    def get(self, key: str):
        """Récupère la valeur d'un paramètre."""
        return self._parameters.get(key)

    def set(self, key: str, value):
        """Met à jour la valeur d'un paramètre."""
        self._parameters[key] = value

    def map_field_parameters(self):
        """Retourne tous les paramètres sous forme de dictionnaire."""
        return {key: value for key, value in self._parameters.items()}
    
    def get_all_parameters(self):
        """Retourne les valeurs de N, K, ALPHA, BETA dans l'ordre spécifié."""
        return (self._parameters[AlgoParameters.N.value], 
                self._parameters[AlgoParameters.K.value], 
                self._parameters[AlgoParameters.ALPHA.value], 
                self._parameters[AlgoParameters.BETA.value])
