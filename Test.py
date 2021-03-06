import tkinter as tk
from tkinter import ttk
from World import World
import keyboard
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import MultipleLocator


def main():
    b['state'] = tk.DISABLED
    _bedQuantities = int(bedQuantities.get())
    _deadRate = float(deadRate.get())
    _reinfected = float(reinfected.get())
    _numberOfPeople = int(numberOfPeople.get())
    start = World(_bedQuantities, _deadRate, _reinfected, _numberOfPeople, hospitalLevel, quarantineRatio)
    # 床位，杀伤力，治愈者是否带有抗体,总人数，医院治疗能力，隔离等级
    start.initialize_container()
    fig = plt.figure(figsize=(10, 10))
    start.oneDay(fig)

    def nextDay():
        start.oneDay(fig)

    """
    使用多线程 matplotlib只能在主线程中绘图 
    使用多进程 多进程无法共享内存
    因此使用键盘监听 实现暂停操作
    """

    def run():
        global flag
        flag = 0
        while flag == 0:
            start.oneDay(fig)
            keyboard.hook(pause)
            if (len(start.INFECTED) <= 0 and len(start.EXPOSED) <= 0) \
                    or (len(start.REMOVED) <= 0 and len(start.SUSCEPTIBLE) <= 0):
                break
        autoButton.config(state=tk.NORMAL)

    def pause(x):
        global flag
        flag = 1

    nextDay = tk.Button(window, text='nextDay', width=10, height=1, command=nextDay)
    nextDay.grid(row=13, column=0, padx=8, pady=10)
    autoButton = tk.Button(window, text='auto', width=10, height=1, command=run)
    autoButton.grid(row=13, column=1, padx=8, pady=10)

    def showSus():
        plt.figure()
        plt.ion()
        myFont = FontProperties(fname='HYShangWeiShouShuW.ttf', size=12)
        plt.title('易感者数量折线图', fontproperties=myFont)
        plt.plot(start.susceptibleHistory, marker='o', color="blue")
        plt.xlim(0, None)
        plt.ylim(0, 6000)
        plt.ylabel("易感者数量", fontproperties=myFont)
        plt.xlabel("天数", fontproperties=myFont)
        plt.show()

    def showExp():
        plt.figure()
        plt.ion()
        myFont = FontProperties(fname='HYShangWeiShouShuW.ttf', size=12)
        plt.title('潜伏者数量折线图', fontproperties=myFont)
        plt.plot(start.exposedHistory, marker='o', color="blue")
        plt.xlim(0, None)
        plt.ylim(0, None)
        plt.ylabel("潜伏着数量", fontproperties=myFont)
        plt.xlabel("天数", fontproperties=myFont)
        plt.show()

    def showInfected():
        plt.figure()
        plt.ion()
        myFont = FontProperties(fname='HYShangWeiShouShuW.ttf', size=12)
        plt.title('感染者数量折线图', fontproperties=myFont)
        plt.plot(start.infectedHistory, marker='o', color="blue")
        plt.xlim(0, None)
        plt.ylim(0, None)
        plt.ylabel("感染者数量", fontproperties=myFont)
        plt.xlabel("天数", fontproperties=myFont)
        plt.show()

    def showRemoved():
        plt.figure()
        plt.ion()
        myFont = FontProperties(fname='HYShangWeiShouShuW.ttf', size=12)
        plt.title('治愈者数量折线图', fontproperties=myFont)
        plt.plot(start.removedHistory, marker='o', color="blue")
        plt.xlim(0, None)
        plt.ylim(0, None)
        plt.ylabel("治愈者数量", fontproperties=myFont)
        plt.xlabel("天数", fontproperties=myFont)
        plt.show()

    def showDead():
        plt.figure()
        plt.ion()
        myFont = FontProperties(fname='HYShangWeiShouShuW.ttf', size=12)
        plt.title('死亡者数量折线图', fontproperties=myFont)
        plt.plot(start.deadHistory, marker='o', color="blue")
        plt.xlim(0, None)
        plt.ylim(0, None)
        plt.ylabel("死亡者数量", fontproperties=myFont)
        plt.xlabel("天数", fontproperties=myFont)
        plt.show()

    def showBeds():
        plt.figure()
        plt.ion()
        myFont = FontProperties(fname='HYShangWeiShouShuW.ttf', size=12)
        plt.title('床位剩余数量折线图', fontproperties=myFont)
        plt.plot(start.bedsHistory, marker='o', color="blue")
        plt.xlim(0, None)
        plt.ylim(0, None)
        plt.ylabel("床位剩余数量", fontproperties=myFont)
        plt.xlabel("天数", fontproperties=myFont)
        plt.show()

    sus = tk.Button(window, text='易感者', width=10, height=1, command=showSus)
    sus.grid(row=14, column=0, padx=5, pady=10)
    exposed = tk.Button(window, text='潜伏者', width=10, height=1, command=showExp)
    exposed.grid(row=14, column=1, padx=5, pady=10)
    infect = tk.Button(window, text='感染者', width=10, height=1, command=showInfected)
    infect.grid(row=15, column=0, padx=5, pady=10)
    removed = tk.Button(window, text='治愈者', width=10, height=1, command=showRemoved)
    removed.grid(row=15, column=1, padx=5, pady=10)
    death = tk.Button(window, text='死亡者', width=10, height=1, command=showDead)
    death.grid(row=16, column=0, padx=5, pady=10)
    beds = tk.Button(window, text='医院床位剩余', width=10, height=1, command=showBeds)
    beds.grid(row=16, column=1, padx=5, pady=10)


if __name__ == '__main__':
    flag = 0
    window = tk.Tk()
    window.title('Simulator')
    window.geometry('500x500')

    tk.Label(window, text='医院容量').grid(row=0, padx=50)
    bedQuantities = tk.Entry(window, width=30)
    bedQuantities.grid(row=0, column=1, padx=10, pady=10)
    bedQuantities.insert(0, "100")

    tk.Label(window, text='病毒杀伤力').grid(row=1)
    deadRate = tk.Entry(window, width=30)
    deadRate.grid(row=1, column=1, padx=10, pady=10)
    deadRate.insert(0, "0.001")

    tk.Label(window, text='治愈者获得抗体的比率').grid(row=2)
    reinfected = tk.Entry(window, width=30)
    reinfected.grid(row=2, column=1, padx=10, pady=10)
    reinfected.insert(0, "0.5")

    tk.Label(window, text='医院治疗水平').grid(row=3)
    hospitalLevel = tk.StringVar
    choice = ttk.Combobox(window, width=28, textvariable=hospitalLevel)
    choice['values'] = ('High', 'Middle', 'Low')
    choice.grid(row=3, column=1, padx=10, pady=10)
    choice.current(0)

    tk.Label(window, text='人群隔离意识').grid(row=11)
    quarantineRatio = tk.StringVar
    choice = ttk.Combobox(window, width=28, textvariable=hospitalLevel)
    choice['values'] = ('High', 'Middle', 'Low')
    choice.grid(row=11, column=1, padx=10, pady=10)
    choice.current(0)

    tk.Label(window, text='模拟的总人数').grid(row=10)
    numberOfPeople = tk.Entry(window, width=30)
    numberOfPeople.grid(row=10, column=1, padx=10, pady=10)
    numberOfPeople.insert(0, "6000")

    b = tk.Button(window, text='start simulating', width=15, height=1, command=main)
    b.grid(row=12, column=1, padx=10, pady=10)

    window.mainloop()
