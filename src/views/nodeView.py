from src.enums.colors import Colors

class NodeView:
    """Classe représentant un nœud affiché sur le canvas."""

    def __init__(self, canvas, x: int, y: int, size: int, color: Colors):
        """
        Initialise et dessine un nœud sur le canvas.
        :param canvas: Le canvas Tkinter sur lequel dessiner.
        :param x: Coordonnée X du coin supérieur gauche du nœud.
        :param y: Coordonnée Y du coin supérieur gauche du nœud.
        :param size: Taille du côté du carré représentant le nœud.
        :param color: Couleur du nœud.
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color

        # Crée un rectangle pour représenter le nœud
        self.node = self.canvas.create_rectangle(
            x, y, x + size, y + size, fill=color.value, outline=color.value
        )

    def update_color(self, new_color: Colors):
        """
        Met à jour la couleur du nœud.
        :param new_color: La nouvelle couleur du nœud.
        """
        self.color = new_color
        self.canvas.itemconfig(self.node, fill=new_color, outline=new_color)