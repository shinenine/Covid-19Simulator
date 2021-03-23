class People:
    def __init__(self, x, y, age, token):
        """
        x, y: 表示这个人的坐标
        age: 表示年龄
        hiddenDay: 表示潜伏期
        immune: 表示是否具有抗体
        state: 表示状态(susceptible, infected, removed, dead)四种
        infectedRate: 感染率，取决于该人的年龄和周围人的感染情况
        deathRate: 感染后的致死率,与年龄相关，40岁以下的人群致死率为0，住院会减少致死率
        inRoom : 仍需住院多少天
        roundPeople：周围的有效感染者总数
        isCount: 当这个人新成为患者或者新成为免疫者的时候，置True，在第一次遍历统计后置False，表明后面不需要再以这个身份进行统计数据了
        InHospital: 感染者是否住院，只有住院后才会停止传播
        """
        self.x = x
        self.y = y
        self.age = age
        self.hiddenDay = 0
        self.immune = False
        self.state = "susceptible"
        self.infectedRate = float(0.005 * self.age)
        self.deathRate = 0.0
        self.inRoom = 0
        self.roundPeople = 0
        self.isCount = True
        self.InHospital = False
        self.token = token
        # Susceptible, Infected, Removed, dead
