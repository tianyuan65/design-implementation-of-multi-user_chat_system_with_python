# _*_ coding : utf-8 _*_
# @Time : 2025/9/13 14:25
# @Author : 田园
# @File : test
# @Project : main.js.py

# 把这段输出的结果截图插入到ppt中
words=input()
result=''

for word in words:
    if 'a'<=word<='z':
        w = (ord(word) - ord('a') + 5) % 26
        encryptWord=chr(w+ord('a'))
        result+=encryptWord
print(result)