import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# q3
# 动态规划

class ProductDecisionDP:
    def __init__(self, defect_rate, unit_price, test_cost, semi_prod_defect_rate, semi_prod_load_cost, semi_prod_test_cost, semi_prod_disa_cost, prod_defect_rate, prod_load_cost, prod_test_cost, prod_disa_cost, price, replacement_loss, max_product = 100):
        # 零件的次品率
        self.defect_rate = defect_rate 
        self.unit_price = unit_price
        self.test_cost = test_cost
        # 半成品
        self.semi_prod_defect_rate = semi_prod_defect_rate
        self.semi_prod_load_cost = semi_prod_load_cost
        self.semi_prod_test_cost = semi_prod_test_cost
        self.semi_prod_disa_cost = semi_prod_disa_cost
        # 成品
        self.prod_defect_rate = prod_defect_rate
        self.prod_load_cost = prod_load_cost
        self.prod_test_cost = prod_test_cost
        self.prod_disa_cost = prod_disa_cost
        self.price = price
        self.replacement_loss = replacement_loss
        
        # 固定需求的成品数量
        self.max_product = max_product
        # 初始化决策
        self.part_decision = []
        self.semi_decision = []
        self.decision = []
        
        self.f1 = []
        self.f2 = []
        self.f3 = []
        self.fsum = []
        self.profit = []

    def test_part(self):
        temp = 100000
        count1 = count2 = count3 = 0
        # 零件的决策
        for i in range(0, 2**8):
            decision1 = self.num2bin(i, 8)
            pos1 = self.semi_dr(decision1) # 半成品的次品率
            count1 += 1
            # 半成品的决策
            for j in range(0, 2**6): 
                decision2 = self.num2bin(j, 6)
                pos2 = self.prod_dr(decision2, pos1) # 成品的次品率
                count2 += 1
                # 成品的决策
                for k in range(0, 4):
                    decision3 = self.num2bin(k, 2)
                    self.f1.append(self.compute_stf1(decision1)) # 记录该决策的绝对成本
                    self.f2.append(self.compute_stf2(decision2, pos1)) # 记录 
                    self.f3.append(self.compute_stf3(decision3, pos2))
                    self.fsum.append(self.f1[count3]+self.f2[count3]+self.f3[count3]) # 总绝对成本
                    self.profit.append(self.income(count3))
                   
                    if self.fsum[count3] < temp: # 成本越小越好
                        # 记录
                        temp = self.fsum[count3]
                        count = [count1, count2, count3]
                        self.part_decision = decision1
                        self.semi_decision = decision2
                        self.decision = decision3
                    
                    count3 += 1

        min_cost = temp
        max_profit = self.profit[count[2]]
        optimal_path = [self.part_decision, self.semi_decision, self.decision]
        # 导出数据
        max_len = max(len(self.f1), len(self.f2), len(self.f3), len(self.fsum), len(self.profit))
        with open('output.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["f1", "f2", "f3", "fsum", "profit"])
            for i in range(max_len):
                row = [
                    self.f1[i] if i < len(self.f1) else '',
                    self.f2[i] if i < len(self.f2) else '',
                    self.f3[i] if i < len(self.f3) else '',
                    self.fsum[i] if i < len(self.fsum) else '',
                    self.profit[i] if i < len(self.profit) else ''
                ]
                writer.writerow(row)

        return min_cost, max_profit, optimal_path
    
    def Heatmap(self):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        img = ax.scatter(self.f1, self.f2, self.f3, c=self.profit, cmap='hot')

        colorbar = plt.colorbar(img, ax=ax, label='Profit')
        ax.set_xlabel('cost1')
        ax.set_ylabel('cost2')
        ax.set_zlabel('cost3')
        
        plt.show()
    
    def income(self, i):
        # 计算收益
        return self.max_product * (self.price - self.fsum[i])

    def num2bin(self, i, n):
        # 转化为决策标识
        binary_str = bin(i)[2:]
        bin_array = [int(bit) for bit in binary_str]
        return [0]*(n - len(bin_array)) + bin_array

    def semi_dr(self, dec):
        # 计算半成品不合格率
        # 返回一个三维数组
        pos = []
        for i in range(0,8):
            if dec[i] == 0:
                pos.append(1-self.defect_rate[i])
            else:
                pos.append(1)
        pos1 = 1 - (1-self.semi_prod_defect_rate[0])*pos[0]*pos[1]*pos[2]
        pos2 = 1 - (1-self.semi_prod_defect_rate[1])*pos[3]*pos[4]*pos[5]
        pos3 = 1 - (1-self.semi_prod_defect_rate[2])*pos[6]*pos[7]
        return [pos1, pos2, pos3]
    
    def prod_dr(self, dec, pos):
        # 计算成品的不合格率
        e = []
        for i in range(0,3):
            if dec[i] == 0:
                e.append(1-pos[i])
            elif dec[i] == 1:
                e.append(1)
            else:
                print("error prod_dr")
        return 1 - (1-self.prod_defect_rate)*e[0]*e[1]*e[2]
    
    def compute_stf1(self, dec):
        # 计算零件的总的绝对成本
        exp = []
        cost1 = cost2 = 0
        for i in range(0,8):
            cost1 = cost1 + self.test_cost[i]*dec[i]
            if dec[i] == 0:
                exp.append(1)
            elif dec[i] == 1:
                exp.append(1/(1-self.defect_rate[i]))
            cost2 = cost2 + self.unit_price[i] * exp[i]
        return cost1 + cost2

    def compute_stf2(self, dec, pos):
        # 计算半成品的总的绝对成本
        exp = []
        cost1 = cost2 = cost3 = 0
        u_price = [self.unit_price[0]+self.unit_price[1]+self.unit_price[2],self.unit_price[3]+self.unit_price[4]+self.unit_price[5], self.unit_price[6]+self.unit_price[7]]
        for i in range(0,3):
            cost1 = cost1 + self.semi_prod_load_cost[i] # 装配成本
            if dec[i] == 0:
                exp.append(0)
            elif dec[i] == 1:
                exp.append(pos[i])
            cost2 = cost2 + self.semi_prod_test_cost[i] * dec[i] # 检测成本
            if (dec[i] + dec[i+3]) == 2:
                # 如果同时选择测试和拆解，包含得到的零件成本
                cost3 = cost3 + (self.semi_prod_disa_cost[i] - u_price[i]) * exp[i]
        return cost1 + cost2 + cost3

    def compute_stf3(self, decn, posn):
        # 计算成品的绝对成本
        price = 0
        for i in range(0,8):
            price = price + self.unit_price[i]
        return self.prod_load_cost + decn[0]*self.prod_test_cost + (1-decn[0])*posn*self.replacement_loss + decn[1] * posn * (self.prod_disa_cost - price)
        

    def is_semi_disa(self):
        # 判断是否需要拆解半成品
        out_dec= []
        if self.semi_prod_disa_cost[0] <= (self.unit_price[0]+self.unit_price[1]+self.unit_price[2]):
                # 拆解费用小，选择拆
                out_dec.append(1)
        else:
            out_dec.append(0)
        if self.semi_prod_disa_cost[1] <= (self.unit_price[3]+self.unit_price[4]+self.unit_price[5]):
                out_dec.append(1)
        else:
            out_dec.append(0)
        if self.semi_prod_disa_cost[2] <= (self.unit_price[6]+self.unit_price[7]):
                out_dec.append(1)
        else:
            out_dec.append(0)
        return out_dec

    def is_disa(self):
        # 判断成品是否需要拆解
        price = 0
        for i in range(0,8):
            price = price + self.unit_price[i]
        if price > self.prod_disa_cost:
            return 1
        else:
            return 0

q3 = ProductDecisionDP(defect_rate=[0.1074, 0.1074, 0.1074, 0.1074, 0.1074, 0.1074, 0.1074, 0.1074], # [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                       unit_price=[2,8,12,2,8,12,8,12], 
                       test_cost=[1,1,2,1,1,2,1,2], 
                       semi_prod_defect_rate=[0.1074, 0.1074, 0.1074], # [0.1,0.1,0.1], 
                       semi_prod_load_cost=[8,8,8], 
                       semi_prod_test_cost=[4,4,4], 
                       semi_prod_disa_cost=[6,6,6], 
                       prod_defect_rate= 0.1074, #0.0908, # 0.1, 0.1074
                       prod_load_cost=8, 
                       prod_test_cost=6, 
                       prod_disa_cost=10, 
                       price=200, 
                       replacement_loss=40,)

min_cost, max_profit, optimal_path = q3.test_part()
print(f"最小总成本: {min_cost}")
print(f"最大总收益: {max_profit}")
print(f"最优决策路径: {optimal_path}")
# q3.Heatmap()
