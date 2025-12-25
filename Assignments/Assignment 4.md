# T-primes + 贪心

Updated 1814 GMT+8 Sep 30, 2025

2025 fall, Complied by 马健文，元培学院



>**说明：**
>
>1. **解题与记录：**
>
>  对于每一个题目，请提供其解题思路（可选），并附上使用Python或C++编写的源代码（确保已在OpenJudge， Codeforces，LeetCode等平台上获得Accepted）。请将这些信息连同显示“Accepted”的截图一起填写到下方的作业模板中。（推荐使用Typora https://typoraio.cn 进行编辑，当然你也可以选择Word。）无论题目是否已通过，请标明每个题目大致花费的时间。
>
>2. 提交安排：**提交时，请首先上传PDF格式的文件，并将.md或.doc格式的文件作为附件上传至右侧的“作业评论”区。确保你的Canvas账户有一个清晰可见的本人头像，提交的文件为PDF格式，并且“作业评论”区包含上传的.md或.doc附件。
> 
>3. **延迟提交：**如果你预计无法在截止日期前提交作业，请提前告知具体原因。这有助于我们了解情况并可能为你提供适当的延期或其他帮助。  
>
>请按照上述指导认真准备和提交作业，以保证顺利完成课程要求。





## 1. 题目

### 34B. Sale

greedy, sorting, 900, https://codeforces.com/problemset/problem/34/B



思路：

排序，抓小于零的电视机。从最亏的开始抓

代码

```python
# 
n,m=map(int,input().split())
a=[int(i) for i in input().split()]
a=sorted(a)
total=0
for i in range(m):
    if a[i]<0:
        total-=a[i]
    else:
        break
print(total)
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251003110450.png]]



### 160A. Twins

greedy, sortings, 900, https://codeforces.com/problemset/problem/160/A



思路：

抓最大的

代码

```python
n=int(input())
coins=[int(i) for i in input().split()]
coins=sorted(coins,reverse=True)
summ=sum(coins)
taken=0
for i in range(n):
    taken+=coins[i]
    if taken*2>summ:
        break
print(i+1)


```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251003111237.png]]



### 1879B. Chips on the Board

constructive algorithms, greedy, 900, https://codeforces.com/problemset/problem/1879/B



思路：

使用贪心算法. 假设有$n-x$行和$n-y$列（$x,y>0$）有格子被选中，则必然有$xy$格未被覆盖。由题干可知每个格子$xy=0$,故either 每一行都有各自被选中 or 每一列都有 （or both）
分类讨论：
	1. 每行都有被选中的格子。则行导致的cost为$\sum a_i$为定值，剩下的列尽可能小即可。因此最终$\rm{cost}=\sum a_i+n\cdot\min(b)$
	2. 每列都有被选中的格子，分析同上$\rm cost=\sum b_i+n\cdot\min(a)$
比较，取最小值即可

代码

```python
def calc(n,a,b):
    # fill each row
    cost=sum(a)+b[0]*n
    # fill each column
    cost1=sum(b)+a[0]*n
    return min(cost,cost1)
t=int(input())
for i in range(t):
    n=int(input())
    lista=[int(j) for j in input().split()]
    listb=[int(j) for j in input().split()]
    print(calc(n,sorted(lista),sorted(listb)))

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20251003181935.png]]




### M01017: 装箱问题

greedy, http://cs101.openjudge.cn/pctbook/M01017/


思路：
这个题目太搞脑子了……
$6\times6$直接fit in
$5\times5$ 只能与$1\times1$拼箱
$3\times3$ 四个一箱可以最优
$4\times4$ 只能与$2\times2$和$1\times1$拼箱 （$2\times2$价值大于$1\times1$,因为4个$1\times1$始终可以替代$2\times2$）
剩下$0\sim3$个$3\times3$，若干$2\times2$和$1\times1$
$2\times2$和$3\times3$的堆积规则：
$$\begin{cases}
2n_3+n_2\leq7, n_3>0\\
n_2<9, n_3=0\end{cases}$$
堆完了以后把$1\times1$塞进空隙里面去，多的$2\times2$和$1\times1$可以自行最密堆积



代码

```python
# 
while True:
    a=[int(i) for i in input().split()]
    if max(a)==0:
        break
    boxes=a[5]+a[4]+a[3] # those which must take up 1 box
    a[0]=max(0,a[0]-11*a[4])# 1*1 fit in 5*5 spaces
    fits=min(a[3]*5,a[1])# number of 2*2 which can fit in 4*4 spaces
    a[0]=max(0,a[0]-(20*a[3]-fits*4))# 1*1 fit in spaces left after 4*4 and 2*2's filling
    boxes+=a[2]//4 # 3*3 clusterization
    a[2]%=4 # 3*3 clusterization
    a[1]-=fits # 2*2 fit in 4*4 spaces
    if a[0]+a[1]+a[2]:# not over
        if a[0]+4*a[1]+9*a[2]<=36:# maybe done in one box
            if (a[2]>0 and a[1]+2*a[2]<=7) or (a[2]==0 and a[0]+4*a[1]<=36):# 3*3 and 2*2 match
                boxes+=1
            else:
                boxes+=2 # area of 36 cannot take up more than 2 boxes
        else:
            if a[2]!=0:# no 3*3
                fits=min(a[1],7-2*a[2])
                a[1]-=fits
                a[0]-=(36-fits*4-a[2]*9)
                a[0]=max(0,a[0])
                a[2]=0
                boxes+=1
            boxes+=(a[0]+4*a[1]-1)//36+1 # left over
    print(boxes)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>


![[Pasted image 20251003234817.png]]


### M01008: Maya Calendar

implementation, http://cs101.openjudge.cn/practice/01008/



思路：
 看起来非常复杂，其实实现起来就按部就班做就好了

代码

```python
def find(lists,key):
    for i in range(len(lists)):
        if lists[i]==key:
            return i
name_of_month=['pop', 'no', 'zip', 'zotz', 'tzec', 'xul'
               , 'yoxkin', 'mol', 'chen', 'yax', 'zac', 'ceh',
               'mac', 'kankin', 'muan', 'pax', 'koyab', 'cumhu','uayet']
name_of_date=['imix', 'ik', 'akbal', 'kan', 'chicchan', 'cimi',
              'manik', 'lamat', 'muluk', 'ok', 'chuen', 'eb',
              'ben', 'ix', 'mem', 'cib', 'caban', 'eznab', 'canac', 'ahau']#Tzolkin date
n=int(input())
print(n)
for i in range(n):
    haab_format=input().split()
    haab_date=int(haab_format[0][:-1:])
    haab_month=find(name_of_month,haab_format[1])
    haab_year=int(haab_format[2])
    total_days=365*haab_year+20*haab_month+haab_date
    tzolkin_year=total_days//260
    tzolkin_date_name=total_days%20
    tzolkin_date_num=total_days%13
    print(f'{tzolkin_date_num+1} {name_of_date[tzolkin_date_name]} {tzolkin_year}')
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20251004174610.png]]




### 230B. T-primes（选做）

binary search, implementation, math, number theory, 1300, http://codeforces.com/problemset/problem/230/B



思路：

之前已经做出来了

代码

```python

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>





## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>

Euler's Sieve:
if $m$ is not-prime:
	$m=p_1^{\alpha_1}\cdot p_2^{\alpha_2}\cdot p_3^{\alpha_3}\dots$
	$m \Leftrightarrow (p_1,p_1^{\alpha_1-1}\cdot p_2^{\alpha_2}\cdot p_3^{\alpha_3}\dots)$
	因此可以扫描$k=p_1^{\alpha_1-1}\cdot p_2^{\alpha_2}\cdot p_3^{\alpha_3}<m$，只需要$p\leq p_1$，也即$p\leq \min\{p>1|\ p|k\}$，即可凑出合法数对$(p,k)$与合数$m$

Banach fixed point theorem:

$$|\frac{1}{2}(x_1+\frac{1}{x_1})-\frac{1}{2}(x_2+\frac{1}{x_2})|=|x_1-x_2|\cdot|\frac{1}{2}-\frac{1}{2x_1x_2}|$$
$$|\frac{1}{2}-\frac{1}{2x_1x_2}|<1 
\Leftrightarrow
-2<1-\frac{1}{x_1x_2}<2
\Leftrightarrow
-1<\frac{1}{x_1x_2}<3
\Leftrightarrow
x_1x_2>\frac{1}{3}
\Leftrightarrow
x_\min>\frac{1}{\sqrt{3}}


$$

$$
\int_0^1\frac{\ln x}{1-x^2}dx=\int_{+\infty}^{1}\frac{1}{1-x^2}d(1/x)
=\int_{+\infty}^{1}\frac{t^2}{t^2-1}dt=\int_{+\infty}^{1}\frac{t^2}{t^2-1}dt
$$
Fermat's Theorem:
for prime number p:
$$
a^{p-1}\equiv1 \mod p
$$
Wilson's Theorem:
$$
(p-1)!\equiv-1 \mod p
$$
Euler's Theorem:
for a and n, if $\gcd(a,n)=1$
$$
a^{\phi(n)}\equiv1\mod p
$$
Lagrange's Inversion Theorem
if $g(f(x))=x$
$$
g(x)=\sum_{k\geq1}\left(\frac{1}{n}[x^{-1}]\frac{1}{f(x)^n}\right)x^n
$$


写了个BFS（我是最快的🐎）：
```python
def find_route(x,y):
    if visited[x][y][0]==0:
        return [[x,y]]
    list1=find_route(visited[x][y][1],visited[x][y][2])
    list1.append([x,y])
    return list1
    
def accessible(foot_pos):
    x=foot_pos[0]
    y=foot_pos[1]
    if x<0 or y<0:
        return False
    if x>10 or y>10:
        return False
    if chess[x][y]:
        return False
    return True

horse_step=[
    [0,1,1,2],
    [0,1,-1,2],
    [1,0,2,1],
    [1,0,2,-1],
    [0,-1,1,-2],
    [0,-1,-1,-2],
    [-1,0,-2,1],
    [-1,0,-2,-1],
    ]
startx,starty=map(int,input().split())
endx,endy=map(int,input().split())
N=12
inf=1000
chess=[[False]*N for i in range(N)]
visited=[[[inf,-1,-1,-1] for i in range(N)] for j in range(N)]
m=int(input())
for i in range(m):
    x,y=map(int,input().split())
    chess[x][y]=True
queue=[[startx,starty]]
visited[startx][starty]=[0,-1,-1,1]#steps=None, from (-1,-1), 1 route(s)
while len(queue):
    current=queue.pop(0)
    for i in range(8):
        foot_pos=[x + y for x, y in zip(current, horse_step[i][0:2])]
        if accessible(foot_pos):
            next_pos=[x + y for x, y in zip(current, horse_step[i][2:4])]
            if accessible(next_pos):
                cur=visited[current[0]][current[1]] #shallow copy!
                new=visited[next_pos[0]][next_pos[1]] #shallow copy!
                if new[0]==inf:
                    queue.append(next_pos)
                if new[0]>cur[0]+1: #better route
                    new[0]=cur[0]+1
                    new[1]=current[0]
                    new[2]=current[1]
                    new[3]=cur[3] #inherit route
                elif new[0]==cur[0]+1: # route with the same time 
                    new[3]+=cur[3] #inherit route
if visited[endx][endy][3]>1:
    print(visited[endx][endy][3])
elif visited[endx][endy][3]==1:
    outstr=''
    for i in find_route(endx,endy):
        outstr=outstr+f'({i[0]},{i[1]})-'
    print(outstr[:-1:])
```
注意！queue.append(next_pos)入队操作必须要是完全没访问过的元素！访问过的坚决不入队！