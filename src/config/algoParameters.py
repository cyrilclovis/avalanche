from src.enums.algoParametersEnum import AlgoParameters
from src.enums.algoChoices import AlgoChoices

class AlgoParametersManager:
    """Gestionnaire pour les paramètres de l'algorithme."""
    def __init__(self):
        self._parameters = {
            AlgoParameters.ALGO.value: AlgoChoices.SNOWFLAKE_LOOP.value,
            AlgoParameters.N.value: 600,
            AlgoParameters.K.value: 3,
            AlgoParameters.ALPHA.value: 0.5,
            AlgoParameters.BETA.value: 10,
            AlgoParameters.BIZANTIN.value: 0,
            AlgoParameters.PANNE.value: 0,
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
        return (self._parameters[AlgoParameters.ALGO.value], 
                self._parameters[AlgoParameters.N.value], 
                self._parameters[AlgoParameters.K.value], 
                self._parameters[AlgoParameters.ALPHA.value], 
                self._parameters[AlgoParameters.BETA.value],
                self._parameters[AlgoParameters.BIZANTIN.value], 
                self._parameters[AlgoParameters.PANNE.value])
    
    def set_all_parameters(self, parameters: dict):
        for (key, val) in parameters:
                val = str(val).strip()

                if key in [AlgoParameters.N.value, AlgoParameters.K.value]:
                    self.set(key, int(val))
                elif key in [AlgoParameters.ALPHA.value, AlgoParameters.BETA.value, AlgoParameters.BIZANTIN.value, AlgoParameters.PANNE.value]:
                    self.set(key, float(val))
                else:
                    self.set(key, val)

    def set_parameters_if_correct_form(self, parameters: dict) -> tuple[bool, list[str]]:
        """
        Analyse et valide chaque paramètre dans le dictionnaire donné, champ par champ.
        Retourne un tuple (validité, liste_des_erreurs).
        
        Args:
            parameters (dict): Dictionnaire contenant les clés et valeurs des paramètres à valider.
            
        Returns:
            tuple[bool, list[str]]: Un booléen indiquant si tous les paramètres sont valides,
                                    et une liste des erreurs détectées.
        """
        errors = []

        for key, val in parameters:
            # Conversion de la valeur en chaîne de caractères
            val_str = str(val).strip()

            # Validation en fonction de la clé (paramètre)
            if key == AlgoParameters.ALGO.value:
                if val_str not in [choice.value for choice in AlgoChoices]:
                    errors.append(f"Paramètre '{AlgoParameters.ALGO.value}' : valeur invalide ({val_str}).")

            elif key == AlgoParameters.N.value:
                try:
                    n = int(val_str)
                    if n <= 0:
                        errors.append(f"Paramètre '{AlgoParameters.N.value}' : doit être un entier positif (actuel : {val_str}).")
                except ValueError:
                    errors.append(f"Paramètre '{AlgoParameters.N.value}' : doit être un entier positif (actuel : {val_str}).")
            
            elif key == AlgoParameters.K.value:
                try:
                    k = int(val_str)
                    if k <= 0:
                        errors.append(f"Paramètre '{AlgoParameters.K.value}' : doit être un entier positif (actuel : {val_str}).")
                except ValueError:
                    errors.append(f"Paramètre '{AlgoParameters.K.value}' : doit être un entier positif (actuel : {val_str}).")
            
            elif key == AlgoParameters.ALPHA.value:
                try:
                    alpha = float(val_str)
                    if not (0 <= alpha <= 1):
                        errors.append(f"Paramètre '{AlgoParameters.ALPHA.value}' : doit être un float entre 0 et 1 (actuel : {val_str}).")
                except ValueError:
                    errors.append(f"Paramètre '{AlgoParameters.ALPHA.value}' : doit être un float entre 0 et 1 (actuel : {val_str}).")
            
            elif key == AlgoParameters.BETA.value:
                try:
                    beta = float(val_str)
                    if beta < 0:
                        errors.append(f"Paramètre '{AlgoParameters.BETA.value}' : doit être un float ou un entier positif (actuel : {val_str}).")
                except ValueError:
                    errors.append(f"Paramètre '{AlgoParameters.BETA.value}' : doit être un float ou un entier positif (actuel : {val_str}).")

            # Vous pouvez ajouter plus de validations pour d'autres paramètres si nécessaire

        if len(errors) == 0:
            self.set_all_parameters(parameters)
            return True, errors
        else:
            return False, errors


