# _*_ coding : utf-8 _*_
# @Time : 2025/10/20 17:38
# @Author : 田园
# @File : test PyQt
# @Project : test.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

# 实例化
app=QApplication(sys.argv)
# 主窗口
window=QMainWindow()
window.setWindowTitle('My First PyQt Application')
# setGeometry(x,y,width,height)
window.setGeometry(100,100,400,300)

window.show() #显示窗口

# 进入主事件循环
sys.exit(app.exec())