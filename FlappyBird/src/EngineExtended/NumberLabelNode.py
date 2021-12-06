from EngineExtended.Node import *

class NumberLabelNode(Node):
    """ 
    Một node dùng để hiển thị các con số. \n
    Ta có thể chỉnh số hiện ra bằng thuộc tính .currentNumber. \n
    Cần chú ý rằng các phép biến đổi sẽ không có tác dụng với node này.
    """
    def __init__(self, width, height):
        super().__init__(width, height)

        self.currentNumber  =  0
        self._currentNumber = -9999999999999999
        self.numbers = self._GR.images['numbers']
        
    def draw(self):
        """ Vẽ số ra màn hình."""
        # Ta cần chú ý rằng các hình ảnh số đều có hiệu ứng "glow", thế nên sẽ có một khoảng pixel thừa khá lớn, nên ta sẽ dùng padding để thu hẹp lại.
        if self.visible == False:
            return None

        # Nếu như không có thay đổi gì, ta chỉ cần trả về surface đã vẽ trước đó.
        if self._currentNumber == self.currentNumber:
            return self.mainSurface

        # Phân tích số thành 1 mảng chứa từng chứ số một.
        self._currentNumber = self.currentNumber
        numberDigits = [int(x) for x in list(str(self._currentNumber))]            
        totalWidth = 0                                              
        for digit in numberDigits:                                  
            totalWidth += self.numbers[digit].get_width() 

        self.mainSurface.fill(0)
        padding = self.numbers[digit].get_width()*0.35                               
        Xoffset = (self.width - totalWidth) / 2 + (len(numberDigits)-1)*padding

        for digit in numberDigits:                                                       
            self.mainSurface.blit(self.numbers[digit], (Xoffset, self.height*0.5))    
            Xoffset += self.numbers[digit].get_width() - padding*2
            
        self.transformedWidth  = self.mainSurface.get_width()
        self.transformedHeight = self.mainSurface.get_height()                           
        return self.mainSurface

class NumberLabelNodeWithLeftSide(NumberLabelNode):
    """ Tương tự như NumberLabelNode, nhưng các số sẽ được vẽ từ lề bên trái. """
    def draw(self):
        if self.visible == False:
            return None
        if self._currentNumber == self.currentNumber:
            return self.mainSurface

        self._currentNumber = self.currentNumber
        numberDigits = [int(x) for x in list(str(self._currentNumber))]            
        totalWidth = 0                                              
        for digit in numberDigits:                                  
            totalWidth += self.numbers[digit].get_width() 

        self.mainSurface.fill(0)
        padding = self.numbers[digit].get_width()*0.35                               
        Xoffset =-padding

        for digit in numberDigits:                                                       
            self.mainSurface.blit(self.numbers[digit], (Xoffset, self.height*0.5))    
            Xoffset += self.numbers[digit].get_width() - padding*2
            
        self.transformedWidth  = self.mainSurface.get_width()
        self.transformedHeight = self.mainSurface.get_height()                           
        return self.mainSurface