
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit,
    QPushButton, QWidget, QVBoxLayout, QHBoxLayout,
    QStatusBar, QMenu, QAction, QToolBar,
    QMessageBox  # 新增：用于登录失败弹窗提示
)
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QFont, QPalette, QBrush, QPixmap  # 整合导入，避免重复

# ===================== SQLite 数据库工具类 =====================
import sys
import os
from typing import Optional
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtWidgets import QMessageBox

class DBService:
    def __init__(self):
        """初始化QSqlDatabase连接（SQLite）"""
        # 初始化数据库连接（指定驱动为SQLite）
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        # 数据库文件路径（绝对路径）
        db_path = "C:/Users/25215/Desktop/sqlite/stugms.db"
        self.db.setDatabaseName(db_path)

        # 打开数据库（失败则退出）
        if not self.db.open():
            QMessageBox.critical(None, "数据库错误", self.db.lastError().text())
            sys.exit(1)

    def query(self, sql: str, *args) -> list:
        """
        执行查询SQL（QSqlQuery方式）
        :param sql: SQL语句（参数用?占位）
        :param args: 绑定的参数
        :return: 查询结果（二维列表）
        """
        query = QSqlQuery()
        query.prepare(sql)
        # 绑定参数
        for arg in args:
            query.addBindValue(arg)
        # 执行查询
        if not query.exec_():
            QMessageBox.critical(None, "查询错误", query.lastError().text())
            return []
        # 解析结果为二维列表
        result = []
        col_count = query.record().count()
        while query.next():
            row = []
            for i in range(col_count):
                row.append(query.value(i))
            result.append(row)
        return result

    def add(self, sql: str, params: tuple = ()) -> Optional[int]:
        """
        执行添加SQL（返回自增ID）
        :param sql: INSERT语句（参数用?占位）
        :param params: 绑定的参数元组
        :return: 新增记录的自增ID（失败返回None）
        """
        query = QSqlQuery()
        query.prepare(sql)
        # 绑定参数
        for param in params:
            query.addBindValue(param)
        # 执行添加
        if not query.exec_():
            QMessageBox.critical(None, "添加错误", query.lastError().text())
            return None
        # 获取自增ID（SQLite的lastInsertId）
        last_id = query.lastInsertId()
        return last_id if last_id is not None else None

    def update(self, sql: str, params: tuple = ()) -> bool:
        """执行更新SQL"""
        query = QSqlQuery()
        query.prepare(sql)
        for param in params:
            query.addBindValue(param)
        if not query.exec_():
            QMessageBox.critical(None, "更新错误", query.lastError().text())
            return False
        return True

    def delete(self, sql: str, params: tuple = ()) -> bool:
        """执行删除SQL"""
        query = QSqlQuery()
        query.prepare(sql)
        for param in params:
            query.addBindValue(param)
        if not query.exec_():
            QMessageBox.critical(None, "删除错误", query.lastError().text())
            return False
        return True

# 实例化数据库服务（全局可用）
service = DBService()


# ===================== 1. 登录窗体类 =====================
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 窗口基础设置
        self.setWindowTitle("学生管理系统-登录")
        self.setFixedSize(600, 400)

        # 1. 设置背景图（可选，无图片则注释）
        self.set_background()

        # 2. 添加标题 + 登录控件
        self.add_title()  # 新增：添加标题
        self.add_login_widgets()

    def set_background(self):
        """设置背景图"""
        # 注意：os.path.join已自动拼接路径，无需手动写全路径（避免重复）
        bg_path = os.path.join(os.path.dirname(__file__), "C:/Users/25215/PycharmProjects/practice/StudentGMS/img/back1.jpg")
        if os.path.exists(bg_path):
            palette = QPalette()
            pixmap = QPixmap(bg_path).scaled(
                self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )
            palette.setBrush(QPalette.Background, QBrush(pixmap))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        else:
            print(f"警告：背景图不存在 → {bg_path}")  # 调试提示

    def add_title(self):
        """新增：添加「学生管理系统」标题"""
        title_label = QLabel("学生成绩管理系统", self)
        # 设置标题位置（居中，顶部）
        title_label.move(0, 30)  # y轴30像素，距离顶部有间距
        title_label.setFixedWidth(600)  # 宽度与窗口一致，实现居中
        # 设置标题样式（字体、大小、颜色）
        title_label.setAlignment(Qt.AlignCenter)  # 文字居中
        title_font = QFont()
        title_font.setFamily("楷体")  # 字体
        title_font.setPointSize(12)  # 原12号字体太小，改为24更醒目
        title_font.setBold(True)  # 加粗
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: black;")  # 标题颜色

    def add_login_widgets(self):
        """添加用户名、密码、按钮（调整控件y轴位置，避开标题）"""
        # 用户名（y轴从120→100，留出标题空间）
        lbl_user = QLabel("用户名：", self)
        lbl_user.move(150, 100)
        lbl_user.setStyleSheet("color: black; font-size: 20px;")
        self.edit_user = QLineEdit(self)
        self.edit_user.move(220, 100)
        self.edit_user.resize(200, 30)

        # 密码（y轴从180→160）
        lbl_pwd = QLabel("密  码：", self)
        lbl_pwd.move(150, 160)
        lbl_pwd.setStyleSheet("color: black; font-size: 20px;")
        self.edit_pwd = QLineEdit(self)
        self.edit_pwd.move(220, 160)
        self.edit_pwd.resize(200, 30)
        self.edit_pwd.setEchoMode(QLineEdit.Password) #密码不显示明文

        # 登录按钮（y轴从250→230）
        btn_login = QPushButton("登录", self)
        btn_login.move(220, 230)
        btn_login.resize(100, 40)
        btn_login.clicked.connect(self.check_login)

        # 退出按钮（y轴从250→230）
        btn_quit = QPushButton("退出", self)
        btn_quit.move(330, 230)
        btn_quit.resize(100, 40)
        btn_quit.clicked.connect(self.close)

    def check_login(self):
            """登录验证：连接SQLite数据库验证用户名密码"""
            # 获取输入的用户名和密码
            user_name = self.edit_user.text().strip()
            user_pwd = self.edit_pwd.text().strip()

            # 1. 非空校验
            if not user_name or not user_pwd:
                QMessageBox.warning(None, '警告', '用户名或密码不能为空！', QMessageBox.Ok)
                return

            # 2. 执行SQLite查询（注意：SQLite用?作为参数占位符，不是%s）
            sql = 'select * from tb_user where userName = ? and userPwd = ?'
            print(sql, user_name, user_pwd)

            # 调用数据库查询方法
            result = service.query(sql, user_name, user_pwd)
            print(result)

            # 3. 验证结果
            if len(result) > 0:
                # 登录成功：打开主窗体，关闭登录窗体
                print("✅ 登录成功！")
                self.main_window = MainWindow(username=user_name)  # 传入登录用户名
                self.main_window.show()
                self.close()  # 关闭登录窗体
            else:
                # 登录失败：清空输入框，提示错误
                QMessageBox.warning(None, '警告', '用户名或密码错误！', QMessageBox.Ok)
                self.edit_user.setText('')
                self.edit_pwd.setText('')


# ===================== 2. 主窗体类 =====================
class MainWindow(QMainWindow):
    refresh_signal = Signal()

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()
        self.set_background()

    def init_ui(self):
        """初始化主窗体"""
        self.setWindowTitle("学生管理系统 - 主界面")
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        # 创建菜单栏/工具栏/中心区/状态栏
        self.create_menu_bar()
        self.create_central_widget()
        self.create_status_bar()

    def set_background(self):
        """设置背景图"""
        # 注意：os.path.join已自动拼接路径，无需手动写全路径（避免重复）
        bg_path = os.path.join(os.path.dirname(__file__), "C:/Users/25215/PycharmProjects/practice/StudentGMS/img/back1.jpg")
        if os.path.exists(bg_path):
            palette = QPalette()
            pixmap = QPixmap(bg_path).scaled(
                self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )
            palette.setBrush(QPalette.Background, QBrush(pixmap))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        else:
            print(f"警告：背景图不存在 → {bg_path}")  # 调试提示



    def create_menu_bar(self):
        """菜单栏：完善层级结构 + 修复语法错误 + 绑定操作方法"""
        menu_bar = self.menuBar()

        # ===================== 1. 基础设置菜单（文件菜单重构）=====================
        file_menu = QMenu("基础设置(&F)", self)
        # 基础设置子菜单 - 各类配置
        grade_action = QAction("年级设置", self)
         # 绑定年级设置方法
        grade_action.triggered.connect(lambda: self.openSet(grade_action))

        class_action = QAction("班级设置", self)
        class_action.triggered.connect(lambda: self.openSet(class_action))

        exam_kind_action = QAction("考试类别设置", self)
        exam_kind_action.triggered.connect(lambda: self.openSet(exam_kind_action))

        subject_action = QAction("考试科目设置", self)
        subject_action.triggered.connect(lambda: self.openSet(subject_action))

        # 退出操作（放到基础设置菜单最后）
        exit_action = QAction("退出(&E)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        # 向基础设置菜单添加子项
        file_menu.addAction(grade_action)
        file_menu.addAction(class_action)
        file_menu.addAction(exam_kind_action)
        file_menu.addAction(subject_action)
        file_menu.addSeparator()  # 添加分隔线
        file_menu.addAction(exit_action)
        menu_bar.addMenu(file_menu)

        # ===================== 2. 基本信息设置菜单 =====================
        info_menu = QMenu("基本信息管理(&I)", self)
        # 学生信息管理
        stu_info_action = QAction("学生信息管理", self)
        stu_info_action.triggered.connect(lambda: self.openSet(stu_info_action))

        # 学生成绩管理
        score_info_action = QAction("学生成绩管理", self)
        score_info_action.triggered.connect(lambda: self.openSet(score_info_action))
        # 添加子项
        info_menu.addAction(stu_info_action)
        info_menu.addAction(score_info_action)
        menu_bar.addMenu(info_menu)

        # ===================== 3. 系统查询菜单 =====================
        query_menu = QMenu("系统查询(&Q)", self)
        # 学生信息查询
        stu_query_action = QAction("学生信息查询", self)
        stu_query_action.triggered.connect(lambda: self.openSet(stu_query_action))
        # 学生成绩查询
        score_query_action = QAction("学生成绩查询", self)
        score_query_action.triggered.connect(lambda: self.openSet(score_query_action))
        # 添加子项
        query_menu.addAction(stu_query_action)
        query_menu.addAction(score_query_action)
        menu_bar.addMenu(query_menu)

        # ===================== 4. 系统管理菜单 =====================
        manage_menu = QMenu("系统管理(&M)", self)
        # 用户维护
        user_manage_action = QAction("用户维护", self)
        user_manage_action.triggered.connect(lambda: self.openSet(user_manage_action))
        # 添加子项
        manage_menu.addAction(user_manage_action)
        menu_bar.addMenu(manage_menu)


    def openSet(self, m):
            if m.text() == '年级设置':
                import grade  # 按需导入，避免循环导入
                self.m = grade.MainWindow()
                self.m.show()
            elif m.text() == '班级设置':
                import classes
                self.m = classes.MainWindow()
                self.m.show()
            elif m.text() == '考试类别设置':
                import examkinds
                self.m = examkinds.MainWindow()
                self.m.show()
            elif m.text() == "考试科目设置":
                import subject
                self.m = subject.MainWindow()
                self.m.show()

            elif m.text() == "学生信息管理":
                import student
                self.m = student.MainWindow()
                self.m.show()
            elif m.text() == "学生成绩管理":
                import result
                self.m = result.MainWindow()
                self.m.show()
            elif m.text() == "学生信息查询":
                import studentInfo
                self.m = studentInfo.MainWindow()
                self.m.show()
            elif m.text() == "学生成绩查询":
                import resultInfo
                self.m = resultInfo.MainWindow()
                self.m.show()
            elif m.text() == "用户维护":
                import user
                self.m = user.MainWindow()
                self.m.show()

    def create_central_widget(self):
        """中心功能区"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)

        # 欢迎语
        welcome_label = QLabel(f"欢迎 {self.username} 登录学生管理系统！", self)
        welcome_font = QFont()
        welcome_font.setPointSize(18)
        welcome_label.setFont(welcome_font)
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)

    def create_status_bar(self):
        """状态栏"""
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        status_bar.showMessage(f"就绪 - 当前用户：{self.username}", 0)



# ===================== 3. 程序入口 =====================
if __name__ == "__main__":

    # 全局唯一的应用实例（关键：所有窗体共用）
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)
    app = QApplication(sys.argv)

    # 先显示登录窗体
    login_win = LoginWindow()
    login_win.show()
    # 运行应用循环
    sys.exit(app.exec_())
