from EngineExtended.Node import *
from EngineExtended.ImageNode import *
from EngineExtended.NumberLabelNode import *
from Menu.CanvasMap import *
from Menu.LoadMenu import *
from Utilities.Config import *
from Utilities.LambdaExpression import *

class MainMenu(Node):
    """ Menu chính của trò chơi. """
    def __init__(self, width, height):
        super().__init__(width, height)

        self.backgroundNode         = ImageNode(self._GR.images['main_menu_background'])
        self.backgroundNode.x       = width *0.5
        self.backgroundNode.y       = height*0.5
        self.addChild(self.backgroundNode)

        self.logoNode               = ImageNode(self._GR.images['main_menu_logo'])
        self.logoNode.x             = width *0.33
        self.logoNode.y             = height*0.20
        self.addChild(self.logoNode)

        self.menuNode               = ImageNode(self._GR.images['main_menu_text'])
        self.menuNode.anchor        = (0.8, 0.5)
        self.menuNode.x             = width *0.87
        self.menuNode.y             = height*0.68
        self.addChild(self.menuNode)

        self.scoreDisplayer         = NumberLabelNodeWithLeftSide(self.width*0.5, self.height*0.3)
        self.scoreDisplayer.anchor  = (0.0, 0.5)
        self.scoreDisplayer.x       = width *0.12
        self.scoreDisplayer.y       = height*0.70
        self.addChild(self.scoreDisplayer)

        self.indicatorState         = 0
        self.indicatorPos           = ((width *0.712, height*0.572), (width *0.64, height*0.676), (width *0.725, height*0.782))

        self.indicator              = ImageNode(self._GR.images['indicator'])
        self.indicator.anchor       = (0.5, 0.5)
        self.indicator.x            = self.indicatorPos[0][0]
        self.indicator.y            = self.indicatorPos[0][1]
        self.addChild(self.indicator)

        self.gradientMask           = ImageNode(self._GR.images['gradient_mask'])
        self.gradientMask.anchor    = (0.5, 0.5)  
        self.gradientMask.x         = width*0.5
        self.gradientMask.y         = height*0.5
        self.gradientMask.alpha     = 0
        self.gradientMask.visible   = False
        self.addChild(self.gradientMask)

        CanvasMap.getInstance().addToMap("MainMenu", self)

    def eventUpdate(self):
        super().eventUpdate()
        for event in self._GD.events:
            if event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_DOWN:
                    # Nếu phím ARROW_DOWN được bấm, di chuyển con trỏ xuống dưới.
                    self.changeIndicatorPosition(+1)
                if event.key == pygame.K_UP:    
                    # Nếu phím ARROW_UP được bấm, di chuyển con trỏ lên trên.
                    self.changeIndicatorPosition(-1)
                if event.key == pygame.K_SPACE:
                    # Nếu phím SPACE được bấm, xử lí chúng bằng hàm selectMenu().
                    self.selectMenu()
                    
    def selectMenu(self):
        """ Hàm này được gọi để xử lí menu đang chọn hiện tại. """
        if self.indicatorState == 0:
            # Nếu chọn dòng đầu tiên, ta chuyển sang PlayMenu.
            self.onPlayTransition()
        if self.indicatorState == 1:
            # Nếu chọn dòng thứ hai, ta chuyển sang Menu cài đặt.
            CanvasMap.getInstance().getFromMap("SettingMenu").onEnterTransition()
            self.hideMenuAndIndicator()
        if self.indicatorState == 2:
            # Dòng thứ 3 sẽ là thoát.
            pygame.quit()
            sys.exit()

    def onEnterTransition(self):
        """ Hoạt ảnh khi bắt đầu hiển thị. """
        # Mỗi khi menu được hiển thị, ta sẽ cập nhật điểm số từ file.
        self.scoreDisplayer.currentNumber = Config.getInstance().data[2]

        self.removeAllActions()
        self.visible = True
        act1 = Parallel(MoveTo(self.width*0.5, self.height*0.5, self._GD.actionDuration_veryShort), FadeTo(255, self._GD.actionDuration_long))
        act2 = Callfunc(LambdaExpression.func_allowEventUpdate, self)
        self.addAction(Sequence(act1, act2))
        self.gradientMask.removeAllActions()
        self.gradientMask.addAction(Sequence(FadeTo(0, 1.5), Callfunc(LambdaExpression.func_hide, self.gradientMask)))

    def onPlayTransition(self):
        """ Hoạt ảnh khi bắt đầu chuyển sang PlayMenu. """
        self.gradientMask.visible = True
        self.gradientMask.removeAllActions()
        self.gradientMask.addAction(FadeTo(255, self._GD.actionDuration_veryShort))
        
        self.removeAllActions()
        self.allowEventUpdate = False
        act1 = FadeTo(0, self._GD.actionDuration_veryLong)
        act2 = MoveTo(self.x, -self._GD.screenHeight, self._GD.actionDuration_veryLong)
        act3 = Callfunc(LambdaExpression.func_hide, self)
        self.addAction(Sequence(Parallel(act1, act2), act3))
        
        CanvasMap.getInstance().getFromMap('LoadMenu').show(5.0)

        playMenu = CanvasMap.getInstance().getFromMap('PlayMenu')
        playMenu.removeAllActions()
        playMenu.addAction(Sequence(Delay(7.0), Callfunc(playMenu.onEnterTransition)))

    def showMenuAndIndicator(self):
        """ Hiển thị menu chính và con trỏ. """
        self.allowEventUpdate = True
        self.menuNode.removeAllActions()
        self.menuNode.addAction(ScaleTo(1.0, self._GD.actionDuration_short))
        self.scoreDisplayer.removeAllActions()
        self.scoreDisplayer.addAction(FadeTo(255, 0.5))
        self.indicator.removeAllActions()
        self.indicator.addAction(ScaleTo(1.0, self._GD.actionDuration_short))

    def hideMenuAndIndicator(self):
        """ Ẩn menu chính và con trỏ. """
        self.allowEventUpdate = False
        self.menuNode.removeAllActions()
        self.menuNode.addAction(ScaleTo(0.0, self._GD.actionDuration_short))
        self.scoreDisplayer.removeAllActions()
        self.scoreDisplayer.addAction(FadeTo(0, 0.5))
        self.indicator.removeAllActions()
        self.indicator.addAction(ScaleTo(0.0, self._GD.actionDuration_short))

    def changeIndicatorPosition(self, delta):
        """ Di chuyển con trỏ."""
        self.indicatorState += delta
        # Nếu con trỏ vượt quá giới hạn, ta cập nhật lại nó về chỉ số bên kia.
        if self.indicatorState > 2:
            self.indicatorState = 0
        if self.indicatorState < 0:
            self.indicatorState = 2

        # Cập nhật vị trí mới của con trỏ.
        x = self.indicatorPos[self.indicatorState][0]
        y = self.indicatorPos[self.indicatorState][1]
        self.indicator.removeAllActions()
        self.indicator.addAction(MoveTo(x, y, self._GD.actionDuration_short))

