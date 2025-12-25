
Updated 1651 GMT+8 Oct 9, 2025

2025 fall, Complied by 马健文 元培学院



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

### E29895: 分解因数

implementation, http://cs101.openjudge.cn/practice/29895/



思路：

Euler Sieve (但好像也没这个必要)

代码

```python
# 
n=int(input())
primelist=[]
R=int(n**0.5)+10
isprime=[True for i in range(R)]
for i in range(2,R):
    if isprime[i]:
        primelist.append(i)
    for j in primelist:
        if i*j>=R:
            break
        isprime[j*i]=False
        if i % j ==0:
            break
for i in primelist:
    if n % i ==0:
        prime = i
        break
print(n // i)
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251012220113.png]]



### E29940: 机器猫斗恶龙

greedy, http://cs101.openjudge.cn/practice/29940/



思路：
一个一个上去干


代码

```python
n=int(input())
a=[int(i) for i in input().split()]
blood=0
minimum=1e9
for i in a:
    blood+=i
    if blood < minimum:
        minimum=blood
print(max(-minimum+1,0))
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20251012220027.png]]




### M29917: 牛顿迭代法

implementation, http://cs101.openjudge.cn/practice/29917/



思路：

直接干
啊啊啊啊啊这个不定行输入怎么这么难记啊啊啊！！！考场上死磕不定行输入磕了半个多小时，最终想起来```except``` 后面接的不是EOFError，而是要做什么！！！直接```break```
还有这个保留有效数字也是难记得很！！！卡了我两道题
```python
>>> print('%f' % 1.11)  # 默认保留6位小数
1.110000
>>> print('%.1f' % 1.11)  # 取1位小数
1.1
>>> print('%e' % 1.11)  # 默认6位小数，用科学计数法
1.110000e+00
>>> print('%.3e' % 1.11)  # 取3位小数，用科学计数法
1.110e+00
>>> print('%g' % 1111.1111)  # 默认6位有效数字
1111.11
>>> print('%.7g' % 1111.1111)  # 取7位有效数字
1111.111
>>> print('%.2g' % 1111.1111)  # 取2位有效数字，自动转换为科学计数法
1.1e+03
```

代码

```python
def iterate(p):
    cycle=1
    x=1
    while True:
        y=x-(x**2-p)/(2*x)
        if abs(y-x)<1e-6:
            x=y
            break
        x=y
        cycle+=1
    return [cycle, x]
final_result=[]
while True:
    try:
        s=float(input())
        result=iterate(s)
        result[1]=round(result[1],2)
        final_result.append(result)
    except:
        break
for i in final_result:
    x=round(i[1],2)
    print(i[0],end=' ')
    print('%(value).2f' %{"value": i[1]})
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251012220202.png]]



### M29949: 贪婪的哥布林

greedy, http://cs101.openjudge.cn/practice/29949/


思路：

当然是贪心地把最大价值的给捞走

代码

```python
# 
n,capacity=map(int,input().split())
a=[]
for i in range(n):
    v,w=map(int,input().split())
    r=v/w
    a.append([r,v,w])
a=sorted(a,reverse=True)
left=capacity
value=0
for i in a:
    if left>=i[2]:
        value+=i[1]
        left-=i[2]
    else:
        if left==0:
            break
        value+=i[0]*left
        left-=left
        if left==0:
            break
value=round(value,2)
print('%(value).2f' %{"value": value})
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251012220647.png]]



### M29918: 求亲和数

implementation, http://cs101.openjudge.cn/practice/29918/



思路：
法1：打表
法2：基于质因数分解的筛法


代码

```python
lists=[[220,284],
[1184,1210],
[2620,2924],
[5020,5564],
[6232,6368],
[10744,10856],
[12285,14595],
[17296,18416],
[63020,76084],
[66928,66992],
[67095,71145],
[69615,87633],
[79750,88730]]
n=int(input())
for i in lists:
    if i[0]<=n and i[l]<=n:
        print(i[0],i[l])
```

```python
def cp(x):
    fact = []
    p = x
    for i in range(len(primelist)):
        if p==1:
            break
        cnt = 0
        while p % primelist[i] == 0:
            p //= primelist[i]
            cnt += 1
        if cnt:
            fact.append([primelist[i],cnt])
    if p!=1:
        fact.append([p,1])
    prod = 1
    for i in fact:
        prod *= (i[0] ** (i[1] + 1) - 1)//(i[0] - 1)
    return prod - x
n = int(input())
#primelist
R = int(n ** 0.5)+10
isprime = [True for i in range(R)]
primelist = []
for i in range(2,R):
    if isprime[i]:
        primelist.append(i)
    for j in primelist:
        if i * j >= R:
            break
        isprime[j * i]=False
        if i % j == 0:
            break
#primelist
for i in range(2,n):
    x = cp(i)
    if x <= i or x > n:
        continue
    if cp(x) == i:
        print(i,x)
```

代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251012215546.png]]



### T29947:校门外的树又来了（选做）

http://cs101.openjudge.cn/practice/29947/



思路：

写了个屎山代码，核心就是把地铁数量的前缀和数组做出来（以站点为索引而非树，不然爆内存+时间），然后直接统计

代码

```python
l,m=map(int,input().split())
a=[]
for i in range(m):
    a.append([int(i) for i in input().split()])
subways=[]
for i in a:
    subways.append([i[0],1])
    subways.append([i[1]+1,-1])
subways=sorted(subways)
#print(subways)
x=0
while x<len(subways)-1:
    if subways[x][0]==subways[x+1][0]:
        subways[x][1]+=subways[x+1][1]
        subways.pop(x)
    else:
        x+=1
cnt=[subways[0][1]]
for i in range(1,len(subways)):
    cnt.append(cnt[-1]+subways[i][1])
#print(cnt)
start=0
flag=True
left=0
for i in range(len(cnt)):
    if cnt[i]!=0 and flag:
        left+=subways[i][0]-start
        flag=False
    elif (not flag) and cnt[i]==0:
        start=subways[i][0]
        flag=True
if flag:
    left+=l+1-subways[-1][0]
print(left)
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251012220814.png]]



## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>

🐎走日
```python
count = 0
n = m = 0
def search(state,x,y):
    global count,n,m
    state = state | (1<<(m*x+y))
    if state + 1 == 1<<(m*n):
        count += 1
        return
    for dx in range(-2,3):
        for dy in range(-2,3):
            if dx ** 2 + dy ** 2 == 5:
                if x + dx >= 0 and x + dx < n:
                    if y + dy >= 0 and y + dy < m:
                        if not(state & (1 << (m * (x + dx) + (y + dy)))):
                            search(state, x+dx, y+dy)
t=int(input())
for i in range(t):
    n,m,x,y=map(int,input().split())
    start=1<<(m*x+y)
    count=0
    search(0,x,y)
    print(count)
```

咒语序列（这类问题还是用栈方便，而且可以处理不止一种括号）
```python
s=input()
stack=[]
pair = [-1 for i in s]
for i in range(len(s)):
    stack.append([s[i],i])
    if len(stack)>=2:
        if stack[-2][0]=='(' and stack[-1][0]==')':
            right=stack.pop(-1)[1]
            left=stack.pop(-1)[1]
            pair[left]=right

#for i in range(len(s)):
#    print(i,end='\t')
#print()
#for i in s:
#    print(i,end='\t')
#print()
#for i in pair:
#    print(i,end='\t')
#print()

i=0
maxx=0
while i < len(s):
    if pair[i]==-1:
        i += 1
    else:
        start = i
        while i < len(s) and pair[i] != -1:
            i = pair[i]+1
            #print(i)
        end = i
        maxx = max(maxx, end-start)
print(maxx)
```

P大卷王
```python
n,x,y=map(int,input().split())
rollers={}
for i in range(n):
    s=input().split()
    if s[1] in rollers:
        xx = rollers[s[1]]
    else:
        xx = [0,0]
    xx[0]+=int(s[2])
    xx[1]+=1
    rollers[s[1]] = xx
n=int(input())
for i in range(n):
    name=input().strip()
    grade = rollers[name]
    if grade[1]>=x and grade[0]>y*grade[1]:
        print('yes')
    else:
        print('no')
```