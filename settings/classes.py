import sys
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTableWidget,
    QLabel, QLineEdit, QPushButton, QMenuBar, QStatusBar,
    QAbstractItemView, QMessageBox, QTableWidgetItem  # 修复：添加QTableWidgetItem导入
)
from PySide2 import QtSql
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from main import DBService


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.service = DBService()
        self.query = QtSql.QSqlQuery()
        self.init_window()
        self.create_central_widget()
        self.create_table_widget()
        self.create_labels_and_edits()
        self.create_buttons()
        self.create_menu_and_status_bar()
        # ========== 初始化时加载数据 ==========
        self.load_class_data()

    def load_class_data(self):
        """加载班级数据到表格（修复SQL表名/字段名）"""
        try:
          #表名是tb_class，字段名应该是classID/className（和表格标题对应）
            results = self.service.query("SELECT * FROM tb_class ORDER BY classID;",)
            self.tableWidget.setRowCount(0)
            if not results:
                QMessageBox.information(self, "提示", "暂无班级数据")
                return

            for row_idx, row_data in enumerate(results):
                self.tableWidget.insertRow(row_idx)
                # 修复：字段名对应tb_class的classID/className
                if isinstance(row_data, dict):
                    class_id = str(row_data["classID"])
                    class_name = row_data["className"]

                else:
                    class_id = str(row_data[0])
                    class_name = row_data[1]

                self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(class_id))
                self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(class_name))
        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"错误信息：{str(e)}")

    def init_window(self):
        self.setGeometry(0, 0, 800, 400)
        self.setWindowTitle("班级管理系统")

    def create_central_widget(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

    def create_table_widget(self):
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(20, 11, 700, 200)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["班级编号", "班级名称"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def add_class(self):
        """添加（手动输入ID和名称）"""
        # 1. 获取并清洗输入数据
        class_id = self.lineEdit.text().strip()
        class_name = self.lineEdit_2.text().strip()

        # 2. 输入校验
        # 校验ID不能为空
        if not class_id:
            QMessageBox.warning(self, "警告", "班级编号不能为空！")
            return
        # 校验ID必须是数字
        if not class_id.isdigit():
            QMessageBox.warning(self, "警告", "班级编号必须是数字！")
            return
        # 转换为整数（数据库gradeID是整型）
        class_id = int(class_id)
        # 校验名称不能为空
        if not class_name:
            QMessageBox.warning(self, "警告", "班级名称不能为空！")
            return

        # 3. 调整SQL：同时插入gradeID和gradeName
        # 注意：INSERT OR IGNORE 会在ID重复时跳过插入
        add_sql = "INSERT OR IGNORE INTO tb_class(classID, className) VALUES (?, ?);"
        # 传入两个参数：ID + 名称
        new_id = self.service.add(add_sql, (class_id, class_name))

        # 4. 结果反馈
        if new_id:
            QMessageBox.information(self, "成功", f"班级添加成功！ID：{new_id}，名称：{class_name}")
            self.load_class_data()  # 刷新表格
            self.clear_input()  # 清空输入框（可选，提升体验）
        else:
            # 失败原因：ID重复 或 名称重复 或 其他错误
            QMessageBox.warning(self, "失败", "添加失败！原因：\n1. 编号已存在\n2. 名称已存在\n3. 数据库错误")


    # 可选：添加清空输入框的方法
    def clear_input(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    def update_class(self):
        """修改年级（根据输入的ID修改名称）"""
        # 1. 获取并清洗输入数据（和add逻辑完全一致）
        class_id_str = self.lineEdit.text().strip()
        new_class_name = self.lineEdit_2.text().strip()

        # 2. 输入校验（复用add的校验逻辑）
        # 校验ID不能为空
        if not class_id_str:
            QMessageBox.warning(self, "警告", "年级编号不能为空！")
            return
        # 校验ID必须是数字
        if not class_id_str.isdigit():
            QMessageBox.warning(self, "警告", "年级编号必须是数字！")
            return
        # 转换为整数
        class_id = int(class_id_str)
        # 校验新名称不能为空
        if not new_class_name:
            QMessageBox.warning(self, "警告", "年级名称不能为空！")
            return

        # 3. 前置检查：校验该ID是否存在（避免修改不存在的年级）
        check_sql = "SELECT * FROM tb_class WHERE classID = ?;"
        check_result = self.service.query(check_sql, class_id)
        if not check_result:
            QMessageBox.warning(self, "警告", f"年级编号{class_id}不存在，无法修改！")
            return

        # 4. 执行修改SQL（根据ID更新名称）
        update_sql = "UPDATE tb_class SET className = ? WHERE classID = ?;"
        # 传入参数：新名称 + 年级ID
        affected_rows = self.service.update(update_sql, (new_class_name, class_id))

        # 5. 结果反馈（和add的反馈风格一致）
        if affected_rows > 0:
            QMessageBox.information(self, "成功", f"年级修改成功！ID：{class_id}，新名称：{new_class_name}")
            self.load_class_data()  # 刷新表格
            self.clear_input()  # 清空输入框
        else:
            QMessageBox.warning(self, "失败", "修改失败！原因：\n1. 年级名称未变更\n2. 名称已存在\n3. 数据库错误")



    def delete_class(self):
        """删除年级（根据输入的ID删除）"""
        # 1. 获取并清洗输入数据（仅需ID，复用add的ID校验逻辑）
        class_id = self.lineEdit.text().strip()

        # 2. 输入校验（复用add的ID校验逻辑）
        # 校验ID不能为空
        if not class_id:
            QMessageBox.warning(self, "警告", "年级编号不能为空！")
            return
        # 校验ID必须是数字
        if not class_id.isdigit():
            QMessageBox.warning(self, "警告", "年级编号必须是数字！")
            return
        # 转换为整数
        class_id = int(class_id)

        # 3. 前置检查：校验该ID是否存在（避免删除不存在的年级）
        check_sql = "SELECT * FROM tb_class WHERE classID = ?;"
        check_result = self.service.query(check_sql, class_id)
        if not check_result:
            QMessageBox.warning(self, "警告", f"年级编号{class_id}不存在，无法删除！")
            return
        # 5. 执行删除SQL
        delete_sql = "DELETE  FROM tb_class WHERE classID = ?;"
        # 传入参数：年级ID
        affected_rows = self.service.delete(delete_sql, (class_id,))

        # 6. 结果反馈（和add的反馈风格一致）
        if affected_rows > 0:
            QMessageBox.information(self, "成功", f"年级删除成功！ID：{class_id}")
            self.load_class_data()  # 刷新表格
            self.clear_input()  # 清空输入框
        else:
            QMessageBox.warning(self, "失败", "删除失败！原因：\n1. 数据库关联约束错误\n2. 数据库执行异常")

    def create_buttons(self):
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(30, 280, 100, 40)
        self.pushButton.setText("添加")
        self.pushButton.clicked.connect(self.add_class)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(130, 280, 100, 40)
        self.pushButton_2.setText("修改")
        self.pushButton_2.clicked.connect(self.update_class)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(240, 280, 100, 40)
        self.pushButton_3.setText("删除")
        self.pushButton_3.clicked.connect(self.delete_class)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(360, 280, 100, 40)
        self.pushButton_4.setText("退出")
        self.pushButton_4.clicked.connect(self.close)

    def create_labels_and_edits(self):
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(30, 230, 81, 31)
        label_font = QFont()
        label_font.setPointSize(7)
        self.label.setFont(label_font)
        self.label.setText("班级编号：")

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(230, 230, 81, 31)
        self.label_2.setFont(label_font)
        self.label_2.setText("班级名称：")

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(120, 230, 100, 30)

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(320, 230, 100, 30)


    def create_menu_and_status_bar(self):
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(0, 0, 518, 22)
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.load_class_data()
    sys.exit(app.exec_())