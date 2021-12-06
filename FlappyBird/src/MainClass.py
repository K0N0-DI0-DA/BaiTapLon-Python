import pygame
import sys

from pygame.locals import *
from EngineExtended.Action import *
from GameData import *
from GameResource import *
from Menu.Canvas import *
from Utilities.Config import *

class MainClass():
    """
    Là lớp bắt đầu của game. \n
    MainClass sẽ khởi tạo các tham số game khi gọi GameData.getInstance() lần đầu. \n
    Đồng thời khởi tạo các tài nguyên game khi gọi GameResource.getInstance(). \n
    Lệnh Config.getInstance().read() sẽ nạp file config (chứa thông tin cài đặt và điểm số).

    MainClass sẽ tạo ra một đối tượng Canvas, đây là một đối tượng chứa các đối tượng khác như MainMenu, PlayMenu, ... \n
    Do Canvas được kế thừa từ Node, việc gọi update() sẽ cập nhật toàn bộ đối tượng con, cháu ... mà nó chứa.
    """
    def __init__(self):
        pygame.init()
        GD = GameData.getInstance()
        GR = GameResource.getInstance().load()
        Config.getInstance().read()

    def run(self):
        GD          = GameData.getInstance()
        GR          = GameResource.getInstance()
        canvas      = Canvas(GD.screenWidth, GD.screenHeight)
        canvas.x    = GD.screenWidth *0.5
        canvas.y    = GD.screenHeight*0.5

        while True:
            GD.FPSClock.tick(GD.FPS) 
            GD.events = pygame.event.get()
            for event in GD.events:
                if event.type == QUIT:    
                    pygame.quit()                                                               
                    sys.exit()   
            canvas.update()
            GD.display.fill(Color(0, 0, 0, 0))
            GD.display.blit(canvas.draw(), canvas.getAnchoredPosition())   
            pygame.display.update()                             
                           



















def main():
    mainClass = MainClass()
    mainClass.run()

if __name__ == '__main__':
    main()