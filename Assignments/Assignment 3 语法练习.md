

Updated 1440 GMT+8 Sep 23, 2025

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

### E28674:《黑神话：悟空》之加密

http://cs101.openjudge.cn/pctbook/E28674/



思路：

直接implementation


代码

```python
# 
n=int(input())
print(''.join(chr((ord(char)-n-65)%26+65) if char.isupper() else chr((ord(char)-n-97)%26+97) for char in input()))

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20250923161055.png]]




### E28691: 字符串中的整数求和

http://cs101.openjudge.cn/pctbook/E28691/



思路：

正则表达式语法
```python
import re 
text = input("请输入内容: ") # 找出所有数字 
digits = re.findall(r'\d', text) 
print("数字:", digits) # 找出所有字母 
letters = re.findall(r'[a-zA-Z]', text) 
print("字母:", letters) # 找出所有字母和数字（即字母数字字符） 
alphanum = re.findall(r'[a-zA-Z0-9]', text) 
print("字母和数字:", alphanum)
```

代码

```python
import re
s=input().split()
summ=0
for i in s:
    digits = re.findall(r'\d', i)
    summ+=int(''.join(digits))
print(summ)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20250923162019.png]]




### M28664: 验证身份证号 

http://cs101.openjudge.cn/pctbook/M28664/



思路：

使用卷积（）
好吧其实就是直接干
**hjkfiecbgdhjkfiecb**

代码

```python
code='hjkfiecbgdhjkfiecb'
n=int(input())
for i in range(n):
    identity=input().replace('X',':')
    summ=0
    for j in range(18):
        summ+=(ord(code[j])-ord('a'))*(ord(identity[j])-48)
        summ%=11
    print('YES' if summ==1 else 'NO')
        

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>
![[Pasted image 20250923164754.png]]




### M28678: 角谷猜想

http://cs101.openjudge.cn/pctbook/M28678/


思路：

直接干！

代码

```python
# 
n=int(input())
while n-1:
    if n%2:
        print(f'{n}*3+1={3*n+1}')
        n=3*n+1
    else:
        print(f'{n}/2={n//2}')
        n//=2
print('End')
```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20250923165356.png]]



### M28700: 罗马数字与整数的转换

http://cs101.openjudge.cn/pctbook/M28700/



思路：
字典+替换实现字母-数字转化和倒序转化
字典的语法确实之前不太熟悉……字典原来是一个Hash表，难怪说很快
```python
dict1={'Apple':1} # (key,value): ('Apple',1)
```

代码

```python
def toRoman(s):
    rom=''
    for key, value in reversed(dict1.items()):
        while value<=s:
            s-=value
            rom=rom+key
    for old, new in reversed(dict2.items()):
        rom = rom.replace(old, new)
    return rom
def tonum(s):
    for new, old in reversed(dict2.items()):
        s = s.replace(old, new)
    summ=0
    for i in s:
        summ+=dict1[i]
    return summ

dict1={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
dict2={'IIII':'IV','VIIII':'IX','XXXX':'XL','LXXXX':'XC','CCCC':'CD','DCCCC':'CM'}
s=input()
if s.isdigit():
    print(toRoman(int(s)))
else:
    print(tonum(s))

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20250923172732.png]]



### 158B. Taxi

*special problem, greedy, implementation, 1100,  https://codeforces.com/problemset/problem/158/B



思路：
4人团先上车，3人团再上车，然后1人团和3人团拼车，最后剩下的人自由组合，一定能组合成最好的情况


代码

```python
n=int(input())
a=[int(i) for i in input().split()]
b=[0]*5
for i in a:
    b[i]+=1
cars=b[4]#4-groups fit in taxis
cars+=b[3]#3-groups take taxis
b[1]=max(0,b[1]-b[3])# 1-group can couple with 3-group
left=b[1]+2*b[2]#1-group and 2-group can all seamlessly fit in
cars+=left//4
left%=4
if left:
    cars+=1
print(cars)

```



代码运行截图 <mark>（至少包含有"Accepted"）</mark>

![[Pasted image 20250923175356.png]]



## 2. 学习总结和收获

<mark>如果作业题目简单，有否额外练习题目，比如：OJ“计概2025fall每日选做”、CF、LeetCode、洛谷等网站题目。</mark>

做了**01094:Sorting It All Out**，犯了一点低级错误，找了半天🤣

	string.insert(index, content)，前面的一个是位置而非内容！
	join函数也挺好用的
```python
Help on built-in function join:

join(iterable, /) method of builtins.str instance
    Concatenate any number of strings.
    
    The string whose method is called is inserted in between each given string.
    The result is returned as a new string.
    
    Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
```
AC代码：
```python
def sets(l,r,value):
    global matrix
    if matrix[l][r] == value:
        return ''
    if matrix[l][r] != 0:
        return 'discrepancy'
    matrix[l][r] = value
    matrix[r][l] = -value
    for i in range(n):
        if i == l or i == r:
            continue
        if matrix[i][l] == value:
            if sets(i,r,value) == 'discrepancy':
                return 'discrepancy'
    for i in range(n):
        if i == r or i == l:
            continue
        if matrix[i][r] == -value:
            if sets(i,l,-value) == 'discrepancy':
                return 'discrepancy'

def full():
    global matrix
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j] == 0:
                return False
    return True

def build():
    global matrix
    seq = []
    for i in range(n):
        if i == 0:
            seq.append(i)
            continue
        flag = False
        for j in range(len(seq)):
            if matrix[seq[j]][i] == -1:
                seq.insert(j,i)#在j位置插入i元素!!!!!!!!
                flag = True
                break
        if not flag:
            seq.append(i)
    string = ''.join(chr(idx + ord('A')) for idx in seq)  #Good to learn
    return string

while True:
    n, m = map(int, input().split())
    if n == 0 and m == 0:
        break
    matrix = [[0] * n for _ in range(n)]
    relations = []
    for _ in range(m):
        relations.append(input())
    
    found = False
    for i in range(m):
        s = relations[i]
        l = ord(s[0]) - ord('A')
        r = ord(s[2]) - ord('A')
        result = sets(l, r, 1)
        if result == 'discrepancy':
            print(f'Inconsistency found after {i+1} relations.')
            found = True
            break
        if full():
            seq = build()
            print(f'Sorted sequence determined after {i+1} relations: {seq}.')
            found = True
            break
    if not found:
        print('Sorted sequence cannot be determined.')
```


