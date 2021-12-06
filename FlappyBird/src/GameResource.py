import pygame

from Menu.CanvasMap import CanvasMap 

class GameResource():
    """  
    Đây là lớp lưu trữ các tài nguyên của game. \n
    Do đây là lớp singleton, sẽ chỉ một thể hiện được tạo ra và dùng xuyên suốt chương trình. \n
    Ta chỉ cần gọi GameResource.getInstance() để tham chiếu tới đối tượng đó. \n
    Hoặc trong một Node (hoặc lớp kế thừa từ Node), ta có thể dùng thuộc tính self._GR, một cách ngắn gọn hơn so với cách trên bởi vì self._GR = GameResource.getInstance() được gán từ khi khởi tạo.
    """
    __instance          = None

    assetsPath              = 'assets/'
    """ Thư mục chứa toàn bộ tài nguyên của game. """

    birdVariantSet          = [[assetsPath + 'sprites/bird-blue (1).png' ,
                                assetsPath + 'sprites/bird-blue (2).png' ,
                                assetsPath + 'sprites/bird-blue (3).png'],
                               [assetsPath + 'sprites/bird-pink (1).png' ,
                                assetsPath + 'sprites/bird-pink (2).png' ,
                                assetsPath + 'sprites/bird-pink (3).png'],
                               [assetsPath + 'sprites/bird-orange (1).png' ,
                                assetsPath + 'sprites/bird-orange (2).png' ,
                                assetsPath + 'sprites/bird-orange (3).png']]
    """ Các set hình ảnh chim khác nhau. """

    groundVariantSet        =  [assetsPath + 'sprites/ground (1).png',
                                assetsPath + 'sprites/ground (2).png',
                                assetsPath + 'sprites/ground (3).png']
    """ Các set hình ảnh mặt đất khác nhau. """

    pipeVariantSet          =  [assetsPath + 'sprites/pipe-blue.png',
                                assetsPath + 'sprites/pipe-pink.png',
                                assetsPath + 'sprites/pipe-orange.png']
    """ Các set hình ảnh vật cản khác nhau. """

    @staticmethod
    def getInstance():
        if GameResource.__instance == None:
            GameResource.__instance = GameResource()   
            GameResource.__instance.images = {}
            GameResource.__instance.audios = {}
        return GameResource.__instance

    def playSound(self, sound):
        """ Yêu cầu một âm thanh được phát ra, âm thanh đó bắt buộc phải được nạp sẵn. """
        if CanvasMap.getInstance().getFromMap("SettingMenu").soundState == False:
            return
        self.audios[sound].play()

    def load(self):
        """ Nạp tài nguyên game. """
        self.images['gradient_mask'] = pygame.image.load(self.assetsPath + 'sprites/gradient_mask.png').convert_alpha()

        self.images['numbers'] = (                                                                          # Font chu hien thi diem so.
            pygame.image.load(self.assetsPath + 'sprites/num (0).png').convert_alpha(),                          #
            pygame.image.load(self.assetsPath + 'sprites/num (1).png').convert_alpha(),                          #
            pygame.image.load(self.assetsPath + 'sprites/num (2).png').convert_alpha(),                          #
            pygame.image.load(self.assetsPath + 'sprites/num (3).png').convert_alpha(),                          #
            pygame.image.load(self.assetsPath + 'sprites/num (4).png').convert_alpha(),                          #
            pygame.image.load(self.assetsPath + 'sprites/num (5).png').convert_alpha(),                          #
            pygame.image.load(self.assetsPath + 'sprites/num (6).png').convert_alpha(),                          #
            pygame.image.load(self.assetsPath + 'sprites/num (7).png').convert_alpha(),                          #
            pygame.image.load(self.assetsPath + 'sprites/num (8).png').convert_alpha(),                          #
            pygame.image.load(self.assetsPath + 'sprites/num (9).png').convert_alpha())                          #
            
        self.images['1'] = pygame.image.load(self.assetsPath + 'sprites/num (1).png').convert_alpha()
        self.images['2'] = pygame.image.load(self.assetsPath + 'sprites/num (2).png').convert_alpha()
        self.images['3'] = pygame.image.load(self.assetsPath + 'sprites/num (3).png').convert_alpha()
    
        self.images['load_circle']          = pygame.image.load(self.assetsPath + 'sprites/load_circle.png').convert_alpha()
        self.images['loading']              = pygame.image.load(self.assetsPath + 'sprites/loading.png').convert_alpha()

        self.images['intro (1)']            = pygame.image.load(self.assetsPath + 'sprites/intro (1).png').convert_alpha()
        self.images['intro (2)']            = pygame.image.load(self.assetsPath + 'sprites/intro (2).png').convert_alpha()

        self.images['on']                   = pygame.image.load(self.assetsPath + 'sprites/on.png').convert_alpha()
        self.images['off']                  = pygame.image.load(self.assetsPath + 'sprites/off.png').convert_alpha()

        self.images['main_menu_background'] = pygame.image.load(self.assetsPath + 'sprites/main_menu_background.png').convert_alpha()
        self.images['main_menu_logo']       = pygame.image.load(self.assetsPath + 'sprites/main_menu_logo.png').convert_alpha()        
        self.images['main_menu_text']       = pygame.image.load(self.assetsPath + 'sprites/main_menu_text.png').convert_alpha()        
        self.images['setting_menu_text']    = pygame.image.load(self.assetsPath + 'sprites/setting_menu_text.png').convert_alpha()        
        self.images['indicator']            = pygame.image.load(self.assetsPath + 'sprites/indicator.png').convert_alpha()        
       
        self.images['play_menu_background'] = pygame.image.load(self.assetsPath + 'sprites/play_menu_background.png').convert_alpha()
        self.images['play_menu_fog']        = pygame.image.load(self.assetsPath + 'sprites/play_menu_fog.png').convert_alpha()
        self.images['play_menu_text']       = pygame.image.load(self.assetsPath + 'sprites/play_menu_text.png').convert_alpha()

        self.images['gameover']             = pygame.image.load(self.assetsPath + 'sprites/gameover.png').convert_alpha()        
        self.images['ground']               = pygame.image.load(self.assetsPath + 'sprites/ground.png').convert_alpha()    

        self.audios['die']                  = pygame.mixer.Sound(self.assetsPath + 'audio/die.wav')
        self.audios['hit']                  = pygame.mixer.Sound(self.assetsPath + 'audio/hit.wav')        
        self.audios['point']                = pygame.mixer.Sound(self.assetsPath + 'audio/point.wav')    
        self.audios['swoosh']               = pygame.mixer.Sound(self.assetsPath + 'audio/swoosh.wav')   
        self.audios['wing']                 = pygame.mixer.Sound(self.assetsPath + 'audio/wing.wav')     

        # Nạp các hình ảnh chim khác nhau.
        birdImages = []
        for variantIndex in range(0, len(self.birdVariantSet)):
            newArr = []
            for i in range(0, len(self.birdVariantSet[variantIndex])):
                newArr.append(pygame.image.load(self.birdVariantSet[variantIndex][i]).convert_alpha())
            birdImages.append(newArr)
        self.images['birds'] = birdImages

        # Nạp các hình ảnh mặt đất khác nhau.
        groundImages = []
        for variantIndex in range(0, len(self.groundVariantSet)):
            groundImages.append(pygame.image.load(self.groundVariantSet[variantIndex]).convert_alpha())
        self.images['grounds'] = groundImages

        # Nạp các hình ảnh vật cản đất khác nhau.
        pipeImages = []
        for variantIndex in range(0, len(self.pipeVariantSet)):
            pipeImages.append(pygame.image.load(self.pipeVariantSet[variantIndex]).convert_alpha())
        self.images['pipes'] = pipeImages
        
        self.audios['die']    = pygame.mixer.Sound(self.assetsPath + 'audio/die.wav')
        self.audios['hit']    = pygame.mixer.Sound(self.assetsPath + 'audio/hit.wav')        
        self.audios['point']  = pygame.mixer.Sound(self.assetsPath + 'audio/point.wav')    
        self.audios['swoosh'] = pygame.mixer.Sound(self.assetsPath + 'audio/swoosh.wav')   
        self.audios['wing']   = pygame.mixer.Sound(self.assetsPath + 'audio/wing.wav')
        