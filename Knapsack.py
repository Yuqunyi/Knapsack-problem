from itertools import product

global w,v,F1,F2  #全局变量

N=int(input("输入物品个数："))
w=eval(input("输入每个物品的重量："))
v=eval(input("输入每个物品的价值："))
C=int(input("设置背包容量："))
choose=input("\033[1;31mPlease choose 分数背包——F   0-1背包——I：\033[0m")


F1=[[0]*(C+1) for i in range(N+1)] #初始化动态规划表——自顶向下动态规划
F2 = [[-1]*(C+1) for i in range(N+1)]  # 初始化动态规划表——改进记忆法
F2[0]=[0]*(C+1)
for i in range(N+1):
    F2[i][0]=0

def Greedy_F(n,c):     #贪婪法求解分数背包最优解
    global opt1
    Sumvalue1=0
    opt1=[0]*n
    danwei_v=[]
    for i in range(n):
        d=v[i]/w[i]
        danwei_v.append(d)   #计算物品单位价值
    value=list(enumerate(danwei_v))
    value.sort(key=lambda a: a[1], reverse=True)  #将物品按照其单位价值降序排序
    while c>0:
        for i in range(n):
            if  w[value[i][0]]<=c:
                Sumvalue1+=v[value[i][0]]
                opt1[value[i][0]]=w[value[i][0]]
                c-=w[value[i][0]]
            else:
                Sumvalue1+=c*danwei_v[value[i][0]]
                opt1[value[i][0]]=c
                c-=c
        else:
            break
    return Sumvalue1

def Greedy_I(n,c):     #贪婪法求解0-1背包近似解
    global opt2
    Sumvalue2=0
    opt2=[0]*n
    danwei_v=[]
    for i in range(n):
        d=v[i]/w[i]
        danwei_v.append(d)
    value=list(enumerate(danwei_v))
    value.sort(key=lambda a: a[1], reverse=True)
    while c>0:
        for i in range(n):
            if  w[value[i][0]]<=c:
                Sumvalue2+=v[value[i][0]]
                opt2[value[i][0]]=1
                c-=w[value[i][0]]
        else:
            break
    return Sumvalue2

def Brute(n,c):   #蛮力法求解0-1背包最优解
    a=[0,1]
    l=list(product(a,repeat=n))   #求解[0,1]笛卡尔积，对应n个物品所有的组合
    maxvalue=0    #记录最大价值
    global opt3
    opt3=[]
    for i in range(len(l)):
        sumweight = 0  # 将总重量与总价值清零，计算下一子集
        sumvalue = 0
        for j in range(n):
            sumweight+=l[i][j]*w[j]   #计算子集的总重量
            sumvalue+=l[i][j]*v[j]
        if sumweight<=c and sumvalue>maxvalue:   #判断该子集物品能否装入背包，并与最大价值比较进行更新
            maxvalue=sumvalue
            opt3=[l[i][j] for j in range(n)]
    return maxvalue

def DP(n,c):   #动态规划法求解0-1背包最优解
    for i in range(1,n+1):
        for j in range(1,c+1):
            if j-w[i-1]<0:
                F1[i][j]=F1[i-1][j]
            else:
                F1[i][j]=max(F1[i-1][j],F1[i-1][j-w[i-1]]+v[i-1])
    return F1[n][c]   #最大总价值

def MFK(i,j):   #记忆功能改进动态规划法
    value=0
    if F2[i][j]<0:
        if j<w[i-1]:
            value=MFK(i-1,j)
        else:
            value=max(MFK(i-1,j),v[i-1]+MFK(i-1,j-w[i-1]))
        F2[i][j]=value  #注意缩进
    return F2[i][j]

def show(F,n,c):   #回溯表格求最优解
    global opt4
    opt4=[0]*n   #记录物品选择状态
    i=n
    j=c
    while c>0:
        if F[i][j]>F[i-1][j]:
            opt4[i-1]=1
            j -= w[i - 1]
            c -= w[i - 1]
            i-=1
        else:
            i-=1
    return opt4

print("--"*30)
if choose=='F':
    print("\033[1;34m贪心算法求得最优总价值为：\033[0m",Greedy_F(N,C))
    print("\033[1;34m最优解：\033[0m",end=' ')
    for i in range(N):
        print("物品{0}——{1}".format(i+1,opt1[i]),end=' ')
if choose=='I':
    method=input("\033[1;35m近似解or最优解—— \033[0m")
    if method=="近似解":
        print("\033[1;34m贪婪法\033[0m"+"求得最优总价值为：", Greedy_I(N, C))
        print("\033[1;34m近似解：\033[0m", end=' ')
        for i in range(N):
            if opt2[i]==1:
                print("物品{0}".format(i + 1), end=',')
    else:
        print("\033[1;34m蛮力法\033[0m"+"求得最优总价值为：", Brute(N,C))
        print("\033[1;34m最优解：\033[0m", end=' ')
        for i in range(N):
            if opt3[i]==1:
                print("物品{0}".format(i + 1), end=',')
        print('\n')
        print("\033[1;34m动态规划法\033[0m" + "求得最优总价值为：", DP(N,C))
        print("\033[1;34m最优解：\033[0m", end=' ')
        for i in range(N):
            if show(F1,N,C)[i]==1:
                print("物品{0}".format(i + 1), end=',')
        print()
        print("\033[1;34m动态规划表为：\033[0m")
        for item in F1:
            print(item)
        print('')
        print("\033[1;34m记忆功能改进动态规划法\033[0m" + "求得最优总价值为：", MFK(N, C))
        print("\033[1;34m最优解：\033[0m", end=' ')
        for i in range(N):
            if show(F2,N,C)[i]==1:
                print("物品{0}".format(i + 1), end=',')
        print()
        print("\033[1;34m动态规划表为：\033[0m")
        for item in F2:
            print(item)



