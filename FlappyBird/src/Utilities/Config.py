
class Config():
    """  
    Đây là lớp đọc ghi các tham số cài đặt và điểm số của game thông qua file. \n
    Do đây là lớp singleton, sẽ chỉ một thể hiện được tạo ra và dùng xuyên suốt chương trình.   
    Trong lớp có một thuộc tính tên là data. Trong đó : \n
        \t data[0] : Cài đặt âm thanh có bật hay không ?
        \t data[1] : Cài đặt tốc độ.
        \t data[2] : Lưu trữ điểm số.
    Mỗi khi ghi vào data, ta cần gọi write() để có thể lưu chúng ra file.
    """
    __instance          = None
    @staticmethod
    def getInstance():
        if Config.__instance == None:
            Config.__instance = Config("assets/config.txt")
        return Config.__instance

    def __init__(self, path):
        self.path = path
        self.data = []

    def read(self):
        """  
        Đọc nội dung nằm trong file config.txt và lưu vào mảng data.
        """
        file = open(self.path, "r")
        lines = file.read().split(',')
        self.data.clear()
        for e in lines:
            self.data.append(int(e))
        file.close()

    def write(self):
        """  
        Ghi dữ liệu nẳm trong data vào config.txt.
        """
        file = open(self.path, "w")
        strData = ''
        for e in self.data:
            if e == '': 
                continue
            strData += str(e) + ','
        strData = strData[0:len(strData)-1]
        file.write(strData)
        file.close()


    