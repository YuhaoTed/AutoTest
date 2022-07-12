import unittest
import time
from playsound import playsound
from Fundament.Pic_Process import *
from Fundament.Snap_shot import *
from Fundament.P_can_test import *
import HTMLTestRunner
import shutil

class Test_Util():

    def __init__(self):
        self.Touch = None
        self.Pic = None
        self.Sc = None
    def Start(self):
        self.Touch = SerialThread()
        self.Pic = Pic_Pro()
        self.Sc = Snap_Shot()
        self.Touch.start()
        self.Sc.Connect()
        self.Sc.Get_png()
    def PrePare_img(self):
        self.Sc.Get_png()
        self.Pic.get_img()

    def Enter_app(self, App_name):
        # print("进入"+App_name)
        self.Sc.Get_png()
        self.Pic.get_img()
        flag = True
        cnt = 0
        coor = None
        while flag and cnt < 5:
            self.Touch.Touch_main()
            time.sleep(0.5)
            self.Sc.Get_png()
            self.Pic.get_img()
            tmp = self.Pic.Pic_OCR()
            for i in tmp:
                if App_name in i:
                    coor = i[0]
                    flag = False
                    break
            cnt += 1
        if coor == None:
            return False
        else:
            # print("kaishidianji app")
            self.Touch.Send_Touch_Command(coor[0][0], coor[0][1])
            time.sleep(1)
            return True

    def Find_Word(self, word,coor=None):
        #[([[209, 21], [285, 21], [285, 65], [209, 65]], '我在', 0.9384478340681012)]
        tmp = self.Pic.Pic_OCR(coor=coor)# y上：y下 ， x左：x右
        x1 = 0
        y1 = 0
        if coor!=None:
            x1 = coor[0][0]
            y1 = coor[0][1]
        for i in tmp:
            for word1 in word:
                if word1 in i[1]:
                    i[0][0][0]+=x1
                    i[0][0][1]+=y1
                    i[0][1][0] += x1
                    i[0][1][1] += y1
                    i[0][2][0] += x1
                    i[0][2][1] += y1
                    i[0][3][0] += x1
                    i[0][3][1] += y1
                    return i[0][0]#[[209, 21], [285, 21], [285, 65], [209, 65]]
        return None
    def Point_Word(self,word,coor=None):
        ret = self.Find_Word(word,coor)
        if ret !=None:
            self.Touch.Send_Touch_Command(ret[0],ret[1])
            return True,'点击成功'
        else:
            return False,'点击失败，未识别'
    def Point_Icon(self,icon,coor=None):
        ret = self.Pic.Pic_Icon('/'+icon)
        if ret !=None:
            self.Touch.Send_Touch_Command(ret[0],ret[1])#x y
            return True,'点击成功'
        else:
            return False,'点击失败，未识别'
    def Add_SC_Report(self, t1):
        # self.PrePare_img()
        shutil.copy('D:\software\pythonProject\SC\\1.PNG',
                    'D:\software\pythonProject\SAVE\\screenpicture' + t1 + '.PNG')
        print("开始截图：")
        print('D:\software\pythonProject\SAVE\\screenpicture' + t1 + '.PNG')

    def Find_Pop(self, Action_word=None):
        self.PrePare_img()
        if self.Pic.Find_Popup():
            if Action_word!=None:
                tmp = self.Find_Word([Action_word])
                if tmp!=None:
                    self.Touch.Send_Touch_Command(tmp[0],tmp[1])
                    print('点击对应文字')
                    return True
                else:
                    print('未找到对应文字')
                    return False
            else:
                print('POP UP 寻找成功')
                return True
        else:
            print('POP UP 寻找失败')
            return False

    def Play_SDS(self,tar):
        playsound(tar)
    def text_comp(self,text1,text2,contain):
        if contain == 1:
            for a in text1:
                if a not in text2:
                    return False
            return True
        else:
            for a in text1:
                if a in text2:
                    return False
            return True
    def icon_comp(self,text1,text2,contain):
        if text1==None or text2==None:
            return False
        if contain == 1:
            #左侧于
            return text1[0]<text2[0]
        elif contain==2:
            # 右侧于
            return text1[0] > text2[0]
        if contain == 3:
            #上于
            return text1[1]>text2[1]
        elif contain==4:
            # 下于
            return text1[1] < text2[1]
#Test_Util_Basic = Test_Util()
global Test_Util1
Test_Util1 = Test_Util()
Test_Util1.Start()

