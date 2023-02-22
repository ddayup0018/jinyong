from pymem import Pymem
from pymem.exception import ProcessNotFound
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import configparser
import os
import sys


# 内存读取类
class JinYong:
    def __init__(self):
        self.processName = r'kys_dragon.exe'  
        self.pm = Pymem(self.processName)
        self.baseadd = self.pm.base_address
        print(hex(self.baseadd))

    def read_address(self,address):
        return self.pm.read_short(address)

    def write_value(self,address,value):
        self.pm.write_short(address,value)

    def read_var_address(self):
        add1 = self.pm.read_int(self.baseadd+0x019290A8)
        add2 = add1+0x2
        return add2


# 属性添加函数
def shuxing(address,labelName,row):
    shuxing_obj = tk.IntVar()
    shuxing_obj.set(jy.read_address(address))
    tk.Label(root_window,text=labelName).grid(row=row,column=0)
    tk.Entry(root_window,textvariable=shuxing_obj).grid(row=row,column=1)
    return shuxing_obj

def reboot():
    os.execl(sys.executable, sys.executable, * sys.argv)

# 添加自定义属性事件函数
def add_zidingyi():
    zidingyi_name = askstring('请输入','自定义名称')
    config.set('zidingyi','name',zidingyi_name)

    zidingyi_address = askstring('请输入','内存地址')
    config.set('zidingyi','address',zidingyi_address)

    config.write(open('config.ini','w',encoding='utf-8'))
    reboot()
    

# 确认提交函数
def commit():
    jy.write_value(0x01d29132,gongji.get())
    jy.write_value(0x01d29134,qinggong.get())
    jy.write_value(0x01d29140,quanzhang.get())
    jy.write_value(0x01d29100,shengming.get())
    jy.write_value(0x01d29130,neili.get())
    jy.write_value(0x01d29154,zizhi.get())
    jy.write_value(jinqian_address,jinqian.get())
    if address != '':
        jy.write_value(ini_address,zidingyi_obj.get())
    root_window.update()
    messagebox.showinfo('提示信息','修改成功')

if __name__ == '__main__':
    # 获取配置文件信息
    config = configparser.ConfigParser()
    config.read(r'config.ini',encoding='utf-8')
    name = config.get('zidingyi','name')
    address = config.get('zidingyi','address')

    try:
        jy = JinYong()
        root_window =tk.Tk()
        root_window.title('金庸修改器加强版')
        root_window.geometry('300x240')


        gongji=shuxing(0x01d29132,'攻击',0)
        qinggong= shuxing(0x01d29134,'轻功',1)
        quanzhang=shuxing(0x01d29140,'拳掌',2)
        shengming=shuxing(0x01d29100,'生命',3)
        neili=shuxing(0x01d29130,'内力',4)
        zizhi=shuxing(0x01d29154,'资质',5)


        jinqian_address=jy.read_var_address()
        jinqian = shuxing(jinqian_address,'金钱',6)


        zidingyi_obj = tk.IntVar() 
        if address != '' :
            ini_address = int(address,16)
            zidingyi_obj.set(jy.read_address(ini_address))
        if name == '':
            zidingyi_name = '自定义'
        else:
            zidingyi_name = name

        tk.Label(root_window,text=zidingyi_name).grid(row=7,column=0)
        tk.Entry(root_window,textvariable=zidingyi_obj).grid(row=7,column=1)
        tk.Button(root_window,text='添加自定义',command=add_zidingyi).grid(row=7,column=2)

        tk.Button(root_window,text='确认修改',command=commit).grid(row=8,column=1)
        tk.Button(root_window,text='刷新',command=reboot).grid(row=8,column=2)

        #开启主循环，让窗口处于显示状态
        root_window.mainloop()
    except ProcessNotFound as e :
        print(e)
        messagebox.showinfo('错误信息','未找到游戏进程!')