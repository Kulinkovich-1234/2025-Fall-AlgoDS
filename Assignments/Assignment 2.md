
Updated 1335 GMT+8 Sep 16, 2025

2025 fall, Complied by 马健文 元培学院



**作业的各项评分细则及对应的得分**

| 标准                  | 等级                                                                       | 得分  |
| ------------------- | ------------------------------------------------------------------------ | --- |
| 按时提交                | 完全按时提交：1分<br/>提交有请假说明：0.5分<br/>未提交：0分                                    | 1 分 |
| 源码、耗时（可选）、解题思路（可选）  | 提交了4个或更多题目且包含所有必要信息：1分<br/>提交了2个或以上题目但不足4个：0.5分<br/>少于2个：0分              | 1 分 |
| AC代码截图              | 提交了4个或更多题目且包含所有必要信息：1分<br/>提交了2个或以上题目但不足4个：0.5分<br/>少于：0分                | 1 分 |
| 清晰头像、PDF文件、MD/DOC附件 | 包含清晰的Canvas头像、PDF文件以及MD或DOC格式的附件：1分<br/>缺少上述三项中的任意一项：0.5分<br/>缺失两项或以上：0分 | 1 分 |
| 学习总结和个人收获           | 提交了学习总结和个人收获：1分<br/>未提交学习总结或内容不详：0分                                      | 1 分 |
| 总得分： 5              | 总分满分：5分                                                                  |     |

>
>
>
>**说明：**
>
>1. **解题与记录：**
>
>   对于每一个题目，请提供其解题思路（可选），并附上使用Python或C++编写的源代码（确保已在OpenJudge， Codeforces，LeetCode等平台上获得Accepted）。请将这些信息连同显示“Accepted”的截图一起填写到下方的作业模板中。（推荐使用Typora https://typoraio.cn 进行编辑，当然你也可以选择Word。）无论题目是否已通过，请标明每个题目大致花费的时间。
>
>2. **课程平台：**课程网站位于Canvas平台（https://pku.instructure.com ）。该平台将在<mark>第2周</mark>选课结束后正式启用。在平台启用前，请先完成作业并将作业妥善保存。待Canvas平台激活后，再上传你的作业。
>
>3. **提交安排：**提交时，请首先上传PDF格式的文件，并将.md或.doc格式的文件作为附件上传至右侧的“作业评论”区。确保你的Canvas账户有一个清晰可见的本人头像，提交的文件为PDF格式，并且“作业评论”区包含上传的.md或.doc附件。
>
>4. **延迟提交：**如果你预计无法在截止日期前提交作业，请提前告知具体原因。这有助于我们了解情况并可能为你提供适当的延期或其他帮助。  
>
>请按照上述指导认真准备和提交作业，以保证顺利完成课程要求。





## 1. 题目

### 263A. Beautiful Matrix

implementation, 800, https://codeforces.com/problemset/problem/263/A



思路：

Trivial

代码

```python
# 
a=[]
try:
    while True:
        line=input().split()
        if line:
            a.append([int(i) for i in line])
except EOFError:
    pass
x=y=-1
for i in range(5):
    for j in range(5):
        if a[i][j]==1:
            x=i
            y=j
            break
    if x!=-1:
        break
print(abs(x-2)+abs(y-2))
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20250916154410.png]]



### 1328A. Divisibility Problem

math, 800, https://codeforces.com/problemset/problem/1328/A



思路：

$(a+(b-a\mod b)) \equiv 0 (mod b)$

代码

```python
n=int(input())
for i in range(n):
    a,b=map(int, input().split())
    print((b-a%b)%b)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20250919083948.png]]




### 427A. Police Recruits

implementation, 800, https://codeforces.com/problemset/problem/427/A



思路：

求maximum crime-police

代码

```python
n=int(input())
a=[int(i) for i in input().split()]
crime_minus_police=0
maximum=0
for i in a:
    crime_minus_police-=i
    maximum=max(maximum, crime_minus_police)
print(maximum)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20250919084458.png]]



### E02808: 校门外的树

implementation, http://cs101.openjudge.cn/pctbook/E02808/


思路：

维护树列数组，删去对应的树，最后求和

代码

```python
# 
L,M=map(int,input().split())
tree=[1 for i in range(L+1)]
for i in range(M):
    start,end=map(int,input().split())
    for j in range(start,end+1):
        tree[j]=0
summ=0
for i in range(L+1):
    summ+=tree[i]
print(summ)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20250919161733.png]]



### sy60: 水仙花数II

implementation, https://sunnywhy.com/sfbj/3/1/60



思路：

直接循环判断
输出比较麻烦

代码

```python
def isnarcissus(x):
    a=[]
    y=x
    while x>0:
        a.append(x%10)
        x//=10
    summ=0
    for i in a:
        summ+=i**3
    return summ==y
a,b=map(int,input().split())
nlist=[]
for i in range(a,b+1):
    if isnarcissus(i):
        nlist.append(i)
if len(nlist):
    print(nlist[0],end='')
    for i in nlist[1::]:
        print(' ',end='')
        print(i,end='')
else:
    print('NO')

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20250919150905.png]]




### M01922: Ride to School

implementation, http://cs101.openjudge.cn/pctbook/M01922/



思路：

**Charley always follows the first rider to start after t=0.**

代码

```python
from math import *
while True:
    n=int(input())
    if n==0:
        break
    minimum=1e9
    for i in range(n):
        v,t=map(int,input().split())
        if t>=0:
            arrive=4.5/v*3600+t
            if arrive<minimum:
                minimum=arrive
    print(ceil(minimum))

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20250919162921.png]]



## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>

![[c0e085e5a0479dfb925edbf189438004.png]]
![[2daa61a21d51648a4a7266ebcfbf3e2b.png]]

