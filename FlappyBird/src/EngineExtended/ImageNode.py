from EngineExtended.Node import *

class ImageNode(Node):
    """
    Là một đối tượng được thừa kế từ node, chúng sẽ hiển thị một hình ảnh duy nhất. \n
    Cần chú ý rằng ta không thể dùng addChild cho nhưng node loại này. Node này chỉ có nhiệm vụ duy nhất là hiển thị ảnh.
    Cách dùng : ImageNode(imageSurface), trong đó :
        \t imageSurface : là một surface cần vẽ, kích cỡ của node sẽ được tính toán bằng đúng với kích cỡ surface.
    """
    def __init__(self, imageSurface):
        super().__init__(imageSurface.get_width(), imageSurface.get_height())
        self.imageSurface = imageSurface
        """ Surface ảnh cần hiển thị. """
        self._imageSurface = imageSurface

    def draw(self):
        if self.visible == False or self.alpha < 1:
            return None

        # Ở đây ta vẽ imageSurface trước, sau đó áp dụng các phép biến đổi như node thông thường.
        if self._imageSurface != self.imageSurface:
            self._imageSurface = self.imageSurface
        self.mainSurface.fill(0)
        self.mainSurface.blit(self._imageSurface, (0, 0))
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

    def addChild(self, child):
        """ Hàm này bị loại bỏ. """
        return