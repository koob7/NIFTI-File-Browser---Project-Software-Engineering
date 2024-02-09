class Contour():
    def __init__(self, panel, layer):
        self.pointList = []
        self.panel = panel #Rozważyć tutaj enum, docelowo left/mid/right
        self.layer = layer #To po prostu int z wartoscia ktora na sliderze - to i panel tworzylyby klucz do jakiegos innego czegos nw mapy moze
