

Updated 1315 GMT+8 Oct 21, 2025

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

### M04147汉诺塔问题(Tower of Hanoi)

dfs, http://cs101.openjudge.cn/pctbook/M04147

思路：

经典递归做法

代码

```python
def search(n,a,b,c):#a to c using b
    if n==0:
        return
    search(n-1,a,c,b)
    print(f'{n}:{a}->{c}')
    search(n-1,b,a,c)
s = input().split()
n = int(s[0])
a,b,c = s[1::]
search(n,a,b,c)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20251028152354.png]]




### M05585: 晶矿的个数

matrices, dfs similar, http://cs101.openjudge.cn/pctbook/M05585

思路：

dfs搜索连通块

代码

```python
dirs = [[1,0],[0,1],[-1,0],[0,-1]]
def notvisited(x,y):
    if x < 0 or x >= n or y < 0 or y >= n:
        return False
    return not visited[x][y]
def search(x,y,mineral):
    visited[x][y] = True
    for i in range(4):
        newx,newy = x + dirs[i][0], y + dirs[i][1]
        if notvisited(newx,newy) and mapp[newx][newy] == mineral:
            search(newx,newy,mineral)
t = int(input())
dict1 = {'#':0, 'r':1, 'b':2}
for _ in range(t):
    n = int(input())
    mapp = []
    for i in range(n):
        mapp.append([dict1[c] for c in input().strip()])
    visited = [[False]*n for i in range(n)]
    red = black = 0
    for i in range(n):
        for j in range(n):
            if mapp[i][j] and notvisited(i,j):
                search(i,j,mapp[i][j])
                if mapp[i][j]==1:
                    red += 1
                else:
                    black += 1
    print(red,black)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251028154003.png]]



### M02786: Pell数列

dfs, dp, http://cs101.openjudge.cn/pctbook/M02786/

思路：

dp，模加法

代码

```python
def Pell(x):
    a=[1,2,5]
    if x<=3:
        return a[x-1]
    for i in range(x-3):
        a[0]=a[1]
        a[1]=a[2]
        a[2]=a[0]+a[1]*2
        for j in range(3):
            a[j] %= 32767
    return a[2]
n=int(input())
for i in range(n):
    print(Pell(int(input())))
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251028154122.png]]



### M46.全排列

backtracking, https://leetcode.cn/problems/permutations/


思路：

基于Cantor的映射，用数学（阶乘进制）办法解决，不用递归✌

代码

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        import math
        n = len(nums)
        result = []
        for i in range(math.factorial(n)):
            indexes = []
            ii = i
            j = n-1
            while j >= 0:
                index = ii // math.factorial(j)
                ii -= index * math.factorial(j)
                indexes.append(index)
                j -= 1
            seq = []
            list1 = list(range(n))
            for j in range(n):
                seq.append(nums[list1.pop(indexes[j])])
            result.append(seq)
        return result
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20251028155851.png]]




### T02754: 八皇后

dfs and similar, http://cs101.openjudge.cn/pctbook/T02754

思路：

直接回溯枚举

代码

```python
import sys
solutions = []
def judge(x):
    a = []
    while x > 0:
        a.append(x%10)
        x //= 10
    for i in range(1,len(a)):
        if a[i] == a[0]:
            return False
        if abs(a[i] - a[0]) == abs(i):
            return False
    return True
def search(x):
    global solutions
    if x > 1e7:
        solutions.append(x)
        return
    for i in range(1,9):
        if judge(x * 10 + i):
            search(x * 10 + i)
search(0)
lines = sys.stdin.read().splitlines()
for i in lines[1::]:
    print(solutions[int(i)-1])
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251016163004.png]]



### T01958 Strange Towers of Hanoi

http://cs101.openjudge.cn/practice/01958/

思路：

打表（）
```python
ans = [0]
for i in range(1,13):
    minn = 1e15
    for j in range(1,i+1):
        minn = min(minn,2 * ans[i - j] + 2**j - 1)
    ans.append(minn)
print(ans)
```
其实就是按照题目思路整

代码

```python
print('1\n3\n5\n9\n13\n17\n25\n33\n41\n49\n65\n81\n')
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20251028162414.png]]


可是为什么这个算法是对的呢？不知道

## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>





