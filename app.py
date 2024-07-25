from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMessageBox, QLineEdit, QPushButton, QMainWindow, QDateEdit, QCheckBox, QLabel, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
import sys
import json
import os

class MessageBox:
    def success_box(self, message):
        box = QMessageBox()
        box.setWindowTitle("Success")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()
    
    def error_box(self, message):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.exec()

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
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

        try:
            with open('data/user.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            msg.error_box("Không tìm thấy dữ liệu người dùng")
            return

        user_found = False
        for user in users:
            if user['email'] == email and user['password'] == password:
                user_found = True
                break

        if user_found:
            msg.success_box("Đăng nhập thành công")
        else:
            msg.error_box("Sai email hoặc mật khẩu")

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()

class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)
        self.fullname = self.findChild(QLineEdit, "txt_fullname")
        self.confirm_password = self.findChild(QLineEdit, "txt_conf_pwd")
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_login.clicked.connect(self.show_login)
        self.btn_register.clicked.connect(self.register)

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

        new_user = {
            "fullname": fullname,
            "email": email,
            "password": password,
            "phone": "",
            "address": "",
            "dob": "",
            "gender": "",
            "avatar": ""
        }

        try:
            if os.path.exists('data/user.json'):
                with open('data/user.json', 'r') as file:
                    users = json.load(file)
            else:
                users = []

            if any(user['email'] == email for user in users):
                msg.error_box("Email đã tồn tại")
                return

            users.append(new_user)
            with open('data/user.json', 'w') as file:
                json.dump(users, file, indent=4)

            msg.success_box("Đăng ký thành công")
            self.show_login()

        except Exception as e:
            msg.error_box(f"Lỗi khi đăng ký: {str(e)}")

    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()

class Information(QMainWindow):
    def __init__(self, email):
        super().__init__()
        uic.loadUi("ui/information.ui", self)
        self.emailUser = email
        self.file = None
        msg = MessageBox()
        try:
            with open('data/user.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            msg.error_box("Không tìm thấy dữ liệu người dùng")
            return
        
        self.user = next((user for user in users if user['email'] == self.emailUser), None)
        
        self.email = self.findChild(QLineEdit, "txt_email")
        self.fullname = self.findChild(QLineEdit, "txt_fullname")
        self.phone = self.findChild(QLineEdit, "txt_phone")
        self.address = self.findChild(QLineEdit, "txt_address")
        self.birthday = self.findChild(QDateEdit, "txt_birthday")
        self.maleCheckBox = self.findChild(QCheckBox, "male_gender")
        self.femaleCheckBox = self.findChild(QCheckBox, "female_gender")
        self.btnUpload = self.findChild(QPushButton, "btn_upload")
        self.avatar = self.findChild(QLabel, "avatar")
        self.btnUpload.clicked.connect(self.uploadAvatar)
        self.btn_apply = self.findChild(QPushButton, "btn_apply")
        self.btn_apply.clicked.connect(self.saveInfo)
        
        self.loadInfo()
        
    def loadInfo(self):
        self.fullname.setText(self.user['fullname'])
        self.email.setText(self.user['email'])
        self.phone.setText(self.user['phone'])
        self.address.setText(self.user['address'])
        self.birthday.setDate(QtCore.QDate.fromString(self.user['dob'], "yyyy-MM-dd"))
        if self.user['gender'] == 'Male':
            self.maleCheckBox.setChecked(True)
        if self.user['gender'] == 'Female':
            self.femaleCheckBox.setChecked(True)
        
    def saveInfo(self):
        self.user['fullname'] = self.fullname.text()
        self.user['email'] = self.email.text()
        self.user['phone'] = self.phone.text()
        self.user['address'] = self.address.text()
        self.user['dob'] = self.birthday.text()
        if self.maleCheckBox.isChecked():
            self.user['gender'] = 'Male'
        if self.femaleCheckBox.isChecked():
            self.user['gender'] = 'Female'
        if self.file:
            self.user['avatar'] = self.file
            
        try:
            with open('data/user.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            msg.error_box("Không tìm thấy dữ liệu người dùng")
            return
        
        for i, user in enumerate(users):
            if user['email'] == self.emailUser:
                users[i] = self.user
                break
            
        with open('data/user.json', 'w') as file:
            json.dump(users, file, indent=4)
        msg = MessageBox()
        msg.success_box("Lưu thông tin thành công")
        
    def uploadAvatar(self):
        # local
        file, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *jpeg *.bmp)")
        if file:
            self.user['avatar'] = file
            self.avatar.setPixmap(QPixmap(file))
            msg = MessageBox()
            msg.success_box("Tải ảnh đại diện thành công")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()
