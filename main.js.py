# _*_ coding : utf-8 _*_
# @Time : 2025/8/13 14:25
# @Author : 田园
# @File : mian.js
# @Project : 地图上找路第二弹.py

# UI道具
# import tkinter as tk
# root=tk.Tk()
# root.geometry('600x600')
# root.title('Chat App')
# box1=tk.Label(root)
# box1['text']='test Box'
# box1.place(x=50,y=50,width=500,height=50)
# box2=tk.Label(root)
# box2['text']='test2'
# box2['bg']='black'
# box2['fg']='white'
# box2.place(x=50,y=100,width=500,height=50)
# root.mainloop()

import tkinter as tk
from tkinter import scrolledtext
import datetime
# 代替数据库
import json
# 加密
import hashlib
import os
import binascii

class LoginApp:
    # 初始化
    def __init__(self, root):
        self.root = root
        self.root.geometry('400x500')
        self.root.title('login or register')
        self.root.configure(bg='white')

        # 用户名输入框
        self.usernameEntry = tk.Entry(root)
        self.usernameEntry['font'] = ('Arial', 10)
        self.usernameEntry.place(x=100, y=80, width=200, height=40)
        self.usernameEntry.insert(0, 'username')

        # 密码输入框
        self.passwordEntry = tk.Entry(root, show='*')
        self.passwordEntry['font'] = ('Arial', 10)
        self.passwordEntry.place(x=100, y=140, width=200, height=40)
        self.passwordEntry.insert(0, 'password')

        # 登录按钮
        self.loginBtn = tk.Label(root)
        self.loginBtn['text'] = 'login'
        self.loginBtn['bg'] = '#FFE100'
        self.loginBtn['fg'] = 'black'
        self.loginBtn['font'] = ('Arial', 12)
        self.loginBtn.place(x=100, y=300, width=200, height=40)
        self.loginBtn.bind('<Button-1>', self.login)

        # 确认密码的输入框，就是需要二次输入密码的输入框，默认先不展示
        self.passwordReEntry = tk.Entry(root, show='*')
        self.passwordReEntry['font'] = ('Arial', 10)

        # 注册按钮
        self.registerBtn = tk.Label(root)
        self.registerBtn['text'] = 'register'
        self.registerBtn['bg'] = 'aqua'
        self.registerBtn['fg'] = 'black'
        self.registerBtn['font'] = ('Arial', 12)
        self.registerBtn.place(x=100, y=360, width=200, height=40)
        self.registerBtn.bind('<Button-1>', self.open_register)

        # 用户数据库（简单模拟）
        # 最高权限使用者
        self.administrator = {'priorityRoot': '123456'}

        # 加载用户数据
        try:
            # 若第一次登录，则创建一个文件来存储用户数据
            with open('usersInfo.json', 'r') as file:
            # with open(f"{self.encryptID('test')}_friends.json", 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            # 若不是第一次登录，则用户的信息会存在，则直接打开已有文件，并继续向里存储后续数据
            with open('usersInfo.json', 'w') as f:
            # with open(f"{self.encryptID('test')}_friends.json", 'w') as f:
                # self.users = {self.encryptID('test'):self.encrypt('1234')}
                # self.users={self.encryptID('makit'):self.encrypt('7890')}
                # 初始化users
                self.users={}
                # 向users中分别添加test和makit用户名及密码
                self.users[self.encryptID('test')]= self.encrypt('1234')
                self.users[self.encryptID('makit')]= self.encrypt('7890')
                json.dump(self.users,f)
        # 通过hash来对用户的信息进行加密操作
        # 用户名用一种算法来进行保密，如A写成O，可以用凯撒加密法
        # 密码用hash加密方式
        # 암호화不是为了永久加密，而且为了开发者自己使用也没法永久加密，即使是开发者也需要定时换一个保密法来保护数据，如SHA256hash
        # 但在Python中不能直接使用hashlib.sha256(password.encode()).hexdigest()，可以用Python内置的hashlib中的 pbkdf2_hmac
        # 值得注意的是用SHA256hash加密的密码，除了黑客用zombie PC强制破解以外，常人无法破解密码，所以一般用户忘记了密码，都会让重新设置密码

    # 登录函数
    def login(self, event=None):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        print(self.users)   #{'whvw': '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'}
        # 加密的ID
        encryptName=self.encryptID(username)
        print('encrypyName-'+encryptName)   #encrypyName-whvw
        encrypt=self.encrypt(password)
        print('encrypt-'+encrypt)   #encrypt-03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4

        # 若加密的id和self.users的id相同并且，加密的密码也进行比较，若相同，则予以登录
        # if encryptName in self.users and self.encrypt('1234')=='03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4':
        if encryptName in self.users and self.users[encryptName]==encrypt:
            self.open_chatApp(username)
        else:
            errorLabel = tk.Label(self.root)
            errorLabel['text'] = 'failed to login'
            errorLabel['bg'] = 'white'
            errorLabel['fg'] = 'red'
            errorLabel.place(x=150, y=250, width=100, height=20)
            self.root.after(2000, errorLabel.destroy)

    # 展示注册按钮，隐藏登录按钮
    def open_register(self, event=None):
        # 隐藏登录按钮
        self.loginBtn.place_forget()
        # 展示二次输入密码的输入框
        self.passwordReEntry.place(x=100,y=200,width=200,height=40)
        # 注册按钮和注册模块函数进行绑定
        self.registerBtn.unbind('<Button-1>')
        self.registerBtn.bind('<Button-1>',self.register)

    # 注册模块函数
    def register(self, event=None):
        # 获取新用户的id和密码
        newUser = self.usernameEntry.get()
        newPwd1 = self.passwordEntry.get()
        newPwd2 = self.passwordEntry.get()

        # 若新用户的id涨肚小于1，或用户名已存在，或密码长度小于4或设置的密码和确认密码不一样
        if len(newUser)<=1 or self.encryptID(newUser) in self.users or len(newPwd1)<4 or newPwd1!=newPwd2:
            # 则报错，注册失败
            errorLabel = tk.Label(self.root)
            errorLabel['text'] = 'failed to register'
            errorLabel['bg'] = 'white'
            errorLabel['fg'] = 'red'
            errorLabel.place(x=150, y=250, width=100, height=20)
            self.root.after(2000, errorLabel.destroy)
            return

        # 注册成功，则保存用户信息
        encryptName=self.encryptID(newUser)
        encryptPwd=self.encrypt(newPwd1)
        self.users[encryptName]=encryptPwd

        # 保存到文件
        with open('usersInfo.json','w') as f:
            # self.users[self.encryptID('user1')] = self.encrypt('2345')
            json.dump(self.users,f)

        # 展示成功信息
        successLabel = tk.Label(self.root)
        successLabel['text'] = 'Registration successful'
        successLabel['bg'] = 'white'
        successLabel['fg'] = 'blue'
        successLabel.place(x=150, y=250, width=100, height=20)
        self.root.after(2000, successLabel.destroy)

        # 注册成功，则隐藏第二个输入密码的输入框，恢复登录页面
        # 隐藏确认密码的输入框
        self.passwordReEntry.place_forget()
        # 恢复登录按钮
        self.loginBtn.place(x=100,y=300,width=200,height=40)
        # 注册按钮和与Button-1解绑
        self.registerBtn.unbind('<Button-1>')
        # 注册按钮和open_register函数重新绑定
        self.registerBtn.bind('<Button-1>', self.open_register)

    # 成功登录，打开聊天框
    def open_chatApp(self, username):
        self.root.destroy()
        chat_root = tk.Tk()
        ChatApp(chat_root, username)
        chat_root.mainloop()

    # 登录是密码加密，方法2
    def encrypt(self,data):
        input_string=data
        encoded_string=input_string.encode('utf-8')
        sha256_hash=hashlib.sha256(encoded_string)
        hex_digest=sha256_hash.hexdigest()
        return hex_digest
    # ID加密，用凯撒加密法，挪三格
    def encryptID(self,data):
        result=''
        for word in data:
            if 'a' <= word <= 'z':
                # 将字符转换为0-25的数字，加上偏移量3，然后取模26确保在字母范围内
                w = (ord(word) - ord('a') + 3) % 26
                encrypted_word = chr(w + ord('a'))
                result += encrypted_word
            else:
                # 非字母字符保持不变
                result += word
        return result

class ChatApp:
    # 初始化，也需要把username接收一下，否则成功登录后，不给显示聊天记录
    def __init__(self, root,username):
        self.root = root
        self.root.geometry('800x600')
        self.root.title('KakaoTalk Clone')
        self.root.configure(bg='#F5F5F5')
        self.username=username

        # 联系人列表框架
        self.contacts_frame = tk.Frame(root, bg='#F5F5F5')
        self.contacts_frame.place(x=0, y=0, width=200, height=600)

        # 搜索框
        search_box = tk.Label(self.contacts_frame)
        search_box['text'] = '搜索联系人...'
        search_box['bg'] = 'white'
        search_box['fg'] = 'gray'
        search_box.place(x=10, y=10, width=170, height=30)

        # 存储聊天记录
        try:
            # 若第一次登录，则创建一个文件来存储数据
            # with open('chatHistory.json','r') as file:
            with open(f"{username}_chatHistory.json", 'r') as file:
                self.chat_history=json.load(file)
        except FileNotFoundError:
            # 若不是第一次登录，则聊天记录会存在，则直接打开已有文件，并继续向里存储数据
            # with open('chatHistory.json','w') as file:
            with open(f"{username}_chatHistory.json", 'w') as file:
                self.chat_history={ "friend1":[],"friend2":[],"friend3":[] }
                json.dump(self.chat_history,file,indent=4)

        # 联系人列表
        # test的联系人："张三", "李四", "王五", "赵六", "钱七"
        # makit的联系人："赵六", "钱七", "孙八", "周九", "吴十"
        # contacts = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
        # contacts={
        #     'test':["张三", "李四", "王五", "赵六", "钱七"],
        #     'makit':["赵六", "钱七", "孙八", "周九", "吴十"]
        # }
        contacts=list(self.chat_history.keys())
        # testContacts=["张三", "李四", "王五", "赵六", "钱七"]
        # makitContacts=["赵六", "钱七", "孙八", "周九", "吴十"]
        # 初始化每个联系人按钮
        self.contact_buttons = []

        # 遍历联系人
        for i, contact in enumerate(contacts):
            # 设置联系人框的样式
            btn = tk.Label(self.contacts_frame)
            btn['text'] = contact
            btn['bg'] = 'white'
            btn['fg'] = 'black'
            btn['anchor'] = 'w'
            btn.place(x=10, y=50 + i * 50, width=180, height=40)
            # 将选中联系人的函数self.select_contact()和联系人按钮绑定在一起
            btn.bind('<Button-1>', lambda e, c=contact: self.select_contact(c))
            self.contact_buttons.append(btn)

        # 聊天区域框架
        self.chat_frame = tk.Frame(root, bg='white')
        self.chat_frame.place(x=200, y=0, width=600, height=600)

        # 聊天标题
        self.chatTitle = tk.Label(self.chat_frame)
        self.chatTitle['text'] = '选择联系人开始聊天'
        self.chatTitle['bg'] = 'white'
        self.chatTitle['fg'] = 'black'
        self.chatTitle['font'] = ('Arial', 12, 'bold')
        self.chatTitle.place(x=10, y=10, width=580, height=30)

        # 分隔线
        separator = tk.Label(self.chat_frame)
        separator['bg'] = '#E0E0E0'
        separator.place(x=10, y=50, width=580, height=1)

        # 聊天消息区域
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD)
        self.chat_area['bg'] = 'white'
        self.chat_area['fg'] = 'black'
        self.chat_area['font'] = ('Arial', 10)
        self.chat_area['state'] = 'disabled'
        self.chat_area.place(x=10, y=60, width=580, height=450)

        # 输入框
        self.input_frame = tk.Frame(self.chat_frame, bg='white')
        self.input_frame.place(x=10, y=520, width=580, height=70)

        # 信息样式
        self.message_entry = tk.Entry(self.input_frame)
        self.message_entry['font'] = ('Arial', 10)
        self.message_entry.place(x=0, y=0, width=480, height=30)
        self.message_entry.bind('<Return>', self.send_message)

        # 发送按钮
        self.send_button = tk.Label(self.input_frame)
        self.send_button['text'] = '发送'
        self.send_button['bg'] = '#FFE100'  # KakaoTalk黄色
        self.send_button['fg'] = 'black'
        self.send_button['font'] = ('Arial', 10, 'bold')
        self.send_button.place(x=490, y=0, width=90, height=30)
        self.send_button.bind('<Button-1>', self.send_message)

        # 当前选中的联系人
        self.current_contact = None

        # 存储聊天记录
        # 即使没有初始聊天记录，也需要创建一个json文件
        # 用try...except...来预防聊天记录已在的情况

        # self.chat_history = {}

        # 加载聊天记录
        self.chat_history_file = f"{username}_chatHistory.json"
        self.load_chat_history()

        # 设置初始选中状态，默认选择contacts列表中的第一个
        self.select_contact(contacts[0])

        # 添加联系人的+
        add_contacts = tk.Label(self.contacts_frame)
        add_contacts['text'] = 'New Chat'
        add_contacts['bg'] = 'aqua'
        add_contacts['fg'] = 'black'
        add_contacts.place(x=30, y=540, width=140, height=40)
        add_contacts.bind('<Button-1>', self.addContacts)

    # 加载聊天记录
    def load_chat_history(self):
        try:
            with open(self.chat_history_file, 'r') as file:
                self.chat_history = json.load(file)
        except FileNotFoundError:
            self.chat_history = {}

    # 保存聊天记录
    def save_chat_history(self):
        with open(self.chat_history_file, 'w') as f:
            json.dump(self.chat_history, f, indent=4)

    # 点击选择聊天对象
    def select_contact(self, contact):
        self.current_contact = contact
        self.chatTitle['text'] = f'与 {contact} 聊天'

        # 重置所有联系人的背景色
        for btn in self.contact_buttons:
            btn['bg'] = 'white'

        # 设置当前选中联系人的背景色
        for btn in self.contact_buttons:
            if btn['text'] == contact:
                btn['bg'] = '#E8E8E8'
                break

        # 显示聊天记录
        self.chat_area.config(state='normal')
        self.chat_area.delete(1.0, tk.END)

        # 选中的联系人在之前有过聊天记录
        if contact in self.chat_history:
            # 获取到与该联系人的聊天记录
            for message in self.chat_history[contact]:
                # 向聊天区域添加新聊天记录中
                self.chat_area.insert(tk.END, message)

        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    # 发送信息
    def send_message(self, event=None):
        # 声明message变量
        message = self.message_entry.get().strip()
        # 若无新输入的信息或没有选中任何联系人
        if not message or not self.current_contact:
            # 则直接返回
            return

        # 获取当前时间
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M")

        # 格式化消息
        formatted_message = f"[{time_str}] 我: {message}\n"

        # 添加到聊天记录
        # 若与选中的联系人无聊天记录
        if self.current_contact not in self.chat_history:
            # 则向聊天记录中添加选中的联系人
            self.chat_history[self.current_contact] = []
        # 将与选中的联系人的聊天记录添加到chat_history中
        self.chat_history[self.current_contact].append(formatted_message)

        # 更新聊天区域
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, formatted_message)
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

        # 清空输入框
        self.message_entry.deletes(0, tk.END)

        # 将聊天记录存储到chatHistory.json文件中
        with open(f"{self.username}_chatHistory.json", 'w') as f:
            json.dump(self.chat_history, f, indent=4)

        # 模拟回复
        self.root.after(1000, self.simulate_reply)

    def simulate_reply(self):
        if not self.current_contact:
            return

        # 获取当前时间
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M")

        # 模拟回复消息
        replies = [
            "好的，我明白了",
            "很有趣的想法",
            "我需要考虑一下",
            "明天再聊吧",
            "谢谢你的消息"
        ]

        # 随机发送上面replies的内容
        import random
        reply = random.choice(replies)
        formatted_reply = f"[{time_str}] {self.current_contact}: {reply}\n"

        # 添加到聊天记录
        self.chat_history[self.current_contact].append(formatted_reply)

        # 更新聊天区域
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, formatted_reply)
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

        # 创建名为chatHistory.json的文件，用于存储聊天记录
        # with open('chatHistory.json','w') as f:
        with open(f"{self.username}_chatHistory.json", 'w') as f:
            json.dump(self.chat_history,f,indent=4)

    # 点击加号，添加新的联系人
    def addContacts(self,event=None):
        # 若该联系人已是好友，则提示他已经是你的好友了，请你们开始聊天吧
        # if newContact in self.contacts:
        #     self.show_message('他已经是你的好友了，请你们开始聊天吧')
        # # 新联系人不能是自己
        # if newContact==self.username:
        #     self.show_message('新的联系人不可以是本人')
        # # 直接添加？
        # self.contacts.append(newContact)

        # 设置联系人框的样式
        btn = tk.Label(self.contacts_frame)
        btn['text'] = 'chat'+str(len(self.contact_buttons)+1)
        btn['bg'] = 'white'
        btn['fg'] = 'black'
        btn['anchor'] = 'w'
        btn.place(x=10, y=50 + len(self.contact_buttons) * 50, width=180, height=40)
        # 将选中联系人的函数self.select_contact()和联系人按钮绑定在一起
        btn.bind('<Button-1>', lambda e, c='chat'+str(len(self.contact_buttons)+1): self.select_contact(c))
        self.contact_buttons.append(btn)
        # 用同一ID，保证每次登录时，上一次登录的记录还在，比如聊天记录和聊天对象
        self.chat_history[btn['text']]=[ ]
        with open(f'{self.username}_chatHistory.json','w') as f:
            json.dump(self.chat_history,f,indent=4)
        # 需要改进的地方，在这里设定是没有好友添加的功能，只有点击了new Chat按钮即可与新联系人开启新聊天窗口的模式，后续会补上添加好友时审核的步骤



if __name__ == "__main__":
    root = tk.Tk()
    # app = ChatApp(root)
    loginApp=LoginApp(root)
    root.mainloop()


# 250830
# 将chatApp的数据细化
# userInfo.json--记录id和密码
# chatHistory.json--存储聊天记录
# {username}_friends.json--分开不同username的联系人
# {username}_chatHistory.json--区分不同username的聊天记录


# 250906
# 用新用户的id和密码成功登录后，加上添加好友的按钮，
# 写好portfolio，上传github
# C语言--HW，embeded(robot) programming
# C++/C#--游戏开发
# JAVA--web开发，安卓开发
# Python--数据分析，人工智能开发，部分robot

# Object-C，Swift--Mac Apple only

