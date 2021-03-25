import random
from decimal import Decimal
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from People import People


class World:

    def __init__(self, bedQuantity, deadRate, reinfected, numberOfPeople):
        """
        坐标系大小 100 x 100
        people_container: 存放people的列表
        bedQuantity: 病床数(100 / 1000)
        deadRate: 致死率(0.005 / 0.01)
        infectedRate: 感染率
        medicine: 康复率
        date:疾病开始爆发后经历的总天数
        latency:潜伏期
        numOfPeopleInfectedMeet患者每天见的人数
        """
        # self.people_container = [] # 用于存放people

        self.numberOfPeople = numberOfPeople
        self.bedQuantity = bedQuantity
        self.peopleInHos = 0
        self.deadRate = deadRate # 0.065373
        self.recoveryRate = 0.23
        self.SUSCEPTIBLE, self.EXPOSED, self.INFECTED, self.REMOVED, self.DEAD = [], [], [], [], []  # 三种人群的数组
        self.date = 0
        self.numOfPeopleInfectedMeet = 10
        self.infectedRate = 0.6
        self.reinfect = reinfected
        self.peopleInfectedRate = 0
        self.susceptibleHistory, self.exposedHistory, self.infectedHistory, self.removedHistory, self.deadHistory =\
            [], [], [], [], []
        self.bedsHistory = []

    def initialize_container(self):
        """
        产生6000个人, 坐标是随机
        """
        for i in range(int(self.numberOfPeople)):
            x = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            y = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            new_people = People(x, y, True)
            self.SUSCEPTIBLE.append(new_people)

        for i in range(2):  # 产生2个零号病人
            x = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            y = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            new_people = People(x, y, False)
            self.INFECTED.append(new_people)

    def UpdateSusInfo(self):
        """
        更新易感人群的基本信息，判断该人是否会成为潜伏者
        """
        count = 0

        for people in self.SUSCEPTIBLE:  # 遍历所有的健康易感人群
            """
            修改易感人群的感染率
            若某易感者没有自主隔离意识，则会移动到其他地方
            """
            if people.token:
                pass
                # people.infectedRate = 0.06 * (1 - self.medicine)
            else:
                deltaX = random.randint(-1, 1)
                deltaY = random.randint(-1, 1)
                people.x += deltaX
                people.y += deltaY

            index = np.random.choice([1, 0], 1,
                                     p=[self.peopleInfectedRate, 1 - self.peopleInfectedRate])  # index 为0，表示不会感染
            if index[0] == 1:
                people.state = 'exposed'
                count += 1
                # print("正常人被感染")

                people.isCount = True
                # 将这个新患者加入到潜伏者队列
                self.EXPOSED.append(people)
                self.SUSCEPTIBLE.remove(people)
        print("疫情爆发第", self.date + 1, "天， 日感染人数：", count)

    def UpdateExpInpo(self):
        count = 0
        for people in self.EXPOSED:
            if people.isCount:
                pass

            toIChoice = np.random.choice([1, 0], 1, p=[people.rateEtoI, 1 - people.rateEtoI])
            if toIChoice[0]:
                people.isCount = True
                people.state = "infected"
                self.INFECTED.append(people)
                self.EXPOSED.remove(people)
                count += 1
        print("疫情爆发第", self.date + 1, "天， 潜伏者爆发人数：", count)

    def updateInfectorInfo(self):
        """
        更新感染者的基本信息，判断感染者是否需要进入医院，以及是否痊愈。感染者的潜伏期遍历时减少一天.致死率会根据初始值，逐步根据当今的医疗水平进行修改。
        同时改变感染者周围的正常人感染概率
        考虑两种传播模式：如果当前爆发的天数小于默认潜伏期，则指数传播，每次两人；如果天数大于，则改为环境影响
        """
        temp_size = len(self.INFECTED)
        for people in self.INFECTED:
            temp_size -= 1
            if temp_size < 0:
                break

            if people.isCount:
                pass

            # 住院的人每天都有概率康复
            if people.InHospital:
                recoChoice = np.random.choice([1, 0], 1, p=[self.recoveryRate, 1 - self.recoveryRate])
                if recoChoice[0]:
                    people.isCount = True
                    people.state = "recovered"
                    if self.reinfect:
                        self.REMOVED.append(people)
                    else:
                        self.SUSCEPTIBLE.append(people)
                    self.INFECTED.remove(people)
                    self.bedQuantity += 1
                    self.peopleInHos -= 1
                    continue

            else:
                if self.bedQuantity > 0:  # 住院成功
                    self.bedQuantity -= 1
                    self.peopleInHos += 1
                    people.InHospital = True
                    # print("住院成功")

            index = np.random.choice([1, 0], 1, p=[self.deadRate, 1 - self.deadRate])  # index 为0，表示不会死亡
            # print(index, "\t", people.infectedRate)

            if index[0] == 1:
                # print("患者死亡...其死亡率此时为", self.deathRate, "年龄为", people.age, "是否死于医院：", people.InHospital)
                people.state = 'dead'
                people.isCount = True
                # people.deathRate = 0
                # people.infectedRate = 0
                if people.InHospital:
                    self.bedQuantity += 1
                    self.peopleInHos -= 1
                self.DEAD.append(people)
                self.INFECTED.remove(people)
                continue

    def UpdateRemInfo(self):
        """
        更新免疫者和死亡人数的信息，即更新其周围人的感染者人数
        """
        for people in self.REMOVED:
            if people.isCount:
                people.isCount = False
                people.immune = True

        for people in self.DEAD:
            if people.isCount:
                people.isCount = False

    def oneDay(self, fig):
        self.Draw(False, fig)
        self.date += 1
        self.peopleInfectedRate = 1 - pow(
            1 - self.numOfPeopleInfectedMeet / (self.numberOfPeople - len(self.DEAD)) * self.infectedRate,
            len(self.INFECTED) - self.peopleInHos)
        if self.date == 7:
            self.deadRate = 0.05373
        if self.date == 14:
            self.deadRate = 0.035373
            self.numOfPeopleInfectedMeet = 8
        if self.date == 28:
            self.numOfPeopleInfectedMeet = 1.5
            self.recoveryRate = 0.95
        if self.date == 42:
            self.numOfPeopleInfectedMeet = 1
            self.deadRate = 0.0173

        print("当前是疫情爆发的第", self.date + 1, "天")
        self.UpdateRemInfo()
        print("治愈人数当前共有", len(self.REMOVED))
        self.removedHistory.append(len(self.REMOVED))
        self.updateInfectorInfo()
        print("当前患者总计人数", len(self.INFECTED))
        self.infectedHistory.append(len(self.INFECTED))
        self.UpdateExpInpo()
        self.UpdateSusInfo()
        print("易感人群总计人数", len(self.SUSCEPTIBLE))
        self.susceptibleHistory.append(len(self.SUSCEPTIBLE))
        print("医院床位还有", self.bedQuantity)
        self.bedsHistory.append(self.bedQuantity)
        print("当前死亡人数为", len(self.DEAD))
        self.deadHistory.append(len(self.DEAD))
        self.exposedHistory.append(len(self.EXPOSED))
        print("\n\n")
        if len(self.INFECTED) <= 0 and len(self.SUSCEPTIBLE) <= 0:
            print("结束")

    # def Happen(self):
    #     self.initialize_container()
    #     self.maxInfect = 2
    #     fig = plt.figure(figsize=(50, 50))
    #     while len(self.INFECTED) > 0 and len(self.SUSCEPTIBLE) > 0:
    #         self.Draw(False, fig)
    #         self.date += 1
    #         self.peopleInfectedRate = 1 - pow(
    #             1 - self.numOfPeopleInfectedMeet / (self.numberOfPeople - len(self.DEAD)) * self.infectedRate,
    #             len(self.INFECTED) - self.peopleInHos)
    #         if self.date == 7:
    #             self.deadRate = 0.05373
    #         if self.date == 14:
    #             self.deadRate = 0.035373
    #             self.numOfPeopleInfectedMeet = 8
    #             self.recoveryRate = 0.95
    #         if self.date == 28:
    #             self.numOfPeopleInfectedMeet = 1.5
    #         if self.date == 42:
    #             self.numOfPeopleInfectedMeet = 1
    #             self.deadRate = 0.0173
    #
    #         print("当前是疫情爆发的第", self.date, "天")
    #         self.UpdateRemInfo()
    #         print("治愈人数当前共有", len(self.REMOVED))
    #         self.updateInfectorInfo()
    #         print("当前患者总计人数", len(self.INFECTED))
    #         self.UpdateExpInpo()
    #         self.UpdateSusInfo()
    #         print("易感人群总计人数", len(self.SUSCEPTIBLE))
    #         print("医院床位还有", self.bedQuantity)
    #         print("当前死亡人数为", len(self.DEAD))
    #         print("\n\n")
    #         if len(self.INFECTED) <= 0 or len(self.SUSCEPTIBLE) <= 0:
    #             print("sleep")
    #             time.sleep(10)
    #             self.Draw(False, fig)
    #         if len(self.INFECTED) > self.maxInfect:
    #             self.maxInfect = len(self.INFECTED)
    #
    #     if len(self.DEAD) >= 6002 or len(self.SUSCEPTIBLE) <= 0:
    #         print("最终所有人都没能逃脱感染和死亡，您的错误决策毁灭了这个世界")
    #         plt.title("最终所有人都没能逃脱感染和死亡，您的错误决策毁灭了这个世界")
    #         plt.show()
    #
    #     else:
    #         print("最终挽回了一切，健康人群还有：", len(self.SUSCEPTIBLE), "死亡人数总计为：", len(self.DEAD), "\t感染总人数当前达到：",
    #               len(self.DEAD + self.REMOVED))

    def Draw(self, choose, fig):
        myFont = FontProperties(fname='HYShangWeiShouShuW.ttf', size=12)
        plt.rcParams['axes.unicode_minus'] = False
        plt.ioff()
        left, bottom, width, height = 0.1, 0.1, 0.8, 0.8

        aGraphic = fig.add_axes([left, bottom, width, height])
        day = "Days:" + str(self.date) + "  S尚未感染人数：" + str(len(self.SUSCEPTIBLE)) + "  E潜伏者人数:" + str(
            len(self.EXPOSED)) + "  I当前患者人数:" + str(len(self.INFECTED)) + "  R当前治愈人数" + str(
            len(self.REMOVED)) + "  D当前死亡人数:" + str(len(self.DEAD))
        aGraphic.set_title(day, fontproperties=myFont)
        npx1, npy1, npx2, npy2, npx3, npy3, npx4, npy4, npx5, npy5 = [], [], [], [], [], [], [], [], [], []
        for people in self.SUSCEPTIBLE:
            npx1.append(people.x)
            npy1.append(people.y)
        for people in self.INFECTED:
            npx2.append(people.x)
            npy2.append(people.y)
        for people in self.REMOVED:
            npx3.append(people.x)
            npy3.append(people.y)
        for people in self.DEAD:
            npx4.append(people.x)
            npy4.append(people.y)
        for people in self.EXPOSED:
            npx5.append(people.x)
            npy5.append(people.y)
        aGraphic.scatter(npx1, npy1, marker="o", color="blue", s=5, label="SUSCEPTIBLE")
        aGraphic.scatter(npx5, npy5, marker="o", color="yellow", s=5, label="EXPOSED")
        aGraphic.scatter(npx2, npy2, marker="o", color="red", s=5, label="INFECTED")
        aGraphic.scatter(npx3, npy3, marker="o", color="green", s=5, label="REMOVED")
        aGraphic.scatter(npx4, npy4, marker="x", color="black", s=5, label="DEAD")
        # ani = animation.FuncAnimation(aGraphic, )
        aGraphic.legend(loc="best")
        if not choose:
            plt.pause(0.5)
            aGraphic.cla()
        # else:
        #     plt.show()
