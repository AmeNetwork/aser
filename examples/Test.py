class A:
    def __init__(self,num):
        self.num=num
a=A(1)
b=a
b.num=2
print(a.num)
