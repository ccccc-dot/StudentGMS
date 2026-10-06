import sys
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTableWidget,
    QLabel, QLineEdit, QPushButton, QMenuBar, QStatusBar,
    QAbstractItemView,QMessageBox,QTableWidgetItem
)
from PySide2.QtCore import Qt
from PySide2 import QtSql
from PySide2.QtGui import QFont
from main import DBService


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.service = DBService()
        self.query = QtSql.QSqlQuery()
        # self.setupUi(self)
        # 初始化窗体基本属性
        self.init_window()
        # 创建中心部件
        self.create_central_widget()
        # 创建表格
        self.create_table_widget()
        # 创建标签和输入框
        self.create_labels_and_edits()
        # 创建按钮
        self.create_buttons()
        # 创建菜单栏和状态栏
        self.create_menu_and_status_bar()
        self.load_subject_data()

    def init_window(self):
        """初始化窗体大小和标题"""
        self.setGeometry(0, 0, 800, 400)
        self.setWindowTitle("考试科目管理系统")

    def create_central_widget(self):
        """创建中心部件"""
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

    def create_table_widget(self):
        """创建表格控件"""
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(20, 11, 700, 200)
        # 表格基础配置（可选，增强体验）

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["科目编号", "科目名称"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def create_labels_and_edits(self):
        """创建标签和输入框"""
        # 年级编号标签
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(30, 230, 81, 31)
        label_font = QFont()
        label_font.setPointSize(7)
        self.label.setFont(label_font)
        self.label.setText("科目编号：")

        # 年级名称标签
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(230, 230, 81, 31)
        self.label_2.setFont(label_font)
        self.label_2.setText("科目名称：")
        label_font.setPointSize(7)

        # 年级编号输入框
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(120, 230, 100, 30)

        # 年级名称输入框
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(320, 230, 100, 30)

    def load_subject_data(self):
        """加载年级数据到表格（核心修复）"""
        try:
            # ========== 修复点4：使用self.service调用方法（作用域问题） ==========
            results = self.service.query("SELECT * FROM tb_subject ORDER BY subID;", )

            # 清空表格
            self.tableWidget.setRowCount(0)

            # 处理空结果
            if not results:
                QMessageBox.information(self, "提示", "暂无数据")
                return

            # 填充表格
            for row_idx, row_data in enumerate(results):
                self.tableWidget.insertRow(row_idx)
                # 兼容字典/元组格式（适配不同DBService返回类型）
                if isinstance(row_data, dict):
                    sub_id = str(row_data["subID"])
                    sub_name = row_data["subName"]
                else:
                    sub_id = str(row_data[0])
                    sub_name = row_data[1]
                self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(sub_id))
                self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(sub_name))
        except Exception as e:
            # ========== 修复点5：捕获异常并提示 ==========
            QMessageBox.critical(self, "加载失败", f"错误信息：{str(e)}")

    def add_subject(self):
        """添加年级（手动输入ID和名称）"""
        # 1. 获取并清洗输入数据
        sub_id = self.lineEdit.text().strip()
        sub_name = self.lineEdit_2.text().strip()

        # 2. 输入校验
        # 校验ID不能为空
        if not sub_id:
            QMessageBox.warning(self, "警告", "年级编号不能为空！")
            return
        # 校验ID必须是数字
        if not sub_id.isdigit():
            QMessageBox.warning(self, "警告", "年级编号必须是数字！")
            return
        # 转换为整数（数据库gradeID是整型）
        sub_id = int(sub_id)
        # 校验名称不能为空
        if not sub_name:
            QMessageBox.warning(self, "警告", "年级名称不能为空！")
            return

        # 3. 调整SQL：同时插入gradeID和gradeName
        # 注意：INSERT OR IGNORE 会在ID重复时跳过插入
        add_sql = "INSERT OR IGNORE INTO tb_subject (subID, subName) VALUES (?, ?);"
        # 传入两个参数：ID + 名称
        new_id = self.service.add(add_sql, (sub_id, sub_name))

        # 4. 结果反馈
        if new_id:
            QMessageBox.information(self, "成功", f"年级添加成功！ID：{new_id}，名称：{sub_name}")
            self.load_subject_data()  # 刷新表格
            self.clear_input()  # 清空输入框（可选，提升体验）
        else:
            # 失败原因：ID重复 或 名称重复 或 其他错误
            QMessageBox.warning(self, "失败", "添加失败！原因：\n1. 年级编号已存在\n2. 年级名称已存在\n3. 数据库错误")

    # 可选：添加清空输入框的方法
    def clear_input(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    def delete_subject(self):
        """删除年级（根据输入的ID删除）"""
        # 1. 获取并清洗输入数据（仅需ID，复用add的ID校验逻辑）
        sub_id_str = self.lineEdit.text().strip()

        # 2. 输入校验（复用add的ID校验逻辑）
        # 校验ID不能为空
        if not sub_id_str:
            QMessageBox.warning(self, "警告", "年级编号不能为空！")
            return
        # 校验ID必须是数字
        if not sub_id_str.isdigit():
            QMessageBox.warning(self, "警告", "年级编号必须是数字！")
            return
        # 转换为整数
        sub_id = int(sub_id_str)

        # 3. 前置检查：校验该ID是否存在（避免删除不存在的年级）
        check_sql = "SELECT * FROM tb_subject WHERE subID = ?;"
        check_result = self.service.query(check_sql, sub_id)
        if not check_result:
            QMessageBox.warning(self, "警告", f"年级编号{sub_id}不存在，无法删除！")
            return
        # 5. 执行删除SQL
        delete_sql = "DELETE  FROM tb_subject WHERE subID = ?;"
        # 传入参数：年级ID
        affected_rows = self.service.delete(delete_sql, (sub_id,))

        # 6. 结果反馈（和add的反馈风格一致）
        if affected_rows > 0:
            QMessageBox.information(self, "成功", f"年级删除成功！ID：{sub_id}")
            self.load_subject_data()  # 刷新表格
            self.clear_input()  # 清空输入框
        else:
            QMessageBox.warning(self, "失败", "删除失败！原因：\n1. 数据库关联约束错误\n2. 数据库执行异常")

    def update_subject(self):
        # 1. 获取并清洗输入数据（和add逻辑完全一致）
        sub_id_str = self.lineEdit.text().strip()
        new_sub_name = self.lineEdit_2.text().strip()

        # 2. 输入校验（复用add的校验逻辑）
        # 校验ID不能为空
        if not sub_id_str:
            QMessageBox.warning(self, "警告", "年级编号不能为空！")
            return
        # 校验ID必须是数字
        if not sub_id_str.isdigit():
            QMessageBox.warning(self, "警告", "年级编号必须是数字！")
            return
        # 转换为整数
        sub_id = int(sub_id_str)
        # 校验新名称不能为空
        if not new_sub_name:
            QMessageBox.warning(self, "警告", "年级名称不能为空！")
            return

        # 3. 前置检查：校验该ID是否存在（避免修改不存在的年级）
        check_sql = "SELECT * FROM tb_subject WHERE subID = ?;"
        check_result = self.service.query(check_sql, sub_id)
        if not check_result:
            QMessageBox.warning(self, "警告", f"年级编号{sub_id}不存在，无法修改！")
            return

        # 4. 执行修改SQL（根据ID更新名称）
        update_sql = "UPDATE tb_subject SET subName = ? WHERE subID = ?;"
        # 传入参数：新名称 + 年级ID
        affected_rows = self.service.update(update_sql, (new_sub_name, sub_id))

        # 5. 结果反馈（和add的反馈风格一致）
        if affected_rows > 0:
            QMessageBox.information(self, "成功", f"年级修改成功！ID：{sub_id}，新名称：{new_sub_name}")
            self.load_subject_data() # 刷新表格
            self.clear_input()  # 清空输入框
        else:
            QMessageBox.warning(self, "失败", "修改失败！原因：\n1. 年级名称未变更\n2. 名称已存在\n3. 数据库错误")

    def update_subject(self):
        """修改年级（根据输入的ID修改名称）"""
        # 1. 获取并清洗输入数据（和add逻辑完全一致）
        sub_id_str = self.lineEdit.text().strip()
        new_sub_name = self.lineEdit_2.text().strip()

        # 2. 输入校验（复用add的校验逻辑）
        # 校验ID不能为空
        if not sub_id_str:
            QMessageBox.warning(self, "警告", "年级编号不能为空！")
            return
        # 校验ID必须是数字
        if not sub_id_str.isdigit():
            QMessageBox.warning(self, "警告", "年级编号必须是数字！")
            return
        # 转换为整数
        sub_id = int(sub_id_str)
        # 校验新名称不能为空
        if not new_sub_name:
            QMessageBox.warning(self, "警告", "年级名称不能为空！")
            return

        # 3. 前置检查：校验该ID是否存在（避免修改不存在的年级）
        check_sql = "SELECT * FROM tb_subject WHERE subID = ?;"
        check_result = self.service.query(check_sql, sub_id)
        if not check_result:
            QMessageBox.warning(self, "警告", f"年级编号{sub_id}不存在，无法修改！")
            return

        # 4. 执行修改SQL（根据ID更新名称）
        update_sql = "UPDATE tb_subject SET subName = ? WHERE subID = ?;"
        # 传入参数：新名称 + 年级ID
        affected_rows = self.service.update(update_sql, (new_sub_name, sub_id))

        # 5. 结果反馈（和add的反馈风格一致）
        if affected_rows > 0:
            QMessageBox.information(self, "成功", f"年级修改成功！ID：{sub_id}，新名称：{new_sub_name}")
            self.load_subject_data()  # 刷新表格
            self.clear_input()  # 清空输入框
        else:
            QMessageBox.warning(self, "失败", "修改失败！原因：\n1. 年级名称未变更\n2. 名称已存在\n3. 数据库错误")



    def create_buttons(self):
        """创建按钮"""
        # 添加按钮
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(30, 280, 100, 40)
        self.pushButton.setText("添加")
        self.pushButton.clicked.connect(self.add_subject)


        # 修改按钮
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(130, 280, 100, 40)
        self.pushButton_2.setText("修改")
        self.pushButton_2.clicked.connect(self.update_subject)

        # 删除按钮
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(240, 280, 100, 40)
        self.pushButton_3.setText("删除")
        self.pushButton_3.clicked.connect(self.delete_subject)

        # 退出按钮
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(360, 280, 100, 40)
        self.pushButton_4.setText("退出")
        # 绑定退出按钮事件
        self.pushButton_4.clicked.connect(self.close)

    def create_menu_and_status_bar(self):
        """创建菜单栏和状态栏"""
        # 菜单栏
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(0, 0, 518, 22)
        self.setMenuBar(self.menubar)

        # 状态栏
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