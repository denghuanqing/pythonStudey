# 我将它封装成一个类，使用会比较方便
from PIL import Image, ImageEnhance
import os




class CrackVerCoder(object):
    def __init__(self, path, savePath):
        self.__path = path  # 图片路径
        self.__savePath = savePath  # 图片保存路径
        self.__image = None  # 图片
        self.__pixel = None  # 图片的所有像素点
        self.__width = None  # 图片的宽度
        self.__height = None  # 图片的高度
        self.__subImageDate = None  # 保存切割完的图片的所有数据

    # 封装了处理45fan验证码的操作
    def dealFor45fan(self):
        self.openImage()
        self.binaryzation()
        self.removeInterfer()
        self.simpleSlice()

    # 打开图片
    def openImage(self):
        self.__image = Image.open(self.__path)

    # 二值化
    def binaryzation(self):
        enhancer = ImageEnhance.Contrast(self.__image)
        self.__image = enhancer.enhance(2)  # 图像增强
        self.__image = self.__image.point(lambda x: 0 if x < 160 else 255)  # 简单处理去噪点(这里的160根据你的验证码背景的阈值来筛选)
        self.__image = self.__image.convert('1')  # 转换成灰度图像
        self.__pixel = self.__image.getdata()  # 获取图像的所有像素
        self.__width, self.__height = self.__image.size  # 获取图像的宽高

    # 去干扰线
    def removeInterfer(self):
        whitePoints = 0  # 统计八个方向的白色像素点个数

        # 对第一行进行处理(由于我要识别的验证码字符往往在第一行，所以我单独为它去干扰线)
        for w in range(1, self.__width - 1):
            mid_pixel = self.__pixel[w]
            if mid_pixel == 0:
                fivePixels = [self.__pixel[self.__width + w],
                              self.__pixel[self.__width + w - 1],
                              self.__pixel[self.__width + w + w + 1],
                              self.__pixel[w + 1],
                              self.__pixel[w - 1]]
                for currentPoints in fivePixels:
                    if currentPoints == 255:  # 如果该像素点为白色，则总白色像素点+1
                        whitePoints += 1
                if whitePoints >= 3:  # 如果白色像素点总数大于等于6个则判断为噪点
                        self.__image.putpixel((w, 0), 255)  # 将该黑色像素点变为白色
                whitePoints = 0  # 重新初始化八方位像素点

        for w in range(1, self.__width - 1):  # 扫描所有像素点(去除边界行列，因为它们没有8个方位点)
            for h in range(1, self.__height - 1):  # 按列扫描
                mid_pixel = self.__pixel[self.__width * h + w]  # 带扫描像素点像素值
                if mid_pixel == 0:  # 当该点为黑色时开始扫描八个方位像素
                    eightPixels = [self.__pixel[self.__width * h + w + 1],
                                   self.__pixel[self.__width * h + w - 1],
                                   self.__pixel[self.__width * (h + 1) + w],
                                   self.__pixel[self.__width * (h + 1) + w],
                                   self.__pixel[self.__width * (h + 1) + w + 1],
                                   self.__pixel[self.__width * (h + 1) + w - 1],
                                   self.__pixel[self.__width * (h - 1) + w],
                                   self.__pixel[self.__width * (h - 1) + w + 1],
                                   self.__pixel[self.__width * (h + 1) + w - 1]]
                    for currentPoints in eightPixels:
                        if currentPoints == 255:  # 如果该像素点为白色，则总白色像素点+1
                            whitePoints += 1
                    if whitePoints >= 6:  # 如果白色像素点总数大于等于6个则判断为噪点
                        self.__image.putpixel((w, h), 255)  # 将该黑色像素点变为白色
                    whitePoints = 0  # 重新初始化八方位像素点

    # 简单的切割字符
    def simpleSlice(self):
        # 由于在去干扰线的时候没有对边界进行处理，所以这里直接将右边界和下边界删去
        self.__image = self.__image.crop((0, 0, self.__width - 1, self.__height - 1))

    # 标准切割字符
    def standSlice(self):
        # 垂直切割
        isFirst = True  # 判断需要寻找字符开头还是结尾
        firstColumn = []  # 记录需要截取的当前字符开头列数
        endColumn = []  # 记录需要截取的当前字符结尾列数

        for w in range(0, self.__width - 1):
            column = [self.__pixel[self.__width * h + w] for h in range(0, self.__height - 1)]  # 将同一列的所有像素值存进列表
            if len(set(column)) != 1 and isFirst is True:  # 如果判断字符的开头则执行该步，如果该列同时含有黑白颜色像素点，则代表该列为字符的开头列数
                # 为了保证字符的截取的完全性，略微扩大图像大小
                if w > 2:
                    firstColumn.append(w - 2)
                else:   # 如果是前两列就不需要扩大了
                    firstColumn.append(w)
                isFirst = False  # 下次寻找字符结尾
            elif len(set(column)) == 1 and isFirst is False:  # 如果判断字符的结尾则执行该步，如果该列仅含有白色像素点，则代表该列为字符的结尾列数
                # 为了保证字符的截取的完全性，略微扩大图像大小
                if w < self.__width - 2:
                    endColumn.append(w + 2)
                else:  # 如果是最后两列就不需要扩大了
                    endColumn.append(w)
                isFirst = True  # 下次寻找字符开头

        # 将每个字符的开始与结束列数封装在同一元组中
        finalColumn = [everyStr for everyStr in zip(firstColumn, endColumn)]
        print('column: ', firstColumn, endColumn)

        # 水平切割
        isFirst = True  # 需要寻找字符开头还是结尾
        firstLine = []  # 记录字符开始行数
        endLine = []  # 记录字符结束行数

        for everyStr in finalColumn:  # 在每个字符开始与结尾列直接寻找水平边界
            startColumn, endingColumn = everyStr
            for h in range(0, self.__height - 1):
                line = [self.__pixel[self.__width * h + w] for w in range(startColumn - 1, endingColumn)]  # 将同一列的所有像素值存进列表(startColumn需要减一，因为下标是从0开始的)
                if len(set(line)) != 1 and isFirst is True:  # 如果判断字符的开头则执行该步，如果该行同时含有黑白颜色像素点，则代表该行为字符的开头行数
                    if h > 2:
                        firstLine.append(h - 2)
                    else:
                        firstLine.append(h)
                    isFirst = False  # 下次寻找字符结尾
                elif len(set(line)) == 1 and isFirst is False:  # 如果判断字符的结尾则执行该步，如果该行仅含有白色像素点，则代表该行为字符的结尾行数
                    if h < self.__height - 2:
                        endLine.append(h + 2)
                    else:
                        endLine.append(h)
                    isFirst = True  # 下次寻找字符开头
                    break  # 防止去干扰线时未清理干净影响切割（其实这里只能预防字符下未清理干净，在字符上方未清理感觉这里是无法解决的）

        print('line: ', firstLine, endLine)

        # 将行列组成元组切割字符
        self.__subImageDate = [everyStr for everyStr in zip(firstColumn, firstLine, endColumn, endLine)]
        print('slice: ', self.__subImageDate)

    # 打印所有像素(可以尝试将所有的255都改成1，你可以清晰的看到这几个数字)
    def printPixels(self):
        for h in range(0, self.__height - 1):
            for w in range(0, self.__width - 1):
                print(self.__pixel[self.__width * h + w], end=' ')
            print()

    # 保存处理完的图片
    def saveImage(self):
        self.__image.save(self.__savePath + "/" + 'result.png')

    # 保存切割完的图片
    def saveSubImage(self):
        name = 1
        for everySubImageDate in self.__subImageDate:
            name += 1
            subImage = self.__image.copy()
            subImage = subImage.crop(everySubImageDate)
            subImage.save(self.__savePath + "/" + str(name) + '.png')

    # 显示图片
    def showImage(self):
        self.__image.show()

    # 显示切割完的图片
    def showSubImage(self):
        for everySubImageDate in self.__subImageDate:
            subImage = self.__image.copy()
            subImage = subImage.crop(everySubImageDate)
            subImage.show()

    # 批量处理所有图片,参数为含有图片的文件名与想要转换的后缀名
    def dealFiles(self, directory, suf=".tiff"):
        # 得到文件夹中所有文件名
        files = os.listdir(directory)
        for fileName in files:
            if fileName.endswith("jpg") or fileName.endswith("jpeg") or fileName.endswith("png"):
                self.__image = Image.open(directory + "/" + fileName)
                self.binaryzation()
                self.removeInterfer()
                self.simpleSlice()
                (root, ext) = os.path.splitext(fileName)  # 得到文件名（root不包括后缀名）
                newFilePath = root + suf
                self.__image.save(self.__savePath + "/" + newFilePath)  # 保存为tiff

myCrack = CrackVerCoder(r"C:\\Users\\HP\\Desktop\\123.png", r"C:\\Users\\HP\\Desktop\\123")
myCrack.dealFor45fan();
myCrack.saveImage()