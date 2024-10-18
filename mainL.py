import sqlite3
import hashlib
import os
import uuid
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QMenuBar, QMenu, QAction, QDialog, QLabel
from Ui_main import Ui_MainWindow
import sys
import pandas as pd
from ctrl.menu_slot import change_page, save_project, load_project
from ctrl.Jieliu_slot import on_compute_button_clicked, compute_pctiz
from ctrl.result_slot import init_result, show_moulde3_image, show_moulde1_image
from ctrl.compute_slot import module3_compute, add_a, delete_a
from PyQt5.QtWidgets import QPushButton, QTextEdit, QVBoxLayout, QDesktopWidget, QWidget
from Gui.NewProject import Ui_Newproject_Dialog
from ctrl.mappint_slot import add_label, rotate_label, change_label_size, add_image_label, delete_lable, label_dict, init_background
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSlot, QSettings, QDateTime, QThread, pyqtSignal
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMessageBox
from Gui.Ui_login import Ui_Login_Form
from data import result_form
from utils.image_utils import png_to_base64
import sys



class myWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        _self = self
        self.setupUi(self)
        # self.resize(800,600)
        # 设置窗口为无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 最大化及最小化
        font = QFont()
        font.setPointSize(15)
        font.setFamily('Webdings')
        self.buttonMinimum.setFont(font)
        self.buttonMaximum.setFont(font)
        self.buttonClose.setFont(font)
        self.buttonMinimum.clicked.connect(self.minimize_window)
        self.buttonMaximum.clicked.connect(self.maximize_window)
        self.buttonClose.clicked.connect(self.close)
        # 记录鼠标按下时的位置
        self.mouse_press_pos = None
        self.mouse_press_time = None
        self.message = message(self)
        self.pushButton.clicked.connect(lambda: on_compute_button_clicked(self))
        # 创建菜单栏
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setStyleSheet('''color:rgb(255,255,255);''')
        self.hL_menuBar.addWidget(self.menu_bar)
        self.hL_menuBar.addStretch(1)  # 添加一个水平弹簧，推挤前面的部件到左边
        # 创建一个菜单
        self.file_menu = QMenu('&工程管理', self)
        self.file_menu.setStyleSheet("""  
            QMenu {  
                background-color: rgb(100,100,100); /* 设置菜单背景颜色 */  
                border: 1px solid #d0d0d0; /* 设置菜单边框 */  
                margin: 2px; /* 设置菜单外边距 */  
                padding: 5px; /* 设置菜单内边距 */ 
                color:rgb(255,255,255); 
            }  

            QMenu::item {  
                height: 30px; /* 设置菜单项的高度 */  
                color: #333333; /* 设置菜单项文字颜色 */  
                background-color: transparent; /* 设置菜单项背景颜色（透明） */  
                padding-left: 20px; /* 设置菜单项左内边距 */  
                margin: 2px 0px; /* 设置菜单项上下外边距 */  
                color:rgb(255,255,255);
            }  

            QMenu::item:selected {  
                background-color: #d0d0d0; /* 设置选中菜单项的背景颜色 */  
                color: #000000; /* 设置选中菜单项的文字颜色 */  
            }  

            QMenu::separator {  
                height: 1px; /* 设置分隔线的高度 */  
                background-color: #c0c0c0; /* 设置分隔线的颜色 */  
                margin: 5px 0px; /* 设置分隔线的上下外边距 */  
            }  
        """)
        # self.edit_menu = QMenu('编辑', self)
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addAction("&节流模块及极限处理产量").triggered.connect(lambda: change_page(self, 1, label_dict))
        self.menu_bar.addAction("&管道绘图").triggered.connect(lambda: change_page(self, 2, label_dict))
        self.menu_bar.addAction("&安全校核模块").triggered.connect(lambda: change_page(self, 3, label_dict))
        self.menu_bar.addAction("&报表展示").triggered.connect(self.show_result)
        self.menu_bar.addAction("&退出").triggered.connect(self.close)
        # self.menu_bar.addMenu(self.edit_menu)
        # 创建菜单项
        self.action_3 = QAction('新建工程', self)
        self.action_4 = QAction('打开工程', self)
        self.action_5 = QAction('保存工程', self)
        # self.actionj = QAction('节流模块及极限处理产量', self)
        # self.actionp = QAction('管道绘图', self)
        # self.actiona = QAction('安全校核模块', self)
        # self.actions = QAction('报表展示', self)
        # self.action_6 = QAction('退出', self)

        # 将菜单项添加到菜单中
        self.file_menu.addAction(self.action_3)
        self.file_menu.addAction(self.action_4)
        self.file_menu.addAction(self.action_5)
        # self.file_menu.addSeparator()
        # self.file_menu.addAction(self.actionj)
        # self.file_menu.addAction(self.actionp)
        # self.file_menu.addAction(self.actiona)
        # self.file_menu.addSeparator()
        # self.file_menu.addAction(self.actions)
        # self.file_menu.addAction(self.action_6)

        self.action_3.triggered.connect(lambda: newProject(_self))
        self.action_4.triggered.connect(lambda: load_project(_self, label_dict))
        self.action_5.triggered.connect(lambda: save_project(_self))
        # 为菜单项绑定事件
        # self.action_6.triggered.connect(self.close)
        #
        # self.actionj.triggered.connect(lambda :self.stackedWidget.setCurrentIndex(1))
        # self.actionp.triggered.connect(lambda :self.stackedWidget.setCurrentIndex(2))
        # self.actiona.triggered.connect(lambda :self.stackedWidget.setCurrentIndex(3))

        # self.actionj.triggered.connect(lambda: change_page(self, 1, label_dict))
        # self.actionp.triggered.connect(lambda: change_page(self, 2, label_dict))
        # self.actiona.triggered.connect(lambda: change_page(self, 3, label_dict))

        self.pushButton_3.clicked.connect(lambda: module3_compute(self))
        self.pushButton_add.clicked.connect(lambda: add_a(self))
        self.pushButton_delete.clicked.connect(lambda: delete_a(self))
        #管道绘图界面
        self.addpipe2.clicked.connect(lambda: add_label(self, "#bc2f19", 5, 300))
        # self.addpipe2.clicked.connect(lambda: add_image_label(self, "resource/guanxian.png", "guanxian"))
        self.addpipe1_3.clicked.connect(lambda: add_image_label(self, "./resource/falan.png", "falan"))
        self.addpipe1_4.clicked.connect(lambda: add_image_label(self, "./resource/wantou.png", "wantou"))
        self.addpipe1_5.clicked.connect(lambda: add_image_label(self, "./resource/gudingdian.png", "gudingdian"))
        self.addpipe1_6.clicked.connect(lambda: add_image_label(self, "./resource/jingkou.png", "jingkou"))
        self.pushButton_2.clicked.connect(self.saveimage)
        self.pushButton_5.clicked.connect(lambda: rotate_label())  # 旋转管道和添加控件导致布局重置
        self.pushButton_4.clicked.connect(lambda: change_label_size())
        self.dele_lable_pushButton.clicked.connect(lambda: delete_lable())

        self.pushButton_6.clicked.connect(lambda: show_moulde1_image(self))
        self.pushButton_7.clicked.connect(lambda: show_moulde3_image(self))

        self.pushButton_8.clicked.connect(lambda: compute_pctiz(self))

        self.pushButton_9.clicked.connect(lambda: show_moulde1_image(self))
        # self.actions.triggered.connect(self.show_result)
        init_background(self)
        self.setHeight()
        self.graphicsView.viewport().installEventFilter(self)


    def box(self, title,  text):
        msg = QMessageBox()
        msg.setWindowModality(Qt.NonModal)
        msg.information(self, title, text, QMessageBox.Ok)
        msg.show()





    def setHeight(self, height=38):
        # 设置右边按钮的大小
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def mousePressEvent(self, event: QMouseEvent):
        # 检查鼠标点击是否在self.widget上
        if event.button() == Qt.LeftButton and self.widget.geometry().contains(
                self.widget.mapFromGlobal(event.globalPos())):
            self.mouse_press_pos = event.globalPos()
            self.mouse_press_time = event.timestamp()

    def mouseMoveEvent(self, event: QMouseEvent):
        # 检查鼠标移动时是否在self.widget上按下
        if event.buttons() == Qt.LeftButton and self.mouse_press_pos and self.widget.geometry().contains(
                self.widget.mapFromGlobal(self.mouse_press_pos)):
            if (event.globalPos() - self.mouse_press_pos).manhattanLength() > QApplication.startDragDistance():
                new_pos = self.pos() + (event.globalPos() - self.mouse_press_pos)
                self.move(new_pos)
                self.mouse_press_pos = event.globalPos()
                event.accept()
    def mouseReleaseEvent(self, event: QMouseEvent):
        # 检查鼠标释放时是否在self.widget上按下
        if event.button() == Qt.LeftButton and self.mouse_press_pos and self.widget.geometry().contains(
                self.widget.mapFromGlobal(self.mouse_press_pos)):
            self.mouse_press_pos = None
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # 双击时切换窗口显示状态
        if event.button() == Qt.LeftButton:
            if self.isMaximized():
                self.showNormal()
                self.resize(1700, 1000)
                self.center()
            else:
                self.showMaximized()

    def minimize_window(self):
        self.showMinimized()

    def maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.resize(1700, 1000)
            self.center()
            self.buttonMaximum.setText('1')
        else:
            self.showMaximized()
            self.buttonMaximum.setText('2')

    def paintEvent(self, event):
        # 这里可以绘制窗口的背景，但由于我们设置了透明背景，所以不需要绘制
        pass

    def center(self):  #窗口居中显示
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop))

    def saveimage(self):
        self = self.frame_Mapping
        # print(self.winId())
        # print(self.frame_Mapping.winId())
        pixmap = QApplication.primaryScreen().grabWindow(self.winId())
        pixmap.save('mapping.png', 'png')
        result_form.image_base64 = png_to_base64('mapping.png')
        QMessageBox.information(self, "提示", "保存成功")

    def show_result(self):
        init_result(self)
        change_page(self, 0, label_dict)

    def eventFilter(self, source, event):
        if (source == self.graphicsView.viewport() and
                event.type() == QtCore.QEvent.Wheel and event.modifiers() == QtCore.Qt.ControlModifier):
            if event.angleDelta().y() > 0:
                scale = 1.25
            else:
                scale = .8
            self.graphicsView.scale(scale, scale)
            # do not propagate the event to the scroll area scrollbars
            return True

        return super().eventFilter(source, event)

class check_mac_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('设备地址校验')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/resource/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setGeometry(300, 300, 500, 360)
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.setGeometry(x, y, window.width(), window.height())

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.btn_check = QPushButton('开始校验', self)
        self.btn_login = QPushButton('登录使用', self)
        self.btn_check.clicked.connect(self.check_and_write_mac)
        self.btn_login.clicked.connect(self.start_login)
        layout.addWidget(self.btn_check)
        layout.addWidget(self.btn_login)
        self.btn_login.setEnabled(False)

        self.setLayout(layout)

    def check_and_write_mac(self):
        #没有txt文件
        if os.path.exists('./mac_pw/mac.txt') == False:
            info_box = QMessageBox(QMessageBox.Warning, "警告", "软件丢失校验模块,文件已损坏,请联系开发者获取完整版安装文件")
            info_box.exec_()
        #有txt文件
        elif os.path.exists('./mac_pw/mac.txt')  == True:
            with open('./mac_pw/mac.txt', 'r') as f:
                content = f.read()
                #有txt文件但为空
                if not content:
                    self.text_edit.append('本机第一次使用软件，正在创建设备校验文件...')
                    self.text_edit.append('请稍候...')
                    self.text_edit.append('正在获取校验信息...')
                    # 获取当前电脑的MAC地址
                    mac_1 = uuid.UUID(int=uuid.getnode()).hex[-12:]
                    #哈希并写入校验文件
                    self.hash_address(mac_1)
                    self.text_edit.append('已将校验信息写入数据库')
                    self.text_edit.append('软件仅限于在此机器运行，请勿转移至其它机器')
                # 有txt文件不为空
                else:
                    mac_2 = uuid.UUID(int=uuid.getnode()).hex[-12:]

                    sha256 = hashlib.sha256()
                    sha256.update(mac_2.encode('utf-8'))
                    mac_2 = sha256.hexdigest()

                    if content == mac_2:
                        self.text_edit.append('校验通过,欢迎使用本系统')
                        self.btn_login.setEnabled(True)
                        self.btn_check.setEnabled(False)
                    else:
                        self.text_edit.append('校验不通过,请与开发者联系')

    def hash_address(self,value):
        # 使用SHA256哈希算法对地址进行哈希
        sha256 = hashlib.sha256()
        sha256.update(value.encode('utf-8'))
        sha256 = sha256.hexdigest()
        # 将哈希后的MAC地址保存到txt文件
        with open('./mac_pw/mac.txt', 'w') as f:
            f.write(sha256)

    def start_login(self):
        self.close()
        LoginWindow.showMaximized()

class loginWindow(QtWidgets.QWidget,Ui_Login_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.make_ui()
        self.Login_btn.setEnabled(False)
        #按钮信号与槽
        self.btn_close.clicked.connect(self.close_win)  #关闭
        self.btn_clear.clicked.connect(self.clear_database)  # 假设btn_clear是你的按钮对象
        # 确保数据库连接已经初始化，或者在需要时重新连接
        self.conn = None
        # 读取配置文件中的登录信息
        self.settings = QSettings("./mac_pw/settings.ini", QSettings.IniFormat)
        self.lineEdit_account.setText(self.settings.value("username", ""))
        self.lineEdit_pwd.setText(self.settings.value("password", ""))
        self.auto_login_checkBox.setChecked(self.settings.value("remember", False, type=bool))
        self.remember_pwd_checkBox.setChecked(self.settings.value("autologin", False, type=bool))
        #
        self.lineEdit_account.textChanged.connect(self.enable_login_btn)
        self.lineEdit_pwd.textChanged.connect(self.enable_login_btn)
        self.enable_login_btn()

    def enable_login_btn(self):
        account = self.lineEdit_account.text()
        password = self.lineEdit_pwd.text()
        if len(account)>0 and len(password)>0:
            self.Login_btn.setEnabled(True)
        else:
            self.Login_btn.setEnabled(False)

    @pyqtSlot(bool)
    def auto_login(self,checked):
        if checked:
            self.remember_pwd_checkBox.setChecked(True)

    def remember_pwd(self,checked):
        if not checked:
            self.auto_login_checkBox.setChecked(False)

    @pyqtSlot()
    def on_Login_btn_clicked(self):
        self.account = self.lineEdit_account.text()
        remeber_account = self.lineEdit_account.text()
        self.password = self.lineEdit_pwd.text()
        remeber_pwd = self.lineEdit_pwd.text()

        # 使用SHA256哈希算法对地址进行哈希
        hash_acount = hashlib.sha256()
        hash_acount.update(self.account.encode('utf-8'))
        self.account = hash_acount.hexdigest()

        hash_password = hashlib.sha256()
        hash_password.update(self.password.encode('utf-8'))
        self.password = hash_password.hexdigest()

        # 保存登录信息到配置文件
        if self.remember_pwd_checkBox.isChecked():
            self.settings = QSettings("./mac_pw/settings.ini", QSettings.IniFormat)
            self.settings.setValue("username", remeber_account)
            self.settings.setValue("password", remeber_pwd)
            self.settings.setValue("remember", self.remember_pwd_checkBox.isChecked())
            self.settings.setValue("autologin", self.auto_login_checkBox.isChecked())
        else:
            self.settings = QSettings("./mac_pw/settings.ini", QSettings.IniFormat)
            self.settings.setValue("username", "")
            self.settings.setValue("password", "")
            self.settings.setValue("remember", False)
            self.settings.setValue("autologin", False)
        # 连接数据库
        conn = sqlite3.connect("./mac_pw/acount_time.db")  # 替换为实际的数据库文件路径
        cursor = conn.cursor()
        # 查询数据库中是否存在与输入的用户名和密码匹配的记录
        cursor.execute("SELECT * FROM acount WHERE UserName = ? AND PassWord = ?", (self.account, self.password))
        result = cursor.fetchone()

        if result:
            self.close()
            mainWindow.showMaximized()
            print('登录成功')
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "账号或密码错误")
            msg_box.exec_()


    def make_ui(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        # self.shadow.setOffset(2, 5)
        self.shadow.setBlurRadius(90)
        # self.shadow.setColor(QtCore.Qt.gray)
        self.frame_2.setGraphicsEffect(self.shadow)
        self.frame_3.setGraphicsEffect(self.shadow)
        # 给 QFrame 设置阴影效果
        shadow_effect = QGraphicsDropShadowEffect(self.frame_3)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(0)
        shadow_effect.setColor(Qt.black)

    def close_win(self):
        self.close()

    def connect_database(self):
        # 这里是连接数据库的代码，你可能已经在某个地方实现了它
        # 假设这是连接数据库的函数
        subdir = './mac_pw/'
        filename = 'acount_time.db'
        filepath = os.path.join(os.getcwd(), subdir, filename)
        if os.path.isfile(filepath):
            self.conn = sqlite3.connect(filepath)
            self.cursor = self.conn.cursor()
            print("数据库连接成功")
        else:
            print("数据库文件不存在")

    def clear_database(self):
        # 首先检查数据库是否已连接
        if not self.conn:
            self.connect_database()

        if self.conn:
            # 弹出警告对话框
            reply = QMessageBox.question(self, '警告',
                                         "确认要清除所有用户账号及密码数据吗？",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                # 执行SQL语句清除表acount的所有数据
                try:
                    self.cursor.execute("DELETE FROM acount")
                    self.conn.commit()
                    print("数据清除成功")
                except sqlite3.Error as e:
                    print(f"清除数据失败: {e}")
            else:
                # 用户点击了否，不执行任何操作
                pass
        else:
            # 数据库连接失败时的处理（可选）
            print("数据库未连接，无法清除数据")


class NewProject_Dialog(QDialog, Ui_Newproject_Dialog):
    _self = None
    def __init__(self):
        super(NewProject_Dialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("新建工程")
        self.setWindowModality(Qt.ApplicationModal)
        self.pushButton.clicked.connect(lambda: self.save_project_inform())
        self.pushButton_2.clicked.connect(lambda: self.close())

    def set_parent(self,_self):
        self._self = _self
    def save_project_inform(self):
        try:
            project_inform = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(),
                              self.lineEdit_4.text()]
            flag = 1
            for i in project_inform:
                if i == '':
                    QMessageBox.information(self, "提示", "请输入完整信息")
                    flag = 0
                    break
        except Exception :
            print("请输入正确信息")
            QMessageBox.information(self, "提示", "请输入正确工程信息")
        if flag == 1:
            result_form.Project_inform = project_inform
            self.close()
            change_page(self._self, 1, label_dict)


def newProject(self):
    result_form.clearData(self)
    dialog = NewProject_Dialog()
    # dialog.setWindowOpacity(0.85)
    dialog.set_parent(self)
    dialog.exec_()


class message(QThread):
    signal = pyqtSignal()
    def __init__(self, Window):
        super(message, self).__init__()
        self.window = Window

    def run(self):
        self.signal.emit()






if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    MAC = check_mac_window()
    LoginWindow = loginWindow()
    mainWindow = myWindow()
    #允用时间检查
    sql_str = "select DateTime from time1 limit 1 offset 0"
    connect = sqlite3.connect("./mac_pw/acount_time.db")
    deadline = connect.execute(sql_str)
    deadline = pd.DataFrame(deadline)
    deadline = deadline.iloc[0, 0]
    deadline = QDateTime.fromString(deadline, "yyyy-MM-dd hh:mm:ss")
    currentDateTime = QDateTime.currentDateTime()
    def time_check():
        if currentDateTime <= deadline:
            print("允许登陆时间范围内")
            MAC.show()
        else:
            QMessageBox.warning(None, '警告', '软件已超过有效使用期限，请与开发者联系！')
    time_check()
    sys.exit(app.exec_())