# q2
class ProductionDecisionDP:
    def __init__(self, defect_rate_c1, defect_rate_c2, test_cost_c1,test_cost_c2, cost_c1, cost_c2, cost_product, defect_rate_product, test_cost_product, price, replacement_loss, cost_disassemble, max_product=100):
        # 初始化参数
        self.i = 5
        # 零件c1 c2的购买单价
        self.cost_c1 = cost_c1[self.i]
        self.cost_c2 = cost_c2[self.i]
        # 零件的次品率
        self.defect_rate_c1 = defect_rate_c1[self.i]
        self.defect_rate_c2 = defect_rate_c2[self.i]
        # 零件的检测成本
        self.test_cost_c1 = test_cost_c1[self.i]
        self.test_cost_c2 = test_cost_c2[self.i]
        # 成品的装配成本
        self.cost_product = cost_product[self.i]
        # 成品的检测成本
        self.test_cost_product = test_cost_product[self.i]
        # 成品的次品率
        self.defect_rate_product = defect_rate_product[self.i]
        # 成品的售价
        self.price = price[self.i]
        # 调换损失
        self.replacement_loss = replacement_loss[self.i]
        # 拆解不合格成品的成本
        self.cost_disassemble = cost_disassemble[self.i]

        # 固定需求的成品数量
        self.max_product = max_product

        # 存储决策的数组，[零件1, 零件2]
        # 默认都检测
        self.part_decision = [1, 1]
        # 存储成品，半成品的决策的数组，[是否检测，是否拆解]
        # 两者背反，默认检测，不拆解
        self.com_decision = [1, 0]


    def compute_optimal_profit(self):
        # 计算最低成本和决策路径
        self.com_cost()
        optimal_path = [self.part_decision, self.com_decision]
        max_profit = self.compute_allcost()
        return max_profit, optimal_path
    
    # 计算成品合格率
    # 输入零件的检测决策，为一个二维数组
    # 输出概率
    def posbility(self, dec):
        if (dec[0] == 1 and dec[1] == 1):
            return self.defect_rate_product
        elif (dec[0] == 0 and dec[1] == 1):
            return 1 - (1 - self.defect_rate_product) * (1 - self.defect_rate_c1)
        elif (dec[0] == 1 and dec[1] == 0):
            return 1 - (1 - self.defect_rate_product) * (1 - self.defect_rate_c2)
        else:
            #都不检测
            return 1 - (1 - self.defect_rate_product) * (1 - self.defect_rate_c1) * (1 - self.defect_rate_c2)
    
    # 输出决策到com_decision
    def com_cost(self):
        dec = self.part_decision
        costs = 0
        new_costs = 0
        # 尝试改变零件的决策
        for i in range(0, 2):
            for j in range(0, 2):
                if i == 1 and j == 1:
                    break
                dec = [i, j]
                # 保持成品检测
                dec.append(self.com_decision[0])
                new_costs = self.compute_cost(dec)
                if new_costs > costs:
                    costs = new_costs
                    self.part_decision = [i, j] # 
                else:
                    continue
        # 决定是否检测成品
        dec.append(0)
        new_costs = self.compute_cost(dec)
        if new_costs > costs:
            self.com_decision = [0, 1]
        # 决定是否拆解
        if self.cost_disassemble < (self.cost_c1 + self.cost_c2):
            self.com_decision[1] = 1
        else:
            self.com_decision[1] = 0

    # 计算相对成本
    # 包括两个零件与成品
    def compute_cost(self, dec):
        pos = self.posbility(dec)
        return (self.test_cost_product * (1-dec[2]) + self.test_cost_c1 * dec[0] + self.test_cost_c2 * dec[1] - pos *  self.replacement_loss) * self.max_product

    # 计算总收益
    def compute_allcost(self):
        dec1 = self.part_decision
        dec2 = self.com_decision
        pos = self.posbility(dec1)
        return self.max_product * (self.price - (dec1[0] * self.test_cost_c1 + dec1[1] * self.test_cost_c2 + dec2[0] * (self.test_cost_product+pos*self.replacement_loss) + dec2[1] * self.cost_disassemble+self.cost_product + self.cost_c1/(1-self.defect_rate_c1) + self.cost_c2/(1-self.defect_rate_c1)))

# 实例化生产决策类
production1_dp = ProductionDecisionDP(
    defect_rate_c1=[0.1074,0.2148,0.1074,0.2148,0.1074,0.0536],#[0.0908,0.1924,0.0908,0.1924,0.0908,0.0418],# [0.1, 0.2, 0.1, 0.2, 0.1, 0.05], 
    defect_rate_c2=[0.1074,0.2148,0.1074,0.2148,0.2148,0.0536],#[0.0908,0.1924,0.0908,0.1924,0.1924,0.0418],# [0.1, 0.2, 0.1, 0.2, 0.2, 0.05], 
    test_cost_c1=[2,2,2,1,8,2], 
    test_cost_c2=[3,3,3,1,1,3], 
    cost_c1=[4,4,4,4,4,4], # 零件c1 c2的购买单价不变
    cost_c2=[18,18,18,18,18,18], 
    cost_product=[6,6,6,6,6,6], # 成品装配成本不变
    defect_rate_product=[0.1074,0.2148,0.1074,0.2148,0.1074,0.0536],#[0.0908,0.1924,0.0908,0.1924,0.0908,0.0418],# [0.1, 0.2, 0.1, 0.2, 0.1, 0.05], 
    test_cost_product=[3,3,3,2,2,3], 
    price=[56,56,56,56,56,56], # 成品售价不变
    replacement_loss=[6,6,30,30,10,10], 
    cost_disassemble=[5,5,5,5,5,40])

max_profit, optimal_path = production1_dp.compute_optimal_profit()
print(f"最大总收益: {max_profit}")
print(f"最优决策路径: {optimal_path}")
