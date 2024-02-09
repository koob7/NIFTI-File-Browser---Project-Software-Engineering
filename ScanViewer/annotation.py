class ContourAnnotation:
    def __init__(self, panel, layer):
        self.annotation = ""
        self.layer = layer
        self.panel = panel

class Annotation():
    def __init__(self):
        self.annotation = ""
        self.contourAnnotations = []

