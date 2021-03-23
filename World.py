import random
from decimal import Decimal
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from People import People


def DistanceCount(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


class World:

    def __init__(self, bedQuantity, deadRate, reinfected, quarantineRatio, numberOfPeople):
        """
        坐标系大小 100 x 100
        people_container: 存放people的列表
        bedQuantity: 病床数(100 / 1000)
        deadRate: 致死率(0.005 / 0.01)
        infectedRate: 感染率
        medicine: 康复率
        date:疾病开始爆发后经历的总天数
        quarantineRation:有自我隔离意识的人群比率
        """
        # self.people_container = [] # 用于存放people
        self.bedQuantity = bedQuantity
        self.deadRate = deadRate
        self.reinfect = reinfected
        self.SUSCEPTIBLE, self.INFECTED, self.REMOVED, self.DEAD = [], [], [], []  # 三种人群的数组
        self.date = 0
        self.medicine = 0.02
        self.quarantineRatio = quarantineRatio
        self.numberOfPeople = numberOfPeople

    def initialize_container(self):
        """
        产生6000个人, 坐标, 年龄都是随机
        """
        for i in range(int(self.numberOfPeople * self.quarantineRatio)):
            x = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            y = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            age = random.randint(1, 80)
            new_people = People(x, y, age, True)
            self.SUSCEPTIBLE.append(new_people)
        for i in range(int(self.numberOfPeople * (1 - self.quarantineRatio))):
            x = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            y = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            age = random.randint(1, 80)
            new_people = People(x, y, age, False)
            self.SUSCEPTIBLE.append(new_people)
        for i in range(2):  # 产生两个零号病人
            x = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            y = Decimal(random.uniform(0, 100)).quantize(Decimal("0.0"))
            age = 40
            new_people = People(x, y, age, True)
            new_people.hiddenDay = 4
            new_people.deathRate = 0
            self.INFECTED.append(new_people)

    def UpdateSusInfo(self):
        """
        更新易感人群的基本信息，判断该人是否会成为感染者，并为其随机生成一个固定范围内的潜伏日期.初始化的住院日期由当天的医疗水平决定
        """
        count = 0
        for people in self.SUSCEPTIBLE:  # 遍历所有的健康易感人群
            """
            修改易感人群的感染率
            若某易感者没有自主隔离意识，则会移动到其他地方
            """
            if people.token:
                people.infectedRate = 0.06 * (1 - self.medicine)
            else:
                deltaX = random.randint(-1, 1)
                deltaY = random.randint(-1, 1)
                people.x += deltaX
                people.y += deltaY
                if 0.01 * people.age >= 0.1:
                    people.infectedRate = (0.01 * people.age) * pow(1.07, people.roundPeople) * (1 - self.medicine)
                else:
                    people.infectedRate = 0.1 * pow(1.07, people.roundPeople) * (1 - self.medicine)
            if people.infectedRate >= 0.8:
                people.infectedRate = 0.8
            elif people.infectedRate < 0:
                people.infectedRate = 0
            if people.roundPeople <= 0:
                people.infectedRate = 0
            # 当易感者周围的患病者大于1时，易感者就有了自我隔离意识，不再移动
            if people.roundPeople > 1:
                people.token = True
            index = np.random.choice([1, 0], 1, p=[people.infectedRate, 1 - people.infectedRate])  # index 为0，表示不会感染

            if index[0] == 1:
                people.state = 'infected'
                print("正常人被感染")
                if people.roundPeople >= 1:
                    print("\n感染者的感染率：", people.infectedRate, "周围人数：", people.roundPeople, "\n")
                count += 1
                people.hiddenDay = random.randrange(4, 7)  # 生成一个随机的潜伏日期
                if people.age > 40:  # 致死率初始化
                    people.deathRate = float(self.deadRate * people.age / 10)
                people.inRoom = int(0.2 * people.age)
                people.isCount = True
                # 将这个新患者加入到感染者队列
                self.INFECTED.append(people)
                self.SUSCEPTIBLE.remove(people)
        print("疫情爆发第", str(self.date + 1), "天， 日感染人数：", str(count))

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
            # 每过一天，感染者的潜伏日期或者住院日期减少一天
            if people.InHospital:
                people.inRoom -= 1
                if people.inRoom <= 0:  # 痊愈
                    people.isCount = True
                    people.deathRate = 0.1
                    people.infectedRate = 0.4
                    if self.reinfect:
                        self.REMOVED.append(people)
                    else:
                        self.SUSCEPTIBLE.append(people)
                    self.INFECTED.remove(people)
                    self.bedQuantity += 1
                    continue
                else:
                    pass

            else:
                people.hiddenDay -= 1
                if people.hiddenDay <= 0:
                    if self.bedQuantity > 0:  # 住院成功
                        self.bedQuantity -= 1
                        people.InHospital = True
                    else:
                        people.hiddenDay = 1

            index = np.random.choice([1, 0], 1, p=[people.deathRate, 1 - people.deathRate])  # index 为0，表示不会死亡

            if index[0] == 1:
                print("患者死亡...其死亡率此时为", people.deathRate, "年龄为", people.age, "是否死于医院：", people.InHospital)
                people.state = 'dead'
                people.isCount = True
                # people.deathRate = 0
                # people.infectedRate = 0
                if people.InHospital:
                    self.bedQuantity += 1
                self.DEAD.append(people)
                self.INFECTED.remove(people)
                continue

            else:  # 患者存活，则修改病人的死亡率,同时进行疾病传播
                if people.hiddenDay > 0 and people.age > 40:  # 针对40岁以上，仍处于潜伏期的人，死亡率增高
                    people.deathRate += self.deadRate
                elif people.hiddenDay <= 0 and people.age > 40:  # 针对40岁以上且已经住院的人
                    people.deathRate = self.deadRate * people.age / 10

                if self.date < 4 and people.InHospital is False:  # 4为默认的第一潜伏期时间
                    temp_count = 2
                    for survival in self.SUSCEPTIBLE:  # 指数传播,每次感染有效距离内最多两个人
                        if DistanceCount(people.x, people.y, survival.x, survival.y) <= 10:
                            survival.state = "infected"
                            survival.hiddenDay = random.randrange(6, 12)
                            if people.age > 40:  # 致死率更新
                                people.deathRate = float(0.001 * people.age)
                            people.inRoom = 20 * people.age * 0.01
                            # 将这个新患者加入到感染者队列
                            self.INFECTED.append(survival)
                            self.SUSCEPTIBLE.remove(survival)

                            temp_count -= 1
                            if temp_count <= 0:
                                break

                if (self.date >= 4) and people.isCount and (people.InHospital is False):
                    people.isCount = False
                    for survival in self.SUSCEPTIBLE:
                        if DistanceCount(people.x, people.y, survival.x, survival.y) <= 3.0:
                            survival.roundPeople += 1

    def UpdateRemInfo(self):
        """
        更新免疫者和死亡人数的信息，即更新其周围人的感染者人数
        """
        for people in self.REMOVED:
            if people.isCount:
                people.isCount = False
                people.immune = True
                people.state = 'removed'
                for survival in self.SUSCEPTIBLE:
                    if DistanceCount(people.x, people.y, survival.x, survival.y) <= 3:
                        if survival.roundPeople >= 1:
                            survival.roundPeople -= 1

        for people in self.DEAD:
            if people.isCount:
                people.isCount = False
                for survival in self.SUSCEPTIBLE:
                    if DistanceCount(people.x, people.y, survival.x, survival.y) <= 3:
                        if survival.roundPeople >= 1:
                            survival.roundPeople -= 1

    def OneDay(self):
        self.initialize_container()
        fig = plt.figure(figsize=(10, 10))
        self.Draw(False, fig)
        self.date += 1
        print("当前是疫情爆发的第", self.date, "天")
        self.UpdateRemInfo()
        print("治愈人数当前共有", len(self.REMOVED))
        self.updateInfectorInfo()
        print("当前患者总计人数", len(self.INFECTED))
        self.UpdateSusInfo()
        if self.medicine < 1:
            self.medicine += 0.01
        print("易感人群总计人数", len(self.SUSCEPTIBLE))
        print("医院床位还有", self.bedQuantity)
        print("当前死亡人数为", len(self.DEAD))
        print("\n\n")
        if len(self.INFECTED) <= 0 or len(self.SUSCEPTIBLE) <= 0:
            print("sleep")
            time.sleep(10)
            self.Draw(False)

    def Happen(self):
        self.initialize_container()
        self.maxInfect = 2
        fig = plt.figure(figsize=(10, 10))
        while len(self.INFECTED) > 0 and len(self.SUSCEPTIBLE) > 0:
            self.Draw(False, fig)
            self.date += 1
            print("当前是疫情爆发的第", self.date, "天")
            self.UpdateRemInfo()
            print("治愈人数当前共有", len(self.REMOVED))
            self.updateInfectorInfo()
            print("当前患者总计人数", len(self.INFECTED))
            self.UpdateSusInfo()
            if self.medicine < 1:
                self.medicine += 0.01
            print("易感人群总计人数", len(self.SUSCEPTIBLE))
            print("医院床位还有", self.bedQuantity)
            print("当前死亡人数为", len(self.DEAD))
            print("\n\n")
            if len(self.INFECTED) <= 0 or len(self.SUSCEPTIBLE) <= 0:
                print("sleep")
                time.sleep(10)
                self.Draw(False)
            if len(self.INFECTED) > self.maxInfect:
                self.maxInfect = len(self.INFECTED)

        if len(self.DEAD) >= 6002 or len(self.SUSCEPTIBLE) <= 0:
            print("最终所有人都没能逃脱感染和死亡，您的错误决策毁灭了这个世界")
            plt.title("最终所有人都没能逃脱感染和死亡，您的错误决策毁灭了这个世界")
            plt.show()

        else:
            print("最终挽回了一切，健康人群还有：", len(self.SUSCEPTIBLE), "死亡人数总计为：", len(self.DEAD), "\t感染总人数当前达到：",
                  len(self.DEAD + self.REMOVED))

    def Draw(self, choose, fig):
        myFont = FontProperties(fname='HYShangWeiShouShuW.ttf', size=15)
        plt.rcParams['axes.unicode_minus'] = False
        left, bottom, width, height = 0.1, 0.1, 0.8, 0.8

        aGraphic = fig.add_axes([left, bottom, width, height])
        day = "Days:" + str(self.date + 1) + "  当前患者人数:" + str(len(self.INFECTED)) + "  当前死亡人数:" + str(
            len(self.DEAD)) + "  尚未感染人数：" + str(len(self.SUSCEPTIBLE)) + "  治愈人数：" + str(len(self.REMOVED))
        aGraphic.set_title(day, fontproperties=myFont)
        npx1, npy1, npx2, npy2, npx3, npy3, npx4, npy4 = [], [], [], [], [], [], [], []
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
        aGraphic.scatter(npx1, npy1, marker="o", color="blue", s=5, label="SUSCEPTIBLE")
        aGraphic.scatter(npx2, npy2, marker="o", color="red", s=5, label="INFECTED")
        aGraphic.scatter(npx3, npy3, marker="o", color="green", s=5, label="REMOVED")
        aGraphic.scatter(npx4, npy4, marker="x", color="black", s=5, label="DEAD")
        aGraphic.legend(loc="best")
        if not choose:
            plt.pause(1)
            aGraphic.cla()
        # else:
        #     plt.show()
