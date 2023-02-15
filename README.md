# 背包问题算法设计  
问题要求在一个物品集合中选择合适的物品放入背包，在放入背包中的物品总重量不超过背包容量的前提下，希望放入背包的物品总价值最大。根据是否允许部分物品放入背包的要求，背包问题可以分为【**分数背包问题**】和【**0-1背包问题**】。
## 1. 概要设计
+ 分数背包问题，使用贪心算法得到最优解。 
+ 0-1背包问题，若求近似解，使用贪心算法；若求最优解，则分别使用蛮力法、动态规划法及记忆功能改进的动态规划法求解，对于两种动态规划法，返回最终得到的动态规划表。  

>算法具体功能设计流程如图:

<img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture1.png" width="500px">

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
②求0-1背包问题近似解，首先求出每个物品的单位价值，利用循环语句，每次选择单位价值最高的物品装入背包，若物品重量小于等于背包容量，则放入背包，否则，比较下一个物品，直到背包剩余容量为0或已经遍历完所有物品时，停止循环，返回最优总价值。函数设计如下：  
```python
def Greedy_I(n,c):     #贪心算法求解0-1背包近似解
    global opt2
    Sumvalue2 = 0
    opt2 = [0]*n
    danwei_v = []
    for i in range(n):
        d = v[i]/w[i]
        danwei_v.append(d)
    value = list(enumerate(danwei_v))
    value.sort(key=lambda a: a[1], reverse=True)
    while c > 0:
        for i in range(n):
            if  w[value[i][0]] <= c:
                Sumvalue2 += v[value[i][0]]
                opt2[value[i][0]] = 1
                c -= w[value[i][0]]
        else:
            break
    return Sumvalue2
```
+ **蛮力法**

求0-1背包问题最优解。首先穷举物品的全部子集，设置一个记录最大价值的变量maxvalue，遍历所有子集，计算每个子集物品的总重量，若能装入背包，且当前的背包价值大于maxvalue，则将当前值赋值给maxvalue，最后循环遍历完所有的物品组合得到最优解，函数设计如下：  
```python
def Brute(n,c):   #蛮力法求解0-1背包最优解
    a = [0,1]
    l = list(product(a,repeat=n))
    #求解[0,1]中元素的全排列组合，repeat=n表示单个元素最大重复次数
    maxvalue = 0    #记录最大价值
    global opt3
    opt3 = []
    for i in range(len(l)):   #遍历所有子集
        sumweight = 0  # 将总重量与总价值清零，计算下一子集
        sumvalue = 0
        for j in range(n):
            sumweight += l[i][j]*w[j]   #计算子集的总重量
            sumvalue += l[i][j]*v[j]
        if sumweight <= c and sumvalue > maxvalue:   #判断该子集物品能否装入背包，并与最大价值比较进行更新
            maxvalue = sumvalue
            opt3 = list(l[i])
    return maxvalue
```
+ **动态规划法**

动态规划算法求0-1背包问题最优解，初始化动态规划表，表中所有元素为0。单元格F(i,j)表示i个物品，承重量为j的背包的最优解的物品总价值，根据递推关系式：
利用循环逐行填表，最后一个单元格的值F(n,c)即为所要求的的最大总价值，核心代码如下：
