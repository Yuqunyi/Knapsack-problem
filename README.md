# 背包问题算法设计  
问题要求在一个物品集合中选择合适的物品放入背包，在放入背包中的物品总重量不超过背包容量的前提下，希望放入背包的物品总价值最大。根据是否允许部分物品放入背包的要求，背包问题可以分为【**分数背包问题**】和【**0-1背包问题**】。
## 1. 概要设计
+ 分数背包问题，使用贪心算法得到最优解。 
+ 0-1背包问题，若求近似解，使用贪心算法；若求最优解，则分别使用蛮力法、动态规划法及记忆功能改进的动态规划法求解，对于两种动态规划法，返回最终得到的动态规划表。  

>算法具体功能设计流程如图:

![img](https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture1.png)
## 2. 具体算法设计  
+ **贪心算法**  
①求分数背包问题最优解，其思想是求出每个物品的单位价值，并由高至低依次选择物品放入背包，若物品重量小于等于背包容量，则放入背包；否则，将物品进行拆分，将部分物品装进背包中。当背包剩余容量为0时，停止循环，返回最优总价值。函数设计如下：  
```python
def Greedy_F(n,c):   #贪心算法求解分数背包问题最优解
    #n表示物品个数,c表示背包容量
    global opt1
    Sumvalue1 = 0  #记录背包内物品总价值
    opt1 = [0]*n  #记录选择的物品
    danwei_v = []
    for i in range(n):
        d = v[i]/w[i]    #计算物品单位价值
        danwei_v.append(d)   
    value = list(enumerate(danwei_v))  #enumerate()函数将物品序号与其对应单位价值组合为一组数对
    value.sort(key=lambda a: a[1], reverse=True)  #按物品单位价值降序排序
    while c > 0:
        for i in range(n):
            if  w[value[i][0]] <= c:
                Sumvalue1 += v[value[i][0]]
                opt1[value[i][0]] = w[value[i][0]]
                c -= w[value[i][0]]
            else:
                Sumvalue1 += c*danwei_v[value[i][0]]
                opt1[value[i][0]] = c
                c -= c
        else:
            break
    return Sumvalue1  #返回最优总价值
```
②求分数背包问题最优解，其思想是求出每个物品的单位价值，并由高至低依次选择物品放入背包，若物品重量小于等于背包容量，则放入背包；否则，将物品进行拆分，将部分物品装进背包中。当背包剩余容量为0时，停止循环，返回最优总价值。函数设计如下： 
