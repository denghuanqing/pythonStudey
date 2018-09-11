def printInfo(obj):
    print ('------------------------------------')
    print ('         人生苦短，我用Python')
    print ('------------------------------------')
    print(len(obj))

def sum(a,b):
   ''' 用来完成对2个数求和 '''
   return a+b

num =sum(5,6)
print(num)
help(sum)


stu_a = {
        "name":"A",
        "age":21,
        "gender":1,
        "hometown":"河北"
}
