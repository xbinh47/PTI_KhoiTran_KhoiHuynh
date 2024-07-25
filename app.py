from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication,QMessageBox,QLineEdit,QPushButton,QMessageBox
from PyQt6 import uic
import sys

class MessageBox():
    def success_box(self,message):
        box = QMessageBox()
        box.setWindowTitle("Success")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()
    
    def error_box(self,message):
        box = QMessageBox
        box.windowTitle("Error")
        box.setText(message)
        box.setIcon(MessageBox.Icon.Critical)
        box.exec()    
class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui",self)
        self.email = self.findChild(QLineEdit, "txtemail")
        self.password = self.findChild(QLineEdit, "txtpassword")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)

    def login(self):
        msg = MessageBox()
        email = self.email.text()
        password = self.password.text()
        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return
        if password == "":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        if email == "admin" and password == "123456":
            self.msg.success_box("Đăng nhập thành công")
        else:
            self.msg.error_box("Sai email hoặc mật khẩu")

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()

class Register(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("register.ui",self)
        self.fullname = self.findChild(QLineEdit, "txt_fullname")
        self.confirm_password = self.findChild(QLineEdit, "txt_conf_pwd")
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_login.clicked.connect(self.register)
        self.btn_register.clicked.connect(self.show_login)

    def register(self):
        msg = MessageBox()
        fullname = self.fullname.text()
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()
        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return
        if password == "":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        if confirm_password == "":
            msg.error_box("Xác nhận mật khẩu không được để trống")
            self.password.setFocus()
            return
        if confirm_password != password:
            msg.error_box("Mật khẩu không trùng khớp")
            self.confirm_password.setText("")
            self.password.setFocus()
            return
        msg.success_box("Đăng ký thành công")


    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()
