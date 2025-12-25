# Assignment #9: Mock Exam立冬前一天

Updated 1658 GMT+8 Nov 6, 2025

2025 fall, Complied by 马健文 元培学院



>**说明：**
>
>1. Nov⽉考： AC6 。考试题⽬都在“题库（包括计概、数算题目）”⾥⾯，按照数字题号能找到，可以重新提交。作业中提交⾃⼰最满意版本的代码和截图。
>
>2. 解题与记录：对于每一个题目，请提供其解题思路（可选），并附上使用Python或C++编写的源代码（确保已在OpenJudge， Codeforces，LeetCode等平台上获得Accepted）。请将这些信息连同显示“Accepted”的截图一起填写到下方的作业模板中。（推荐使用Typora https://typoraio.cn 进行编辑，当然你也可以选择Word。）无论题目是否已通过，请标明每个题目大致花费的时间。
>
>3. 提交安排：提交时，请首先上传PDF格式的文件，并将.md或.doc格式的文件作为附件上传至右侧的“作业评论”区。确保你的Canvas账户有一个清晰可见的本人头像，提交的文件为PDF格式，并且“作业评论”区包含上传的.md或.doc附件。
> 
>4. 延迟提交：如果你预计无法在截止日期前提交作业，请提前告知具体原因。这有助于我们了解情况并可能为你提供适当的延期或其他帮助。  
>
>请按照上述指导认真准备和提交作业，以保证顺利完成课程要求。





## 1. 题目

### E29982:一种等价类划分问题

hashing, http://cs101.openjudge.cn/practice/29982

思路：

直接Implementation

代码

```python
m,n,k = map(int,input().split(','))
a = [[] for i in range(1000)]
for i in range(m+1,n):
    num = i
    summ = 0
    while num:
        summ += num % 10
        num //= 10
    if summ % k:
        continue
    a[summ // k].append(i)
for i in a:
    if i:
        print(','.join([str(j) for j in i]))
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251106171719.png]]



### E30086:dance

greedy, http://cs101.openjudge.cn/practice/30086

思路：

贪心，最矮的肯定要和次矮的配对，如果不行就都不行

代码

```python
n,d = map(int,input().split())
def judge(h):
    if not len(h):
        return True
    if h[1]-h[0] > d:
        return False
    return judge(h[2::])
h = [int(_) for _ in input().split()]
h = sorted(h)
if judge(h):
    print('Yes')
else:
    print('No')
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251106171800.png]]



### M25570: 洋葱

matrices, http://cs101.openjudge.cn/practice/25570

思路：

遍历每个元素，加到对应的桶里面

代码

```python
n = int(input())
mat = []
for i in range(n):
    mat.append([int(_) for _ in input().split()])
cnt = [0]*n
for i in range(n):
    for j in range(n):
        cnt[min(i,j,n-1-i,n-1-j)] += mat[i][j]
print(max(cnt))
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251106171840.png]]



### M28906:数的划分

dfs, dp, http://cs101.openjudge.cn/practice/28906


思路：

记忆化搜索，每次记录n，k以及划分的maximum
似乎还有双变量递推的方式，以及五边形数的做法，但是我不会

代码

```python
memory = {}
def divide(n,k,maxx):
    #print(f'n={n} k={k} maxx={maxx}')
    global memory
    if n<0:
        return 0
    if n==0:
        if k==0:
            return 1
        else:
            return 0
    if k==0:
        return 0
    if maxx*k < n:
        return 0
    if maxx*k == n:
        return 1
    if (n,k,maxx) in memory:
        return memory[(n,k,maxx)]
    result = 0
    for i in range(1,maxx+1):
        result += divide(n-i,k-1,i)
    memory[(n,k,maxx)] = result
    return result
n,k = map(int,input().split())
print(divide(n,k,n))
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[1dfc7d227eb84a7e391c5c817a9ca033.png]]



### M29896:购物

greedy, http://cs101.openjudge.cn/practice/29896

思路：

这道贪心题目思路确实很巧妙。把需要组合出来的金额从小到大列成一张表格，从小往大遍历并依次解决。每次遇到当前硬币配置无法组合出来的情况时，挑选1个可以解决的最大的硬币（这样可以尽可能解决多的金额）

代码

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



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20251106172008.png]]



### T25353:排队

greedy, http://cs101.openjudge.cn/practice/25353

思路：

思路很复杂，见后

代码

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



代码运行截图 <mark>（至少包含有"Accepted"）</mark>


![[Pasted image 20251106172049.png]]


## 2. 学习总结和收获

如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。



排队题目的思路：

观察：如果一个元素A前面有与之不对易的元素B（差距大于D），则A不可能交换到B之前
推论：能够交换到队首的元素$h_i$必定能够满足$\max(h_{1\sim i-1})\leq h_i+D$, $\min(h_{1\sim i-1})\leq h_i-D$
因此扫描队列，将能够交换到队首的元素中最小者交换到队首（此处有一个问题：如何保证能交换到队首的元素始终能交换到队首（以及所有的在它前面的位置）？）
而后相同办法处理后续序列

继续交换时：将原来的可交换到队首的元素称为集合$S$. 为了保证字典序最小，我们要把$S$中的最小元素$s_1$交换到队首。这个时候我们再研究从第二个开始的序列。此时我们同样寻找类似的集合$S_1$. 容易发现，$S\backslash \{s_1\} \subset S_1$，并且可以证明$\min(S_1 \backslash S) \geq \min(S)$. 因此应该放在第二位的元素也是S中第二小的（只要$S\backslash \{s_1\} \neq \emptyset$）.依此类推，最终的最优序列的前$\rm \# S$个元素都应该是顺序排列的$S$.这样一轮做完以后，重新寻找能够排到队首的元素并排序，再考虑剩余元素，循环往复直到完成

---

使用有向无环图（DAG）的拓扑排序进行论证则会更易理解且更加严谨：
## 问题定义与 DAG 构建
- 有 $N$ 名同学，初始序列为 $h_1, h_2, \dots, h_N$。
- 操作：如果相邻两名同学的身高差 $|h_i - h_j| \leq D$，则可以交换他们的顺序。
- 目标：通过操作得到字典序最小的身高序列。
定义有向图 $G = (V, E)$，其中 $V = \{1, 2, \dots, N\}$ 表示同学的初始索引，边集 $E$ 定义如下：
- 对于任意 $i < j$，如果 $|h_i - h_j| > D$，则添加有向边 $i \to j$。
- **性质**：$G$ 是有向无环图（DAG），因为边只从索引小的节点指向索引大的节点。

### 序列与 DAG 的关系
**引理 1**：一个序列是通过相邻交换操作**可及**的当且仅当它是 DAG $G$ 的一个拓扑排序。
- **证明**（简要）：
  - 必要性：如果序列可及，则对于任意边 $i \to j$，$i$ 必须在 $j$ 之前，否则违反交换规则（因为 $|h_i - h_j| > D$ 时无法交换）。
  - 充分性：由下面的 Claim 证明。

**Claim：每个 DAG  的拓扑排序都是操作可及的。**

- **证明**：
	- **基例**（序列长度为 1）：  
	  当序列只有一个节点时，只有一个可能的序列，且无法进行任何交换操作，因此该序列是操作可及的。
	
	- **递归步骤**（序列长度为 $n$）：  
	  假设对于所有长度小于 $n$ 的序列，该Claim成立（即递归假设）。考虑一个长度为 $n$ 的DAG $G$ 和一个拓扑排序 $S$。设 $a$ 是 $S$ 中的第一个元素（队首）。
	
	  由于 $S$ 是 $G$ 的拓扑排序，节点 $a$ 在 $G$ 中的入度为 0。根据 DAG $G$ 的定义，边 $i \to j$ 存在当且仅当 $i < j$ 且 $|h_i - h_j| > D$。因此，入度为 0 意味着对于所有初始索引 $b < a$，有 $|h_b - h_a| \leq D$（否则边 $b \to a$ 存在，与 $a$ 入度为 0 矛盾）。
	
	  现在，从初始序列 $I$ 出发，我们需要证明 $a$ 可以通过操作移动到队首。由于对于所有在 $a$ 左边的元素 $b$（即初始索引 $b < a$)，有 $|h_b - h_a| \leq D$，因此 $a$ 可以与这些相邻元素交换。具体地，从 $a$ 的当前位置开始，重复交换 $a$ 与其左边的相邻元素（每次交换都是允许的，因为身高差不超过 $D$)，直到 $a$ 到达队首。这个过程类似于冒泡排序，且只涉及 $a$ 与左边元素的交换，不影响其他元素的相对顺序。
	
	  设 $I'$ 为将 $a$ 移动到队首后的序列，即 $I' = (a, I_{-a})$，其中 $I_{-a}$ 是初始序列移除 $a$ 后剩余元素的序列（保持原有顺序）。
	
	  接下来，考虑子图 $G' = G \setminus \{a\}$（即从 $G$ 中移除节点 $a$ 及其相关边）。序列 $S$ 移除 $a$ 后得到序列 $S'$，由于 $S$ 是 $G$ 的拓扑排序，$S'$ 是 $G'$ 的拓扑排序。序列 $I_{-a}$ 是 $G'$ 的初始序列（因为 $I_{-a}$ 是剩余元素的初始顺序）。
	
	  由于 $G'$ 有 $n-1$ 个节点，根据递归假设，任何 $G'$ 的拓扑排序（包括 $S'$) 都可以从 $I_{-a}$ 通过操作达到。因此，从序列 $I' = (a, I_{-a})$ 出发，可以通过操作仅对剩余部分进行交换，将 $I_{-a}$ 变为 $S'$，从而得到序列 $(a, S') = S$。
	
	  因此，拓扑排序 $S$ 可以从初始序列 $I$ 通过操作达到。
	
	由递归原理，对于任意长度 $n$，每个 DAG $G$ 的拓扑排序都是操作可及的。

### 贪心算法（基于图论）
根据 Claim，问题转化为求 DAG $G$ 的字典序最小拓扑排序。算法如下：
- 计算每个节点的入度。
- 维护一个优先队列（最小堆），存储当前入度为 0 的节点，按身高 $h_i$ 排序（身高相同时按初始索引排序）。
- 每次从堆中取出身高最小的节点 $u$，输出 $h_u$，并移除 $u$ 及其出边，更新邻居入度。如果邻居入度变为 0，则加入堆。
- 时间复杂度：$O(N \log N)$，但显式构建图需要 $O(N^2)$ 时间，对于大规模数据可能不可行。

因此进行优化：
## 优化
可以对以上的想法进行优化，以避免显式构建图，而是通过多轮扫描找到入度为 0 的节点集合。设 $S_1$ 为初始入度为 0 的节点集合。当从 $S_1$ 中取出最小元素 $x$ 后，新入度为 0 的节点集合记为 $T_2$。用户断言 $T_2$ 中所有元素的身高都大于 $S_1$ 中剩余元素的身高，因此在 $S_1$ 未被取完时，只需从 $S_1$ 中取最小，无需考虑 $T_2$。以下进行严谨证明。

#### 定义和符号
- $S_1$: 初始入度为 0 的节点集合。
- $x$: $S_1$ 中身高最小的节点（即 $h_x = \min_{q \in S_1} h_q$)。
- $T_2$: 在删除 $x$ 后，入度变为 0 的节点集合。

#### 断言一：$\forall p \in T_2$, $|h_p - h_x| > D$
- **证明**：由于 $p$ 在删除 $x$ 后入度变为 0，且在删除前 $p$ 的入度正好为 1（仅来自 $x$），因此边 $x \to p$ 存在。根据边定义，$x < p$ 且 $|h_x - h_p| > D$，故 $|h_p - h_x| > D$.

#### 断言二：$\forall p \in T_2$, $\forall q \in S_1 \setminus \{x\}$, $|h_p - h_q| \leq D$
- **证明**：考虑任意 $q \in S_1 \setminus \{x\}$。
  - 案例一：如果 $q < p$，假设 $|h_q - h_p| > D$，则边 $q \to p$ 存在。但 $q$ 在删除 $x$ 前仍在图中，且指向 $p$，这与 $p$ 在删除 $x$ 前入度仅为 1（来自 $x$）矛盾。因此 $|h_q - h_p| \leq D$。
  - 案例二：如果 $p < q$，假设 $|h_p - h_q| > D$，则边 $p \to q$ 存在。但 $q \in S_1$ 意味着 $q$ 的初始入度为 0，即没有边指向 $q$，矛盾。因此 $|h_p - h_q| \leq D$.
- 综上，$\forall q \in S_1 \setminus \{x\}$, $|h_p - h_q| \leq D$.

#### 断言三：$\forall p \in T_2$, $h_p > h_x + D$
- **证明**：从断言一，$|h_p - h_x| > D$，所以要么 $h_p > h_x + D$ 要么 $h_p < h_x - D$。假设 $h_p < h_x - D$，则对于任意 $q \in S_1 \setminus \{x\}$，有 $h_q \geq h_x$（因为 $x$ 是 $S_1$ 中最小），所以 $|h_q - h_p| = h_q - h_p > h_x - (h_x - D) = D$，与断言二矛盾。因此 $h_p > h_x + D$.

#### 断言四：$\forall q \in S_1$, $h_q \leq h_x + D$
- **证明**：考虑任意 $q \in S_1$。
  - 案例一：如果 $q < x$，假设 $h_q > h_x + D$，则 $|h_q - h_x| > D$，边 $q \to x$ 存在，与 $x \in S_1$（入度为 0）矛盾。因此 $h_q \leq h_x + D$。
  - 案例二：如果 $q > x$，假设 $h_q > h_x + D$，则 $|h_x - h_q| > D$，边 $x \to q$ 存在，与 $q \in S_1$（入度为 0）矛盾。因此 $h_q \leq h_x + D$.
- 综上，$\forall q \in S_1$, $h_q \leq h_x + D$.

#### 推论：$\forall p \in T_2$, $\forall q \in S_1 \setminus \{x\}$, $h_p > h_q$
- **证明**：从断言三和断言四，$h_p > h_x + D \geq h_q$，所以 $h_p > h_q$.

因此，在删除 $x$ 后，$T_2$ 中所有元素的身高都大于 $S_1$ 中剩余元素的身高。这意味着在 $S_1$ 未被取完时，字典序最小的选择始终来自 $S_1$ 中的最小元素，无需考虑 $T_2$.

### 归纳扩展
上述论证可归纳应用于算法每一步：只要初始 $S_1$ 中还有节点未被取出，任何新生成的入度为 0 的节点（如 $T_2, T_3, \dots$）的身高都大于 $S_1$ 中剩余节点的身高。因此，算法可优先处理 $S_1$ 直到其为空，再处理新生成的集合。

## 基于多轮扫描的算法
根据上述论断，我们可以设计一个不显式构建图的算法，通过多轮扫描直接找到当前入度为 0 的节点集合 $S$，排序后输出。算法如下：

#### 算法描述
- **输入**：$N, D$ 和身高列表 $H = [h_1, h_2, \dots, h_N]$。
- **输出**：字典序最小的身高序列。
- **步骤**：
  1. 初始化一个列表 $L$，包含元组 $(h_i, i)$ for $i = 1, 2, \dots, N$，其中 $i$ 是初始索引（用于排序时打破平局）。
  2. 初始化一个空列表 $R$ 用于存储结果。
  3. 当 $L$ 不为空时：
     - 初始化 $\text{current\_min} = \infty$, $\text{current\_max} = -\infty$。
     - 初始化一个空列表 $S$。
     - 对于 $L$ 中的每个元素 $(h, \text{idx})$ 按顺序（即按初始索引顺序）：
       - 检查条件：如果 $h \geq \text{current\_max} - D$ 且 $h \leq \text{current\_min} + D$，则将 $(h, \text{idx})$ 加入 $S$。
       - 更新 $\text{current\_min} = \min(\text{current\_min}, h)$, $\text{current\_max} = \max(\text{current\_max}, h)$。
     - 将 $S$ 按身高 $h$ 从小到大排序，如果身高相同，按初始索引 $\text{idx}$ 从小到大排序。
     - 将 $S$ 中的元素（按排序后的顺序）追加到 $R$。
     - 从 $L$ 中移除 $S$ 中的所有元素。
  4. 输出 $R$ 中的身高序列。

#### 算法正确性证明
- **入度为 0 的节点识别**：对于列表 $L$ 中的元素，入度为 0 当且仅当对于所有在它左边的元素（在 $L$ 中），身高差不超过 $D$。该条件等价于 $h \geq \text{current\_max} - D$ 且 $h \leq \text{current\_min} + D$，其中 $\text{current\_min}$ 和 $\text{current\_max}$ 是当前左边元素的最小值和最大值。这是因为：
  - 必要性：如果元素入度为 0，则它与所有左边元素身高差不超过 $D$，尤其与最小值和最大值的差不超过 $D$，所以条件满足。
  - 充分性：如果条件满足，则对于任意左边元素 $h_j$，有 $|h_j - h| \leq \max(\text{current\_max} - h, h - \text{current\_min}) \leq D$。
- **输出顺序的字典序最小**：根据论断，在每一轮中，集合 $S$ 中的元素是当前入度为 0 的节点，且输出 $S$ 中最小身高元素（同时排序）不会影响后续选择，因为新生成的入度为 0 的节点身高都大于 $S$ 中剩余元素。因此，按排序顺序输出 $S$ 确保字典序最小。

#### 时间复杂度分析
- 最坏情况下，每次迭代可能只移除一个元素，导致 $O(N)$ 次迭代，每次迭代需要 $O(|L|)$ 时间，总时间复杂度为 $O(N^2)$。
- 对于 $N \leq 10^5$，最坏情况 $O(N^2)$ 可能较慢，但平均情况下可能更快。可以通过维护链表或其他数据结构优化扫描过程，但本算法简单且基于数学论断。
