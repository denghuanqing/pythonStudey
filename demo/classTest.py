# 定义汽车类
class Car:

    def __init__(self, newWheelNum, newColor):
        self.wheelNum = newWheelNum
        self.color = newColor

    def move(self):
        print('车在跑，目标:夏威夷')

# 创建对象
BMW = Car(4, 'green')

print('车的颜色为:%s'%BMW.color)
print('车轮子数量为:%d'%BMW.wheelNum)