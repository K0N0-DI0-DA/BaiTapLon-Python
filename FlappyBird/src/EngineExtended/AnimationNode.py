from EngineExtended.Node import *

class AnimationNode(Node):
    """
    Là một đối tượng được thừa kế từ node, chúng sẽ hiển thị hoạt ảnh theo thời gian. \n
    Ta có thể dừng/tiếp tục hoạt ảnh bằng thuộc tính .animationRunning. \n
    Cách dùng : AnimationNode(width, height, animationArray), trong đó :
        \t width : Chiều rộng của surface chứa hoạt ảnh, thông thường ta hay lấy frame có kích cỡ lớn nhất. \n
        \t height : Chiều cao của surface chứa hoạt ảnh, thông thường ta hay lấy frame có kích cỡ lớn nhất. \n
        \t animationArray : Một mảng chứa các surface.
    Cần chứ ý răng .animationSwapTime ban đầu bằng 1.0, nghĩa là cứ 1s đổi hoạt ảnh 1 lần.
    Do đó ta có thể chỉnh sửa tốc độ hoạt ảnh bằng thuộc tính này.
    """

    def __init__(self, width, height, animationArray):
        super().__init__(width, height)
        self.animationArray     = animationArray
        """ Mảng surface chứa hoạt ảnh. """
        self.animationIndex     = 0
        """ Index dùng để xác định frame hiện tại. """
        self.animationMxIdx     = len(animationArray)
        self.animationTimer     = 0.0
        """ Bộ đém thời gian. """
        self.animationSwapTime  = 1.0
        """ Thời gian tối đa mà một frame được hiển thị. """
        self.animationRunning   = True
        """ Cho phép hoạt ảnh chạy hay không ? """

    def draw(self):
        if self.visible == False or self.alpha < 1:
            return None

        self.calculateAnimationIndex()
        self.mainSurface.fill(0)
        # Ta cần đảm bảo frame được vẽ chính giữa surface vẽ, bất kể frame đó có kích thước bao nhiêu.
        self.mainSurface.blit(self.animationArray[self.animationIndex], (0, 0))
        #    (self.width - self.animationArray[self.animationIndex].get_width() *0.5, 
        #     self.width - self.animationArray[self.animationIndex].get_height()*0.5))

        # Các thao tác vẽ tương tự như Node.
        retSurface = self.mainSurface
        if self.flipX or self.flipY:
            retSurface = pygame.transform.flip(retSurface, self.flipX, self.flipY)
        if self.scale != 1:
            retSurface = pygame.transform.scale(retSurface, (self.width*self.scale, self.height*self.scale))
        if self.rotation != 0:
            retSurface = pygame.transform.rotate(retSurface, self.rotation)
        self.transformedWidth  = retSurface.get_width()
        self.transformedHeight = retSurface.get_height()
        return retSurface

    def calculateAnimationIndex(self):
        """ Được gọi tự động, dùng để tính toán frame hiện tại. """
        if self.animationRunning == False:
            return
        if (self.animationTimer <= 0):
            self.animationIndex += 1
            if self.animationIndex >= self.animationMxIdx:
                self.animationIndex = 0
            self.animationTimer = self.animationSwapTime
        self.animationTimer -= self._GD.FPSClock.get_time() / 1000