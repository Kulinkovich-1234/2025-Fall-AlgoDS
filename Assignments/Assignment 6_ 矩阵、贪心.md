

Updated 1432 GMT+8 Oct 14, 2025

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

### M18211: 军备竞赛

greedy, two pointers, http://cs101.openjudge.cn/pctbook/M18211



思路：

$n_{sold}\leq n_{made}$
$cost_{made}\leq asset+cost_{sold}$

maximize $n_{made}-n_{sold}$
为了维持不负债，一开始买的越小越好，卖的越多越好
因此从小的开始买，从大的开始卖（此为最优情况）

如果某一时刻即使采用最优策略依然无法满足优势要求，则终止交易
使用superiority记录最佳情况，最后输出

代码

```python
# 
asset = int(input())
weapons = [int(_) for _ in input().split()]
weapons = sorted(weapons)
buy = 0
sell = len(weapons)-1
superiority = 0
while buy <= sell:
    if asset >= weapons[buy]:
        asset -= weapons[buy]
        buy += 1
    else:
        asset += weapons[sell]
        sell -= 1
    if (buy-0)-(len(weapons)-1-sell)<0:
        break #if neighbor's power is greater than ours despite using the best strategy, then halt dealing
    superiority = max(superiority,(buy-0)-(len(weapons)-1-sell)) # record the best situation in every possibility
print(superiority)

```

![[Pasted image 20251014155002.png]]

代码运行截图 <mark>（至少包含有"Accepted"）</mark>





### M21554: 排队做实验

greedy, http://cs101.openjudge.cn/pctbook/M21554/



思路：

最快的人放前面，最慢的人放后面

代码

```python
n = int(input())
t = 0
request = [[int(i),t:=t+1] for i in input().split()]
request = sorted(request, key = lambda x: x[0])
for i in request:
    print(i[1], end=' ')
print()
summ = [request[0][0]]
for i in request[1::]:
    summ.append(summ[-1]+i[0])
#for i in request:
    #print(i)
print('%.2f' % (sum(summ[:-1:])/n))

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251014160606.png]]



### E23555: 节省存储的矩阵乘法

implementation, matrices, http://cs101.openjudge.cn/pctbook/E23555



思路：

稀疏矩阵，只进行非零元的相乘，找到$a_j^i * b_k^j$，并记录，最终合并

代码

```python
n, m1, m2 = map(int,input().split())
matrix1 = []
matrix2 = []
for i in range(m1):
    matrix1.append([int(_) for _ in input().split()])
for i in range(m2):
    matrix2.append([int(_) for _ in input().split()])
# matrix1 (x,y,n)* matrix2(y,z,m) to (x,z,n*m)
# therefore we should sort them by y to scan
matrix1 = sorted(matrix1, key = lambda x:x[1])
matrix2 = sorted(matrix2, key = lambda x:x[0])
#print('matrix1')
#for i in matrix1:
#    print(i)
#print('matrix2')
#for i in matrix2:
#    print(i)
matrix = []
i = 0
j = 0
while True:
    if i >= len(matrix1) or j >= len(matrix2):
        break
    while True:
        while i < len(matrix1) and j < len(matrix2) and matrix1[i][1] < matrix2[j][0]:
            i += 1
        while i < len(matrix1) and j < len(matrix2) and matrix1[i][1] > matrix2[j][0]:
            j += 1
        if i >= len(matrix1) or j >= len(matrix2):
            break
        if matrix1[i][1] == matrix2[j][0]:
            break
    if i >= len(matrix1) or j >= len(matrix2):
        break
    #print(f'ready to multiplicate: i={i} j={j}')
    scan_i = i
    scan_j = j
    while scan_i < len(matrix1) and matrix1[scan_i][1] == matrix1[i][1]:
        scan_i += 1
    while scan_j < len(matrix2) and matrix2[scan_j][0] == matrix2[j][0]:
        scan_j += 1
    #print(f'scanned: scan_i={scan_i} j={scan_j}')
    for index_i in range(i,scan_i):
        for index_j in range(j,scan_j):
            matrix.append([matrix1[index_i][0],matrix2[index_j][1],matrix1[index_i][2]*matrix2[index_j][2]])
    i = scan_i
    j = scan_j
    #print(f'next step: i={i} j={j}')
matrix = sorted(matrix, key = lambda x:x[1])
matrix = sorted(matrix, key = lambda x:x[0])
result = []
result.append(matrix[0])
#print('matrix = \n',matrix)
for i in range(1,len(matrix)):
    if matrix[i][:-1:] == result[-1][:-1:]:
        result[-1][2] += matrix[i][2]
    else:
        result.append(matrix[i])
for i in result:
    print(f'{i[0]} {i[1]} {i[2]}')

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251015094357.png]]



### M12558: 岛屿周⻓

matices, http://cs101.openjudge.cn/pctbook/M12558


思路：

dfs，每次从陆向海就对应于1的周长

代码
一开始忘记声明全局变量了
 
```python
dx = [1,0,-1,0]
dy = [0,1,0,-1]
circ = 0
visited = []
island_map = []
def search(x,y):
    global circ,visited
    visited[x][y] = True
    '''for i in visited:
        for j in i:
            if j:
                print(1,end='')
            else:
                print(0,end='')
        print()'''
    #print()
    for i in range(4):
        newx = x + dx[i]
        newy = y + dy[i]
        #print(f'({x},{y})->({newx},{newy})',end=' ')
        if not island_map[newx][newy]:
            circ += 1
            #print(f'outcome: new border')
        else:
            if not visited[newx][newy]:
                #print(f'outcome: go on')
                search(newx, newy)
            #else:
                #print(f'outcome: visited')
n,m=map(int,input().split())
island_map = [[0 for i in range(m+2)]]
for i in range(n):
    row = [int(_) for _ in input().split()]
    row = [0] + row + [0]
    island_map.append(row)
island_map.append([0 for i in range(m+2)])
visited = [[False for j in range(m+2)] for i in range(n+2)]
found = False
for i in range(1,n+1):
    for j in range(1,m+1):
        if island_map[i][j]:
            search(i,j)
            found = True
            break
    if found:
        break
print(circ)
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>





### M01328: Radar Installation

greedy, http://cs101.openjudge.cn/practice/01328/



思路：

把每一个岛屿对应的雷达安装区间算出来，然后求最少的能够把区间全部覆盖的点数
从最左边开始尝试安装雷达，只要没有过右端点就可以往右侧移动，这样可以尽可能干掉多的岛屿区间；
遇到**第一个右端点**时，我们发现如果不安装的话这个岛就没有对应的雷达了，所以必须在次数放下一个雷达，于是整个局面形势就可以更新了
因此我们需要按照右端点进行排序


代码

```python
import sys
index = 0
lines = sys.stdin.read().splitlines()
cases = 0
while True:
    n,d = map(int,lines[index].split())
    index += 1
    if n==0 and d==0:
        break
    cases += 1
    islands = []
    for i in range(n):
        islands.append([int(i) for i in lines[index].split()])
        index += 1
    index += 1
    #print(f'islands=\n{islands}')
    Nosolution = False
    radars = []
    for island in islands:
        if d < island[1]:
            print(f'Case {cases}: -1')
            Nosolution = True
            break
        radars.append([island[0]-(d**2-island[1]**2)**0.5,island[0]+(d**2-island[1]**2)**0.5])
    if Nosolution:
        continue
    #print(f'radars=\n{radars}')
    radars = sorted(radars, key = lambda x:x[1])
    installation = 0
    i = 0
    while i < n:
        pos = radars[i][1]
        installation += 1
        while i < n and radars[i][0] <= pos:
            i += 1
    print(f'Case {cases}: {installation}')

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>


![[Pasted image 20251014175335.png]]


### 545C. Woodcutters

dp, greedy, 1500, https://codeforces.com/problemset/problem/545/C



思路：

dp+贪心
向左/向右/不倒的三种情况的最大可砍数进行状态转移

代码

```python
n = int(input())
trees = []
dp = []
for i in range(n):
    trees.append([int(i) for i in input().split()]) #coordinate and height
dp.append([1,0,1]) # the maximum number of trees that you can cut down when i-th tree is left/stand/right (Not considering collision after i-th tree)
dpi = []
for i in range(1,n):
    dpi = [0,0,0]
    # lean left
    coord_prev = trees[i-1][0]
    height_prev = trees[i-1][1]
    coord_now = trees[i][0]
    height_now = trees[i][1]
    outmost_extension = [coord_prev, coord_prev, coord_prev + height_prev]
    inmost_extension = [coord_now - height_now, coord_now, coord_now]
    for prev in range(3):
        for now in range(3):
            if outmost_extension[prev]<inmost_extension[now]:
                dpi[now] = max(dp[i-1][prev] + abs(now - 1), dpi[now])
    dp.append(dpi)
    #print(dp)
print(max(dp[-1]))
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20251014211951.png]]




## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>

排序指定key的方法（感觉还是lambda比较好）：
```python
# Sorting a list of strings case-insensitively
strings = ["banana", "Apple", "cherry"]
sorted_strings = sorted(strings, key=str.lower)
print(sorted_strings) # Output: ['Apple', 'banana', 'cherry']

# Sorting a list of tuples by the third element (age)
student_tuples = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
sorted_students = sorted(student_tuples, key=lambda student: student[2])
print(sorted_students) # Output: [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

from operator import itemgetter
# Sorting by age using itemgetter
sorted_students = sorted(student_tuples, key=itemgetter(2))
print(sorted_students) # Output: [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

# Sorting by grade then by age
sorted_students = sorted(student_tuples, key=itemgetter(1, 2))
print(sorted_students) # Output: [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]
```

括号匹配：
居然1. maxn写成j了 2. exist忘记判断了
太愚蠢了
```python
class Solution:
    def isValid(self, s: str) -> bool:
        def match(c1,c2):
            if (c1 == '(') and (c2 == ')'):
                return True
            if (c1 == '{') and (c2 == '}'):
                return True
            if (c1 == '[') and (c2 == ']'):
                return True
            return False
        stack = []
        for i in s:
            stack.append(i)
            if stack[-1] in {')',']','}'}:
                if len(stack) < 2:
                    return False
                if not match(stack[-2],stack[-1]):
                    return False
                stack.pop(-1)
                stack.pop(-1)
        if len(stack):
            return False
        return True
```

AI修改的稀疏矩阵乘法（不用难懂的三重嵌套循环）：
```python
import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    
    n, m1, m2 = map(int, data[0].split())
    
    matrix1 = []
    matrix2 = []
    
    index = 1
    for _ in range(m1):
        row, col, val = map(int, data[index].split())
        matrix1.append((row, col, val))
        index += 1
        
    for _ in range(m2):
        row, col, val = map(int, data[index].split())
        matrix2.append((row, col, val))
        index += 1

    # 按 A 的列 和 B 的行 排序，以便匹配内维度
    matrix1.sort(key=lambda x: x[1])  # A: sort by col (k)
    matrix2.sort(key=lambda x: x[0])  # B: sort by row (k)

    temp_result = []

    i = j = 0
    while i < len(matrix1) and j < len(matrix2):
        col_A = matrix1[i][1]
        row_B = matrix2[j][0]

        if col_A < row_B:
            i += 1
        elif col_A > row_B:
            j += 1
        else:
            # col_A == row_B，找到匹配的 k 维
            k = col_A

            # 收集 matrix1 中所有 col == k 的项
            start_i = i
            while i < len(matrix1) and matrix1[i][1] == k:
                i += 1
            block_A = matrix1[start_i:i]

            # 收集 matrix2 中所有 row == k 的项
            start_j = j
            while j < len(matrix2) and matrix2[j][0] == k:
                j += 1
            block_B = matrix2[start_j:j]

            # 笛卡尔积：A[i][0] x B[j][1] 贡献到结果
            for a_row, _, a_val in block_A:
                for b_col, _, b_val in block_B:
                    product = a_val * b_val
                    if product != 0:  # 避免加入零值
                        temp_result.append((a_row, b_col, product))

    # 若无结果，退出
    if not temp_result:
        return

    # 按行、列排序
    temp_result.sort(key=lambda x: (x[0], x[1]))

    # 合并相同位置的项
    result = []
    last_row, last_col, last_val = temp_result[0]
    for r, c, v in temp_result[1:]:
        if r == last_row and c == last_col:
            last_val += v
        else:
            if last_val != 0:  # 再次检查累加后是否为零
                result.append((last_row, last_col, last_val))
            last_row, last_col, last_val = r, c, v
    # 添加最后一项
    if last_val != 0:
        result.append((last_row, last_col, last_val))

    # 输出结果
    for r, c, v in result:
        print(f"{r} {c} {v}")

if __name__ == "__main__":
    main()
```

线段树、树状数组、单调栈、堆、红黑树、并查集、稳定排序
全局变量必须放到程序前面，不然OJ过不了

$2^{x_1}\cdot3^{x_2}\cdot5^{x_3}\cdot7^{x_4}$
$n=(x_1+1)(x_2+1)(x_3+1)$
count n奇数
$2^0, 2^2, 2^4, 2^6$ 筛掉：$\left \lfloor \frac{N}{2}\right \rfloor-\left \lfloor \frac{N}{4}\right \rfloor+\left \lfloor \frac{N}{8}\right \rfloor-\dots$
$3^0, 3^2, 3^4, 3^6$ 筛掉：
