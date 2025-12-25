

Updated 1427 GMT+8 Sep 9, 2025

2025 fall, Complied by ==马健文、元培学院==



**作业的各项评分细则及对应的得分**

| 标准                  | 等级                                                                       | 得分  |
| ------------------- | ------------------------------------------------------------------------ | --- |
| 按时提交                | 完全按时提交：1分<br/>提交有请假说明：0.5分<br/>未提交：0分                                    | 1 分 |
| 源码、耗时（可选）、解题思路（可选）  | 提交了4个或更多题目且包含所有必要信息：1分<br/>提交了2个或以上题目但不足4个：0.5分<br/>少于2个：0分              | 1 分 |
| AC代码截图              | 提交了4个或更多题目且包含所有必要信息：1分<br/>提交了2个或以上题目但不足4个：0.5分<br/>少于：0分                | 1 分 |
| 清晰头像、PDF文件、MD/DOC附件 | 包含清晰的Canvas头像、PDF文件以及MD或DOC格式的附件：1分<br/>缺少上述三项中的任意一项：0.5分<br/>缺失两项或以上：0分 | 1 分 |
| 学习总结和个人收获           | 提交了学习总结和个人收获：1分<br/>未提交学习总结或内容不详：0分                                      | 1 分 |
| 总得分： 5              | 总分满分：5分                                                                  |     |
|                     |                                                                          |     |

>
>
>
>**说明：**
>
>1. **解题与记录：**
>
>   对于每一个题目，请提供其解题思路（可选），并附上使用Python或C++编写的源代码（确保已在OpenJudge， Codeforces，LeetCode等平台上获得Accepted）。请将这些信息连同显示“Accepted”的截图一起填写到下方的作业模板中。（推荐使用Typora https://typoraio.cn 进行编辑，当然你也可以选择Word。）无论题目是否已通过，请标明每个题目大致花费的时间。
>
>2. **课程平台：**课程网站位于Canvas平台（https://pku.instructure.com ）。该平台将在<mark>第2周</mark>选课结束后正式启用。在平台启用前，请先完成作业并将作业妥善保存。待Canvas平台激活后，再上传你的作业。
>
>3. **提交安排：**提交时，请首先上传PDF格式的文件，并将.md或.doc格式的文件作为附件上传至右侧的“作业评论”区。确保你的Canvas账户有一个清晰可见的本人头像，提交的文件为PDF格式，并且“作业评论”区包含上传的.md或.doc附件。
>
>4. **延迟提交：****如果你预计无法在截止日期前提交作业，请提前告知具体原因。这有助于我们了解情况并可能为你提供适当的延期或其他帮助。  
>
>请按照上述指导认真准备和提交作业，以保证顺利完成课程要求。





## 1. 题目

### E02733: 判断闰年

http://cs101.openjudge.cn/pctbook/E02733/



思路：

Trivial. Do what should be done.

代码

```python
# 
x=int(input())
print('Y' if (x%4==0) and ((x%100 !=0) or (x%400==0)) else 'N')
```



代码运行截图 ==（至少包含有"Accepted"）==


![[Pasted image 20250909195243.png]]



### E02750: 鸡兔同笼

http://cs101.openjudge.cn/pctbook/E02750/



思路：分类讨论：腿必为偶数，故奇数者直接无解；鸡越多，动物越多，故max为x//2；兔越多，动物越多，然若腿数非4n则无法全为兔，只得(n-2)//4只兔与1只鸡

代码

```python
# 
x=int(input())
if x%2==1:
    print(0,0)
elif x%4==0:
    print(x//4, x//2)
else:
    print(x//4+1, x//2)

```



代码运行截图 ==（至少包含有"Accepted"）==


![[Pasted image 20250909200118.png]]




### 50A. Domino piling

greedy, math, 800, http://codeforces.com/problemset/problem/50/A



思路：

偶$\times$偶：直接正交镶嵌即可
奇$\times$偶：直接正交镶嵌即可(长边沿偶边方向)
奇$\times$奇：拆成奇$\times$偶+奇$\times 1$，前者可铺满后者差一块，由染色可知必然至少有一个未被覆盖的格子
归纳可知，$$\# Domino = [\frac{mn}{2}] $$

代码

```python
# 
m,n=map(int, input().split())
print(m*n//2)
```



代码运行截图 ==（至少包含有"Accepted"）==

![[Pasted image 20250909212653.png]]



### 1A. Theatre Square

math, 1000, https://codeforces.com/problemset/problem/1/A



思路：
Trivial and Apparant


代码

```python
# 
n,m,a=map(int, input().split())
print(((m-1)//a+1)*((n-1)//a+1))
```



代码运行截图 ==（至少包含有"Accepted"）==

![[Pasted image 20250909213219.png]]



### 112A. Petya and Strings

implementation, strings, 1000, http://codeforces.com/problemset/problem/112/A



思路：

Trivial

代码

```python
# 
s1=input().upper()
s2=input().upper()
print(int(s1>s2) - int(s1<s2))
```



代码运行截图 ==（至少包含有"Accepted"）==

![[Pasted image 20250909213749.png]]



### 231A. Team

bruteforce, greedy, 800, http://codeforces.com/problemset/problem/231/A



思路：

Trivial

代码

```python
# 
n=int(input())
count=0
for i in range(n):
    a,b,c=map(int,input().split())
    count+=int(a+b+c>1)
print(count)
```



代码运行截图 ==（至少包含有"Accepted"）==

![[Pasted image 20250909214430.png]]



## 2. 学习总结和收获

==如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。==



作业题目太简单了，写了一个KMP算法（自己的版本，和标准的有出入）
```python
def judge(s1,s2): # judge whether s1 and s2 have discrepancy
    L=min(len(s1),len(s2))
    #print('judge(',s1,'==',s2,')=',(s1[0:L]==s2[0:L]))
    return (s1[0:L]==s2[0:L])
seg=' '+input().lower()+' '
text=' '+input().lower()+' '
jump=[1]
for i in range(1,len(seg)+1):
    j=1
    common=seg[0:i]
    #print('common=',common)
    while j<=i:
        #print(j, end=' ')
        if judge(common,common[j::1]):#[0,i) matched, but seg[i] doesn't match
            break;
        j+=1
    #print(j)
    jump.append(j)
#print(jump)
i=0
exist=False
count=0
while i+len(seg)<=len(text):
    l=0
    while l<len(seg) and text[i+l]==seg[l]:
        l+=1
    if l==len(seg):
        if not exist:
            first=i
            exist=True
            #print(i)
        count+=1
    i+=jump[l]
if exist:
    print(count,first)
else:
    print(-1)

```

![[Pasted image 20250910114250.png]]
![[Pasted image 20250910114258.png]]
但是发现其实根本用不上KMP，时间是足够的
