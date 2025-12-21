
# f-string输出格式：
```python
pi = 3.1415926535

# 保留2位小数
print(f"{pi:.2f}")      # 3.14

# 保留5位小数
print(f"{pi:.5f}")      # 3.14159

# 保留0位小数（取整）
print(f"{pi:.0f}")      # 3
```

---
# LRU_cache演示使用方法 数的划分
```python
from functools import lru_cache

# 例1：计算整数n的划分方案数（无序划分）
@lru_cache(maxsize=None)  # maxsize=None表示缓存没有大小限制
def partition(n, m=None):
    """
    将整数n划分成若干个正整数之和的方案数
    m: 划分中最大的部分
    """
    if m is None:
        m = n
    
    # 基础情况
    if n == 0:
        return 1
    if n < 0 or m == 0:
        return 0
    
    # 递归关系：包含m的划分 + 不包含m的划分
    return partition(n - m, m) + partition(n, m - 1)

# 测试
print(partition(5))  # 输出: 7
print(partition(10))  # 输出: 42
print(partition.cache_info())  # 查看缓存信息
```

---
# merge sort + count inv
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

---
# 快速幂
```python
def pow_mod(a, b, m):
    """快速幂取模 - 一行实现"""
    r = 1
    while b:
        if b & 1: r = r * a % m
        a = a * a % m
        b >>= 1
    return r % m
```

矩阵快速幂：
```python
def mat_mul(A, B, m):
    """矩阵乘法取模"""
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % m
    return C

def mat_pow(A, b, m):
    """矩阵快速幂"""
    n = len(A)
    # 单位矩阵
    res = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
    while b:
        if b & 1:
            res = mat_mul(res, A, m)
        A = mat_mul(A, A, m)
        b >>= 1
    return res
```


---
# 熄灯问题：
深搜
```python
def solve_lights_out():
    # 读入初始状态
    grid = [list(map(int, input().split())) for _ in range(5)]
    
    # 枚举第一行的所有操作状态
    for first in range(1 << 6):
        cur = [row[:] for row in grid]  # 当前状态
        press = [[0] * 6 for _ in range(5)]  # 操作记录
        
        # 设置第一行的操作
        for j in range(6):
            if first >> j & 1:
                press[0][j] = 1
                # 按下(0,j)的影响
                for dx, dy in [(0,0), (-1,0), (1,0), (0,-1), (0,1)]:
                    x, y = dx, dy + j
                    if 0 <= x < 5 and 0 <= y < 6:
                        cur[x][y] ^= 1
        
        # 递推确定其他行的操作
        for i in range(1, 5):
            for j in range(6):
                if cur[i-1][j] == 1:  # 上一行灯亮着，必须按当前位置
                    press[i][j] = 1
                    for dx, dy in [(0,0), (-1,0), (1,0), (0,-1), (0,1)]:
                        x, y = i + dx, j + dy
                        if 0 <= x < 5 and 0 <= y < 6:
                            cur[x][y] ^= 1
        
        # 检查最后一行是否全灭
        if all(cur[4][j] == 0 for j in range(6)):
            for row in press:
                print(' '.join(map(str, row)))
            return

# 调用函数
if __name__ == "__main__":
    solve_lights_out()
```

---
# 基于堆的优先队列卷积，并取出前几个元素：

```python
import heapq

T = int(input())

def convolve(seqs, n):
    """使用堆合并多个有序序列的前n个最小和"""
    if not seqs:
        return []
    if len(seqs) == 1:
        return seqs[0][:n]
    
    # 递归分治合并
    mid = len(seqs) // 2
    left = convolve(seqs[:mid], n)
    right = convolve(seqs[mid:], n)
    
    # 使用堆合并两个有序序列的前n个最小和
    heap = [(left[0] + right[0], 0, 0)]
    visited = {(0, 0)}
    result = []
    
    while len(result) < n:
        num, i, j = heapq.heappop(heap)
        result.append(num)
        
        # 扩展下一个可能的组合
        if i + 1 < len(left) and (i + 1, j) not in visited:
            heapq.heappush(heap, (left[i + 1] + right[j], i + 1, j))
            visited.add((i + 1, j))
        if j + 1 < len(right) and (i, j + 1) not in visited:
            heapq.heappush(heap, (left[i] + right[j + 1], i, j + 1))
            visited.add((i, j + 1))
    
    return result

for _ in range(T):
    m, n = map(int, input().split())
    seqs = []
    
    # 读取m个有序序列
    for _ in range(m):
        seq = sorted(map(int, input().split()))
        seqs.append(seq)
    
    # 计算合并后的前n个最小和
    result = convolve(seqs, n)
    print(*result)
```

---
# 食物链：边上带有信息的并查集
```python
class UFS:
    def __init__(self, items = 0):
        """initialization"""
        self.point = [(i,0) for i in range(items)] # phase: relative to me (x)!
        self.depth = [1 for i in range(items)]

    def union(self, x, y, phase):# phase: y relative to x
        x, phase_x = self.find(x)
        y, phase_y = self.find(y)
        phase = phase - phase_x + phase_y
        phase %= 3
        if x == y:
            if phase != 0:
                return False
            else:
                return True
        if self.depth[x] > self.depth[y]:
            self.point[y] = (x,(-phase) % 3)
            self.depth[x] = max(self.depth[x], self.depth[y] + 1)
        else:
            self.point[x] = (y,phase)
            self.depth[y] = max(self.depth[y], self.depth[x] + 1)
        return True

    def find(self, x):
        #print('x= ',x)
        if self.point[x][0] == x:
            return (x, 0)
        root, phase = self.find(self.point[x][0])
        phase += self.point[x][1]
        phase %= 3
        self.point[x] = (root, phase)
        return (root, phase)

    def __str__(self):
        return str(self.point)

n,k = map(int,input().split())
ufs = UFS(n + 1)
fake = 0
for i in range(k):
    d,x,y = map(int,input().split())
    if (x > n) or (y > n) or (not ufs.union(x,y,d-1)):
        fake += 1
print(fake)

```

AI version:
```python
class UFS:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rel = [0] * n  # rel[i] 表示 i 到 parent[i] 的关系 (0:同类, 1: i 吃 parent[i], 2: parent[i] 吃 i)
        self.depth = [1] * n  # 按秩合并的深度

    def find(self, x):
        if self.parent[x] == x:
            return (x, 0)
        root, r = self.find(self.parent[x])
        # 更新 x 到根节点的关系：x->parent[x] + parent[x]->root
        new_rel = (self.rel[x] + r) % 3
        self.parent[x] = root
        self.rel[x] = new_rel
        return (root, new_rel)

    def union(self, x, y, phase):
        x_root, x_rel = self.find(x)
        y_root, y_rel = self.find(y)
        if x_root == y_root:
            # 检查 x 和 y 的关系是否符合要求
            if (x_rel - y_rel) % 3 != phase:
                return False
            return True
        else:
            # 按深度合并：将深度小的树挂到深度大的树上
            if self.depth[x_root] >= self.depth[y_root]:
                # 将 y_root 挂到 x_root 上
                r = (x_rel - y_rel - phase + 3) % 3
                self.parent[y_root] = x_root
                self.rel[y_root] = r
                if self.depth[x_root] == self.depth[y_root]:
                    self.depth[x_root] += 1
                return True
            else:
                # 将 x_root 挂到 y_root 上
                r = (phase - x_rel + y_rel + 3) % 3
                self.parent[x_root] = y_root
                self.rel[x_root] = r
                if self.depth[x_root] == self.depth[y_root]:
                    self.depth[y_root] += 1
                return True

def main():
    import sys
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    k = int(data[1])
    ufs = UFS(n)
    fake = 0
    index = 2
    for _ in range(k):
        d = int(data[index])
        x = int(data[index + 1])
        y = int(data[index + 2])
        index += 3
        # 检查 2: X 或 Y 超出范围
        if x > n or y > n:
            fake += 1
            continue
        # 检查 3: X 吃 X
        if d == 2 and x == y:
            fake += 1
            continue
        # 转换为 0-indexed
        x0 = x - 1
        y0 = y - 1
        if not ufs.union(x0, y0, d - 1):
            fake += 1
    print(fake)

if __name__ == "__main__":
    main()
```

---
# 接雨水：单调栈
1. 双指针
每个点的积水高度为其左侧的$\rm max\_height$和右侧$\rm max\_height$的minimum
将从左往右和从右往左的$\rm max\_height$记为$\rm leftmax$和$\rm rightmax$
因此如果短板在左侧：$\rm leftmax(pos - 1) < \rm rightmax(pos + k)$，则该格水位高度为左侧的max
此时可以把pos的水量算出来，并向右前进一格）（或者更新max）
如果不然，则右侧为短板，显然右侧可以求出水量并累计，右指针向左进发

用双指针法简单得多：
```python
t = int(input())
for _ in range(t):
    n = int(input())
    height = [int(i) for i in input().split()]
    leftmax = 0
    rightmax = 0
    left = 0
    right = n - 1
    water = 0
    while left <= right:
        if leftmax <= rightmax:# move left
            water += max(leftmax - height[left],0)
            leftmax = max(leftmax, height[left])
            left += 1
        else:
            water += max(rightmax - height[right],0)
            rightmax = max(rightmax, height[right])
            right -= 1
    print(water)
```
2. dp
维护一个点的leftmax和rightmax数组（$\rm O(n)$）然后直接求和
```python
t = int(input())
for _ in range(t):
    n = int(input())
    height = [int(i) for i in input().split()]
    leftmax = [-1] * n
    rightmax = [-1] * n
    leftmax[0] = height[0]
    rightmax[n - 1] = height[n - 1]
    water = 0
    for i in range(1,n):
        leftmax[i] = max(leftmax[i - 1], height[i])
    for i in range(n - 2,-1,-1):
        rightmax[i] = max(rightmax[i + 1], height[i])
    for i in range(n):
        water += min(leftmax[i], rightmax[i]) - height[i]
    print(water)
```
3. 单调栈
```python
n = int(input())
h = list(map(int, input().split()))

stack = []  # 存储索引的单调递减栈
water = 0

for i, height in enumerate(h):
    # 当当前高度大于栈顶高度时，可以形成凹槽
    while stack and h[stack[-1]] < height:
        bottom = stack.pop()  # 弹出底部
        if not stack:
            break  # 没有左边界，无法接水
        left = stack[-1]  # 左边界索引
        width = i - left - 1  # 凹槽宽度
        depth = min(h[left], height) - h[bottom]  # 可接水深度
        water += width * depth
    
    stack.append(i)

print(water)
```


---
# 护林员盖房子：单调栈
这个单调栈搞起来真麻烦，一开始调试的时候死活调不对。这个和接雨水是类似的，都需要找到下凹或者上突序列并统计。**单调栈可以理解为：每次弹出都相当于填平沟壑（或者削平山峰）**

<mark>还没有代码</mark>

---
# 删除数字问题：单调栈

```python
s = input().strip()
k = int(input())

stack = []
to_remove = k

for ch in s:
    while stack and stack[-1] > ch and to_remove > 0:
        stack.pop()
        to_remove -= 1
    stack.append(ch)

# 如果还有剩余删除次数，从末尾删除（因为此时栈是递增的）
result = ''.join(stack[:len(stack) - to_remove])

# 去除前导零（但保留最后一个0）
print(int(result) if result else 0)
```
---
# next_permutation:

## 算法1：Narayana Pandita 算法（直接模拟k次）

```python
import bisect

def succ(arr, n):
    for _ in range(k):
        i = n - 2
        while i >= 0 and arr[i] >= arr[i + 1]:
            i -= 1
        if i < 0:
            arr = list(range(1, n + 1))
            continue
        j = n - 1
        while arr[j] <= arr[i]:
            j -= 1
        arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1:] = reversed(arr[i + 1:])
    return arr

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    print(*succ(arr, n))
```

## 算法2：康托展开（数学方法）

```python
def succ(arr, n, k):
    # 康托展开
    fact = 1
    for i in range(2, n):
        fact *= i
    
    code = [0] * n
    for i in range(n):
        cnt = 0
        for j in range(i + 1, n):
            if arr[j] < arr[i]:
                cnt += 1
        code[i] = cnt
    
    # 将康托编码视为特殊进制数并加k
    carry = n - 1
    code[-1] += k
    for i in range(n - 1, 0, -1):
        if code[i] > carry:
            code[i - 1] += code[i] // (carry + 1)
            code[i] %= (carry + 1)
        carry -= 1
    
    # 逆康托展开
    used = [False] * (n + 1)
    result = []
    for i in range(n):
        cnt = code[i]
        num = 1
        while cnt or used[num]:
            if not used[num]:
                cnt -= 1
            num += 1
        used[num] = True
        result.append(num)
    
    return result

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    print(*succ(arr, n, k))
```

## 极简版（使用Python内置函数）

如果允许使用Python的itertools，可以更简单：

```python
import itertools

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    arr = tuple(map(int, input().split()))
    perms = list(itertools.permutations(range(1, n + 1)))
    idx = perms.index(arr)
    result = perms[(idx + k) % len(perms)]
    print(*result)
```

## 主要精简点：

1. **移除多余函数定义**：将函数内联到主逻辑中
2. **简化变量名**：使用更短的变量名
3. **优化算法逻辑**：
   - 算法1：使用`reversed()`简化序列反转
   - 算法2：简化康托编码的计算
4. **减少代码行数**：通过合并操作减少代码行数
5. **使用Python特性**：如列表切片、内置函数等

**注意**：算法2中，carry的变化是因为第i位的最大值为`n-i-1`，所以进制从`n-1`递减到`0`。

---
# 世界杯只因：贪心-区间点覆盖

经典的贪心-区间覆盖
```python
n = int(input())
a = [int(i) for i in input().split()]
ranges = []
for i,d in enumerate(a):
    ranges.append([i - d,i + d])
ranges = sorted(ranges, key = lambda x:x[0])
right = 0 # the first right point which can't be covered
index = 0
cameras = 0
while right < n:
    cameras += 1
    rightmax = right - 1
    #print(f'right = {right} index = {index} cameras = {cameras}')
    while index < n and ranges[index][0] <= right: # index<n prevent out of range
        rightmax = max(ranges[index][1],rightmax)
        index += 1
    right = rightmax + 1 #the first uncovered point is the next og 
print(cameras)
```
$\rm index<n$防止越界，但是不能$\rm index<n - 1$，这样就会漏掉最后一个区间了

# 区间问题

## 1. 区间合并（Merge Intervals）：左端点排序

```python
def merge_intervals(intervals):
    """合并重叠区间"""
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged
```

## 2. 无重叠区间（Non-overlapping Intervals）：右端点排序

```python
def erase_overlap_intervals(intervals):
    """移除最少数量的区间使剩余区间互不重叠"""
    if not intervals:
        return 0
    
    # 按结束时间排序
    intervals.sort(key=lambda x: x[1])
    count = 0
    end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:  # 有重叠
            count += 1
        else:
            end = intervals[i][1]
    
    return count
```

## 3. 区间覆盖（Minimum Interval Coverage）：左端点排序，贪心右端点

```python
def min_intervals_to_cover(target, intervals):
    """选择最少数量的区间覆盖目标区间"""
    intervals.sort(key=lambda x: x[0])
    result = []
    i = 0
    current_end = target[0]
    
    while i < len(intervals) and current_end < target[1]:
        max_end = current_end
        # 选择能覆盖当前起点的最长区间
        while i < len(intervals) and intervals[i][0] <= current_end:
            max_end = max(max_end, intervals[i][1])
            i += 1
        
        if max_end == current_end:  # 无法扩展覆盖
            return []
        
        result.append([current_end, max_end])
        current_end = max_end
    
    return result if current_end >= target[1] else []
```

## 4. 会议室问题（Meeting Rooms）（校门外的树问题）

```python
def can_attend_meetings(intervals):
    """判断能否参加所有会议（无重叠）"""
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True

def min_meeting_rooms(intervals):
    """需要的最少会议室数量"""
    starts = sorted(i[0] for i in intervals)
    ends = sorted(i[1] for i in intervals)
    
    rooms = 0
    end_ptr = 0
    
    for start in starts:
        if start < ends[end_ptr]:
            rooms += 1
        else:
            end_ptr += 1
    
    return rooms
```

## 5. 区间查询优化（前缀和）

```python
def interval_sum(nums, intervals):
    """快速计算多个区间和（前缀和优化）"""
    n = len(nums)
    prefix = [0] * (n + 1)
    
    # 构建前缀和数组
    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + nums[i - 1]
    
    # 查询区间和
    result = []
    for left, right in intervals:
        result.append(prefix[right + 1] - prefix[left])
    
    return result
```

## 6. 贪心区间选择（Select Intervals）：右端点排序，贪心右端点

```python
def select_intervals(intervals):
    """选择最多不重叠区间（贪心）"""
    if not intervals:
        return 0
    
    # 按结束时间排序
    intervals.sort(key=lambda x: x[1])
    count = 1
    end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] >= end:
            count += 1
            end = intervals[i][1]
    
    return count
```

## 综合使用示例

```python
# 示例：解决多个区间问题
intervals = [[1,3], [2,6], [8,10], [15,18]]
new_interval = [4,9]

print("原始区间:", intervals)
print("合并后:", merge_intervals(intervals))
print("插入[4,9]后:", insert_interval(intervals, new_interval))
print("可参加所有会议:", can_attend_meetings(intervals))

# 计算区间交集
A = [[0,2], [5,10], [13,23], [24,25]]
B = [[1,5], [8,12], [15,24], [25,26]]
print("区间交集:", interval_intersection(A, B))

# 无重叠区间
intervals2 = [[1,2], [2,3], [3,4], [1,3]]
print("需移除区间数:", erase_overlap_intervals(intervals2))
```

## 关键技巧总结：

1. **排序是关键**：大多数区间问题都需要先按起点或终点排序
2. **贪心策略**：按结束时间排序通常能得到最优解
3. **扫描线算法**：将区间拆分为起点和终点事件
4. **差分数组**：用于区间批量更新
5. **前缀和**：用于快速区间查询
6. **双指针**：处理两个区间列表的交集

---

# 最大与最小整数：循环小数排序
```python
n = int(input())
a = [i for i in input().split()]
a = sorted(a,key = lambda x: int(x) / (10**(len(x))-1))
print(''.join(a[::-1]),''.join(a))
```


---
# 跳房子

```python
from collections import deque

while True:
    n,m = map(int,input().split())
    if n == 0 and m == 0:
        break
    # Create a deque object
    queue = deque()
    
    queue.append([n,'']) # position, sequence
    visited = {n}
    if m == n:
        print('1\n\n')
    while True:
        pos,seq = queue.popleft()
        for i in range(2):
            if i==0:
                nowpos, nowseq = pos * 3, seq + 'H'
            else:
                nowpos, nowseq = pos // 2, seq + 'O'
            if nowpos in visited:
                continue
            queue.append([nowpos,nowseq])
            visited.add(nowpos)
            if nowpos == m:
                print(len(nowseq))
                print(nowseq)
                break
        if nowpos == m:
            break
        if len(nowseq) > 25:
            print('no solution')
            break

```

---
## Dijkstra算法：
```python
import heapq

def dijkstra(n, start, graph):
    """邻接矩阵版 Dijkstra"""
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]  # (距离, 节点)
    
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v in range(n):
            if graph[u][v] > 0 and dist[v] > d + graph[u][v]:
                dist[v] = d + graph[u][v]
                heapq.heappush(heap, (dist[v], v))
    return dist
```

---
# Kadane

```python
def max_subarray_sum(arr):
    """基础Kadane算法：返回最大子数组和"""
    max_sum = curr_sum = arr[0]
    for num in arr[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum

def max_subarray(arr):
    """Kadane算法：返回最大和及子数组的起止索引"""
    max_sum = curr_sum = arr[0]
    start = end = 0
    curr_start = 0
    
    for i in range(1, len(arr)):
        if arr[i] > curr_sum + arr[i]:
            curr_sum = arr[i]
            curr_start = i
        else:
            curr_sum = curr_sum + arr[i]
        
        if curr_sum > max_sum:
            max_sum = curr_sum
            start = curr_start
            end = i
    
    return max_sum, start, end
```

---
# Manacher

```python
def longest_palindrome(s):
    """Manacher算法：返回最长回文子串"""
    if not s:
        return ""
    
    # 预处理字符串，插入特殊字符
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n  # 回文半径数组
    center = right = max_len = start = 0
    
    for i in range(n):
        # 利用对称性初始化回文半径
        if i < right:
            p[i] = min(right - i, p[2 * center - i])
        
        # 尝试扩展回文
        while i - p[i] - 1 >= 0 and i + p[i] + 1 < n and t[i - p[i] - 1] == t[i + p[i] + 1]:
            p[i] += 1
        
        # 更新中心和右边界
        if i + p[i] > right:
            center = i
            right = i + p[i]
        
        # 更新最长回文信息
        if p[i] > max_len:
            max_len = p[i]
            start = (i - max_len) // 2
    
    return s[start:start + max_len]
```
---
# 购物：dp+贪心
```python
value, ncoin = map(int,input().split())
coins = [int(_) for _ in input().split()]
coins = sorted(coins,reverse = True)
available = 0
cnt = 0
while available < value:
    # studying available + 1
    for coin in coins:
        if available + 1 - coin >= 0:
            cnt += 1
            available += coin
            break
print(cnt)
```

---
# 排队
```python
n,d = map(int,input().split())
h = []
for i in range(n):
    h.append(int(input()))
result = []
used = [False] * n
while len(result)<n:
    seq = [] # Those who can swap to the front
    cur_max = -1
    cur_min = 1e10
    for i in range(0,n):
        if used[i]:#skip used men
            continue
        cur_max = max(cur_max,h[i])
        cur_min = min(cur_min,h[i])
        if cur_max - h[i] <= d and h[i] - cur_min <= d:
            used[i] = True
            seq.append(h[i])
    result = result + sorted(seq)# Fronters float
for j in result:
    print(j)
```

---
## Book my spacecraft内容

随着做题量的增加，你对栈和队列这两种数据结构的理解会越来越多元。

- 从数据处理的角度，栈和队列为数据处理提供了一种逻辑思路。

如[OpenJudge - T29947:校门外的树又来了](http://cs101.openjudge.cn/pctbook/T29947/)，我们可以利用`stack`
对种树的区间进行合并。按左端点排序遍历区间，如果当前区间与栈尾的区间有重叠，则更新栈尾的区间，否则将当前区间压入栈中。

```python
L, M = map(int, input().split())
interval = []
for _ in range(M):
    interval.append(list(map(int, input().split())))
interval.sort()
stack = []
for t in interval:
    if stack and t[0] <= stack[-1][1]:
        stack[-1][1] = max(stack[-1][1], t[1])
    else:
        stack.append(t)
print(L + 1 - sum(map(lambda x: x[1] - x[0] + 1, stack)))
```

如[OpenJudge - 27371:Playfair密码](http://cs101.openjudge.cn/practice/27371/)，其中有一步是将明文转变为字母对，我们可以利用
`stack`进行处理。

```python
word = input()
stack = []
for a in word:
    if a == 'j':
        a = 'i'
    if not stack:
        stack.append(a)
        continue
    if len(stack[-1]) == 2:
        stack.append(a)
        continue
    if stack[-1] != a:
        b = stack.pop()
        stack.append(b + a)
    else:
        if stack[-1] == 'x':
            stack.pop()
            stack.append('xq')
            stack.append(a)
        else:
            b = stack.pop()
            stack.append(b + 'x')
            stack.append(a)
if len(stack[-1]) == 1:
    if stack[-1] == 'x':
        stack.pop()
        stack.append('xq')
    else:
        b = stack.pop()
        stack.append(b + 'x')
```

---

# TSP 问题：
```python
from functools import lru_cache

n = int(input())
cost = [list(map(int, input().split())) for _ in range(n)]

@lru_cache(maxsize=None)
def dfs(mask, i):
    if mask == (1 << n) - 1:
        return cost[i][0] or float('inf')
    
    res = float('inf')
    for j in range(n):
        if not (mask >> j & 1) and cost[i][j]:
            res = min(res, cost[i][j] + dfs(mask | (1 << j), j))
    return res

print(dfs(1, 0))  # 从城市0开始，mask=1表示城市0已访问
```

---

# candy贪心：

每一种方案都唯一对应一些$(x_i,y_i)$和一些互不相同的$x_i$

根据贪心的原理，我们应该全部选用最小的$(x_i+y_i)$，互不相同的$x_i$应该从小往大选

代码

```python
n,m = map(int,input().split())
x = []
summ = []
for i in range(n):
    xi,yi = map(int,input().split())
    x.append(xi)
    summ.append(xi+yi)
x = sorted(x)
couple = min(summ)

single = 0
epochs = m // couple * 2
for i in range(n):
    single += x[i]
    epochs = max(epochs,i + 1 + (m-single) // couple * 2)
print(epochs)
```