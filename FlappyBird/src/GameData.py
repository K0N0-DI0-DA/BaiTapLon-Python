import pygame

class GameData():
    """  
    Đây là lớp lưu trữ các tham số của game. \n
    Do đây là lớp singleton, sẽ chỉ một thể hiện được tạo ra và dùng xuyên suốt chương trình. \n
    Ta chỉ cần gọi GameData.getInstance() để tham chiếu tới đối tượng đó. \n
    Hoặc trong một Node (hoặc lớp kế thừa từ Node), ta có thể dùng thuộc tính self._GD, một cách ngắn gọn hơn so với cách trên bởi vì self._GD = GameData.getInstance() được gán từ khi khởi tạo.
    """
    __instance          = None

    @staticmethod
    def getInstance():
        if GameData.__instance == None:
            GameData.__instance                     = GameData()
            GameData.__instance.FPS                 = 60
            GameData.__instance.FPSClock            = pygame.time.Clock()

            GameData.__instance.screenWidth         = int(1280 * 0.5)
            """ Kích cỡ chiều rộng cửa sổ. """
            GameData.__instance.screenHeight        = int(720  * 0.5)
            """ Kích cỡ chiều cao cửa sổ. """

            GameData.__instance.display  = pygame.display.set_mode((int(1280 * 0.5), int(720  * 0.5)))
            pygame.display.set_caption('Flappy Bird')

            GameData.__instance.events              = None
            """ Các events được sinh ra trong game sẽ lưu tại đây. Mỗi một vòng lặp sẽ clear() chúng trước khi nhận các event mới. """

            # Các thời lượng hoạt ảnh của game.
            GameData.__instance.actionDuration_veryShort    = 0.10
            GameData.__instance.actionDuration_short        = 0.25
            GameData.__instance.actionDuration_medium       = 0.50
            GameData.__instance.actionDuration_long         = 0.75
            GameData.__instance.actionDuration_veryLong     = 1.00
        return GameData.__instance
