import random

class RandomTable():
    """  
    Đây là lớp lưu trữ các giá trị ngẫu nhiên. \n
    Do đây là lớp singleton, sẽ chỉ một thể hiện được tạo ra và dùng xuyên suốt chương trình. \n 
    Ta chỉ cần gọi GameData.getInstance() để tham chiếu tới đối tượng đó. \n
    Ta sẽ sử dụng lớp này thay vì gọi trực tiếp random(). \n
    """
    __instance          = None

    @staticmethod
    def getInstance():
        if RandomTable.__instance == None:
            RandomTable.__instance = RandomTable(200)
        return RandomTable.__instance

    def __init__(self, capacity):
        self.array = []
        self.capacity = capacity
        for i in range(0, capacity):
            self.array.append(random.random())
        self.currentIndex = -1   

    def reset(self):
        """ Reset """
        self.array.clear()
        for i in range(0, self.capacity):
            self.array.append(random.random())
        self.currentIndex = -1   

    def getRandom(self, scale = 1.0):
        """  
        Lấy một số ngẫu nhiên. Nằm trong khoảng từ 0 đến scale. \n
        (Tham số scale mặc định bằng 1.0)
        """
        self.currentIndex += 1
        if self.currentIndex >= self.capacity:
            self.currentIndex = 0
        return self.array[self.currentIndex]*scale

