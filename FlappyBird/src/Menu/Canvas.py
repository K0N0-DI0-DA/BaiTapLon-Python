from EngineExtended.Node import *
from EngineExtended.ImageNode import *
from Menu.IntroMenu import *
from Menu.LoadMenu import LoadMenu
from Menu.MainMenu import *
from Menu.PlayMenu import *
from Menu.SettingMenu import SettingMenu

class Canvas(Node):
    """
    Một Canvas sẽ chứa toàn bộ các menu và đối tượng con. Nói cách khác, đây chính là đối tượng gốc của cây. \n
    Khi Canvas được tạo, introMenu luôn là menu được chạy dầu tiên. \n
    Canvas sẽ luôn đi kèm với CanvasMap, một bản đồ giúp ta tham chiếu tới bất kì đối tượng nào thuộc Canvas (tất nhiên đó phải là đối tượng duy nhất).
    """   
    def __init__(self, width, height):
        super().__init__(width, height)
        GR = GameResource.getInstance()

        self.introMenu                      = IntroMenu(width, height)
        self.introMenu.x                    = width *0.5
        self.introMenu.y                    = height*0.5
        self.addChild(self.introMenu)

        self.mainMenu                       = MainMenu(width, height)
        self.mainMenu.x                     = width *0.5
        self.mainMenu.y                     = height*0.5
        self.mainMenu.alpha                 = 0
        self.mainMenu.visible               = False
        self.mainMenu.allowEventUpdate      = False
        self.addChild(self.mainMenu)
    
        self.settingMenu                    = SettingMenu(width, height)
        self.settingMenu.x                  = width *0.0
        self.settingMenu.y                  = height*0.5
        self.settingMenu.alpha              = 0
        self.settingMenu.scale              = 0.0
        self.settingMenu.visible            = False
        self.settingMenu.allowUpdate        = False
        self.settingMenu.allowEventUpdate   = False
        self.addChild(self.settingMenu)

        self.playMenu                       = PlayMenu(width, height)
        self.playMenu.x                     = width *0.5
        self.playMenu.y                     = height*1.5
        self.playMenu.alpha                 = 0
        self.playMenu.visible               = False
        self.playMenu.allowUpdate           = False
        self.playMenu.allowEventUpdate      = False
        self.addChild(self.playMenu)

        self.loadMenu                       = LoadMenu(width, height)
        self.loadMenu.x                     = width *0.5
        self.loadMenu.y                     = height*0.5
        self.loadMenu.alpha                 = 0
        self.loadMenu.visible               = False
        self.addChild(self.loadMenu)

        self.introMenu.onEnterTransition()
        CanvasMap.getInstance().addToMap("Canvas", self)

























'''
        newNode = AnimationNode(self._GR.images['birds'][0][0].get_width(), 
                                self._GR.images['birds'][0][0].get_height(), 
                                self._GR.images['birds'][0])
        newNode.x                   = width*-0.5
        newNode.y                   = height*0.5
        newNode.animationSwapTime   = 0.3
        newNode.addAction(Sequence(
                            MoveTo(width*1.5, height*0.5, 5.0), 
                            Callfunc(self.introMenu.onEnterTransition)))
        self.addChild(newNode)
'''

        

    
        
        