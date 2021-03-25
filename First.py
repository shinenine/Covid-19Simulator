from World import World
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt


def startSimulate():
    _bedQuantities = int(bedQuantities.get())
    _deadRate = float(deadRate.get())
    _numberOfPeople = int(numberOfPeople.get())
    start = World(_bedQuantities, _deadRate, reinfected, _numberOfPeople)  # 床位，杀伤力，治愈者是否带有抗体
    start.initialize_container()
    fig = plt.figure(figsize=(10, 10))
    start.oneDay(fig)

    def nextDay():
        start.oneDay(fig)

    def auto():
        while True:
            start.oneDay(fig)

    nextDay = tk.Button(window, text='nextDay', width=10, height=1, command=nextDay)
    nextDay.grid(row=6, column=0, padx=10, pady=10)
    auto = tk.Button(window, text='auto', width=10, height=1, command=auto)
    auto.grid(row=6, column=1, padx=10, pady=10)


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Simulator')
    window.geometry('500x300')

    tk.Label(window, text='医院容量').grid(row=0, padx=50)
    bedQuantities = tk.Entry(window, width=30)
    bedQuantities.grid(row=0, column=1, padx=10, pady=10)
    bedQuantities.insert(0, "100")

    tk.Label(window, text='病毒杀伤力').grid(row=1)
    deadRate = tk.Entry(window, width=30)
    deadRate.grid(row=1, column=1, padx=10, pady=10)
    deadRate.insert(0, "0.001")

    tk.Label(window, text='治愈者是否有抗体').grid(row=2)
    reinfected = tk.BooleanVar
    choice = ttk.Combobox(window, width=28, textvariable=reinfected)
    choice['values'] = (True, False)
    choice.grid(row=2, column=1, padx=10, pady=10)
    choice.current(0)
    #
    # tk.Label(window, text='患者具有自我隔离意识的初始比例').grid(row=3)
    # quarantineRatio = tk.Entry(window, width=30)
    # quarantineRatio.grid(row=3, column=1, padx=10, pady=10)
    # quarantineRatio.insert(0, "0.33")

    tk.Label(window, text='模拟的总人数').grid(row=3)
    numberOfPeople = tk.Entry(window, width=30)
    numberOfPeople.grid(row=3, column=1, padx=10, pady=10)
    numberOfPeople.insert(0, "6000")

    b = tk.Button(window, text='start simulating', width=15, height=1, command=startSimulate)
    b.grid(row=4, column=1, padx=10, pady=10)

    window.mainloop()
