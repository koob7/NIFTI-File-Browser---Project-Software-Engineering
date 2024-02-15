class Contour:
    """
    Class representing a single countour

    Holds all the points where a patch has to be drawn.
    The panel and layer together form a key that allow one Contour to belong to one specific layer in a scan.
    """
    def __init__(self, panel, layer):
        self.pointList = []
        self.panel = panel
        self.layer = layer
