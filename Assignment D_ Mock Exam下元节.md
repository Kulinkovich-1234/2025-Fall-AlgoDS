# Assignment #D: Mock Exam下元节

Updated 1729 GMT+8 Dec 4, 2025

2025 fall, Complied by 马健文 元培学院



>**说明：**
>
>1. Dec⽉考： AC4😭😭😭 。考试题⽬都在“题库（包括计概、数算题目）”⾥⾯，按照数字题号能找到，可以重新提交。作业中提交⾃⼰最满意版本的代码和截图。
>
>2. 解题与记录：对于每一个题目，请提供其解题思路（可选），并附上使用Python或C++编写的源代码（确保已在OpenJudge， Codeforces，LeetCode等平台上获得Accepted）。请将这些信息连同显示“Accepted”的截图一起填写到下方的作业模板中。（推荐使用Typora https://typoraio.cn 进行编辑，当然你也可以选择Word。）无论题目是否已通过，请标明每个题目大致花费的时间。
>
>3. 提交安排：提交时，请首先上传PDF格式的文件，并将.md或.doc格式的文件作为附件上传至右侧的“作业评论”区。确保你的Canvas账户有一个清晰可见的本人头像，提交的文件为PDF格式，并且“作业评论”区包含上传的.md或.doc附件。
> 
>4. 延迟提交：如果你预计无法在截止日期前提交作业，请提前告知具体原因。这有助于我们了解情况并可能为你提供适当的延期或其他帮助。  
>
>请按照上述指导认真准备和提交作业，以保证顺利完成课程要求。





## 1. 题目

### E29945:神秘数字的宇宙旅行 

implementation, http://cs101.openjudge.cn/practice/29945

思路：

冰雹，直接实现
第一遍忘记输出`End`了，有点愚蠢

代码

```python
n = int(input())
while n>1:
    if n%2:
        print(f'{n}*3+1={n*3+1}')
        n = n*3 + 1
    else:
        print(f'{n}/2={n//2}')
        n //= 2
print('End')
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![Pasted image 20251208192335.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251208192335.png?JWSuyQz2ms)



### E29946:删数问题

monotonic stack, greedy, http://cs101.openjudge.cn/practice/29946

思路：

### 删除数字问题的贪心做法：
```python
s = input().strip()
k = int(input())
n = len(s)
start = 0
result = ''
while True:
    right = len(result) + k
    if start == right:
        break
    if right == n:
        break
    #print(f'result = {result}, available = {s[start:right+1]}')
    minn = min(list(s[start:right+1]))
    while s[start] != minn:
        start += 1
    result = result + minn
    start += 1
if len(result) < n-k:
    result = result + s[start::]
print(int(result))
```
#### 注意！！！题目意思是删除数字以后形成的数码对应的数，也就是删除后可以保留前导0！！！
#### 但是输出的时候你得把前导零去掉！！

### dp做法：

```python
s = input().strip()
k = int(input())
n = len(s)

dp = [['x'] * (n + 1) for _ in range(n)]

# 初始状态：第一个字符
dp[0][0] = ''  # 保留 0 位
dp[0][1] = s[0]  # 保留 1 位

# 填充 DP 表
for i in range(1, n):  # 从第二个字符开始
    dp[i][0] = ''
    for length in range(1, i + 2):  # 长度范围：1 到 i+1（当前最多保留 i+1 位）
        # 选项1：保留当前字符 s[i]
        option1 = dp[i-1][length-1] + s[i]
        
        # 选项2：不保留当前字符（直接继承上一个状态）
        option2 = dp[i-1][length]
        
        # 取 min（'x' 会被自动忽略，因为 'x' > 任何数字字符串）
        dp[i][length] = min(option1, option2)

# 输出：保留 n-k 位的最小字符串
print(int(dp[n-1][n - k]))
```

## 最快速的单调栈做法：

如果你一开始选数字的时候遇到了1357532...的序列，则我们可以发现：在前面（7以前）的序列固定的情况下，把7删除可以使得序列比保留7而删除5更优。根据贪心的原理，最优解一定是会把7删除。究其原因，就是因为7>5，不满足单调递增。
如果两个数相同则应该先保留看情况。
如果删除到删除不了了就不删除
时间复杂度$O(n)$

代码

```python
s = input().strip()
k = int(input())
n = len(s)


result = ''
deleted = 0
idx = 0

while idx < len(s):
    if not result:
        result = result + s[idx]
        idx += 1
        continue

    if result[-1] <= s[idx]:
        result = result + s[idx]
        idx += 1
        continue

    while result and result[-1] > s[idx] and deleted < k:
        result = result[:-1:]
        deleted += 1

    result = result + s[idx]
    idx += 1

while deleted < k:
    result = result[:-1:]
    deleted += 1

print(int(result))

```

记得注意：
1.处理完后还没删除完成的情况
2.处理完之前就已经删除完成的情况

代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![Pasted image 20251208200703.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251208200703.png?V72wu5WloZ)




### E30091:缺德的图书馆管理员

greedy, http://cs101.openjudge.cn/practice/30091

思路：

两个人相撞等价于没相撞

代码

```python
L = int(input())
N = int(input())
a = [int(_) for _ in input().split()]
minn = max([min(_,L+1-_) for _ in a])
maxx = max([max(_,L+1-_) for _ in a])
print(minn,maxx)
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![Pasted image 20251208200927.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251208200927.png?fS8Ntq7PlW)



### M27371:Playfair密码

simulation，string，matrix, http://cs101.openjudge.cn/practice/27371


思路：

直接模拟。注意：调试部分一定记得删掉!!!!

代码

```python
key = input()
n = int(input())
list1 = []
for c in key:
    c1 = c
    if c == 'j':
        c1 = 'i'
    if c1 not in list1:
        list1.append(c1)
for c in [chr(x) for x in range(97,123)]:
    c1 = c
    if c == 'j':
        c1 = 'i'
    if c1 not in list1:
        list1.append(c1)
matrix = [list1[5*i:5*i+5] for i in range(5)]
def find(c):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == c:
                return i,j
def replacement(s):
    pos0x,pos0y = find(s[0])
    pos1x,pos1y = find(s[1])
    if pos0x == pos1x:
        pos0y += 1
        pos1y += 1
        pos0y %= 5
        pos1y %= 5
        return matrix[pos0x][pos0y]+matrix[pos1x][pos1y]
    if pos0y == pos1y:
        pos0x += 1
        pos1x += 1
        pos0x %= 5
        pos1x %= 5
        return matrix[pos0x][pos0y]+matrix[pos1x][pos1y]
    return matrix[pos0x][pos1y]+matrix[pos1x][pos0y]
for _ in range(n):
    s = input().strip().replace('j','i')
    idx = 0
    pairs = []
    while idx < len(s):
        if idx == len(s)-1:
            pair = s[idx] + 'x'
            if pair == 'xx':
                pair = 'xq'
            pairs.append(pair)
            break
        else:
            pair = s[idx:idx+2]
            if pair[0] == pair[1]:
                if pair[0] != 'x':
                    pair = pair[0] + 'x'
                else:
                    pair = pair[0] + 'q'
                idx += 1
            else:
                idx += 2
            pairs.append(pair)
    replaced = [replacement(pair) for pair in pairs]
    print(''.join(replaced))
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![Pasted image 20251208201626.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251208201626.png?0nI4NQKBT2)



### T30201:旅行售货商问题

dp,dfs, http://cs101.openjudge.cn/practice/30201

思路：

经典的TSP问题，使用状压dp即可

代码

```python
n = int(input())
cost = []
for _ in range(n):
    cost.append([int(i) for i in input().split()])
inf = int(1e7)
dp = [[inf] * n for i in range(1<<(n-1))] #dp[0111010101][1] means : city 1 3 4 7 8 9 visited, now at city 1
mincost = inf
for i in range(1,n):
    dp[1<<(i-1)][i] = cost[0][i]
def search(state,nowpos):
    #print(bin(state),' nowpos = ',nowpos,'searching...')
    if dp[state][nowpos] != inf:
        return dp[state][nowpos]
    result = inf+7
    prev_state = state ^ (1<<(nowpos - 1))
    for i in range(1,n):
        if prev_state & (1<<(i-1)): # city i visited
            #print('->')
            result = min(result,search(prev_state,i) + cost[i][nowpos])
    dp[state][nowpos] = result
    return result
for i in range(1,n):
    mincost = min(mincost,search((1<<(n-1))-1,i)+cost[i][0])# all finished and at city i
print(mincost)
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![Pasted image 20251208201856.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251208201856.png?4wIRJktvnv)



### T30204:小P的LLM推理加速

greedy, http://cs101.openjudge.cn/practice/30204

思路：

没看懂题目。这道题目强行套用AI的背景，实则完全不符合AI训练的基本逻辑，题干也没有讲明白训练周期是什么东西。

实际上和candy是一样的。每一种方案都唯一对应一些$(x_i,y_i)$和一些互不相同的$x_i$

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



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![Pasted image 20251208203513.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251208203513.png?ISImcEUHJE)



## 2. 学习总结和收获

如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。

🦅🥚问题：

考虑最简单的情形：一个蛋，H层楼。此时如果蛋碎了但是没找到就没辙了。为了保证必须能够找到临界楼层，只能从下往上一个一个试。所以最坏的情况要从$1$试到$H$，共$H$次；

稍微复杂一些的情形：$2$个蛋，$H$层楼。
假设第一个蛋从第$x$层楼释放，存在两种情况：
1.碎了，则第二个蛋需要搜寻$1$~$x-1$，需要$x-1$次
2.没碎，则目前的局势相当于用两个蛋搜寻$x+1$~$H$，这实际上等价于$1$~$H-x$

所以我们发现，如果设`dp[eggs][height]`表示最坏情况下`eggs`个蛋搜寻$0$~$H$的临界楼层的次数，则可以得出：
$$
\rm dp[eggs][height] = 1+\min_{x=1}^{height} \left(\max(dp[eggs-1][x-1],dp[eggs][height-x])\right)
$$
由朴素的直觉可以知道，`dp[eggs-1][x-1]`随x单调递增，`dp[eggs][height-x]`随x单调递减，因此可以考虑二分查找x


根据以上方法，我们可以得出以下表格：

|      | height | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19  |
| ---- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eggs | 1      | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19  |
| eggs | 2      | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   | 5   | 6   | 6   | 6   | 6   |
| eggs | 3      | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   | 5   |
| eggs | 4      | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 5      | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 6      | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 7      | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 8      | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 9      | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 10     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 11     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 12     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 13     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 14     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 15     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 16     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 17     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 18     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
| eggs | 19     | 0   | 1   | 2   | 2   | 3   | 3   | 3   | 3   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 4   | 5   | 5   | 5   | 5   |
```cpp

#include <iostream>
#include <algorithm>
#include <climits>
using namespace std;

const int MAX_EGGS = 1005;
const int MAX_HEIGHT = 1005;
int dp[MAX_EGGS][MAX_HEIGHT];

void precompute() {
    // 初始化边界
    for (int h = 1; h < MAX_HEIGHT; h++) dp[1][h] = h;
    for (int e = 1; e < MAX_EGGS; e++) dp[e][0] = 0;

    // DP
    for (int e = 2; e < MAX_EGGS; e++) {
        for (int h = 1; h < MAX_HEIGHT; h++) {
            int low = 1, high = h;
            while (low + 1 < high) {
                int mid = (low + high) / 2;
                int break_case = dp[e-1][mid-1];
                int not_break_case = dp[e][h-mid];
                if (break_case < not_break_case) low = mid;
                else if (break_case > not_break_case) high = mid;
                else low = high = mid;
            }
            dp[e][h] = 1 + min(
                max(dp[e-1][low-1], dp[e][h-low]),
                max(dp[e-1][high-1], dp[e][h-high])
            );
        }
    }
}

int main() {
    precompute();
    int eggs, height;
    while (cin >> eggs >> height && (eggs || height)) {
        cout << dp[eggs][height] << endl;
    }
    return 0;
}
```

可以发现，在鸡蛋数量较多的时候，很少几步操作就可以解决很多楼层的问题
并且当鸡蛋数量很多的时候，$\rm steps = \lceil \log_2  (height+1) \rceil$
$\rm steps \geq \lceil \log_2  (height+1) \rceil$




如果楼层极多，不妨考虑换一个角度思考：
记`dp[eggs][steps]=max_height`，dp维护eggs个鸡蛋在step次操作下最坏情况能够覆盖的楼层数

则此时当$\rm eggs \geq steps$时，`dp[eggs][steps]=2**steps-1`
![Pasted image 20251205003046.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251205003046.png?w9UzezbnOo)
红色的部分为二分区域，剩下的为鸡蛋相对不足的区域
可以发现，`dp[eggs][steps]=1+dp[eggs-1][steps-1]+dp[eggs][steps-1]`
原理就是：碎了可以判断`dp[eggs-1][steps-1]`,没碎可以判断`dp[eggs][steps-1]`，最好的情况就是充分利用这两段

观察到，如果将整张表+1，则可得到
$$
\rm g[eggs][steps]=g[eggs-1][steps-1]+g[eggs][steps-1]
$$
定义母函数：
$$
f_\text{steps}(x)=\sum_{i=0}^{\infty} g[i][\text{steps}]\cdot x^i
$$
则
$$
f_\text{steps+1}=f_\text{steps}+xf_\text{steps}=(x+1)f_\text{steps}
$$
$$
f_0(x)=\sum_{i=0}^\infty x^i=\frac{1}{1-x}
$$
故可得
$$
f_\text{step}=\frac{(x+1)^\text{step}}{1-x}
$$
$$
\rm dp[eggs][steps] = [x^\text{eggs}]\frac{(x+1)^\text{step}}{1-x}-1=\sum_{i=0}^{\min(\rm egg,step)}\binom{step}{i}-1\geq h
$$

以下是利用滚动数组求解
```python
import sys
import math

def egg_drop(eggs, height):
    """使用优化的动态规划求解鹰蛋问题"""
    # 特殊情况
    if eggs == 1:
        return height
    if height <= 1:
        return height
    
    # 创建DP表
    dp = [0] * (eggs + 1)
    
    # m表示实验次数
    m = 0
    while dp[eggs] < height:
        m += 1
        # 反向更新，避免覆盖
        for e in range(eggs, 0, -1):
            dp[e] = dp[e] + dp[e-1] + 1
    
    return m

def main():
    results = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        eggs, height = map(int, line.split())
        if eggs == 0 and height == 0:
            break
        
        # 调用函数计算结果
        results.append(str(egg_drop(eggs, height)))
    
    print("\n".join(results))

if __name__ == "__main__":
    main()
```
当step很大时，可以近似：
$$
\sum_{i=0}^{\min(\rm egg,step)}\binom{\rm step}{\rm i}-1\approx 2^{\rm step} \cdot\Phi(\frac{2\min(\rm egg,step)+1-step}{\sqrt{\rm step}})-1\approx h
$$





