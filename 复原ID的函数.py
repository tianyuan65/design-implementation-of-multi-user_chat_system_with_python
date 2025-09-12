# _*_ coding : utf-8 _*_
# @Time : 2025/8/30 13:38
# @Author : 田园
# @File : 复原ID的函数
# @Project : main.js.py

# 复原ID的操作主要用在管理员身上，比如用户丢失了用户名和密码时，需要管理员用手机号、邮箱地址等用户的其他信息找到用户的真实用户名
# 或者坏蛋在干坏事时，警方或管理者需要根据加密的ID名找到真是的用户名来打击犯罪。
def decryptID(data):
    result=''
    for res in data:
        if 'a'<=res<='z':
            w=(ord(res)-ord('a')-3)%26
            decrypt_res=chr(w+ord('a'))
            result+=decrypt_res
        else:
            result+=res

    return result

print(decryptID('nbtf'))

