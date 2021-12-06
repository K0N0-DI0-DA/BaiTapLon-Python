import pygame
from pygame import Surface

from EngineExtended.Action import *
from GameData import *
from GameResource import *

class Node():
    """
    Là một đối tượng nằm trong game, chúng có thể chứa hình ảnh (ImageNode), hoạt ảnh (AnimationNode), hoặc chứa các node khác. \n
    Các phép biến đổi xoay, thu phóng, tịnh tiến sẽ áp dụng lên những node con. (Tuy nhiên sẽ phải vẽ lại surface, điều này có ảnh hưởng tới hiệu suất, hạn chế dùng). \n
    Mỗi đối tượng node có thể sử dụng Action để tạo một hoạt ảnh đơn giản.
    """
    def __init__(self, width, height):
        self._GD, self._GR      = GameData.getInstance(), GameResource.getInstance()
        self.mainSurface        = Surface((width, height), pygame.SRCALPHA)
        """ Surface chính của node, surface này chưa bị biến đổi scale, hay rotate. """
        self.mainSurface.convert_alpha()

        self.alpha              = 255
        """ Độ mờ đục của node và node con của chúng. Giá trị thuộc khoảng [0, 255]"""
        self.__alpha            = self.alpha
        """ Một biến thứ 2 dùng để cập nhật mỗi khi alpha bị thay đổi. """
        self.anchor             = (0.5, 0.5)
        """ Điểm neo của node khi được vẽ trên node cha. """
        self.width              = width
        """ Kích cỡ chiều rộng của node, được cung cấp khi khởi tạo"""
        self.height             = height
        """ Kích cỡ chiều cao của node, được cung cấp khi khởi tạo"""
        self.transformedWidth   = 0
        """ Kích cỡ chiều rộng của node, được tính toán khi áp dụng các phép biến đổi"""
        self.transformedHeight  = 0
        """ Kích cỡ chiều cao của node, được tính toán khi áp dụng các phép biến đổi"""
        self.x                  = 0
        """ Vị trí x của node khi vẽ trên tọa độ node cha. """
        self.y                  = 0
        """ Vị trí y của node khi vẽ trên tọa độ node cha. """
        self.flipX              = False
        """ Lật theo phương ngang. """
        self.flipY              = False
        """ Lật theo phương dọc. """
        self.scale              = 1.0
        """ Tỉ lệ thu phóng, khi tham số này khác 1.0, hàm draw() sẽ phải vẽ thêm 1 lần. """
        self.rotation           = 0.0
        """ Góc xoay, khi tham số này khác 1.0, hàm draw() sẽ phải vẽ thêm 1 lần. """
        self.parent             = None
        """ Node cha. Khác None khi node này được addChild() từ cha. """
        self.children           = []
        """ Các node con. """
        self.actions            = []
        """ Các actions hiện tại. """
        self.allowEventUpdate   = True
        """ Cho phép ghi nhận sự kiện. """
        self.allowUpdate        = True
        """ Cho phép cập nhât. """
        self.visible            = True
        """ Cho phép hiển thị. """

    def draw(self):
        """
        Vẽ các node con và trả về surface đã vẽ.
        Draw() sẽ trả về None nếu node quá mờ (alpha < 1.0) hoặc visible == False. \n
        Cần chú ý các node con được thêm trước thì sẽ được vẽ sau.
        Với mỗi một phép biến đổi (scale, rotate, flip) được áp dụng, surface sẽ phải vẽ lại 1 lần.
        Các phép biến đổi được áp dụng lên toàn thể các node con.
        """
        if self.visible == False or self.alpha < 1:
            return None
            
        self.mainSurface.fill(0)
        for child in self.children:
            if child.visible == True:
                childDrawed = child.draw()
                if childDrawed != None:
                    self.mainSurface.blit(childDrawed, child.getAnchoredPosition())
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

    def eventUpdate(self):
        """ Được goi để xử lí các sự kiện từ người dùng khi cờ allowEventUpdate = True. """
        pass

    def update(self):
        """ 
        Được gọi mỗi khi vòng lặp game được cập nhật và cờ allowUpdate = True. \n
        Hàm này sẽ cập nhật các actions được đính vào node gọi luôn update() của các node con. \n
        Cần chú ý rằng các actions vẫn luôn thực thi kể cả cờ allowUpdate = False. \n
        Sẽ trả về False nếu như không cập nhật được, ngược lại True.
        """
        for action in self.actions:
            action.update()
        if self.allowUpdate == False:
            return False
        if self.allowEventUpdate == True and self.visible == True:
            self.eventUpdate()

        for child in self.children:
            child.update()
        if self.__alpha != self.alpha:
            self.__alpha = self.alpha
            self.mainSurface.set_alpha(self.__alpha)
        
        return True

    def addAction(self, action):
        """ Thêm một actions vào node. """
        if issubclass(type(action), Action) == False:
            return
        action.setTargetNode(self)
        self.actions.append(action)

    def addChild(self, child):
        """ Thêm một node con vào node hiện thời, cần chú ý một node con không thể có 2 cha. """
        if issubclass(type(child), Node) == False or child.parent != None or child == self:
            return
        child.parent = self
        self.children.append(child)

    def removeAction(self, action):
        """ Xóa bỏ một action. """
        if action in self.actions:
            self.actions.remove(action)

    def removeAllActions(self):
        """ Xóa bỏ toàn bộ actions. """
        self.actions.clear()

    def removeChild(self, child):
        """ Xóa bỏ một node con. """
        if issubclass(child, Node) == False:
            return
        self.children.remove(child)

    def removeAllChildren(self):
        """ Xóa bỏ toàn bộ node con. s"""
        self.children.clear()

    def removeFromParent(self):
        """ Tự xóa bỏ khỏi node cha. """
        if self.parent != None:
            self.parent.removeChild(self)

    def getAnchoredPosition(self):
        """ Láy vị trí của node (đã được tính toán các phép biến đổi) nằm trong tọa độ node cha. """
        retX = self.x - self.transformedWidth *self.anchor[0]
        retY = self.y - self.transformedHeight*self.anchor[1]
        return (retX, retY)

