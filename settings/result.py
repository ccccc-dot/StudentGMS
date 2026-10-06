import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QComboBox,
                               QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
                               QStatusBar, QMessageBox)
from PySide2.QtGui import QFont
from PySide2 import QtSql
from PySide2.QtCore import Qt
from main import DBService  # 保留你的原有DBService，不新增模拟数据


# 主窗口类（考试成绩管理系统）
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initComboBoxData()  # 修复：先初始化下拉框，后加载表格
        self.service = DBService()  # 关键：用self.service保存实例，全局可用
        self.query = QtSql.QSqlQuery()
        self.load_result_data()  # 修复：后加载表格数据

    def initUI(self):
        # 窗口基本属性
        self.setGeometry(0, 0, 900, 900)
        self.setMinimumSize(900, 900)
        self.setMaximumSize(900, 900)
        self.setWindowTitle("考试成绩管理系统")
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ========== 顶部筛选与功能按钮区域 ==========
        # 考试种类标签与下拉框
        self.label_exam_type = QLabel("考试种类：", central_widget)
        self.label_exam_type.setGeometry(10, 30, 91, 21)
        self.label_exam_type.setFont(QFont("", 11))
        self.comboBox_exam_type = QComboBox(central_widget)
        self.comboBox_exam_type.setGeometry(100, 30, 80, 30)

        # 所属年级标签与下拉框
        self.label_grade = QLabel("所属年级：", central_widget)
        self.label_grade.setGeometry(180, 30, 91, 21)
        self.label_grade.setFont(QFont("", 11))
        self.comboBox_grade = QComboBox(central_widget)
        self.comboBox_grade.setGeometry(268, 30, 80, 30)

        # 所属班级标签与下拉框
        self.label_class = QLabel("所属班级：", central_widget)
        self.label_class.setGeometry(350, 30, 91, 21)
        self.label_class.setFont(QFont("", 11))
        self.comboBox_class = QComboBox(central_widget)
        self.comboBox_class.setGeometry(440, 30, 100, 30)

        # 功能按钮
        self.btn_refresh = QPushButton("刷新", central_widget)
        self.btn_refresh.setGeometry(550, 20, 61, 41)
        self.btn_refresh.clicked.connect(self.on_refresh_click)

        self.btn_add = QPushButton("添加", central_widget)
        self.btn_add.setGeometry(610, 20, 61, 41)
        self.btn_add.clicked.connect(self.on_add_click)

        self.btn_modify = QPushButton("修改", central_widget)
        self.btn_modify.setGeometry(670, 20, 61, 41)
        self.btn_modify.clicked.connect(self.on_modify_click)

        self.btn_delete = QPushButton("删除", central_widget)
        self.btn_delete.setGeometry(730, 20, 61, 41)
        self.btn_delete.clicked.connect(self.on_delete_click)

        self.btn_quit = QPushButton("退出", central_widget)
        self.btn_quit.setGeometry(790, 20, 61, 41)
        self.btn_quit.clicked.connect(self.close)

        # ========== 表格显示区域 ==========
        self.tableWidget = QTableWidget(central_widget)
        self.tableWidget.setGeometry(25, 70, 841, 381)

        # ========== 底部信息输入区域 ==========

        # 学生姓名标签与下拉框
        self.label_stu_name = QLabel("学生姓名：", central_widget)
        self.label_stu_name.setGeometry(20, 490, 91, 21)
        self.label_stu_name.setFont(QFont("", 11))
        self.comboBox_stu_name = QComboBox(central_widget)
        self.comboBox_stu_name.setGeometry(120, 490, 200, 30)

        # 考试科目标签与下拉框
        self.label_subject = QLabel("考试科目：", central_widget)
        self.label_subject.setGeometry(400, 490, 91, 21)
        self.label_subject.setFont(QFont("", 11))
        self.comboBox_subject = QComboBox(central_widget)
        self.comboBox_subject.setGeometry(500, 490, 100, 30)


        self.label_depart= QLabel("所属院系：", central_widget)
        self.label_depart.setGeometry(10, 530, 91, 21)
        self.label_depart.setFont(QFont("", 11))
        self.comboBox_depart = QComboBox(central_widget)
        self.comboBox_depart.setGeometry(100, 530, 300, 31)
        self.comboBox_depart.addItems( ["信息工程学院", "生物工程学院", "文法学院", "艺术学院", "外国语学院", "食品工程学院", "经济与管理学院","机电工程学院"])

        self.label_major = QLabel("所属专业：", central_widget)
        self.label_major.setGeometry(10, 580, 91, 21)
        self.label_major.setFont(QFont("", 11))
        self.lineEdit_major = QLineEdit(central_widget)
        self.lineEdit_major.setGeometry(100, 580, 300, 31)

        # 成绩标签与输入框
        self.label_score = QLabel("成绩：", central_widget)
        self.label_score.setGeometry(620, 490, 61, 21)
        self.label_score.setFont(QFont("", 11))
        self.lineEdit_score = QLineEdit(central_widget)
        self.lineEdit_score.setGeometry(670, 490, 120, 40)

        # ========== 状态栏 ==========
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("就绪")

    def initComboBoxData(self):
        """初始化所有下拉框的选项数据"""
        # 考试种类
        self.comboBox_exam_type.addItems(["期中", "期末", "月考", "模拟"])
        # 所属年级
        self.comboBox_grade.addItems(["大一", "大二", "大三", "大四"])
        # 所属班级
        self.comboBox_class.addItems(["一班", "二班", "三班", "四班","五班", "六班", "七班", "八班","九班", "十班", "十一班", "十二班",])
        # 学生姓名
        self.comboBox_stu_name.addItems(["江离", "江只", "江零", "江林", "江小", "江知"])
        # 考试科目
        self.comboBox_subject.addItems(["语文", "数学", "英语", "科学", "道德", "ASDF"])

    def load_result_data(self):
        """加载数据库中的成绩数据（仅修复问题，不新增初始化数据）"""
        try:
            # 1. 执行视图查询（明确指定列顺序，避免依赖SELECT *）
            view_sql = """
                   SELECT kindName, gradeName, className,departmentName,majorName, stuName, subName, result FROM tb_result;"""
            view_results = self.service.query(view_sql)
            # 2. 清空表格
            self.tableWidget.setRowCount(0)
            if len(view_results) == 0:
                QMessageBox.information(self, "提示", "暂无数据")
                self.statusbar.showMessage("暂无数据")
                return
            # 3. 设置表格列数和表头（表头顺序不变，但数据映射要对应视图列）
            self.tableWidget.setColumnCount(8)
            headers = ["考试种类", "所属年级", "所属班级","所属院系", "所属专业", "学生姓名", "考试科目", "成绩"]
            self.tableWidget.setHorizontalHeaderLabels(headers)
            # 4. 填充表格数据（重点修复成绩列显示问题）
            for row_idx, row_data in enumerate(view_results):
                self.tableWidget.insertRow(row_idx)
                # 兼容字典/元组格式（按视图列顺序取值）
                if isinstance(row_data, dict):
                    kind_name = row_data.get("kindName", "") or ""
                    grade_name = row_data.get("gradeName", "") or ""
                    class_name = row_data.get("className", "") or ""
                    department_name = row_data.get("departmentName", "") or ""
                    major_name = row_data.get("majorName", "") or ""
                    stu_name = row_data.get("stuName", "") or ""
                    sub_name = row_data.get("subName", "") or ""
                    result = row_data.get("result")
                    score_str = str(result) if result is not None else ""
                else:
                    kind_name = row_data[0] if len(row_data) > 0 else ""
                    grade_name = row_data[1] if len(row_data) > 1 else ""
                    class_name = row_data[2] if (len(row_data) > 2 and row_data[2] is not None) else ""
                    department_name = row_data[3] if len(row_data) > 3 else ""
                    major_name = row_data[4] if len(row_data) > 4 else ""
                    stu_name = row_data[5] if len(row_data) > 5 else ""
                    sub_name = row_data[6] if len(row_data) > 6 else ""
                    # 修复1：成绩字段转为字符串，处理None值
                    result = row_data[7] if len(row_data) > 7 else None
                    score_str = str(result) if result is not None else ""

                # 填充单元格（对应表头顺序），设置不可编辑
                item0 = QTableWidgetItem(str(kind_name))
                item1 = QTableWidgetItem(str(grade_name))
                item2 = QTableWidgetItem(str(class_name))
                item3 = QTableWidgetItem(str(department_name))
                item4 = QTableWidgetItem(str(major_name))
                item5 = QTableWidgetItem(str(stu_name))
                item6 = QTableWidgetItem(str(sub_name))
                item7 = QTableWidgetItem(score_str)  # 传入处理后的字符串

                # 统一设置单元格不可编辑
                for item in [item0, item1, item2, item3, item4, item5,item6,item7]:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                self.tableWidget.setItem(row_idx, 0, item0)
                self.tableWidget.setItem(row_idx, 1, item1)
                self.tableWidget.setItem(row_idx, 2, item2)
                self.tableWidget.setItem(row_idx, 3, item3)
                self.tableWidget.setItem(row_idx, 4, item4)
                self.tableWidget.setItem(row_idx, 5, item5)  # 成绩列正常显示
                self.tableWidget.setItem(row_idx, 6, item6)
                self.tableWidget.setItem(row_idx, 7, item7)

            # 修复5：表格列宽自适应，避免成绩列被遮挡
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.statusbar.showMessage(f"成功加载 {len(view_results)} 条数据")
        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"错误信息：{str(e)}")
            import traceback
            print(traceback.format_exc())
            self.statusbar.showMessage("数据加载失败")



    def on_refresh_click(self):
        """刷新按钮点击事件：重新加载数据库数据，清空输入框"""
        # 修复3：新增数据库数据重新加载
        self.load_result_data()
        self.clear_input_fields()
        self.statusbar.showMessage("表格已刷新")

    def on_add_click(self):
        """添加按钮点击事件：将输入信息添加到表格"""
        # 获取各控件数据
        exam_type = self.comboBox_exam_type.currentText()
        grade = self.comboBox_grade.currentText()
        cls = self.comboBox_class.currentText()
        department = self.comboBox_depart.currentText()
        major = self.lineEdit_major.text().strip()
        stu_name = self.comboBox_stu_name.currentText()
        subject = self.comboBox_subject.currentText()
        score = self.lineEdit_score.text().strip()

        # 数据校验
        if not score:
            self.statusbar.showMessage("请填写成绩信息")
            return
        if not score.isdigit() or not (0 <= int(score) <= 100):
            self.statusbar.showMessage("成绩请填写0-100的数字")
            return

        # 获取当前表格行数，新增一行
        new_row_idx = self.tableWidget.rowCount()
        self.tableWidget.insertRow(new_row_idx)

        # 填充新增行数据
        row_data = [exam_type, grade, cls,department,major, stu_name, subject, score]
        for col_idx, cell_data in enumerate(row_data):
            item = QTableWidgetItem(cell_data)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tableWidget.setItem(new_row_idx, col_idx, item)

        # 清空输入框
        self.clear_input_fields()
        self.statusbar.showMessage(f"已添加【{stu_name} - {subject}】成绩")

    def on_modify_click(self):
        """修改按钮点击事件：修改选中行的信息"""
        # 获取选中的行
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            self.statusbar.showMessage("请先选中要修改的行")
            return
        selected_row = selected_items[0].row()

        # 获取输入数据
        exam_type = self.comboBox_exam_type.currentText()
        grade = self.comboBox_grade.currentText()
        cls = self.comboBox_class.currentText()
        department = self.comboBox_depart.currentText()
        major = self.lineEdit_major.text().strip()
        stu_name = self.comboBox_stu_name.currentText()
        subject = self.comboBox_subject.currentText()
        score = self.lineEdit_score.text().strip()

        # 数据校验
        if not score:
            self.statusbar.showMessage("请填写成绩信息")
            return
        if not score.isdigit() or not (0 <= int(score) <= 100):
            self.statusbar.showMessage("成绩请填写0-100的数字")
            return

        # 更新选中行数据
        row_data = [exam_type, grade, cls, department,major,stu_name, subject, score]
        for col_idx, cell_data in enumerate(row_data):
            item = QTableWidgetItem(cell_data)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tableWidget.setItem(selected_row, col_idx, item)

        # 清空输入框
        self.clear_input_fields()
        self.statusbar.showMessage(f"已修改第{selected_row + 1}行数据")

    def on_delete_click(self):
        """删除按钮点击事件：删除选中行"""
        # 获取选中的行
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            self.statusbar.showMessage("请先选中要删除的行")
            return
        selected_row = selected_items[0].row()

        # 删除行
        self.tableWidget.removeRow(selected_row)
        self.clear_input_fields()
        self.statusbar.showMessage(f"已删除第{selected_row + 1}行数据")

    def clear_input_fields(self):
        """清空所有输入/选择控件"""
        self.comboBox_exam_type.setCurrentIndex(0)
        self.comboBox_grade.setCurrentIndex(0)
        self.comboBox_class.setCurrentIndex(0)
        self.comboBox_stu_name.setCurrentIndex(0)
        self.comboBox_subject.setCurrentIndex(0)
        self.lineEdit_score.clear()


if __name__ == "__main__":
    # 创建应用实例
    app = QApplication(sys.argv)
    # 创建主窗口实例
    window = MainWindow()
    # 显示窗口
    window.show()
    # 运行应用
    sys.exit(app.exec_())