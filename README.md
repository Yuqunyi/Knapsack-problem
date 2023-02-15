# 背包问题算法设计  
问题要求在一个物品集合中选择合适的物品放入背包，在放入背包中的物品总重量不超过背包容量的前提下，希望放入背包的物品总价值最大。根据是否允许部分物品放入背包的要求，背包问题可以分为【**分数背包问题**】和【**0-1背包问题**】。
## 1. 概要设计
+ 分数背包问题，使用贪心算法得到最优解。 
+ 0-1背包问题，若求近似解，使用贪心算法；若求最优解，则分别使用蛮力法、动态规划法及记忆功能改进的动态规划法求解，对于两种动态规划法，返回最终得到的动态规划表。  

>算法具体功能设计流程如图:

<img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture1.png" width="450px">

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

动态规划算法求0-1背包问题最优解，初始化动态规划表，表中所有元素为0。单元格F(i,j)表示i个物品，承重量为j的背包最优解时的物品总价值，根据递推关系式：

<img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture2.png" width="500px">

利用循环逐行填表，最后一个单元格的值F(n,c)即为所要求的的最大总价值，函数设计如下：  
```python
def DP(n,c):   #动态规划法求解0-1背包问题最优解
    for i in range(1,n+1):
        for j in range(1,c+1):
            if j-w[i-1] < 0:
                F1[i][j] = F1[i-1][j]   #F1为初始化动态规划表，且为全局变量
            else:
                F1[i][j] = max(F1[i-1][j],F1[i-1][j-w[i-1]]+v[i-1])
    return F1[n][c]   #最大总价值
```
+ **记忆功能改进动态规划算法**

该算法重点在于维护一个类似自底向上动态规划算法使用的表格，初始化动态规划表，表中第一行和第一列元素均为0，其他元素为-1，表明该单元格还没有被计算过。F(i,j)表示i个物品，承重量为j的背包最优解时的物品总价值。首先检查表中单元格的值是否小于0，若小于0，根据动态规划法的递推关系式使用递归调用进行计算，将返回的结果记录在表中，否则，直接返回单元格中的值。函数设计如下：  
```python
def MFK(i,j):   #记忆功能改进动态规划法
    value = 0
    if F2[i][j] < 0:    #F2为初始化动态规划表，且为全局变量
        if j < w[i-1]:
            value = MFK(i-1,j)
        else:
            value = max(MFK(i-1,j),v[i-1]+MFK(i-1,j-w[i-1]))
        F2[i][j] = value  #注意缩进
    return F2[i][j]
```
+ **回溯表格单元求最优子集的组成元素**

利用while循环及条件判断语句，从最后一个单元格开始，若F[i][j]>F[i-1][j],表明物品i以及F[i-1][j-w[i]]的一个最优子集包括在最优解中；否则，物品i不是最优子集的一部分，比较F[i-1][j]与F[i-2][j]，当回溯至背包剩余容量为0时，返回最优解。函数设计如下：  
```python
def show(F,n,c):   #F为动态规划表
    global opt4
    opt4 = [0]*n   #记录物品选择状态
    i = n
    j = c
    while c > 0:
        if F[i][j] > F[i-1][j]:
            opt4[i-1] = 1
            j -= w[i - 1]
            c -= w[i - 1]
            i -= 1
        else:
            i -= 1
    return opt4
```
## 3. 项目测试  
**考虑下列数据给出的实例：**

<img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture3.png" width="250px">

+ **分数背包问题**

通过贪心算法求得最优总价值为38.333，最优解为{物品2，物品3，物品4}，物品3只有2/3放入了背包。

<img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture4.png" width="400px">

+ **0-1背包问题**

1、贪心算法求其近似解，得到最大总价值为37，近似解为{物品1，物品2，物品4}。

<img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture5.png" width="400px">

2、蛮力法、动态规划法、记忆功能改进的动态规划法求最优解，得到最优总价值为37，最优解为{物品1，物品2，物品4}。可以看出，动态规划表F1中每个单元格的值都进行了计算，在F2中，-1表示没有计算的值，即只计算了11个值，从而应用记忆功能改进后，动态规划法的效率得到了提高。

<img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture6.png" width="400px">
  
根据测试结果可以看出，对于该实例，用**贪心算法**得到的近似解与蛮力法等得到的最优解是一样的，即该近似解就是最优解，但该算法**并不总是能给出最优解**，反例如下：

<img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture7.png" width="250px">

利用贪心算法得到近似解为{物品1}，总价值为40；而利用蛮力法得到最优解为{物品2，物品3}，最优总价值为50，即该近似解不是最优解。

<img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture8.png" width="400px">  <img src="https://raw.githubusercontent.com/Yuqunyi/Knapsack-problem/main/image/picture9.png" width="400px">
