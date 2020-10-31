class Hud:
    def __init__(self, Renderer, playerObject):
        self.Renderer = Renderer
        self.player = playerObject
    
    def drawHud(self):
        self.Renderer.drawHud()