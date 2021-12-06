import pygame
import sys

class CanvasMap():
    """ 
    Khi mà Canvas trở nên quá lớn, ta sẽ không thể tham chiếu tới những đối tượng nằm trong đó. \n
    CanvasMap giúp ta giải quyết vấn đề này. \n
    Do đây là lớp singleton, sẽ chỉ một thể hiện được tạo ra và dùng xuyên suốt chương trình. \n
    Khi muốn thêm vào CanvasMap, ta chỉ việc sử dụng CanvasMap.getInstance().addToMap(key, targetNode), trong đó:
        \t key : Là key được lưu trữ nhằm xác định đối tượng trong map.
        \t targetNode : Đối tượng được thêm vào.
    """
    __instance          = None

    @staticmethod
    def getInstance():
        if CanvasMap.__instance == None:
            CanvasMap.__instance = CanvasMap()
            CanvasMap.__map      = {}
        return CanvasMap.__instance

    def addToMap(self, key, targetNode):
        """ Thêm một đối tượng vào map với key tương ứng. """
        targetNodeType = type(targetNode) 
        self.__map[key] = targetNode

    def getFromMap(self, key):
        """ Tìm một đối tượng đã thêm, nếu không có, thông báo lỗi và thoát chương trình. """
        if key not in self.__map:
            print("Khong tim thay : " + str(key))
            pygame.quit()                                                               
            sys.exit()
        return self.__map[key]

    def clear(self):
        self.__map.clear()

