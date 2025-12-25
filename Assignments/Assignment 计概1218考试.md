## M04135:月度开销
[OpenJudge - 04135:月度开销](http://cs101.openjudge.cn/practice/04135/)

```python
import sys
lines = sys.stdin.read().splitlines()
n,m = map(int,lines[0].split())
a = [int(line.strip()) for line in lines[1::]]
max_money = max(a)
def judge(maxx):
    if maxx < max_money:
        return False
    fajos = 1
    current_left = maxx
    for i in range(n):
        
        if current_left >= a[i]:
            current_left -= a[i]
            continue
        fajos += 1
        current_left = maxx - a[i]
        if fajos > m:
            return False
    return True

def bisect():
    L,R = max_money,sum(a)
    while L + 1 < R:
        mid = (L+R)//2
        if judge(mid):
            R = mid
        else:
            L = mid + 1
    if not judge(L):
        return R
    return L

print(bisect())
```

## 20106:走山路
[OpenJudge - 20106:走山路](http://cs101.openjudge.cn/practice/20106/)

```python
from heapq import *
dirx = [1,0,-1,0]
diry = [0,1,0,-1]
n,m,p = map(int,input().split())
mapp = []
for i in range(n):
    line = [int(_) if _.isdigit() else -1 for _ in input().split()]
    mapp.append(line)

def judge(x,y):
    if x<0 or x >= n or y < 0 or y >= m:
        return False
    if mapp[x][y] == -1:
        return False
    return True

for _ in range(p):
    startx,starty,endx,endy = map(int,input().split())
    if mapp[startx][starty] == -1 or mapp[endx][endy] == -1:
        print('NO')
        continue
    visited = [[False]*m for i in range(n)]
    distance = [[1e9]*m for i in range(n)]
    heap = [[0,startx,starty]]
    heapify(heap)
    visited[startx][starty] = True
    distance[startx][starty] = 0
    found = False
    
    while heap:
        nowdis,nowx,nowy = heappop(heap)
        if (nowx,nowy) == (endx,endy):
            found = True
            print(nowdis)
            break
        for d in range(4):
            newx,newy = nowx+dirx[d],nowy+diry[d]
            if judge(newx,newy):
                visited[newx][newy] = True
                newdis = distance[nowx][nowy] + abs(mapp[nowx][nowy]-mapp[newx][newy])
                if newdis < distance[newx][newy]:
                    distance[newx][newy] = newdis
                    heappush(heap,[newdis,newx,newy])

    '''for line in visited:
        print(line)
    print()
    for line in distance:
        print(line)
    print()'''
    
    if found:
        continue
    print('NO')

```

## 28776:国王游戏
[OpenJudge - 28776:国王游戏](http://cs101.openjudge.cn/practice/28776/)

```python
n = int(input())
a,b = map(int,input().split())
money = []
prod = [1]*n
minister = [1]*n
for i in range(n):
    money.append(list(map(int,input().split())))
money = sorted(money,key = lambda x:x[0]*x[1])
prod[0] = 1
minister[0] = 1 // money[0][1]
for i in range(1,n):
    prod[i] = prod[i-1]*money[i-1][0]
    minister[i] = prod[i] // money[i][1]
print(max(minister))

```

## 26977:接雨水
[OpenJudge - 26977:接雨水](http://cs101.openjudge.cn/practice/26977/)

```python
n = int(input())
h = [int(_) for _ in input().split()]
stack = []

start = -1
for i in range(len(h)-1):
    if h[i]>h[i+1]:
        start = i
        break
water = 0
for i,height in enumerate(h):
    if not stack or height < stack[-1][1]:
        stack.append([i,height])
    else:
        while stack and stack[-1][1] <= height:
            x,h = stack.pop(-1)
            if stack:
                water += (i-stack[-1][0]-1)*(min(stack[-1][1],height)-h)
        stack.append([i,height])
    #print(stack,'water=',water)
print(water)

```

## T30212:二进制问题
[OpenJudge - 30212:二进制问题](http://cs101.openjudge.cn/practice/30212/)

```python
from math import comb
def solve(N,k):
    #print(N,k)
    if k == 0:
        return 1
    if N == 0:
        return 0
    l = len(str(bin(N)))-2
    if k > l:
        return 0
    result = comb(l-1,k) + solve(N - (1 << (l-1)),k-1)
    #print('result=',result)
    return result
n,k = map(int,input().split())
if not k:
    print(0)
else:
    print(solve(n,k))
```

## T30339:愉悦的假期
[OpenJudge - T30339:愉悦的假期](http://cs101.openjudge.cn/20251218mockexam/T30339/)

描述

新年&春节假期要来了，陈哥也来到了富人岛上找李哥游玩。

李哥在富人岛群上拥有三座小岛，为了方便，这块海域用一个N*M的矩阵来表示，像这样：  
```
................  
..XXXX....XXX...  
...XXXX....XX...  
.XXXX......XXX..  
........XXXXX...  
..XXX....XXX....
```
每个 X 表示小岛的一部分。如果两个 X 在竖直或水平方向上相邻，则它们属于同一个小岛（对角线相邻不算），而 . 则表示这里是海水。

陈哥觉得用游艇往来不安全，因此想帮李哥财大气粗地把三座小岛联通，具体来说，就是填海：可以选择将 . 填成陆地 X 。对于上图，下面是一种填海格点数最少的方案：  
```
................  
..XXXX....XXX...  
...XXXX*...XX...  
.XXXX..**..XXX..  
...*....XXXXX...  
..XXX....XXX....  
```
（只填了四个格点，填海的使用*来表示）

你知道的，李哥向来喜好省钱，为了他们俩能拥有一个愉悦的假期，所以请你帮陈哥想一个最少填海格点数的方案。

输入

第一行两个整数 N,M（1≤N,M≤50）。  
接下来 N 行，每行 M 个字符（ . 或 X），描述李哥的小岛在海域内的分布情况。保证恰好有三个小岛。

输出

输出将三个小岛通过填海联通最少需要填多少格点。

样例输入

```
6 16
................
..XXXX....XXX...
...XXXX....XX...
.XXXX......XXX..
........XXXXX...
..XXX....XXX....
```

样例输出
```
4
```
提示

友善的陈哥提醒你：  
1. 岛之间联通起来的形式只有两种情况  
2. 计算一个位置到另一个位置之间的距离可以利用 |xi-xj| + |yi-yj| （即曼哈顿距离，当然你也可以不用）