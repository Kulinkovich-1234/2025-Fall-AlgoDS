# Assignment #C: bfs & dp

Updated 1436 GMT+8 Nov 25, 2025

2025 fall, Complied by 马健文 元培学院



**说明：**

1）请把每个题目解题思路（可选），源码Python, 或者C++（已经在Codeforces/Openjudge上AC），截图（包含Accepted），填写到下面作业模版中（推荐使用 typora https://typoraio.cn ，或者用word）。AC 或者没有AC，都请标上每个题目大致花费时间。

2）提交时候先提交pdf文件，再把md或者doc文件上传到右侧“作业评论”。Canvas需要有同学清晰头像、提交文件有pdf、"作业评论"区有上传的md或者doc附件。

3）如果不能在截止前提交作业，请写明原因。



## 1. 题目

### sy321迷宫最短路径

bfs, https://sunnywhy.com/sfbj/8/2/321

思路：

通过prev数组记录每个点的上个点

代码：

```python
from collections import deque
dirs = [[1,0],[0,1],[-1,0],[0,-1]]
n,m = map(int,input().split())
mapp = [[int(_) for _ in input().split()] for i in range(n)]
q = deque([(0,0,0)])
visited = [[False]*m for _ in range(n)]
prev = [[(-1,-1)]*m for _ in range(n)]
def judge(x,y):
    return (0<=x<n) and (0<=y<m) and mapp[x][y] == 0
def backtrack(x,y):
    if (x,y) != (0,0):
        prevx,prevy = prev[x][y][0],prev[x][y][1]
        backtrack(prevx,prevy)
    print(x+1,y+1)
found = False
while q:
    start = q.popleft()
    startx,starty = start[0],start[1]
    for d in range(4):
        newx,newy = startx + dirs[d][0],starty + dirs[d][1]
        if judge(newx,newy) and not visited[newx][newy]:
            q.append((newx,newy))
            visited[newx][newy] = True
            prev[newx][newy] = (startx,starty)
            if (newx,newy) == (n-1,m-1):
                backtrack(newx,newy)
                found = True
                break
    if found:
        break

        

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251202153718.png]]



### sy324多终点迷宫问题

bfs, https://sunnywhy.com/sfbj/8/2/324

思路：

bfs，记录distance即可

代码：

```python
from collections import deque
dirs = [[1,0],[0,1],[-1,0],[0,-1]]
n,m = map(int,input().split())
mapp = [[int(_) for _ in input().split()] for i in range(n)]
q = deque([(0,0,0)])
visited = [[False]*m for _ in range(n)]
dist = [[-1]*m for _ in range(n)]
def judge(x,y):
    return (0<=x<n) and (0<=y<m) and mapp[x][y] == 0
def backtrack(x,y):
    if (x,y) != (0,0):
        prevx,prevy = prev[x][y][0],prev[x][y][1]
        backtrack(prevx,prevy)
    print(x+1,y+1)
found = False
visited[0][0] = True
dist[0][0] = 0
while q:
    start = q.popleft()
    startx,starty = start[0],start[1]
    for d in range(4):
        newx,newy = startx + dirs[d][0],starty + dirs[d][1]
        if judge(newx,newy) and not visited[newx][newy]:
            q.append((newx,newy))
            visited[newx][newy] = True
            dist[newx][newy] = dist[startx][starty] + 1
for _ in dist:
    print(*_)
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251202154050.png]]



### M02945: 拦截导弹

dp, greedy http://cs101.openjudge.cn/pctbook/M02945

思路：

dp, 最长下降子序列

代码：

```python
n = int(input())
heights = [int(_) for _ in input().split()]
dp = [0] * n
for i in range(n):
    dp[i] = 1
    for j in range(i):
        if heights[j] >= heights[i]:
            dp[i] = max(dp[i],dp[j] + 1)
print(max(dp))

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251202155102.png]]



### 189A. Cut Ribbon

brute force/dp, 1300, https://codeforces.com/problemset/problem/189/A

思路：

dp最大可以切的段数

代码：

```python
n,a,b,c = map(int,input().split())
pieces = [-1e9] * (n+1)
pieces[0] = 0
for i in range(1,n+1):
    if i >= a:
       pieces[i] = max(pieces[i],pieces[i-a] + 1)
    if i >= b:
       pieces[i] = max(pieces[i],pieces[i-b] + 1)
    if i >= c:
       pieces[i] = max(pieces[i],pieces[i-c] + 1)
print(pieces[n])


```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251202160155.png]]





### M01384: Piggy-Bank

dp, http://cs101.openjudge.cn/practice/01384/

思路：

dp，每个重量下的最小可能面值（不可能就用inf）

代码：

```python
t = int(input())
inf = int(1e9+7)
for _ in range(t):
    empty,filled = map(int,input().split())
    n = int(input())
    coins = []
    for i in range(n):
        coins.append(list(map(int,input().split()))) # coins[][0] = price, coins[][1] = weight
    weight = filled - empty
    dp = [inf] * (weight + 1)
    dp[0] = 0
    for i in range(1,weight + 1):
        for j in coins:
            if i >= j[1]:
                dp[i] = min(dp[i],dp[i - j[1]] + j[0])
    if dp[weight] == inf:
        print('This is impossible.')
    else:
        print(f'The minimum amount of money in the piggy-bank is {dp[weight]}.')

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251202162016.png]]



### M02766: 最大子矩阵

dp, kadane, http://cs101.openjudge.cn/pctbook/M02766

思路：

枚举上下边界进行1D Kadane

代码：

```python
import sys
lines = sys.stdin.read().splitlines()
N = int(lines[0].split()[0])
nums = []
for line in lines[1::]:
    num = [int(_) for _ in line.split()]
    nums = nums + num
matrix = [[0]*(N + 1)] + [[0] + nums[i*N:i*N+N] for i in range(N)]
summ = [[0]*(N + 1) for _ in range(N + 1)]
for i in range(1,N+1):
    for j in range(1,N+1):
        summ[i][j] = summ[i][j-1] + summ[i-1][j] - summ[i-1][j-1] + matrix[i][j]
area = 0
def kadane(list1):
    minimum_so_far = list1[0]
    result = 0
    for i in range(1,N+1):
        minimum_so_far = min(minimum_so_far,list1[i])
        result = max(result,list1[i] - minimum_so_far)
    return result
for U in range(1,N+1):
    for D in range(U,N+1):
        list1 = [(summ[D][i] - summ[U - 1][i]) for i in range(N+1)]
        area = max(area,kadane(list1))
print(area)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251202165944.png]]



## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2024fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>


```python
sys.setrecursionlimit(3000)

@lru_cache(maxsize=128)  # maxsize=None表示无限缓存
def fib_with_cache(n):
    if n < 2:
        return n
    return fib_with_cache(n-1) + fib_with_cache(n-2)

# translate方法示例

# 创建转换表
# 方法1: 使用str.maketrans()
translation_table1 = str.maketrans('aeiou', '12345')
text = "hello world"
result1 = text.translate(translation_table1)
print(f"转换1: '{text}' -> '{result1}'")

# 方法2: 使用字典创建转换表
translation_dict = {97: 65, 98: 66, 99: 67}  # ASCII: a->A, b->B, c->C
translation_table2 = str.maketrans(translation_dict)
text2 = "abc def"
result2 = text2.translate(translation_table2)
print(f"转换2: '{text2}' -> '{result2}'")

# 方法3: 删除特定字符
# 第三个参数指定要删除的字符
translation_table3 = str.maketrans('', '', 'aeiou')
text3 = "beautiful python"
result3 = text3.translate(translation_table3)
print(f"删除元音: '{text3}' -> '{result3}'")

# 实际应用：清理字符串
import string
# 删除所有标点符号
translator = str.maketrans('', '', string.punctuation)
text4 = "Hello, World! This is a test."
result4 = text4.translate(translator)
print(f"清理标点: '{text4}' -> '{result4}'")

# 删除数字
translator2 = str.maketrans('', '', string.digits)
text5 = "Room 101 is at floor 5"
result5 = text5.translate(translator2)
print(f"删除数字: '{text5}' -> '{result5}'")


sys.stdin.read().splitline()


# f-string 格式化示例
name = "Alice"
age = 25
height = 1.68

# 基本f-string
print(f"姓名: {name}, 年龄: {age}, 身高: {height}")

# 格式化浮点数 %f 风格
pi = 3.141592653589793

# 1. 固定宽度和小数位数
print(f"Pi值: {pi:.2f}")      # 两位小数
print(f"Pi值: {pi:8.3f}")    # 总宽度8，3位小数
print(f"Pi值: {pi:08.3f}")   # 用0填充宽度

# 2. 科学计数法
print(f"科学计数: {pi:.2e}")
print(f"科学计数: {pi:12.3e}")

# 3. 百分比格式
score = 0.875
print(f"百分比: {score:.1%}")
print(f"百分比: {score:.2%}")

# 4. 对齐和填充
number = 123.456
print(f"左对齐: |{number:<10.2f}|")
print(f"右对齐: |{number:>10.2f}|")
print(f"居中对齐: |{number:^10.2f}|")
print(f"用*填充: |{number:*^10.2f}|")

# 5. 大数字分隔符
big_number = 1234567.8912
print(f"千位分隔: {big_number:,.2f}")
print(f"千位分隔: {big_number:_.2f}")  # 使用下划线分隔

# 6. 条件格式化
temperature = 23.5
print(f"温度: {temperature:.1f}°C ({'热' if temperature > 25 else '舒适'})")

# 7. 表达式内计算
radius = 5
print(f"半径 {radius} 的圆面积: {3.14159 * radius ** 2:.2f}")

# 8. 格式化字典
person = {"name": "Bob", "age": 30, "salary": 50000.50}
print(f"员工: {person['name']}, 年龄: {person['age']}, 薪资: ${person['salary']:,.2f}")

# 9. 对比老式%格式化
# 老式%格式化
print("老式%%格式化: %.2f" % pi)
print("老式%%格式化: %8.3f" % pi)
print("老式%%格式化: 姓名: %s, 年龄: %d, 分数: %.1f" % (name, age, score))

# 10. 日期格式化
from datetime import datetime
now = datetime.now()
print(f"当前时间: {now:%Y-%m-%d %H:%M:%S}")
print(f"日期: {now:%A, %B %d, %Y}")

# 11. 嵌套f-string
width = 10
precision = 3
print(f"嵌套格式化: |{pi:{width}.{precision}f}|")

# 12. 调试功能（Python 3.8+）
value = 42
print(f"{value = }")  # 输出: value = 42
print(f"{value * 2 = }")  # 输出: value * 2 = 84

```

月考有点小难，最后一道太困难

在D老师帮助下写的代码TLE了...
```python
import copy
import sys
from collections import defaultdict

# 设置调试模式
DEBUG = False

def debug_print(*args, **kwargs):
    """调试输出函数"""
    if DEBUG:
        print(*args, **kwargs)

class Chessboard:
    def __init__(self, board, h, w):
        # 使用列表推导式浅拷贝，避免deepcopy
        self.board = [row[:] for row in board]
        self.h = h
        self.w = w
    
    def incline(self, d):
        """优化后的倾斜操作"""
        debug_print(f"执行倾斜操作: {d} ({['↓', '→', '↑', '←'][d]})")
        
        new_board = [['.'] * self.w for _ in range(self.h)]
        
        if d == 0:  # 向下
            for j in range(self.w):
                idx = self.h - 1
                for i in range(self.h-1, -1, -1):
                    if self.board[i][j] != '.':
                        new_board[idx][j] = self.board[i][j]
                        idx -= 1
                        
        elif d == 1:  # 向右
            for i in range(self.h):
                idx = self.w - 1
                for j in range(self.w-1, -1, -1):
                    if self.board[i][j] != '.':
                        new_board[i][idx] = self.board[i][j]
                        idx -= 1
                        
        elif d == 2:  # 向上
            for j in range(self.w):
                idx = 0
                for i in range(self.h):
                    if self.board[i][j] != '.':
                        new_board[idx][j] = self.board[i][j]
                        idx += 1
                        
        else:  # 向左
            for i in range(self.h):
                idx = 0
                for j in range(self.w):
                    if self.board[i][j] != '.':
                        new_board[i][idx] = self.board[i][j]
                        idx += 1
        
        self.board = new_board
        debug_print("倾斜操作完成")
        return self

    def get_state(self):
        return tuple(tuple(row) for row in self.board)
    
    def get_tile_positions(self):
        """获取所有棋子的位置和颜色"""
        positions = {}
        for i in range(self.h):
            for j in range(self.w):
                if self.board[i][j] != '.':
                    positions[(i, j)] = self.board[i][j]
        return positions
    
    def print_board(self, title=""):
        """打印棋盘状态（调试用）"""
        if DEBUG:
            print(f"{title}:")
            for row in self.board:
                print(''.join(row))
            print()

def create_labeled_board(board, h, w):
    """创建带标签的棋盘，每个棋子用(x,y,color)表示"""
    labeled_board = [[None] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            if board[i][j] != '.':
                labeled_board[i][j] = (i, j, board[i][j])
    return labeled_board

def incline_labeled_board(labeled_board, d, h, w):
    """优化后的带标签棋盘倾斜操作"""
    debug_print(f"执行带标签棋盘的倾斜操作: {d} ({['↓', '→', '↑', '←'][d]})")
    
    new_board = [[None] * w for _ in range(h)]
    
    if d == 0:  # 向下
        for j in range(w):
            idx = h - 1
            for i in range(h-1, -1, -1):
                if labeled_board[i][j] is not None:
                    new_board[idx][j] = labeled_board[i][j]
                    idx -= 1
                
    elif d == 1:  # 向右
        for i in range(h):
            idx = w - 1
            for j in range(w-1, -1, -1):
                if labeled_board[i][j] is not None:
                    new_board[i][idx] = labeled_board[i][j]
                    idx -= 1
                
    elif d == 2:  # 向上
        for j in range(w):
            idx = 0
            for i in range(h):
                if labeled_board[i][j] is not None:
                    new_board[idx][j] = labeled_board[i][j]
                    idx += 1
                
    else:  # 向左
        for i in range(h):
            idx = 0
            for j in range(w):
                if labeled_board[i][j] is not None:
                    new_board[i][idx] = labeled_board[i][j]
                    idx += 1
    
    debug_print("带标签棋盘的倾斜操作完成")
    return new_board

def analyze_cycle_permutation(start_cb, cycle_sequence, h, w):
    """分析一个完整循环操作后的置换结构，基于位置建立映射"""
    debug_print("分析循环置换结构...")
    dir_names = ['↓', '→', '↑', '←']
    seq_str = ' -> '.join(dir_names[d] for d in cycle_sequence)
    debug_print(f"循环序列: {seq_str}")
    
    # 创建带标签的棋盘
    labeled_board = create_labeled_board(start_cb.board, h, w)
    
    # 应用完整循环操作（4次）
    for d in cycle_sequence:
        labeled_board = incline_labeled_board(labeled_board, d, h, w)
    
    # 构建位置映射：初始位置 -> 结束位置
    position_map = {}
    for i in range(h):
        for j in range(w):
            if labeled_board[i][j] is not None:
                x, y, color = labeled_board[i][j]
                position_map[(x, y)] = (i, j)
                debug_print(f"映射: ({x},{y}) -> ({i},{j})")
    
    debug_print(f"位置映射构建完成，包含 {len(position_map)} 个映射")
    
    # 检查映射是否完整
    start_positions = start_cb.get_tile_positions()
    if len(position_map) != len(start_positions):
        debug_print(f"警告: 映射不完整！初始位置数: {len(start_positions)}, 映射数: {len(position_map)}")
        return None
    
    return position_map

def find_cycles(position_map):
    """将置换分解为循环"""
    debug_print("分解置换为循环...")
    
    visited = set()
    cycles = []
    
    for start_pos in position_map:
        if start_pos not in visited:
            debug_print(f"开始新循环，起始位置: {start_pos}")
            cycle = []
            current = start_pos
            
            while current not in visited:
                visited.add(current)
                cycle.append(current)
                debug_print(f"添加到循环: {current}")
                
                if current not in position_map:
                    debug_print(f"错误: 位置 {current} 不在位置映射中!")
                    debug_print(f"位置映射键: {list(position_map.keys())}")
                    raise KeyError(f"位置 {current} 不在位置映射中")
                
                next_pos = position_map[current]
                debug_print(f"从 {current} 映射到 {next_pos}")
                
                # 检查是否回到起点
                if next_pos == start_pos:
                    debug_print(f"循环完成: {cycle}")
                    break
                
                current = next_pos
                
                # 安全检查，防止无限循环
                if len(cycle) > len(position_map):
                    debug_print(f"警告: 循环过长，可能存在问题。循环: {cycle}")
                    break
            
            if len(cycle) > 1:  # 只考虑长度大于1的循环
                cycles.append(cycle)
                debug_print(f"找到循环: {cycle} (长度 {len(cycle)})")
    
    debug_print(f"共找到 {len(cycles)} 个循环")
    return cycles

def find_color_period(color_sequence):
    """找到颜色序列的周期"""
    debug_print(f"计算颜色序列周期: {color_sequence}")
    n = len(color_sequence)
    for period in range(1, n + 1):
        if n % period == 0:
            is_periodic = True
            for i in range(n):
                if color_sequence[i] != color_sequence[i % period]:
                    is_periodic = False
                    break
            if is_periodic:
                debug_print(f"颜色序列周期: {period}")
                return period
    debug_print(f"颜色序列无周期，使用长度: {n}")
    return n

def solve_congruence_system(cycle_equations):
    """求解同余方程组"""
    debug_print("求解同余方程组...")
    if not cycle_equations:
        debug_print("空方程组，总是有解")
        return True  # 没有约束，总是有解
    
    debug_print(f"方程组: {cycle_equations}")
    
    # 使用中国剩余定理求解
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y
    
    def solve_two(a1, m1, a2, m2):
        debug_print(f"解方程: x ≡ {a1} (mod {m1}), x ≡ {a2} (mod {m2})")
        gcd, x, y = extended_gcd(m1, m2)
        if (a2 - a1) % gcd != 0:
            debug_print(f"无解: gcd({m1}, {m2}) = {gcd} 不能整除 {a2} - {a1} = {a2 - a1}")
            return None, None
        lcm = m1 // gcd * m2
        k = (a2 - a1) // gcd
        x0 = a1 + x * k * m1
        debug_print(f"解得: x ≡ {x0 % lcm} (mod {lcm})")
        return x0 % lcm, lcm
    
    # 逐个合并方程
    current_a, current_m = cycle_equations[0]
    debug_print(f"初始方程: x ≡ {current_a} (mod {current_m})")
    
    for i in range(1, len(cycle_equations)):
        a, m = cycle_equations[i]
        result = solve_two(current_a, current_m, a, m)
        if result[0] is None:
            debug_print("方程组无解")
            return False
        current_a, current_m = result
        debug_print(f"合并后: x ≡ {current_a} (mod {current_m})")
    
    debug_print("方程组有解")
    return True

def main():
    data = sys.stdin.read().splitlines()
    
    if not data:
        debug_print("输入为空")
        print("no")
        return
        
    h, w = map(int, data[0].split())
    debug_print(f"棋盘尺寸: {h}x{w}")
    
    start_lines = data[1:1+h]
    end_lines = data[1+h+1:1+h+1+h]

    start_board = [list(line.strip()) for line in start_lines]
    end_board = [list(line.strip()) for line in end_lines]

    start_cb = Chessboard(start_board, h, w)
    end_cb = Chessboard(end_board, h, w)
    
    start_cb.print_board("初始状态")
    end_cb.print_board("目标状态")
    
    start_state = start_cb.get_state()
    target_state = end_cb.get_state()
    
    # 步骤1: 检查五种直接情况
    debug_print("=== 步骤1: 检查五种直接情况 ===")
    if start_state == target_state:
        debug_print("✓ 初始状态等于目标状态")
        print("yes")
        return
    
    dir_names = ['↓', '→', '↑', '←']
    for d in range(4):
        debug_print(f"检查方向 {d} ({dir_names[d]})")
        test_board = Chessboard([list(row) for row in start_state], h, w)
        test_board.incline(d)
        if test_board.get_state() == target_state:
            debug_print(f"✓ 通过方向 {d} ({dir_names[d]}) 达到目标状态")
            print("yes")
            return
        else:
            debug_print(f"✗ 方向 {d} ({dir_names[d]}) 不能达到目标状态")
    
    # 步骤2: 检查目标状态的稳定方向
    debug_print("=== 步骤2: 检查目标状态的稳定方向 ===")
    stable_dirs = []
    for d in range(4):
        debug_print(f"测试方向 {d} ({dir_names[d]}) 是否稳定")
        test_board = Chessboard([list(row) for row in target_state], h, w)
        test_board.incline(d)
        if test_board.get_state() == target_state:
            debug_print(f"✓ 方向 {d} ({dir_names[d]}) 是稳定的")
            stable_dirs.append(d)
        else:
            debug_print(f"✗ 方向 {d} ({dir_names[d]}) 不稳定")
    
    debug_print(f"稳定方向: {[dir_names[d] for d in stable_dirs]}")
    
    # 如果没有两个相邻的稳定方向，则无解
    has_adjacent = False
    adjacent_pair = None
    for i in range(len(stable_dirs)):
        for j in range(i+1, len(stable_dirs)):
            d1, d2 = stable_dirs[i], stable_dirs[j]
            debug_print(f"检查方向 {d1} ({dir_names[d1]}) 和 {d2} ({dir_names[d2]}) 是否相邻")
            if (d1 + 1) % 4 == d2 or (d2 + 1) % 4 == d1:
                if (d2 + 1) % 4 == d1:
                    d1, d2 = d2, d1
                debug_print(f"✓ 方向 {d1} ({dir_names[d1]}) 和 {d2} ({dir_names[d2]}) 相邻")
                has_adjacent = True
                adjacent_pair = (d1, d2)
                break
        if has_adjacent:
            break
    
    if not has_adjacent:
        debug_print("没有两个相邻的稳定方向，输出 'no'")
        print("no")
        return
    
    d1, d2 = adjacent_pair
    debug_print(f"找到相邻稳定方向对: {dir_names[d1]} 和 {dir_names[d2]}")
    
    # 步骤3: 生成八种循环序列
    debug_print("=== 步骤3: 生成八种循环序列 ===")
    sequences = []
    for start_dir in range(4):
        # 顺时针序列
        clockwise = []
        current = start_dir
        for _ in range(9):
            clockwise.append(current)
            current = (current + 1) % 4
        seq_str = ' -> '.join(dir_names[d] for d in clockwise)
        debug_print(f"顺时针序列 (起始 {dir_names[start_dir]}): {seq_str}")
        sequences.append(clockwise)
        
        # 逆时针序列
        counterwise = []
        current = start_dir
        for _ in range(9):
            counterwise.append(current)
            current = (current - 1) % 4
        seq_str = ' -> '.join(dir_names[d] for d in counterwise)
        debug_print(f"逆时针序列 (起始 {dir_names[start_dir]}): {seq_str}")
        sequences.append(counterwise)
    
    debug_print(f"共生成 {len(sequences)} 种序列")
    
    # 步骤4: 对每种序列分析置换结构并构建同余方程
    debug_print("=== 步骤4: 分析置换结构并构建同余方程 ===")
    for idx, seq in enumerate(sequences):
        debug_print(f"分析序列 {idx+1}/{len(sequences)}")
        
        # 先执行前5个操作，检查是否达到目标状态
        temp_board = Chessboard([list(row) for row in start_state], h, w)
        for i in range(5):
            temp_board.incline(seq[i])
            if temp_board.get_state() == target_state:
                debug_print(f"✓ 在序列第 {i+1} 步达到目标状态")
                print("yes")
                return
        
        # 从第2-5个操作中选择稳定方向操作中靠后的那个
        to_be_selected = d2 if (seq[0] + 1) % 4 == seq[2] else d1
        selected_index = -1
        for i in range(1, 5):  # 索引1-4
            if seq[i] == to_be_selected:
                selected_index = i
        
        if selected_index == -1:
            debug_print("序列中没有稳定方向操作，跳过")
            continue
        
        debug_print(f"选择从第 {selected_index} 个操作后开始分析")
        
        # 执行前selected_index个操作，得到起始状态
        start_analysis_board = Chessboard([list(row) for row in start_state], h, w)
        for i in range(selected_index + 1):
            start_analysis_board.incline(seq[i])
        
        distribution_matched = True
        for i in range(h):
            for j in range(w):
                if (start_analysis_board.board[i][j] == '.') != (end_cb.board[i][j] == '.'):
                    debug_print(f"({i},{j})位置处，棋子分布与目标状态不符!")
                    debug_print(f"起始状态: '{start_analysis_board.board[i][j]}', 目标状态: '{end_cb.board[i][j]}'")
                    distribution_matched = False
                    break
            if not distribution_matched:
                break
        if not distribution_matched:
            debug_print("分布不匹配，跳过该序列")
            continue
        
        # 分析置换结构
        position_map = analyze_cycle_permutation(start_analysis_board, seq[selected_index+1:selected_index+5], h, w)
        if position_map is None:
            debug_print("置换分析失败，跳过该序列")
            continue
        
        # 分解为循环
        try:
            cycles = find_cycles(position_map)
        except KeyError as e:
            debug_print(f"在分解循环时出现错误: {e}")
            debug_print("跳过该序列")
            continue
        
        # 构建同余方程
        cycle_equations = []
        valid = True
        
        for cycle_idx, cycle in enumerate(cycles):
            L = len(cycle)
            debug_print(f"分析循环 {cycle_idx+1}/{len(cycles)} (长度 {L}): {cycle}")
            
            # 获取初始颜色序列和目标颜色序列
            start_colors = []
            target_colors = []
            
            for pos in cycle:
                i, j = pos
                start_colors.append(start_analysis_board.board[i][j])
                
                # 找到目标状态中对应位置的颜色
                found = False
                for end_pos, end_color in end_cb.get_tile_positions().items():
                    if end_pos == pos:
                        target_colors.append(end_color)
                        found = True
                        break
                if not found:
                    target_colors.append('.')  # 目标位置为空
            
            debug_print(f"初始颜色序列: {start_colors}")
            debug_print(f"目标颜色序列: {target_colors}")
            
            # 检查颜色序列是否匹配（考虑循环移位）
            found_k = None
            for k in range(L):
                # 检查循环移位k次后是否匹配
                match = True
                for i in range(L):
                    if start_colors[(i - k) % L] != target_colors[i]:
                        match = False
                        break
                if match:
                    found_k = k
                    debug_print(f"找到匹配: 需要移位 {k} 次")
                    break
            
            if found_k is None:
                debug_print("未找到匹配的移位，该序列无效")
                valid = False
                break
            
            # 计算颜色序列的周期
            period = find_color_period(start_colors)
            
            # 添加同余方程
            equation = (found_k % period, period)
            cycle_equations.append(equation)
            debug_print(f"添加同余方程: x ≡ {equation[0]} (mod {equation[1]})")
        
        if not valid:
            debug_print("序列无效，继续下一个序列")
            continue
        
        debug_print(f"构建的同余方程组: {cycle_equations}")
        
        # 步骤5: 求解同余方程组
        debug_print("=== 步骤5: 求解同余方程组 ===")
        if solve_congruence_system(cycle_equations):
            debug_print("同余方程组有解，输出 'yes'")
            print("yes")
            return
        else:
            debug_print("同余方程组无解，继续下一个序列")
    
    debug_print("所有序列都无解，输出 'no'")
    print("no")

if __name__ == "__main__":
    main()

```
