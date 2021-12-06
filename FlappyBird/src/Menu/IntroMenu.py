from EngineExtended.Node import *
from EngineExtended.ImageNode import *
from Menu.CanvasMap import *
from Menu.MainMenu import *
from Utilities.LambdaExpression import *

class IntroMenu(Node):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.introNode1         = ImageNode(self._GR.images['intro (1)'])
        self.introNode1.alpha   = 0
        self.introNode1.x       = width *0.50
        self.introNode1.y       = height*0.40
        self.addChild(self.introNode1)

        self.introNode2         = ImageNode(self._GR.images['intro (2)'])
        self.introNode2.alpha   = 0
        self.introNode2.x       = width *0.50
        self.introNode2.y       = height*0.55
        self.addChild(self.introNode2)

        CanvasMap.getInstance().addToMap("IntroMenu", self)

    def onEnterTransition(self):
        self.introNode1.removeAllActions()
        self.introNode1.addAction(FadeTo(255, 1.5))
        self.introNode2.removeAllActions()
        self.introNode2.addAction(Sequence(Delay(1.0), FadeTo(255, 1.5)))
        self.removeAllActions()
        self.addAction(Sequence(Delay(3.0), Callfunc(self.onExitTransition)))

    def onExitTransition(self):
        act1 = FadeTo(0, 1.5)
        act2 = Callfunc(LambdaExpression.func_hide, self)
        act3 = Callfunc(CanvasMap.getInstance().getFromMap('MainMenu').onEnterTransition)
        self.removeAllActions()
        self.addAction(Sequence(act1, act2, act3))




    
        
        