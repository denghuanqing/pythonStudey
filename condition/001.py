chinese = 50
if chinese > 75:
    print("优秀")
elif chinese > 60:
    print("及格")
else:
    print("不及格")

# -------------------------------------
height = 1.76
weight = 61.5

bmi = weight/(height*height);

if bmi<18.5:
    print("过轻")
elif bmi < 25:
    print("正常")
elif bmi < 28:
    print("过重")
elif bmi < 32:
    print("肥胖")
else:
    print("严重肥胖")