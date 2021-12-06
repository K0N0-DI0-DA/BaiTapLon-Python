from EngineExtended.Node import *
from EngineExtended.ImageNode import *
from Menu.CanvasMap import *
from Utilities.LambdaExpression import *

class LoadMenu(Node):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.loadCircle         = ImageNode(self._GR.images['load_circle'])
        self.loadCircle.x       = width *0.5
        self.loadCircle.y       = height*0.5
        self.loadCircle.scale   = 0.6
        self.addChild(self.loadCircle)

        self.loading            = ImageNode(self._GR.images['loading'])
        self.loading.x          = width *0.5
        self.loading.y          = height*0.7
        self.loading.scale      = 1.0
        self.addChild(self.loading)


        CanvasMap.getInstance().addToMap("LoadMenu", self)

    def show(self, duration):
        self.visible = True
        self.allowUpdate = True

        self.loadCircle.removeAllActions()
        self.loadCircle.addAction(RotateBy(8.0, duration))
        
        self.removeAllActions()
        act1 = FadeTo(255, duration*0.2)
        act2 = Delay(duration*0.6)
        act3 = FadeTo(0, duration*0.2)
        act4 = Callfunc(LambdaExpression.func_deactivate, self)
        self.addAction(Sequence(act1, act2, act3, act4))
        

