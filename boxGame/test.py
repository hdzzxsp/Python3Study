import tkinter

wuya = tkinter.Tk()
wuya.title("wuya")
wuya.geometry("300x200+10+20")
# 创建菜单栏下方的菜单条
mubar = tkinter.Menu(wuya)
wuya.config(menu=mubar)
# 添加菜单
# 设置菜单中的内容
mu1 = tkinter.Menu(mubar)
for i in ['上海','北京','广州','海南','天津','退出']:
    if i == '退出':
        # 将内容添加进菜单
        mu1.add_separator()  # 添加分割线
        mu1.add_command(label=i,command=wuya.quit)
    else:
        mu1.add_command(label=i)
# 添加进菜单栏
mubar.add_cascade(label="城市",menu=mu1)

mu2 = tkinter.Menu(mubar,tearoff=0)
mubar.add_cascade(label='帮助',menu=mu2)

wuya.mainloop()
