class ContourAnnotation:
    """
    Class that represents an annotation for a single contour.

    The annotation is just a text describing what the contour is highlighting.
    The panel and layer together form a key that allow one ContourAnnotation to belong to one specific layer in a scan.
    """
    def __init__(self, panel, layer):
        self.annotation = ""
        self.layer = layer
        self.panel = panel


class Annotation:
    """
    A class that represents an annotation for a single scan.

    The annotation is a text describing the patients general situation/diagnosis.
    The class holds a list of all the contour annotations associated with this scan.
    """
    def __init__(self):
        self.annotation = ""
        self.contourAnnotations = []

    def set_annotation(self, text):
        """This function sets the text of the annotation. Used by the textChanged signal in GUIWindow."""
        self.annotation = text
