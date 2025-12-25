# Assignment #B: dp

Updated 1448 GMT+8 Nov 18, 2025

2025 fall, Complied by 马健文+元培学院



**说明：**

1）请把每个题目解题思路（可选），源码Python, 或者C++（已经在Codeforces/Openjudge上AC），截图（包含Accepted），填写到下面作业模版中（推荐使用 typora https://typoraio.cn ，或者用word）。AC 或者没有AC，都请标上每个题目大致花费时间。

2）提交时候先提交pdf文件，再把md或者doc文件上传到右侧“作业评论”。Canvas需要有同学清晰头像、提交文件有pdf、"作业评论"区有上传的md或者doc附件。

3）如果不能在截止前提交作业，请写明原因。



## 1. 题目

### LuoguP1255 数楼梯

dp, bfs, https://www.luogu.com.cn/problem/P1255

思路：

Fibonacci

代码：

```python
dp = [0,1]
n = int(input())
while len(dp)<n+2:
    dp.append(dp[-1]+dp[-2])
print(dp[-1])

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>


![Pasted image 20251124210635.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251124210635.png?CiuMhuLs4i)


### 27528: 跳台阶

dp, http://cs101.openjudge.cn/practice/27528/

思路：

等比数列，公比2

代码：

```python
print(1<<(int(input())-1))
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![Pasted image 20251124211033.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251124211033.png?wvTWBsN358)



### M23421:《算法图解》小偷背包问题

dp, http://cs101.openjudge.cn/pctbook/M23421/

思路：

经典的01背包

代码：

```python
items,load = map(int,input().split())
values = [int(i) for i in input().split()]
weights = [int(i) for i in input().split()]
dp = [0]*(load+1)
for i in range(items):
    new = [_ for _ in dp]
    for j in range(load+1):
        if j + weights[i] <= load:
            new[j + weights[i]] = max(new[j + weights[i]],dp[j] + values[i])
    dp = [_ for _ in new]
print(max(dp))
            
        

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![Pasted image 20251124214825.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251124214825.png?c6Q7DDDc6y)



### M5.最长回文子串

dp, two pointers, string, https://leetcode.cn/problems/longest-palindromic-substring/

思路：

经典Manacher算法：
先把字符串`'abc'`预处理成`'#a#b#c#'`的形式
维护一个`p[i]`数组，记录以i为中心的最大回文串半径
维护center，表示当前找到的边界最靠右的回文串的中心位置
通过对称性快速获得初始回文串长度
之后再进行扩展
如果扩展到超出Center对应的回文串，则center变成i


代码：

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""
        
        # 预处理字符串
        t = '#' + '#'.join(s) + '#'
        n = len(t)
        p = [0] * n  # 回文半径数组
        
        center = right = 0  # 当前中心和右边界
        max_center = max_radius = 0  # 记录最长回文的中心和半径
        
        for i in range(n):
            # 利用对称性快速获得初始半径
            if i < right:
                mirror = 2 * center - i
                p[i] = min(p[mirror], right - i)
            
            # 中心扩展
            left_idx = i - p[i] - 1
            right_idx = i + p[i] + 1
            while left_idx >= 0 and right_idx < n and t[left_idx] == t[right_idx]:
                p[i] += 1
                left_idx -= 1
                right_idx += 1
            
            # 更新中心和右边界
            if i + p[i] > right:
                center = i
                right = i + p[i]
            
            # 更新最长回文
            if p[i] > max_radius:
                max_radius = p[i]
                max_center = i
        
        # 提取结果并去除特殊字符
        start = (max_center - max_radius) // 2
        return s[start:start + max_radius]
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![Pasted image 20251125110306.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251125110306.png?61H547ZrIb)





### 474D. Flowers

dp, 1700 https://codeforces.com/problemset/problem/474/D

思路：

状态转移方程
`dp[i]=dp[i-1]+dp[i-k]`
如果i-k<0认为是1

代码：

```python
import sys
lines = sys.stdin.read().splitlines()
t,k = map(int,lines[0].split())
dp = [1] * (int(1e5) + 5)
summ = [1] * (int(1e5) + 5)
mod = int(1e9 + 7)
for i in range(1,int(1e5) + 2):
    if i >= k:
        dp[i] = (dp[i - 1] + dp[i - k]) % mod
    else:
        dp[i] = dp[i - 1]
    summ[i] = (summ[i - 1] + dp[i]) % mod
for line in lines[1::]:
    L,R = map(int,line.split())
    print((summ[R] - summ[L - 1]) % mod)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![Pasted image 20251125112618.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251125112618.png?38Kirr6K7V)



### M198.打家劫舍

dp, https://leetcode.cn/problems/house-robber/

思路：

dp，分rob和不去rob两种情况讨论

代码：

```python
class Solution:

    def rob(self, nums: List[int]) -> int:

        n = len(nums)

        dp = [[0,0] for i in range(n)]

        dp[0][1] = nums[0]

        for i in range(1,n):

            dp[i][0] = max(dp[i-1][0],dp[i-1][1])

            dp[i][1] = dp[i-1][0] + nums[i]

        return max(dp[n - 1])
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>


![Pasted image 20251125113343.png](https://obsidian-note-kulinkovich.oss-cn-beijing.aliyuncs.com/obsidian-images/202512/18/Pasted%20image%2020251125113343.png?NWb9XuUG8i)


## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2024fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>





