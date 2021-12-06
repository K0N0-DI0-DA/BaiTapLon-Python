from EngineExtended.Node import *
from EngineExtended.ImageNode import *
from Menu.CanvasMap import *
from Menu.LoadMenu import *
from Utilities.Config import *
from Utilities.LambdaExpression import *

class SettingMenu(Node):
    """
    Lớp menu giúp thao tác cài đặt game, mỗi lần chỉnh sửa cài đặt sẽ lưu vào trong config file.
    """
    def __init__(self, width, height):
        super().__init__(width, height)

        # Menu chính
        self.menuNode           = ImageNode(self._GR.images['setting_menu_text'])
        self.menuNode.anchor    = (0.5, 0.5)
        self.menuNode.x         = width *0.4
        self.menuNode.y         = height*0.5
        self.addChild(self.menuNode)

        # Trạng thái hiện thời của âm thanh, tắt hay bật phụ thuộc vào giá trị nằm trong config file.
        self.soundState                 = True if Config.getInstance().data[0] == 1 else False
        self.soundStateNode             = ImageNode(self._GR.images['on' if self.soundState == True else 'off'])
        self.soundStateNode.anchor      = (0.0, 0.5)
        self.soundStateNode.x           = width *0.5
        self.soundStateNode.y           = height*0.41
        self.addChild(self.soundStateNode)

        # Tốc độ chim, phụ thuộc vào giá trị nằm trong config file.
        self.speedState                 = Config.getInstance().data[1]
        self.speedStateNode             = ImageNode(self._GR.images[str(self.speedState)])
        self.speedStateNode.anchor      = (0.0, 0.5)
        self.speedStateNode.x           = width *0.5
        self.speedStateNode.y           = height*0.51
        self.addChild(self.speedStateNode)

        # Chỉ số index của con trỏ, 
        self.indicatorState     = 0
        self.indicatorPos       = ((width *0.25, height*0.41), (width *0.25, height*0.51), (width *0.32, height*0.61))

        # Con trỏ menu.
        self.indicator          = ImageNode(self._GR.images['indicator'])
        self.indicator.anchor   = (0.5, 0.5)
        self.indicator.x        = self.indicatorPos[0][0]
        self.indicator.y        = self.indicatorPos[0][1]
        self.addChild(self.indicator)

        CanvasMap.getInstance().addToMap("SettingMenu", self)

    def eventUpdate(self):
        """ Điều hướng con trỏ menu mỗi khi các phím ARROW_UP / DOWN hay BACKSPACE được bấm. """
        super().eventUpdate()
        for event in self._GD.events:
            if event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_UP:    
                    self.changeIndicatorPosition(-1)
                if event.key == pygame.K_DOWN:    
                    self.changeIndicatorPosition(+1)
                if event.key == pygame.K_SPACE:
                    self.selectMenu()

    def selectMenu(self):
        """ Được gọi mỗi khi phím BACKSPACE được bấm. """

        # Khi con trỏ menu nằm ở dòng "Sound".
        if self.indicatorState == 0:
            self.soundState = not self.soundState
            value = 'on' if self.soundState else 'off'
            self.soundStateNode.imageSurface = self._GR.images[value]
            Config.getInstance().data[0] = 1 if value == 'on' else 0
        
        # Khi con trỏ menu nằm ở dòng "Speed".
        if self.indicatorState == 1:
            self.speedState += 1
            if self.speedState > 3:
                self.speedState = 1
            valueStr = str(self.speedState)
            self.speedStateNode.imageSurface = self._GR.images[valueStr]
            Config.getInstance().data[1] = self.speedState

        # Khi con trỏ menu nằm ở dòng "Quit"
        if self.indicatorState == 2:
            self.onExitTransition()

        Config.getInstance().write()

    def onEnterTransition(self):
        """ Hoạt ảnh menu khi bắt đầu hiển thị lên trên màn hình. """
        self.indicatorState     = 0
        self.indicator.x        = self.indicatorPos[0][0]
        self.indicator.y        = self.indicatorPos[0][1]
        self.removeAllActions()
        self.visible = True
        duration = self._GD.actionDuration_medium
        act1 = Parallel(FadeTo(255, duration), MoveTo(self.width*0.5, self.height*0.5, duration), ScaleTo(1, duration))
        act2 = Callfunc(LambdaExpression.func_activate, self)
        self.addAction(Sequence(act1, act2))

    def onExitTransition(self):
        """ Hoạt ảnh menu khi thoát hiển thị khỏi màn hình. """
        self.removeAllActions()
        self.allowEventUpdate = False
        duration = self._GD.actionDuration_medium
        self.addAction(Parallel(FadeTo(0, duration), MoveTo(self.width*0.0, self.height*0.5, duration), ScaleTo(0, duration)))
        CanvasMap.getInstance().getFromMap('MainMenu').showMenuAndIndicator()

    def changeIndicatorPosition(self, delta):
        """ Mội khi phím ARROW_UP hay ARROW_DOWN được bấm, hàm này được gọi để thay đổi vị trí con trỏ menu. """
        self.indicatorState += delta
        if self.indicatorState > 2:
            self.indicatorState = 0
        if self.indicatorState < 0:
            self.indicatorState = 2
        x = self.indicatorPos[self.indicatorState][0]
        y = self.indicatorPos[self.indicatorState][1]
        self.indicator.removeAllActions()
        self.indicator.addAction(MoveTo(x, y, self._GD.actionDuration_short))

