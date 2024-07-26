class test_class:
    def __init__(self,taijuu,sinntyou):
        self.taijuu=taijuu
        self.sinntyou=sinntyou
        print("test_classのコンストラクタが呼ばれました")

    def mbt(self):

        bmi = self.taijuu / (self.sinntyou/100)**2
        print("BMI値は{:.1f}です".format(bmi))
        return bmi  
    
asan=test_class(60,170)
aasddssssssssssssssssssssssssssss
bmi=asan.mbt()