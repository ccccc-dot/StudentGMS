import sys
import os


# ========== 修复点1：调整导入顺序（先加路径，后导入DBService） ==========
# 添加项目根目录到Python路径（必须放在导入main之前！）
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
        # ========== 修复点2：实例化DBService为类属性（所有方法可访问） ==========
        self.service = DBService()  # 关键：用self.service保存实例，全局可用
        self.query=QtSql.QSqlQuery()
        # 初始化窗体流程
        self.init_window()
        self.create_central_widget()
        self.create_table_widget()
        self.create_labels_and_edits()
        self.create_buttons()
        self.create_menu_and_status_bar()
        # ========== 修复点3：初始化时加载数据 ==========
        self.load_grade_data()


    def init_window(self):
        """初始化窗体大小和标题"""
        self.setGeometry(0, 0, 800, 400)
        self.setWindowTitle("年级管理系统")

    def create_central_widget(self):
        """创建中心部件"""
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

    def create_table_widget(self):
        """创建表格控件"""
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(20, 11, 700, 200)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["年级编号", "年级名称"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def create_labels_and_edits(self):
        """创建标签和输入框"""
        label_font = QFont()  # 修复：避免重复定义label_font
        label_font.setPointSize(7)

        # 年级编号标签
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(30, 230, 81, 31)
        self.label.setFont(label_font)
        self.label.setText("年级编号：")

        # 年级名称标签
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(230, 230, 81, 31)
        self.label_2.setFont(label_font)
        self.label_2.setText("年级名称：")

        # 年级编号输入框
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(120, 230, 100, 30)

        # 年级名称输入框
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(320, 230, 100, 30)

    def load_grade_data(self):
        """加载年级数据到表格（核心修复）"""
        try:
            # ========== 修复点4：使用self.service调用方法（作用域问题） ==========
            results = self.service.query("SELECT * FROM tb_grade ORDER BY gradeID;", )

            # 清空表格
            self.tableWidget.setRowCount(0)

            # 处理空结果
            if not results:
                QMessageBox.information(self, "提示", "暂无年级数据")
                return

            # 填充表格
            for row_idx, row_data in enumerate(results):
                self.tableWidget.insertRow(row_idx)
                # 兼容字典/元组格式（适配不同DBService返回类型）
                if isinstance(row_data, dict):
                    grade_id = str(row_data["gradeID"])
                    grade_name = row_data["gradeName"]
                else:
                    grade_id = str(row_data[0])
                    grade_name = row_data[1]
                self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(grade_id))
                self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(grade_name))
        except Exception as e:
            # ========== 修复点5：捕获异常并提示 ==========
            QMessageBox.critical(self, "加载失败", f"错误信息：{str(e)}")

    def add_grade(self):
        """添加年级（手动输入ID和名称）"""
        # 1. 获取并清洗输入数据
        grade_id = self.lineEdit.text().strip()
        grade_name = self.lineEdit_2.text().strip()

        # 2. 输入校验
        # 校验ID不能为空
        if not grade_id:
            QMessageBox.warning(self, "警告", "年级编号不能为空！")
            return
        # 校验ID必须是数字
        if not grade_id.isdigit():
            QMessageBox.warning(self, "警告", "年级编号必须是数字！")
            return
        # 转换为整数（数据库gradeID是整型）
        grade_id = int(grade_id)
        # 校验名称不能为空
        if not grade_name:
            QMessageBox.warning(self, "警告", "年级名称不能为空！")
            return

        # 3. 调整SQL：同时插入gradeID和gradeName
        # 注意：INSERT OR IGNORE 会在ID重复时跳过插入
        add_sql = "INSERT OR IGNORE INTO tb_grade (gradeID, gradeName) VALUES (?, ?);"
        # 传入两个参数：ID + 名称
        new_id = self.service.add(add_sql, (grade_id, grade_name))

        # 4. 结果反馈
        if new_id:
            QMessageBox.information(self, "成功", f"年级添加成功！ID：{new_id}，名称：{grade_name}")
            self.load_grade_data()  # 刷新表格
            self.clear_input()  # 清空输入框（可选，提升体验）
        else:
            # 失败原因：ID重复 或 名称重复 或 其他错误
            QMessageBox.warning(self, "失败", "添加失败！原因：\n1. 年级编号已存在\n2. 年级名称已存在\n3. 数据库错误")

    # 可选：添加清空输入框的方法
    def clear_input(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    # def update_grade(self, sql: str, params: tuple = ()) -> int:
    #     """执行更新SQL，返回受影响行数"""
    #     query = QSqlQuery()
    #     query.prepare(sql)
    #     for param in params:
    #         query.addBindValue(param)
    #     if not query.exec_():
    #         QMessageBox.critical(None, "更新错误", query.lastError().text())
    #         return 0
    #     # 返回受影响的行数（0表示无数据修改）
    #     return query.numRowsAffected()


    def delete_grade(self):
        """删除年级（根据输入的ID删除）"""
        # 1. 获取并清洗输入数据（仅需ID，复用add的ID校验逻辑）
        grade_id_str = self.lineEdit.text().strip()

        # 2. 输入校验（复用add的ID校验逻辑）
        # 校验ID不能为空
        if not grade_id_str:
            QMessageBox.warning(self, "警告", "年级编号不能为空！")
            return
        # 校验ID必须是数字
        if not grade_id_str.isdigit():
            QMessageBox.warning(self, "警告", "年级编号必须是数字！")
            return
        # 转换为整数
        grade_id = int(grade_id_str)

        # 3. 前置检查：校验该ID是否存在（避免删除不存在的年级）
        check_sql = "SELECT * FROM tb_grade WHERE gradeID = ?;"
        check_result = self.service.query(check_sql, grade_id)
        if not check_result:
            QMessageBox.warning(self, "警告", f"年级编号{grade_id}不存在，无法删除！")
            return
        # 5. 执行删除SQL
        delete_sql = "DELETE  FROM tb_grade WHERE gradeID = ?;"
        # 传入参数：年级ID
        affected_rows = self.service.delete(delete_sql, (grade_id,))

        # 6. 结果反馈（和add的反馈风格一致）
        if affected_rows > 0:
            QMessageBox.information(self, "成功", f"年级删除成功！ID：{grade_id}")
            self.load_grade_data()  # 刷新表格
            self.clear_input()  # 清空输入框
        else:
            QMessageBox.warning(self, "失败", "删除失败！原因：\n1. 数据库关联约束错误\n2. 数据库执行异常")

    def update_grade(self):
        """修改年级（根据输入的ID修改名称）"""
        # 1. 获取并清洗输入数据（和add逻辑完全一致）
        grade_id_str = self.lineEdit.text().strip()
        new_grade_name = self.lineEdit_2.text().strip()

        # 2. 输入校验（复用add的校验逻辑）
        # 校验ID不能为空
        if not grade_id_str:
            QMessageBox.warning(self, "警告", "年级编号不能为空！")
            return
        # 校验ID必须是数字
        if not grade_id_str.isdigit():
            QMessageBox.warning(self, "警告", "年级编号必须是数字！")
            return
        # 转换为整数
        grade_id = int(grade_id_str)
        # 校验新名称不能为空
        if not new_grade_name:
            QMessageBox.warning(self, "警告", "年级名称不能为空！")
            return

        # 3. 前置检查：校验该ID是否存在（避免修改不存在的年级）
        check_sql = "SELECT * FROM tb_grade WHERE gradeID = ?;"
        check_result = self.service.query(check_sql, grade_id)
        if not check_result:
            QMessageBox.warning(self, "警告", f"年级编号{grade_id}不存在，无法修改！")
            return

        # 4. 执行修改SQL（根据ID更新名称）
        update_sql = "UPDATE tb_grade SET gradeName = ? WHERE gradeID = ?;"
        # 传入参数：新名称 + 年级ID
        affected_rows = self.service.update(update_sql, (new_grade_name, grade_id))

        # 5. 结果反馈（和add的反馈风格一致）
        if affected_rows > 0:
            QMessageBox.information(self, "成功", f"年级修改成功！ID：{grade_id}，新名称：{new_grade_name}")
            self.load_grade_data()  # 刷新表格
            self.clear_input()  # 清空输入框
        else:
            QMessageBox.warning(self, "失败", "修改失败！原因：\n1. 年级名称未变更\n2. 名称已存在\n3. 数据库错误")


    def create_buttons(self):
        """创建按钮（绑定添加事件）"""
        # 添加按钮
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(30, 280, 100, 40)
        self.pushButton.setText("添加")
        self.pushButton.clicked.connect(self.add_grade)  # 绑定添加方法

        # 修改按钮
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(130, 280, 100, 40)
        self.pushButton_2.setText("修改")
        self.pushButton_2.clicked.connect(self.update_grade)

        # 删除按钮
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(240, 280, 100, 40)
        self.pushButton_3.setText("删除")
        self.pushButton_3.clicked.connect(self.delete_grade)

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