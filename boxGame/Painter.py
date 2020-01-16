from initGame import *
import tkinter  as tkinter
import tkinter.messagebox as mb
from pygame import mixer
import  os

img = []
mpath = os.path.dirname(__file__)


class Painter():
    def __init__(self, map, mapIndex, step, gateCount):
        self.width = 0
        self.height = 0
        self.boxs = 0
        self.person_x = 0
        self.person_y = 0
        self.person_back = 0
        self.step = step
        self.map = map
        self.mapIndex = mapIndex
        self.gateCount = gateCount
        self.root = tkinter.Tk()
        mixer.init()
        self.mixer = mixer

    def initData(self):
        self.width = 0
        self.height = 0
        self.boxs = 0
        self.person_x = 0
        self.person_y = 0
        self.person_back = 0

    def setMap(self, map):
        self.map = map

    def setDataByMap(self):
        self.initData()
        # 做循环变量
        m, n = 0, 0
        for i in self.map:
            for j in i:
                # 获取宽
                if (n == 0):
                    self.width += 1
                if (j == 3):
                    self.boxs += 1
                if (j == 2 or j == 6):
                    self.person_x = m
                    self.person_y = n
                m += 1
            m = 0
            n += 1
        self.height = n

    def paintMap(self):
        root = self.root
        width = self.width
        height = self.height
        step = self.step
        root.title("欢迎使用推箱子游戏")
        root.geometry(str(width*step) + "x" + str(height*step+30))    # 设置大小
        root.geometry("+400+200")   # 设置上左边距
        root.resizable(0, 0)    # 禁止改变大小
        # 创建菜单
        # mubar = tkinter.Menu(self.root)
        # self.root.config(menu=mubar)
        # 添加菜单
        # 设置菜单中的内容
        # mu1 = tkinter.Menu(mubar)
        # for i in ['重玩','上一关','下一关','退出']:
        #    if i == '退出':
                # 将内容添加进菜单
        #        mu1.add_separator()  # 添加分割线
        #        mu1.add_command(label=i,command=self.root.quit)
        #    else:
        #        mu1.add_command(label=i)

        # 创建一个白色的画板
        self.cv = tkinter.Canvas(root, bg='white', height=height*step, width=width*step)
        self.drawMap()
        # 关联Canvas
        self.cv.pack()
        # 使用Frame增加一层容器
        # fm2 = tkinter.Frame(root, background="blue")
        fm2 = tkinter.Frame(root)
        tkinter.Button(fm2, text='帮助', command=self.openHelp).grid(row = 1, column = 1)
        tkinter.Label(fm2, text=" ").grid(row = 1, column = 2)
        tkinter.Button(fm2, text='重玩一次', command=self.reStart).grid(row = 1, column = 3)
        self.gateLabel = tkinter.Label(fm2, text=" 第"+str(self.mapIndex + 1)+"关 ", background="SkyBlue")
        self.gateLabel.grid(row = 1, column = 4)
        tkinter.Button(fm2, text='上一关', command=self.prevGate).grid(row = 1, column = 5) 
        tkinter.Label(fm2, text=" ").grid(row = 1, column = 6)
        tkinter.Button(fm2, text='下一关', command=self.nextGate).grid(row = 1, column = 7)
        tkinter.Label(fm2, text="  ").grid(row = 1, column = 8)
        tkinter.Button(fm2, text='退出', command=root.quit).grid(row = 1, column = 9)
        fm2.pack()

    def clearCV(self):
        self.cv.delete("all")

    def playSound(self, filename):
        # 播放背景音乐
        mixer = self.mixer
        mixer.music.load(filename)
        mixer.music.play()

    # 定义监听方法
    def move(self, event):
        direction = event.char
        mCursors = event.keycode
        self.updateMapData(direction, mCursors)
        # 清除屏幕
        self.clearCV()
        self.drawMap()
        if(self.boxs == 0):
            self.winner()

    def drawMap(self):
        """用来根据map列表绘制地图"""
        imgLen = 0
        global img
        # 循环变量
        x, y = 0, 0
        for i in self.map:
            for j in list(i):
                lx = x * self.step
                ly = y * self.step

                # 画空白处
                if (j == 0):
                    self.cv.create_rectangle(lx, ly, lx + self.step, ly+self.step, fill="white", width=0)
                # 画墙
                elif (j == 1):
                    img.append(tkinter.PhotoImage(file=mpath+"\\imgs\\wall.png"))
                    self.cv.create_image(lx, ly, anchor=tkinter.NW, image=img[imgLen - 1])
                elif (j == 2):
                    img.append(tkinter.PhotoImage(file=mpath+"\\imgs\\human.png"))
                    self.cv.create_image(lx, ly, anchor=tkinter.NW, image=img[imgLen - 1])
                # 画箱子
                elif (j == 3):
                    img.append(tkinter.PhotoImage(file=mpath+"\\imgs\\box.png"))
                    self.cv.create_image(lx, ly, anchor=tkinter.NW, image=img[imgLen - 1])
                elif (j == 4):
                    img.append(tkinter.PhotoImage(file=mpath+"\\imgs\\terminal.png"))
                    self.cv.create_image(lx, ly, anchor=tkinter.NW, image=img[imgLen - 1])
                elif (j == 5):
                    img.append(tkinter.PhotoImage(file=mpath+"\\imgs\\star.png"))
                    self.cv.create_image(lx, ly, anchor=tkinter.NW, image=img[imgLen - 1])
                elif (j == 6):
                    img.append(tkinter.PhotoImage(file=mpath+"\\imgs\\t_man.png"))
                    self.cv.create_image(lx, ly, anchor=tkinter.NW, image=img[imgLen - 1])
                x += 1
            x = 0
            y += 1

    def updateMapData(self, direction, mCursors):
        map = self.map
        x = self.person_x
        y = self.person_y
        back = self.person_back
        boxs = self.boxs
        # 判断人背后的东西
        # 在空白处的人
        if (map[y][x] == 2):
            self.person_back = 0
        # 在终点上的人
        elif (map[y][x] == 6):
            self.person_back = 4
        # 向上移动
        if(direction == 'w' or mCursors == 38):
            ux, uy = x, y-1
            if(map[uy][ux] == 1):
                return
            # 前方为空白
            if (map[uy][ux] == 0):
                map[uy][ux] = 2
            # 前方为终点
            elif (map[uy][ux] == 4):
                map[uy][ux] = 6

            # 前方为已完成的箱子
            elif (map[uy][ux] == 5):
                if (map[uy - 1][ux] == 3 or map[uy - 1][ux] == 5 or map[uy - 1][ux] == 1):
                    return
                # 已完成前面为空白
                elif (map[uy - 1][ux] == 0):
                    map[uy - 1][ux] = 3
                    map[uy][ux] = 6
                    self.boxs += 1
                elif (map[uy - 1][ux] == 4):
                    map[uy - 1][ux] = 5
                    map[uy][ux] = 6
            # 前方为箱子
            elif (map[uy][ux] == 3):
                # 箱子不能移动
                if (map[uy - 1][ux] == 1 or map[uy - 1][ux] == 3 or map[uy - 1][ux] == 5):
                    return
                # 箱子前方为空白
                elif (map[uy - 1][ux] == 0):
                    map[uy - 1][ux] = 3
                    map[uy][ux] = 2
                # 箱子前方为终点
                elif (map[uy - 1][ux] == 4):
                    map[uy - 1][ux] = 5
                    map[uy][ux] = 2
                    self.boxs -= 1
            map[y][x] = back
            self.person_y = uy
        # 向下移动
        elif(direction == "s" or mCursors == 40):
            ux, uy = x, y + 1
            if (map[uy][ux] == 1):
                return
            # 前方为空白
            if (map[uy][ux] == 0):
                map[uy][ux] = 2
            # 前方为终点
            elif (map[uy][ux] == 4):
                map[uy][ux] = 6

            # 前方为已完成的箱子
            elif (map[uy][ux] == 5):
                if (map[uy + 1][ux] == 3 or map[uy+1][ux] == 5 or map[uy+1][ux] == 1):
                    return
                # 已完成前面为空白
                elif (map[uy+1][ux] == 0):
                    map[uy+1][ux] = 3
                    map[uy][ux] = 6
                    self.boxs += 1
                elif (map[uy+1][ux] == 4):
                    map[uy+1][ux] = 5
                    map[uy][ux] = 6
            # 前方为箱子
            elif (map[uy][ux] == 3):
                # 箱子不能移动
                if (map[uy+1][ux] == 1 or map[uy+1][ux] == 3 or map[uy+1][ux] == 5):
                    return
                # 箱子前方为空白
                elif (map[uy+1][ux] == 0):
                    map[uy+1][ux] = 3
                    map[uy][ux] = 2
                # 箱子前方为终点
                elif (map[uy+1][ux] == 4):
                    map[uy+1][ux] = 5
                    map[uy][ux] = 2
                    self.boxs -= 1
            map[y][x] = back
            self.person_y = uy
        # 向左移动
        elif (direction == "a" or mCursors == 37):
            ux, uy = x-1, y
            if (map[uy][ux] == 1):
                return
            # 前方为空白
            if (map[uy][ux] == 0):
                map[uy][ux] = 2
            # 前方为终点
            elif (map[uy][ux] == 4):
                map[uy][ux] = 6

            # 前方为已完成的箱子
            elif (map[uy][ux] == 5):
                if (map[uy][ux-1] == 3 or map[uy][ux-1] == 5 or map[uy][ux-1] == 1):
                    return
                # 已完成前面为空白
                elif (map[uy][ux-1] == 0):
                    map[uy][ux-1] = 3
                    map[uy][ux] = 6
                    self.boxs += 1
                elif (map[uy][ux-1] == 4):
                    map[uy][ux-1] = 5
                    map[uy][ux] = 6
            # 前方为箱子
            elif (map[uy][ux] == 3):
                # 箱子不能移动
                if (map[uy][ux-1] == 1 or map[uy][ux-1] == 3 or map[uy][ux-1] == 5):
                    return
                # 箱子前方为空白
                elif (map[uy][ux-1] == 0):
                    map[uy][ux-1] = 3
                    map[uy][ux] = 2
                # 箱子前方为终点
                elif (map[uy][ux-1] == 4):
                    map[uy][ux-1] = 5
                    map[uy][ux] = 2
                    self.boxs -= 1
            map[y][x] = back
            self.person_x = ux
        # 向右移动
        elif (direction == "d" or mCursors == 39):
            ux, uy = x + 1, y
            if (map[uy][ux] == 1):
                return
            # 前方为空白
            if (map[uy][ux] == 0):
                map[uy][ux] = 2
            # 前方为终点
            elif (map[uy][ux] == 4):
                map[uy][ux] = 6

            # 前方为已完成的箱子
            elif (map[uy][ux] == 5):
                if (map[uy][ux + 1] == 3 or map[uy][ux + 1] == 5 or map[uy][ux + 1] == 1):
                    return
                # 已完成前面为空白
                elif (map[uy][ux + 1] == 0):
                    map[uy][ux + 1] = 3
                    map[uy][ux] = 6
                    boxs += 1
                elif (map[uy][ux + 1] == 4):
                    map[uy][ux + 1] = 5
                    map[uy][ux] = 6
            # 前方为箱子
            elif (map[uy][ux] == 3):
                # 箱子不能移动
                if (map[uy][ux + 1] == 1 or map[uy][ux + 1] == 3 or map[uy][ux + 1] == 5):
                    return
                # 箱子前方为空白
                elif (map[uy][ux + 1] == 0):
                    map[uy][ux + 1] = 3
                    map[uy][ux] = 2
                # 箱子前方为终点
                elif (map[uy][ux + 1] == 4):
                    map[uy][ux + 1] = 5
                    map[uy][ux] = 2
                    self.boxs -= 1
            map[y][x] = back
            self.person_x = ux

    def startPlay(self):
        # 播放声音
        soundname = mpath+'\\bgm.mp3'
        self.playSound(soundname)
        self.root.bind("<Key>", self.move)
        self.root.mainloop()

    def reStart(self):
        # 播放声音
        soundname = mpath+'\\bgm.mp3'
        painter.playSound(soundname)
        self.map = getMap(self.mapIndex)
        self.reDrawByMap()

    def nextGate(self):
        self.mapIndex = self.mapIndex+1 if self.mapIndex+1 < self.gateCount else self.mapIndex
        self.map = getMap(self.mapIndex)
        self.reDrawByMap()

    def reDrawByMap(self):
        # 清除屏幕
        self.clearCV()
        self.setDataByMap()
        self.drawMap()
        self.gateLabel["text"] = " 第"+str(self.mapIndex+1)+"关 "

    def prevGate(self):
        self.mapIndex = self.mapIndex-1 if (self.mapIndex-1) > 0 else 0
        self.map = getMap(self.mapIndex)
        self.reDrawByMap()

    def winner(self):
        a = tkinter.messagebox.askokcancel('提示信息', '恭喜您，您赢了！\n 您要继续挑战下一关？')
        if a:
            self.nextGate()

    def openHelp(self):
        tkinter.messagebox.showinfo("帮助提示","可以通过光标键控制移动")
