import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTableWidget,
    QLabel, QLineEdit, QPushButton, QMenuBar, QStatusBar,
    QAbstractItemView, QTableWidgetItem, QMessageBox  # 修复：合并重复导入
)
from PySide2 import QtSql  # 如果你用PyQt5则写：from PyQt5 import QtSql
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from main import DBService

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.service = DBService()
        self.query=QtSql.QSqlQuery()
        # 初始化窗体流程
        self.init_window()
        self.create_central_widget()
        self.create_table_widget()
        self.create_labels_and_edits()
        self.create_buttons()
        self.create_menu_and_status_bar()
        # ========== 修复点3：初始化时加载数据 ==========
        self.load_user_data()


    def init_window(self):
        """初始化窗体大小和标题"""
        self.setGeometry(0, 0, 800, 400)
        self.setWindowTitle("用户管理系统")

    def create_central_widget(self):
        """创建中心部件"""
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

    def create_table_widget(self):
        """创建表格控件"""
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(20, 11, 700, 200)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["用户名称", "用户密码"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def create_labels_and_edits(self):
        """创建标签和输入框"""
        label_font = QFont()  # 修复：避免重复定义label_font
        label_font.setPointSize(7)


        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(30, 230, 81, 31)
        self.label.setFont(label_font)
        self.label.setText("用户名称：")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(230, 230, 81, 31)
        self.label_2.setFont(label_font)
        self.label_2.setText("用户密码：")


        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(120, 230, 100, 30)


        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(320, 230, 100, 30)

    def load_user_data(self):

        try:
            results = self.service.query("SELECT * FROM tb_user;", )
            # 清空表格
            self.tableWidget.setRowCount(0)
            # 处理空结果
            if not results:
                QMessageBox.information(self, "提示", "暂无数据")
                return

            # 填充表格
            for row_idx, row_data in enumerate(results):
                self.tableWidget.insertRow(row_idx)

                if isinstance(row_data, dict):
                    user_name = row_data["userName"]
                    user_pwd = row_data["userPwd"]
                else:
                    user_name = row_data[0]
                    user_pwd = row_data[1]
                self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(user_name))
                self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(user_pwd))
        except Exception as e:

            QMessageBox.critical(self, "加载失败", f"错误信息：{str(e)}")

    def add_user(self):
        """添加（手动输入ID和名称）"""
        # 1. 获取并清洗输入数据
        user_name = self.lineEdit.text().strip()
        user_pwd = self.lineEdit_2.text().strip()

        if not user_name:
            QMessageBox.warning(self, "警告", "用户名不能为空！")
            return
        if not user_pwd:
            QMessageBox.warning(self, "警告", "密码不能为空！")
            return

        add_sql = "INSERT OR IGNORE INTO tb_user(userName, userPwd) VALUES (?, ?);"
        new_id = self.service.add(add_sql, (user_name,user_pwd))

        # 4. 结果反馈
        if new_id:
            QMessageBox.information(self, "成功", f"班级添加成功！用户：{new_id}，密码：{user_pwd}")
            self.load_user_data()  # 刷新表格
            self.clear_input()  # 清空输入框（可选，提升体验）
        else:
            # 失败原因：ID重复 或 名称重复 或 其他错误
            QMessageBox.warning(self, "失败", "添加失败！")


    # 可选：添加清空输入框的方法
    def clear_input(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    def delete_user(self):
        """删除年级（根据输入的ID删除）"""
        # 1. 获取并清洗输入数据（仅需ID，复用add的ID校验逻辑）
        user_name = self.lineEdit.text().strip()

        # 2. 输入校验（复用add的ID校验逻辑）
        # 校验ID不能为空
        if not user_name:
            QMessageBox.warning(self, "警告", "用户名不能为空！")
            return
        # 3. 前置检查：校验该ID是否存在（避免删除不存在的年级）
        check_sql = "SELECT * FROM tb_user WHERE userName = ?;"
        check_result = self.service.query(check_sql, user_name)
        if not check_result:
            QMessageBox.warning(self, "警告", f"用户{user_name}不存在，无法删除！")
            return
        # 5. 执行删除SQL
        delete_sql = "DELETE  FROM tb_user WHERE userName = ?;"
        affected_rows = self.service.delete(delete_sql, (user_name,))

        # 6. 结果反馈
        if affected_rows > 0:
            QMessageBox.information(self, "成功", f"删除成功！用户：{user_name}")
            self.load_user_data()  # 刷新表格
            self.clear_input()  # 清空输入框
        else:
            QMessageBox.warning(self, "失败", "删除失败！原因：\n1. 数据库关联约束错误\n2. 数据库执行异常")


    def update_user(self):

        # 1. 获取并清洗输入数据（和add逻辑完全一致）
        user_name = self.lineEdit.text().strip()
        user_pwd= self.lineEdit_2.text().strip()
        # 2. 输入校验
        if not user_name:
            QMessageBox.warning(self, "警告", "用户名不能为空！")
            return
        # 校验新名称不能为空
        if not user_pwd:
            QMessageBox.warning(self, "警告", "密码不能为空！")
            return
        # 3. 前置检查：（避免修改不存在的用户）
        check_sql = "SELECT * FROM tb_user WHERE userName = ?;"
        check_result = self.service.query(check_sql, user_name)
        if not check_result:
            QMessageBox.warning(self, "警告", f"用户{user_name}不存在，无法修改！")
            return
        # 4. 执行修改SQL
        update_sql = "UPDATE tb_user SET userPwd = ? WHERE userName = ?;"
        affected_rows = self.service.update(update_sql, (user_name, user_pwd))

        # 5. 结果反馈（和add的反馈风格一致）
        if affected_rows > 0:
            QMessageBox.information(self, "成功", f"修改成功！用户名：{user_name}，密码：{user_pwd}")
            self.load_user_data()  # 刷新表格
            self.clear_input()  # 清空输入框
        else:
            QMessageBox.warning(self, "失败", "修改失败！")

    def create_buttons(self):
        """创建按钮（绑定添加事件）"""
        # 添加按钮
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(30, 280, 100, 40)
        self.pushButton.setText("添加")
        self.pushButton.clicked.connect(self.add_user)  # 绑定添加方法

        # 修改按钮
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(130, 280, 100, 40)
        self.pushButton_2.setText("修改")
        self.pushButton_2.clicked.connect(self.update_user)

        # 删除按钮
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(240, 280, 100, 40)
        self.pushButton_3.setText("删除")
        self.pushButton_3.clicked.connect(self.delete_user)

        # 退出按钮
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(360, 280, 100, 40)
        self.pushButton_4.setText("退出")
        self.pushButton_4.clicked.connect(self.close)

    def create_menu_and_status_bar(self):
        """创建菜单栏和状态栏"""
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(0, 0, 518, 22)
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)


if __name__ == "__main__":
    # 解决高DPI缩放问题
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)
    # 创建应用程序实例
    app = QApplication(sys.argv)
    # 创建并显示窗体
    window = MainWindow()
    window.show()
    # 运行应用程序
    sys.exit(app.exec_())