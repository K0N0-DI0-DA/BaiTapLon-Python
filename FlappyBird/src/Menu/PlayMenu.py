from random import Random
from EngineExtended.Node import *
from EngineExtended.ImageNode import *
from EngineExtended.AnimationNode import *
from EngineExtended.NumberLabelNode import *
from Menu.CanvasMap import *
from Menu.LoadMenu import *
from Menu.MainMenu import *
from Utilities.LambdaExpression import *
from Utilities.RandomTable import *

class PlayMenu(Node):
    """ 
    Là lớp được chạy khi chơi game.
    """
    def __init__(self, width, height):
        super().__init__(width, height)

        self.backgroundNode = PlayMenuScrollBackground(self._GR.images['play_menu_background'],-0.2)
        self.backgroundNode.x = 0
        self.backgroundNode.y = height*0.5
        self.addChild(self.backgroundNode)

        self.bird = Bird(self._GR.images['birds'][0])
        self.bird.x = width*0.2
        self.bird.y = height*0.5
        self.bird.selectRandomVariant()
        self.addChild(self.bird)

        self.pipeManager = PipeManager(width, height, 4)
        self.pipeManager.x = width *0.5
        self.pipeManager.y = height*0.5
        self.pipeManager.refreshAllPipes()
        self.addChild(self.pipeManager)

        self.fogNode = PlayMenuScrollBackground(self._GR.images['play_menu_fog'],-1.0)
        self.fogNode.x = 0
        self.fogNode.y = height*0.5
        self.addChild(self.fogNode)

        self.ground = PlayMenuScrollBackground(self._GR.images['grounds'][0],-2.0)
        self.ground.x = 0
        self.ground.y = height*0.85
        self.addChild(self.ground)

        self.scoreDisplayer         = ScoreDisplayer(width, height*0.3)
        self.scoreDisplayer.anchor  = (0.5, 0.0)
        self.scoreDisplayer.x       = width*0.5
        self.scoreDisplayer.y       = height*-0.05
        self.addChild(self.scoreDisplayer)

        self.gradientMask           = ImageNode(self._GR.images['gradient_mask'])
        self.gradientMask.x         = width*0.5
        self.gradientMask.y         = height*0.5
        self.gradientMask.alpha     = 255
        self.gradientMask.visible   = True
        self.gradientMask.flipY     = True
        self.addChild(self.gradientMask)

        self.textNode               = ImageNode(self._GR.images['play_menu_text'])
        self.textNode.anchor        = (0.5, 1.0)
        self.textNode.x             = width*0.5
        self.textNode.y             = height*1.05
        self.textNode.alpha         = 255
        self.textNode.visible       = True
        self.addChild(self.textNode)

        CanvasMap.getInstance().addToMap("PlayMenu", self)

    def eventUpdate(self):
        super().eventUpdate()
        for event in self._GD.events:
            if event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_SPACE:
                    # State = 0 tương ứng với trạng thái game chưa bắt đầu.
                    # Ta sẽ khởi tạo toàn bộ thuộc tính các đối tượng liên quan.
                    if self.bird.state == 0:
                        self.state                          = 1
                        self.bird.state                     = 1
                        difficult                           = CanvasMap.getInstance().getFromMap("SettingMenu").speedState
                        self.pipeManager.pipeSpeed          = difficult * - 3
                        self.backgroundNode.speedX          = difficult * - 0.3
                        self.fogNode.speedX                 = difficult * - 1.5
                        self.ground.speedX                  = difficult * - 3.0
                        self.scoreDisplayer.multiplier      = difficult*difficult
                        self.scoreDisplayer.currentNumber   = 0
                        self.hideTextNode()
                    # Không có state 1 vì chả có cái gì để xử lí cả :)
                    # State = 2 tương ứng với trạng thái game đã kết thúc. 
                    if self.bird.state == 2:
                        # Reset lại bảng số ngẫu nhiên.
                        RandomTable.getInstance().reset()
                        # Ở đây ta sẽ reset lại hình ảnh chim, trạng thái chim và vị trí, góc xoay của chim.
                        self.bird.selectRandomVariant()
                        self.bird.state = 0
                        self.bird.animationRunning  = True
                        self.bird.x, self.bird.y    = self.width*0.2, self.height*0.5
                        self.bird.rotation          = 0
                        # Reset toàn bộ vật cản.
                        self.pipeManager.refreshAllPipes()
                        # Cập nhật hình ảnh mặt đất mới.
                        newIndex = int(RandomTable.getInstance().getRandom(len(self._GR.images['grounds'])))
                        self.ground.imageSurface    = self._GR.images['grounds'][newIndex]
                        self.setBackgroundScrollEnabled(True)
                if event.key == pygame.K_ESCAPE:
                    # Nếu phím ESC được bấm, ta thoát ra ngoài menu.
                    self.allowEventUpdate = False
                    self.onExitTransition()
                    
    def onEnterTransition(self):
        """ Hoạt ảnh khi bắt đầu menu. """
        duration = self._GD.actionDuration_medium
        self.visible = True
        self.allowUpdate = True
        self.allowEventUpdate = True
        act1 = MoveTo(self.width*0.5, self.height*0.5, duration)
        act2 = FadeTo(255, duration)
        self.removeAllActions()
        self.addAction(Parallel(act1, act2))
        gmAct1 = Delay(1.0)
        gmAct2 = FadeTo(0, duration)
        gmAct3 = Callfunc(LambdaExpression.func_hide, self.gradientMask)
        self.gradientMask.removeAllActions()
        self.gradientMask.addAction(Sequence(gmAct1, gmAct2, gmAct3))

    def onExitTransition(self):
        """ Hoạt ảnh khi kết thúc menu. """
        self.allowEventUpdate = False
        duration = self._GD.actionDuration_medium
        act1 = Delay(0.3)
        act2 = MoveTo(self.width*0.5, self.height*1.5, duration)
        act3 = FadeTo(0, duration)
        self.removeAllActions()
        self.addAction(Sequence(act1, Parallel(act2, act3), Callfunc(LambdaExpression.func_hide, self),  Callfunc(self.showLoadMenu)))
        gmAct = FadeTo(255, 0.5)
        self.gradientMask.visible = True
        self.gradientMask.removeAllActions()
        self.gradientMask.addAction(gmAct)

        mainMenu = CanvasMap.getInstance().getFromMap("MainMenu")
        mainMenu.removeAllActions()
        mainMenu.addAction(Sequence(Delay(6.0), Callfunc(mainMenu.onEnterTransition)))

    def showLoadMenu(self):
        """ Trở về màn hình nạp. """
        CanvasMap.getInstance().getFromMap("LoadMenu").show(3.0)

    def setBackgroundScrollEnabled(self, value):
        """ Cho phép nền chạy. """
        self.backgroundNode.scrollEnabled = value
        self.ground.scrollEnabled = value
        self.fogNode.scrollEnabled = value

    def showTextNode(self):
        """ Hiển thị thông báo (nằm ở phía dưới màn hình). """
        self.textNode.removeAllActions()
        self.textNode.addAction(FadeTo(255, 2.0))

    def hideTextNode(self):
        """ Ẩn thông báo (nằm ở phía dưới màn hình). """
        self.textNode.removeAllActions()
        self.textNode.addAction(FadeTo(0, 3.0))
################################################################################################

class PlayMenuScrollBackground(ImageNode):
    """ Một node có khả năng "cuộn", yêu cầu hình ảnh ở 1/3 đoạn đầu và 1/3 đoạn cuối phải giống nhau. """
    def __init__(self, imageSurface, speedX):
        super().__init__(imageSurface)

        self.anchor         = (0, 0.5)
        self.speedX         = speedX
        self.rollbackX      =-imageSurface.get_width()*2/3
        self.scrollEnabled  = True

    def update(self):
        super().update()
        if self.scrollEnabled == True:
            self.x += self.speedX
            if self.x <= self.rollbackX:
                self.x = 0

class Bird(AnimationNode):
    def __init__(self, animationArray):
        super().__init__(animationArray[0].get_width(), animationArray[0].get_height(), animationArray)
        difficult               = CanvasMap.getInstance().getFromMap("SettingMenu").speedState
        self._pipeManager       = None
        self.state              = 0
        """ Trạng thái hiện thời của chim (0: chưa bắt đầu, 1: bắt đầu bay, 2: chết). """
        self.animationTimer     = 0.1
        """ Thời lượng một frame ảnh của chim được hiển thị. """
        self.animationSwapTime  = self.animationTimer
        """ Đặt lại bố đếm thời gian hoạt ảnh. """
        self.posYVel            = 0
        """ Vận tốc rơi của chim. """
        self.posYVelDelta       = 0.1 + difficult*0.1
        """ Gia tốc rơi. """
        self.posYVelMin         =-3.0 - difficult*1.0
        """ Vận tốc bay lên lớn nhất. """
        self.posYVelMax         = 2.0 + difficult*1.0
        """ Vận tốc rơi xuống lớn nhất. """
        self.rotationVel        =-1.0 - difficult*0.3
        """ Vận tốc góc xoay. """
        self.minimalRotation    =-45
        """ Góc xoay nhỏ nhất. """
        self.groundLimit        = 240
        """ Độ cao mặt đất. """
        CanvasMap.getInstance().addToMap("Bird", self)

    def selectRandomVariant(self):
        """ Chọn một hình ảnh khác của chim. """
        newSetIndex = int(RandomTable.getInstance().getRandom(len(self._GR.images['birds'])))
        self.animationArray = self._GR.images['birds'][newSetIndex]

    def eventUpdate(self):
        super().eventUpdate()
        for event in self._GD.events:
            if event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_SPACE and self.state == 1:
                    # Nếu phím SPACE được bấm, chim sẽ chuyển góc xoay và tăng tốc độ bay lên cao. Đồng thời phát ra âm thanh được nạp sẵn.
                    self.rotation = 45
                    self.posYVel  = self.posYVelMin
                    self._GR.playSound('wing')

    def update(self):
        if super().update() == False:
            return

        if self.state == 0:
            # Nếu như chim chưa bắt đầu bay, ta không xử lí gì cả.
            return
        elif self.state == 1:
            # Nếu như chim đang bay, ta sẽ kiểm tra va chạm với vật cản Gần nhất.
            if self.checkCollision() == True:
                # Nếu va chạm xảy ra, chuyển trạng thái chim sang 2. Và tắt hoạt ảnh của chim.
                self.state   = 2
                self.animationRunning = False
                # Ghi điểm cao.
                Config.getInstance().data[2] = max(Config.getInstance().data[2], CanvasMap.getInstance().getFromMap("ScoreDisplayer").currentNumber)
                Config.getInstance().write()
                CanvasMap.getInstance().getFromMap("PipeManager").pause()                       # Dừng di chuyển toàn bộ vật cản.
                CanvasMap.getInstance().getFromMap("PlayMenu").showTextNode()                   # Hiện thông báo.
                CanvasMap.getInstance().getFromMap("PlayMenu").setBackgroundScrollEnabled(False)# Dừng di chuyển nền.
        elif self.state == 2 and self.y > self.groundLimit:
            # Nếu như chim đã chết, ta không xử lí gì cả.
            return

        # Xử lí cao độ của chim.
        if self.posYVel < self.posYVelMax:
            # Nếu như vận tốc rơi chưa đạt tối đa, ta sẽ tăng vận tốc lên bởi gia tốc .posYVelDelta
            self.posYVel += self.posYVelDelta
        # Đặt cao độ mới bằng cách lấy cao độ cũ cộng với tốc độ rơi.
        self.y       += self.posYVel

        # Luôn giữ cho chim không bay quá cao.
        if self.y < -50:
            self.y = -50
        # Nếu như góc xoay của chim chưa đạt tối đa, ta sẽ tăng góc lên lên bởi vận tốc góc .rotationVel
        if self.rotation > self.minimalRotation:
            self.rotation += self.rotationVel
        return True

    def checkCollision(self):
        """ Kiểm tra va chạm, """
        if self._pipeManager == None:
            self._pipeManager = CanvasMap.getInstance().getFromMap("PipeManager")
        if self.y > self.groundLimit:
            self._GR.playSound('die')
            return True

        pipe = self._pipeManager.pipes[self._pipeManager.currentFocus]
        
        padding  = 16
        birdRect = ((self.x - self.width* self.anchor[0]      + padding, self.y - self.height*(self.anchor[1] - 1) - padding),
                    (self.x - self.width*(self.anchor[0] - 1) - padding, self.y - self.height* self.anchor[1]      + padding))
        pipeRect = ((pipe.x - pipe.width* pipe.anchor[0]      + padding, pipe.y - pipe.height*(pipe.anchor[1] - 1) - padding),
                    (pipe.x - pipe.width*(pipe.anchor[0] - 1) - padding, pipe.y - pipe.height* pipe.anchor[1]      + padding))

        if birdRect[0][0] == pipeRect[0][0] or birdRect[0][1] == pipeRect[0][1] or birdRect[1][0] == pipeRect[1][0] or birdRect[1][1] == pipeRect[1][1]:
            return False
        if birdRect[0][0] >= pipeRect[1][0] or pipeRect[0][0] >= birdRect[1][0]:
            return False
        if birdRect[1][1] >= pipeRect[0][1] or pipeRect[1][1] >= birdRect[0][1]:
            return False
        
        self._GR.playSound('hit')
        return True 
        
class PipeManager(Node):
    """ 
    Lớp quản lí toàn bộ vật cản, cung cấp các hàm pause()/resume() dùng để tạm dừng/di chuyển vật cản.
    """
    def __init__(self, width, height, numberOfPipe):
        super().__init__(width, height)

        self._bird              = CanvasMap.getInstance().getFromMap('Bird')
        self.numberOfPipe       = numberOfPipe
        """ Số lượng vật cản. """
        self.pipes              = []
        """ Mảng chứa vật cản. """
        self.pipeSpeed          = 0
        """ Tốc độ di chuyển của tất cả vật cản. """
        self.oldPipeSpeed       = 0
        """ Biến tạm, được sử dụng khi pause được gọi. """
        self._pipeSpeed         = 0
        self.minimalGap         = 80
        """ Khoảng trống nhỏ nhất mà vật cản tạo ra cho chim bay qua. """
        self.currentFocus       = 0
        """ Vật cản hiện tại được theo dõi. """

        CanvasMap.getInstance().addToMap("PipeManager", self)

    def pause(self):
        """ Tam dừng toàn bộ vật cản. """
        self.oldPipeSpeed = self._pipeSpeed
        self.pipeSpeed = 0

    def resume(self):
        """ Tiếp tục chạy các vật cản. """
        self.pipeSpeed = self.oldPipeSpeed

    def refreshAllPipes(self):
        """ Reset toàn bộ vật cản về ban đầu. """
        self.pipes.clear()
        self.removeAllChildren()
        self.currentFocus = 0
        for i in range(0, self.numberOfPipe):
            newPipe = Pipe(self._GR.images['pipes'][0])
            newPipe.refresh()
            #newPipe.x = self.width + self.width*(i/self.numberOfPipe + 0.5)
            self.pipes.append(newPipe)
            self.addChild(newPipe)

    def update(self):
        if super().update() == False:
            return False

        if self.pipeSpeed != self._pipeSpeed:
            self._pipeSpeed = self.pipeSpeed
            for pipe in self.pipes:
                pipe.speedX = self._pipeSpeed

        if self.pipes[self.currentFocus].x < self._bird.x - self._bird.width*0.5:
            self.currentFocus += 1
            if self.currentFocus >= self.numberOfPipe:
                self.currentFocus = 0
            CanvasMap.getInstance().getFromMap('ScoreDisplayer').addScore()
        return True
        
class Pipe(ImageNode):
    """ Một lớp vật cản, cần chú ý rằng chúng có nhiều thể hiện khác nhau. Do đó không thêm vào CanvasMap. """
    lastRefresh = None
    def __init__(self, imageSurface):
        super().__init__(imageSurface)
        self._manager           = CanvasMap.getInstance().getFromMap('PipeManager')
        self._randomTable       = RandomTable.getInstance()
        self.speedX             = 0
        self._oldSpacing        = 0
        """ Vận tốc của vật cản. """

    def setImageSurface(self, newSurface):
        self.imageSurface = newSurface

    def update(self):
        # Cập nhật vị trí X của vật cản.
        # Nếu như đi quá màn hình, chúng sẽ tự làm mới hình ảnh, ví trí, ...
        self.x += self.speedX
        if self.x + self.width < 0:
            self.refresh()

    def refresh(self):
        """ Làm mới một vật cản. Vật cản sẽ có hình ảnh mới, vị trí và lật theo phương Y. """
        newIndex = int(RandomTable.getInstance().getRandom(len(self._GR.images['pipes'])))
        self.imageSurface = self._GR.images['pipes'][newIndex]

        if self.lastRefresh != None:
            offset = RandomTable.getInstance().getRandom(self._manager.width/self._manager.numberOfPipe*1.0) + self._manager.width/self._manager.numberOfPipe
            self.x = self.lastRefresh.x + offset
        else:
            self.x = self._manager.width + self.width

        self.flipY = self._randomTable.getRandom() >= 0.5
        randVal = self._randomTable.getRandom(self._manager.height*0.3) + self._manager.height*0.1

        # Tính toán vị trí mới dựa theo trạng thái lật.
        if self.flipY == True:
            self.y = randVal - self._manager.minimalGap - self._manager.height*0.15
        else:
            self.y = randVal + self._manager.minimalGap + self._manager.height*0.4

        Pipe.lastRefresh = self

class ScoreDisplayer(NumberLabelNode):
    """ Một lớp dùng để hiển thị điểm số."""
    def __init__(self, width, height):
        super().__init__(width, height)    
        self.multiplier = 1
        CanvasMap.getInstance().addToMap("ScoreDisplayer", self)

    def addScore(self):
        """ Nâng điểm số, độ khó càng cao, nâng càng nhiều. """
        self.currentNumber += 1*self.multiplier
        self._GR.playSound('point')