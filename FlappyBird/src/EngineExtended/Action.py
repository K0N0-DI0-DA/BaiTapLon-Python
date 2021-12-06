from GameData import *

class Action():
    """
    Lớp action là một lớp thực thi các hoạt ảnh của node. \n
    Sau khi thêm vào node và thi thực xong, chúng sẽ tự xóa bỏ khỏi node.
    """
    def __init__(self):
        self._GD        = GameData.getInstance()
        self.duration   = 0.0
        self.running    = False
        self.targetNode = None

    def setTargetNode(self, targetNode):
        if targetNode == None:
            return False
        self.running    = True
        self.targetNode = targetNode
        return True

    def check(self):
        if self.targetNode == None or self.running == False:
            return False
        return True

    def update(self):
        if self.duration <= 0:
            self.dispose()
            return
        self.duration -= 1.0 / self._GD.FPS

    def dispose(self):
        self.running    = False
        self.targetNode.removeAction(self)
        self.targetNode = None

class Sequence(Action):
    """ 
    Một Action chứa các actions khác, Đươc dùng để thực thi tuần tự những actions đó. \n
    Thứ tự thực hiện phụ thuộc theo thứ tự chúng được thêm vào.
    """
    def __init__(self, *actions):
        super().__init__()
        self.actions = actions
        self.currentAction = 0

    def addAction(self, action):
        """ Thêm một action vào danh sách thực thi. """
        if issubclass(type(action), Action) == False:
            return
        self.actions.append(action)
        
    def setTargetNode(self, targetNode):
        if super().setTargetNode(targetNode) == False:
            return False
        for action in self.actions:
            self.duration += action.duration
        return True
    
    def update(self):
        if self.actions[self.currentAction].targetNode == None:
            self.actions[self.currentAction].setTargetNode(self.targetNode)
        self.actions[self.currentAction].update()
        if self.actions[self.currentAction].running == False:
            self.currentAction += 1
            if self.currentAction >= len(self.actions):
                self.dispose()
                return
        self.duration -= 1.0 / self._GD.FPS

class Parallel(Action):
    """ 
    Một Action chứa các actions khác, Đươc dùng để thực thi đồng thời toàn bộ những actions đó. \n
    Không quan trọng thứ tự được thêm vào. \n
    """
    def __init__(self, *actions):
        super().__init__()
        self.actions = actions

    def addAction(self, action):
        if issubclass(type(action), Action) == False:
            return
        self.actions.append(action)
        
    def setTargetNode(self, targetNode):
        if super().setTargetNode(targetNode) == False:
            return False
        for action in self.actions:
            action.setTargetNode(targetNode)
            self.duration = max(self.duration, action.duration)
        return True
    
    def update(self):
        for action in self.actions:
            if action.running == True:
                action.update()
        super().update()

# HIEN THUC CAC LOP THUA KE.
class Callfunc(Action):
    """ 
    Một action chứa callback. Dùng để gọi 1 hàm. \n
    Hiện tại chỉ hỗ trợ tối đa 3 tham số, tất nhiên ta có thế chỉnh sửa hàm __init()__ để hỗ trợ nhiều hơn. \n
    Các dùng : Callfunc(<hàm mục tiêu>, tham số 1, tham số 2, tham số 3).
    """

    def __init__(self, target, arg1 = None, arg2 = None, arg3 = None):
        super().__init__()
        self.targetFunc = target
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

        if   arg1 == None:
            self.callType = 0
        elif arg2 == None:
            self.callType = 1
        elif arg3 == None:
            self.callType = 2
        else:
            self.callType = 3

    def invoke(self):
        if self.callType == 0:
            self.targetFunc()
        elif self.callType == 1:
            self.targetFunc(self.arg1)
        elif self.callType == 2:
            self.targetFunc(self.arg1, self.arg2)
        elif self.callType == 3:
            self.targetFunc(self.arg1, self.arg2, self.arg3) 
        
    def update(self):
        if self.check() == False:
            return
        self.invoke()
        super().update()

class Delay(Action):
    """ 
    Một action dùng để tạo thời gian chờ.
    """
    def __init__(self, duration):
        super().__init__()
        self.duration = duration

class FadeTo(Action):
    """ Một action thay đổi alpha của node. """
    def __init__(self, targetAlpha, duration):
        super().__init__()
        self.targetAlpha    = targetAlpha
        self.deltaAlphaPS   = 0
        self.duration       = duration

    def setTargetNode(self, targetNode):
        if super().setTargetNode(targetNode) == False:
            return
        self.deltaAlphaPS = (self.targetAlpha - targetNode.alpha) / self.duration
        return True

    def update(self):
        if self.check() == False:
            return
        self.targetNode.alpha += self.deltaAlphaPS / self._GD.FPS
        super().update()

class MoveTo(Action):
    """ Một action dùng để thay đổi vị trí của node. """
    def __init__(self, x, y, duration):
        super().__init__()
        self. x, self. y    = x, y
        self.dx, self.dy    = 0, 0
        self.duration       = duration

    def setTargetNode(self, targetNode):
        if super().setTargetNode(targetNode) == False:
            return
        self.dx = (self.x - targetNode.x) / self.duration
        self.dy = (self.y - targetNode.y) / self.duration
        return True

    def update(self):
        if self.check() == False:
            return
        deltaPosX = self.dx * self._GD.FPSClock.get_time() / 1000
        deltaPosY = self.dy * self._GD.FPSClock.get_time() / 1000
        disX = self.x - self.targetNode.x
        disY = self.y - self.targetNode.y
        if disX*disX + disY*disY < deltaPosX*deltaPosX + deltaPosY*deltaPosY:
            self.targetNode.x = self.x
            self.targetNode.y = self.y
            self.dispose()
            return
        self.targetNode.x += deltaPosX
        self.targetNode.y += deltaPosY
        super().update() 

class ScaleTo(Action):
    """ Một action dùng để thay đổi độ thu phóng của node. """
    def __init__(self, scale, duration):
        super().__init__()
        self.scale          = scale
        self.ds             = 0
        self.duration       = duration

    def setTargetNode(self, targetNode):
        if super().setTargetNode(targetNode) == False:
            return
        self.ds = (self.scale - targetNode.scale) / self.duration
        return True

    def update(self):
        if self.check() == False:
            return
        deltaS = self.ds * self._GD.FPSClock.get_time() / 1000
        disS   = self.scale - self.targetNode.scale
        if abs(disS) < abs(deltaS):
            self.targetNode.scale = self.scale
            self.dispose()
            return
        self.targetNode.scale += deltaS
        super().update() 

class RotateBy(Action):
    """ Một action dùng để thay đổi góc xoay của node theo thời gian. """

    def __init__(self, deltaRotation, duration):
        super().__init__()
        self.deltaRotation  = deltaRotation
        self.duration       = duration

    def update(self):
        if self.check() == False:
            return
        self.targetNode.rotation += self.deltaRotation
        super().update() 

# Ở đầy chỉ bao gồm các action cơ bản.
# Ta có thể thêm nhiều action khác nhau thêm nữa bằng cách thừa kế từ Actions.
# Hiện tại, các action không hỗ trợ phép nội suy để thực thi các chuyển động phúc tạp 
#   mà chỉ thực hiện một cách tuyến tính theo thời gian.