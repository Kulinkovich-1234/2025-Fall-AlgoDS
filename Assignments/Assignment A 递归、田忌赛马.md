# Assignment #A: 递归、田忌赛马

Updated 2355 GMT+8 Nov 4, 2025

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

### M018160: 最大连通域面积

dfs similar, http://cs101.openjudge.cn/pctbook/M18160

思路：

dfs，搜索，判断

代码

```python
direct = [[0,1],[1,0],[0,-1],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
visited = []
mapp = []
area = 0
def search(x,y,c):
    global area
    visited[x][y] = True
    area += 1
    for step in direct:
        newx,newy = x+step[0], y+step[1]
        if newx < 0 or newx >= n or newy < 0 or newy >= m:
            continue
        if visited[newx][newy]:
            continue
        if mapp[newx][newy] != c:
            continue
        search(newx,newy,c)
t = int(input())
for _ in range(t):
    n,m = map(int,input().split())
    mapp = []
    for i in range(n):
        mapp.append(input().strip())
    visited = [[False for j in range(m)] for i in range(n)]
    max_area = 0
    for i in range(n):
        for j in range(m):
            if not visited[i][j]:
                area = 0
                if mapp[i][j] == '.':
                    continue
                search(i,j,mapp[i][j])
                max_area = max(area,max_area)
    print(max_area)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251118190516.png]]



### sy134: 全排列III 中等

https://sunnywhy.com/sfbj/4/3/134

思路：

进位序列为后缀递减序列

代码

```python
import math
def next_perm(seq):
    j = len(seq)-1
    while j > 0 and seq[j-1] >= seq[j]:
        j -= 1
    if j == 0:
        return []
    # [j,n) is longest descending sequence
    # j-1 is the element to be inserted
    result = seq[:j-1]
    for i in range(n-1,j-1,-1):
        if seq[i] > seq[j-1]:
            j -= 1
            result = result + [seq[i]] + sorted(seq[j:i]+seq[i+1:n])
            return result
    return []
n = int(input())
a = [int(i) for i in input().split()]
a = sorted(a)
for i in range(math.factorial(n)):
    print(*a)
    a = next_perm(a)
    if a == []:
        break

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20251118193129.png]]




### sy136: 组合II 中等

https://sunnywhy.com/sfbj/4/3/136

给定一个长度为的序列，其中有n个互不相同的正整数，再给定一个正整数k，求从序列中任选k个的所有可能结果。

思路：

枚举，传递序列

代码

```python
def find(seq,k):
    if len(seq)==m:
        print(*seq)
        return
    if k == n:
        return
    find(seq+[a[k]],k+1)
    find(seq,k+1)
n,m = map(int,input().split())
a = [int(i) for i in input().split()]
a = sorted(a)
find([],0)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>


![[Pasted image 20251118203929.png]]


### sy137: 组合III 中等

https://sunnywhy.com/sfbj/4/3/137


思路：

用Hashable的tuple构建set实现输出

代码

```python
ans = set()
def find(seq,k):
    if len(seq)==m:
        ans.add(tuple(seq))
        return
    if k == n:
        return
    find(seq+[a[k]],k+1)
    find(seq,k+1)
n,m = map(int,input().split())
a = [int(i) for i in input().split()]
a = sorted(a)
find([],0)
for _ in ans:
    print(*_)
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251118204132.png]]



### M04123: 马走日

dfs, http://cs101.openjudge.cn/pctbook/M04123

思路：

直接dfs搜索

代码

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



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251118193232.png]]



### T02287: Tian Ji -- The Horse Racing

greedy, dfs http://cs101.openjudge.cn/pctbook/T02287

思路：

分类讨论

解决这道题的关键在于**用最差的马去输掉一些比赛，保留最好的马去赢一些比赛**。具体策略如下：

1. **先排序**：将田忌和齐王的马按速度从快到慢排序
2. **双指针比较**：
    - 如果田忌最快的马 > 齐王最快的马 → 用田忌最快的马赢齐王最快的马
    - 如果田忌最快的马 < 齐王最快的马 → 用田忌最慢的马输给齐王最快的马
    - 如果田忌最快的马 = 齐王最快的马 → 需要再比较最慢的马：
        - 如果田忌最慢的马 > 齐王最慢的马 → 用田忌最慢的马赢齐王最慢的马
        - 如果田忌最慢的马 ≤ 齐王最慢的马 → 用田忌最慢的马输给齐王最快的马

## 为什么这个策略正确？

这个策略的精髓在于**最小化损失**和**最大化收益**：

- 当田忌的马肯定赢不了齐王的马时，我们用最差的马去输，这样可以保留好的马
- 当田忌的马能赢齐王的马时，我们直接用最好的马去赢
- 当马匹速度相同时，我们比较最慢的马，决定是"平局"还是"用最差马输"

代码

```python
from collections import deque
def judge(k,t):
    if k > t:
        return -1
    if k < t:
        return 1
    return 0
while True:
    n = int(input())
    if not n:
        break
    tian = deque(sorted([int(i) for i in input().split()]))
    king = deque(sorted([int(i) for i in input().split()]))
    score = 0
    while len(king):
        if king[-1] > tian[-1]:
            score += judge(king.pop(),tian.popleft())
        elif king[-1] < tian[-1]:
            score += judge(king.pop(),tian.pop())
        else:
            if tian[0] > king[0]:
                score += judge(king.popleft(),tian.popleft())
            elif tian[0] <= king[0]:
                score += judge(king.pop(),tian.popleft())
    print(score*200)
    

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251118210717.png]]



## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>



期中考试，所以就没怎么做题。。。

研究了以下五边形数

