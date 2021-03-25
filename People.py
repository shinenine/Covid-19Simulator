class People:
    def __init__(self, x, y, token):
        """
        x, y: 表示这个人的坐标
        immune: 表示是否具有抗体
        state: 表示状态(susceptible, infected, removed, dead)四种
        isCount: 当这个人新成为患者或者新成为免疫者的时候，置True，在第一次遍历统计后置False，表明后面不需要再以这个身份进行统计数据了
        InHospital: 感染者是否住院，只有住院后才会停止传播
        rateEtoI:感染率
        """
        self.x = x
        self.y = y
        self.state = "susceptible"
        self.immune = False
        self.InHospital = False
        self.rateEtoI = 0.125  # 潜伏期的倒数
        self.isCount = True
        self.token = token
        # Susceptible, Infected, Removed, dead
