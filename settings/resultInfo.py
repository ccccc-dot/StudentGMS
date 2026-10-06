import sys
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QAbstractItemView, QHeaderView
)
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlDatabase, QSqlQuery

# ========== 沿用你原有结构的SQLite数据库类 ==========
class DBService:
    def __init__(self):
        """初始化QSqlDatabase连接（SQLite）"""
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        db_path = "C:/Users/25215/Desktop/sqlite/stugms.db"
        self.db.setDatabaseName(db_path)
        if not self.db.open():
            QMessageBox.critical(None, "数据库错误", self.db.lastError().text())
            sys.exit(1)

    def query(self, sql: str, *args) -> list:
        """
        执行查询SQL（QSqlQuery方式）
        :param sql: SQL语句（参数用?占位）
        :param args: 绑定的参数（逐个传入）
        :return: 查询结果（二维列表）
        """
        print("执行SQL:", sql)
        print("传入参数:", args)
        query = QSqlQuery()
        query.prepare(sql)
        for arg in args:
            query.addBindValue(arg)
        if not query.exec_():
            QMessageBox.critical(None, "查询错误", query.lastError().text())
            return []
        result = []
        col_count = query.record().count()
        while query.next():
            row = []
            for i in range(col_count):
                row.append(query.value(i))
            result.append(row)
        print("查询结果行数:", len(result))
        return result


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.service = DBService()
        self.init_ui()
        self.bind_events()
        self.init_table_widget()
        self.load_combobox_data()
        # 沿用你最初的无参数调用
        self.load_resultInfo_data()

    # ========== 完全保留你最初的init_ui结构 ==========
    def init_ui(self):
        self.setGeometry(0, 0, 900, 600)
        self.setWindowTitle("学生成绩查询")

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.label_query_type = QLabel("学生姓名：", self.centralwidget)
        self.label_query_type.setGeometry(10, 20, 101, 21)
        self.label_query_type.setFont(QFont("", 11))
        self.comboBox_query_type = QComboBox(self.centralwidget)
        self.comboBox_query_type.setGeometry(110, 20, 100, 30)

        self.label_2 = QLabel("考试类别：", self.centralwidget)
        self.label_2.setGeometry(230, 20, 80, 21)
        self.label_2.setFont(QFont("", 10))

        self.label_3 = QLabel("考试科目：", self.centralwidget)
        self.label_3.setGeometry(430, 22, 75, 21)
        self.label_3.setFont(QFont("", 10))

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(110, 19, 121, 30)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setGeometry(320, 20, 111, 30)

        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(510, 20, 141, 30)

        self.pushButton = QPushButton("查询", self.centralwidget)
        self.pushButton.setGeometry(660, 20, 61, 41)

        self.pushButton_2 = QPushButton("退出", self.centralwidget)
        self.pushButton_2.setGeometry(730, 20, 61, 41)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(20, 70, 800, 400)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("就绪")

    # ========== 保留你最初的bind_events ==========
    def bind_events(self):
        self.pushButton.clicked.connect(self.on_query_click)
        self.pushButton_2.clicked.connect(self.close)

    # ========== 保留你最初的init_table_widget（修复枚举错误） ==========
    def init_table_widget(self):
        self.tableWidget.setColumnCount(6)
        headers = ["考试类别", "所属年级", "所属班级", "学生姓名", "考试科目", "成绩"]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        for col in range(6):
            self.tableWidget.horizontalHeader().setSectionResizeMode(
                col, QHeaderView.ResizeToContents
            )

    # ========== 保留你最初的load_combobox_data ==========
    def load_combobox_data(self):
        self.comboBox.addItem("全部")
        self.comboBox.addItems(["期中", "期末"])
        self.comboBox_2.addItem("全部")
        self.comboBox_2.addItems(["大学语文", "高等数学", "大学英语", "概率论", "政治"])

    # ========== 核心：考试类别/科目都用模糊匹配，解决“期中测”截断问题 ==========
    def load_resultInfo_data(self, filter_name="", filter_kind="全部", filter_subject="全部"):
        """
        修复：下拉框显示截断为“期中测”，数据库是“期中测试”，用模糊匹配
        """
        try:
            view_sql = """
                SELECT kindName, gradeName, className, stuName, subName, result 
                FROM tb_result
                WHERE 1=1
            """
            params = []
            # 姓名：模糊匹配
            if filter_name:
                view_sql += " AND LOWER(stuName) LIKE LOWER(?)"
                params.append(f"%{filter_name}%")
            # 考试类别：模糊匹配
            if filter_kind != "全部":
                view_sql += " AND LOWER(kindName) LIKE LOWER(?)"
                params.append(f"%{filter_kind}%")
            # 考试科目：模糊匹配
            if filter_subject != "全部":
                view_sql += " AND LOWER(subName) LIKE LOWER(?)"
                params.append(f"%{filter_subject}%")

            print("拼接后的SQL:", view_sql)
            print("参数列表params:", params)

            # 解包传参
            view_results = self.service.query(view_sql, *params)

            self.tableWidget.setRowCount(0)
            if len(view_results) == 0:
                QMessageBox.information(self, "提示", "暂无数据")
                self.statusbar.showMessage("暂无数据")
                return

            # 沿用你最初的6列表格填充逻辑（元组格式）
            for row_idx, row_data in enumerate(view_results):
                self.tableWidget.insertRow(row_idx)
                kind_name = row_data[0] if len(row_data) > 0 else ""
                grade_name = row_data[1] if len(row_data) > 1 else ""
                class_name = row_data[2] if (len(row_data) > 2 and row_data[2] is not None) else ""
                stu_name = row_data[3] if len(row_data) > 3 else ""
                sub_name = row_data[4] if len(row_data) > 4 else ""
                result = row_data[5] if len(row_data) > 5 else None
                score_str = str(result) if result is not None else ""

                item0 = QTableWidgetItem(str(kind_name))
                item1 = QTableWidgetItem(str(grade_name))
                item2 = QTableWidgetItem(str(class_name))
                item3 = QTableWidgetItem(str(stu_name))
                item4 = QTableWidgetItem(str(sub_name))
                item5 = QTableWidgetItem(score_str)

                for item in [item0, item1, item2, item3, item4, item5]:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                self.tableWidget.setItem(row_idx, 0, item0)
                self.tableWidget.setItem(row_idx, 1, item1)
                self.tableWidget.setItem(row_idx, 2, item2)
                self.tableWidget.setItem(row_idx, 3, item3)
                self.tableWidget.setItem(row_idx, 4, item4)
                self.tableWidget.setItem(row_idx, 5, item5)

            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.statusbar.showMessage(f"成功加载 {len(view_results)} 条数据")
        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"错误信息：{str(e)}")
            import traceback
            print(traceback.format_exc())
            self.statusbar.showMessage("数据加载失败")

    # ========== 完全保留你最初的on_query_click ==========
    def on_query_click(self):
        filter_name = self.lineEdit.text().strip()
        filter_kind = self.comboBox.currentText().strip()
        filter_subject = self.comboBox_2.currentText().strip()
        print("点击查询时筛选条件:", filter_name, "|", filter_kind, "|", filter_subject)
        self.load_resultInfo_data(filter_name, filter_kind, filter_subject)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.raise_()
    sys.exit(app.exec_())