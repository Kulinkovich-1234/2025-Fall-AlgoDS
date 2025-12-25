

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

### M12560: 生存游戏

matrices, http://cs101.openjudge.cn/pctbook/M12560/

思路：

直接判断

代码

```python
n,m = map(int,input().split())
def judge(x,y):
    return (x >= 0) and (x < n) and (y >= 0) and (y < m)
mapp = []
for i in range(n):
    mapp.append([int(j) for j in input().split()])
newmap = [[0]*m for i in range(n)]
for i in range(n):
    for j in range(m):
        neighbor = -mapp[i][j]
        for dx in range(-1,2):
            for dy in range(-1,2):
                if judge(i+dx,j+dy):
                    neighbor += mapp[i+dx][j+dy]
        if neighbor < 2:
            newmap[i][j] = 0
        elif neighbor == 2:
            newmap[i][j] = mapp[i][j]
        elif neighbor == 3:
            newmap[i][j] = 1
        else:
            newmap[i][j] = 0
for i in newmap:
    print(*i)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251021143440.png]]



### M04133:垃圾炸弹

matrices, http://cs101.openjudge.cn/pctbook/M04133/

思路：

维护每个垃圾堆的“炸弹可及区域”的边界
将网格划分为不同的区域，每个区域各自计算
**注意！！！！！!**
1.上下边界为-0.5和1024.5
2.排序后重复边界不能计入（去掉面积为零的区域）
3.炸弹放置位点不可以出界！！！！！！

代码

```python

dist = int(input())
n = int(input())
garbages = []
xs = [-0.5,1024.5]
ys = [-0.5,1024.5]

def count(x,y):
    result = 0
    for gx,gy,garb in garbages:
        if abs(x-gx)>dist:
            continue
        if abs(y-gy)>dist:
            continue
        result += garb
    return result
for i in range(n):
    x,y,garb = map(int,input().split())
    garbages.append([x,y,garb])
    xs.append(x-dist-0.5)
    xs.append(x+dist+0.5)
    ys.append(y-dist-0.5)
    ys.append(y+dist+0.5)
xs.sort()
ys.sort()
nums = max_clear = 0
for i in range(1,len(xs)):
    for j in range(1,len(ys)):
        if xs[i-1] < -0.5 or xs[i] > 1024.5 or ys[j-1] < -0.5 or ys[j] > 1024.5:
            continue
        # out of range
        if (xs[i]-xs[i-1]) * (ys[j]-ys[j-1]) < 1e-3:
            continue
        # zero
        x_drop = (xs[i-1]+xs[i])/2
        y_drop = (ys[j-1]+ys[j])/2
        clear = count(x_drop,y_drop)
        if max_clear == clear:
            nums += int((xs[i]-xs[i-1])*(ys[j]-ys[j-1]))
        elif max_clear < clear:
            nums = int((xs[i]-xs[i-1])*(ys[j]-ys[j-1]))
        max_clear = max(max_clear,clear)
print(nums,max_clear)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251022233613.png]]



### M02746: 约瑟夫问题

implementation, queue, http://cs101.openjudge.cn/pctbook/M02746/

思路：

使用递推法，每次去除一个人就变成一个更小的子Joseph问题


代码

```python
def joseph(n,m):
    if n == 1:
        return 1
    return ((joseph(n-1,m)+m)-1)%n+1
while True:
    n,m = map(int,input().split())
    if n == 0:
        break
    print(joseph(n,m))

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251021151026.png]]



### M26976:摆动序列

greedy, http://cs101.openjudge.cn/pctbook/M26976/


思路：

我用dp，走到第n个位置的最长波动子序列
但似乎贪心也是可以解决的？为什么可以？

### 一个一维序列必定可以划分为严格单增和严格单减和常值区间
### 同样也可以划分为单增和单减区间，不管如何划分其数量不变
每个单增区间选最小和最大两个点，每个单减区间也同样选择，这样可以取到最优解
如果有一个更优解，则

代码

```python
n = int(input())
array = [int(i) for i in input().split()]
dp = [[0,0] for i in range(n)]
dp[0] = [1,1]
for i in range(1,n):
    for j in range(0,i):
        if array[j] < array[i]:
            dp[i][0] = max(dp[i][0], dp[j][1] + 1)
        if array[j] > array[i]:
            dp[i][1] = max(dp[i][1], dp[j][0] + 1)
maxx = 0
for i in range(n):
    maxx = max(maxx, dp[i][0], dp[i][1])
print(maxx)

```

```Cpp
class Solution { 
public: 
	int wiggleMaxLength(vector<int>& nums) { 
		int n = nums.size(); 
		if (n < 2) { 
			return n; 
		} 
		
		int prev_diff = 0; 
		int count = 1; 
		
		for (int i = 1; i < n; i++) { 
			int diff = nums[i] - nums[i-1]; 
			if ((diff > 0 && prev_diff <= 0) || (diff < 0 && prev_diff >= 0)) { 
				count++; 
				prev_diff = diff; 
			} 
		} 
			
		return count; 
	} 
};

```


代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251021152416.png]]



### T26971:分发糖果

greedy, http://cs101.openjudge.cn/pctbook/T26971/

思路：

从左往右扫描，再反向扫描看看有没有“不公平”

代码

```python

n = int(input())
a = [int(i) for i in input().split()]
candy = [1]*n

def left_scan():
    global candy
    settled = True
    for i in range(1,n):
        if a[i] > a[i-1] and candy[i] <= candy[i-1]:
            candy[i] = candy[i-1]+1
            settled = False
    return settled

def right_scan():
    global candy
    settled = True
    for i in range(n-2,-1,-1):
        if a[i] > a[i+1] and candy[i] <= candy[i+1]:
            candy[i] = candy[i+1]+1
            settled = False
    return settled

while True:
    A = left_scan()
    B = right_scan()
    if A and B:
        break
print(sum(candy))

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251021154851.png]]



### 1868A. Fill in the Matrix

constructive algorithms, implementation, 1300, https://codeforces.com/problemset/problem/1868/A

思路：

构造形如下的矩阵：
6 0 1 2 3 4 5
5 6 0 1 2 3 4
4 5 6 0 1 2 3
3 4 5 6 0 1 2
2 3 4 5 6 0 1
1 2 3 4 5 6 0
进行循环即可
这是最优解

代码

```python
t = int(input())
for _ in range(t):
    n,m = map(int,input().split())
    if m == 1:
        print(0)
        for i in range(n):
            print(0)
    else:
        print(min(m,n+1))
        for i in range(n):
            start = (-i-1) % (m - 1) + 1
            k = start
            for j in range(m):
                print(k,end=' ')
                k = (k+1) % m
            print()

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>


![[Pasted image 20251021165337.png]]


## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>



---
求逆序数：merge sort + count inv
```python
n = int(input())
num_list = [int(i) for i in input().split()]
inv = 0

def merge_sort(L,R):
    global num_list, inv
    if L+1 >= R:
        return
    mid = (L + R) // 2
    merge_sort(L,mid)
    merge_sort(mid,R)
    index_left = L
    index_right = mid
    combined_list = []
    while True:
        if index_left >= mid or index_right >= R:
            break
        if num_list[index_left] <= num_list[index_right]:
            combined_list.append(num_list[index_left])
            index_left += 1
        else:
            combined_list.append(num_list[index_right])
            inv += mid - index_left
            index_right += 1
    while index_left < mid:
        combined_list.append(num_list[index_left])
        index_left += 1
    while index_right < R:
        combined_list.append(num_list[index_right])
        index_right += 1
    for i in range(L,R):
        num_list[i] = combined_list[i - L]

merge_sort(0,n)
print(inv)

```
![[Pasted image 20251016161802.png]]

---
八皇后，easy！
![[Pasted image 20251016163004.png]]

---
快速幂+高精度 小菜一碟
![[Pasted image 20251016164755.png]]

---
二进制棋盘十字形联合反转：
深搜，但我感觉我这个解法Low爆了
```python
bitmap = []
manip = []
dirx = [0,0,-1,0,1]
diry = [0,1,0,-1,0]
#-----------------------------#
def printmap(lists):
    for i in range(5):
        for j in range(6):
            print(1 if lists[i][j] else 0,end=' ')
        print()
#-----------------------------#

for i in range(5):
    bitmap.append([True if _=='1' else False for _ in input().split()])
    manip.append([False]*6)

def search(kx,ky):
    if ky >= 6:
        return search(kx+1,ky-6)
    global manip,bitmap
    #--------------
    #print(f'kx={kx} ky={ky}')
    #print('manip')
    #printmap(manip)
    #print('bitmap')
    #printmap(bitmap)
    #--------------
    if kx==5:
        for i in range(6):
            if bitmap[4][i]:
                return False
        #print('solution found')
        return True
    for state in [True, False]:
        manip[kx][ky] = state
        # forward
        if state:
            for d in range(5):
                posx = kx + dirx[d]
                posy = ky + diry[d]
                if 0 <= posx < 5 and 0 <= posy < 6:
                    bitmap[posx][posy] = not bitmap[posx][posy]
        posx = kx - 1
        if (posx < 0) or (posx >= 0 and (not bitmap[posx][ky])):
            if search(kx, ky + 1):
                return True
        # recursion
        if state:
            for d in range(5):
                posx = kx + dirx[d]
                posy = ky + diry[d]
                if 0 <= posx < 5 and 0 <= posy < 6:
                    bitmap[posx][posy] = not bitmap[posx][posy]
search(0,0)
printmap(manip)
```
优化了一下：
```python
bitmap = []
manip = []
dirx = [0,0,-1,0,1]
diry = [0,1,0,-1,0]
#-----------------------------#
def printmap(lists):
    for i in range(5):
        for j in range(6):
            print(1 if lists[i][j] else 0,end=' ')
        print()
#-----------------------------#
for i in range(5):
    bitmap.append([True if _=='1' else False for _ in input().split()])
    manip.append([False]*6)

def stamp(kx,ky,state):
    if not state:
        return
    global bitmap
    for d in range(5):
        posx = kx + dirx[d]
        posy = ky + diry[d]
        if 0 <= posx < 5 and 0 <= posy < 6:
            bitmap[posx][posy] = not bitmap[posx][posy]
    return
def search(kx,ky):
    if ky >= 6:
        return search(kx + 1,ky - 6)
    global manip,bitmap
    #--------------
    if kx==5:
        for i in range(6):
            if bitmap[4][i]:
                return False
        return True
    #----------------------
    if kx == 0:
        for state in [True, False]:
            manip[kx][ky] = state
            stamp(kx,ky,state) # forward
            if search(kx, ky + 1):
                return True
            stamp(kx,ky,state) # recursion
        return False
    #--------kx > 0--------
    state = bitmap[kx - 1][ky]
    manip[kx][ky] = state
    stamp(kx,ky,state) # forward
    posx = kx - 1
    if search(kx, ky + 1):
        return True
    stamp(kx,ky,state) # recursion
    #----------------------
    return False
search(0,0)
printmap(manip)

```
![[Pasted image 20251016174239.png]]
应该有更加聪明的解法（？）

---

無神高题：
二进制串A和B长度均为n，从A变成B有$C_n^3$个**联合反转**开关，问拨动k个开关使得A变成B的总方法数？

考虑串A和串B，从串A变到串B的所有方法实际上都等价于从
$$
000\dots0\to A \oplus B
$$
因为任何的串S都可以映射为$S \oplus A$ , 且位的相对异同情况不变

因此实际上只需要考虑
$$
000\dots0\to S_1 \to S_2 \to \dots \to A \oplus B
$$
维护一个数组 $\rm dp[step][diff]$，表示从$000\dots0$出发到所有的串S满足S中有$\rm diff$个1的总方法数

对于任意一个有$\rm diff$个1的串$S$, 可以分成如下三种情况：
1. 对3个0位翻转，$\rm diff'=diff + 3$, $\rm cases = C_{N-diff}^3$
2. 对2个0位和1个1翻转，$\rm diff'=diff + 1$, $\rm cases = C_{N-diff}^2\cdot C_{diff}^1$
3. 对1个0位和2个1翻转，$\rm diff'=diff - 1$, $\rm cases = C_{N-diff}^1\cdot C_{diff}^2$
4. 对3个1翻转，$\rm diff'=diff - 3$, $\rm cases = C_{diff}^3$
```python
from math import *

dp[0][0] = 1
for step in range(1,total_steps):
    for diff in range(0,N):
        for j in range(4):# num of 1 chosen
            new_diff = diff + 3 - 2 * j
            if new_diff >= 0 and new_diff <= N:
                dp[new_diff][step + 1] += dp[diff][step] * comb(N - diff, 3 - j) * comb(diff, j)
```
如果不考虑一个开关拨动两回的情况，则又有变数：

在以上递推公式的基础上，我们还需要扣除因为拨动两回导致的多余解
	对$j$个1和$3-j$个0位翻转，$\rm diff'=diff + 3 - 2j$, 由于之前的数组元素都已经去除重复，所以由于如此拨动而造成重复拨动的情况，必然是本次操作与**先前操作P**重合了。我们需要求出这样的情况数。**先前操作P**可能位于第1~step共step回，并且由于操作**满足交换律**，因此**先前操作P**在这step步中每一步出现的情况数均相同。而去掉**先前操作P**和当前操作，**剩下的操作序列**均是不重合的。并且由于操作两回等价于恒等操作，因此**剩下的操作序列**是一个step-1步从0到S的操作序列。每个重复序列和（**P**，$\rm 0\overset{step-1}\to S_{diff}$）可以建立一一映射，因此其数量为$\rm dp[diff][step-1] \cdot step$

总结：
```python
from math import *

dp[0][0] = 1
for step in range(1,total_steps):
    for diff in range(0,N):
        for j in range(4):# num of 1 chosen
            new_diff = diff + 3 - 2 * j
            if new_diff >= 0 and new_diff <= N:
                route = dp[diff][step] * comb(N - diff, 3 - j) * comb(diff, j)
                repeat = dp[diff][step - 1] * step
                dp[new_diff][step + 1] +=  route - repeat 
```
正则表达式

