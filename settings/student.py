import sys
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QTableView, QPushButton, QLineEdit,
    QLabel, QComboBox, QWidget, QTableWidget, QTableWidgetItem,
    QMessageBox, QAbstractItemView
)
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide2.QtGui import QFont
from PySide2 import QtSql  # 补充导入QtSql
from main import DBService

# ========== 修复1：重命名数据模型类，避免和主窗口类冲突 ==========
class MainWindow(QAbstractTableModel):
    def __init__(self, data=[], headers=[]):
        super(StudentTableModel, self).__init__()
        self.service = DBService()  # 关键：用self.service保存实例，全局可用
        self.query = QtSql.QSqlQuery()
        self._data = data  # 表格数据
        self._headers = headers  # 表头
        self.load_student_data()
        self.cboGrade()
        self.cboClass()


    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers) if self._headers else 0

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data) or index.column() >= len(self._headers):
            return None
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section < len(self._headers):
                return self._headers[section]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            if 0 <= index.row() < len(self._data) and 0 <= index.column() < len(self._headers):
                self._data[index.row()][index.column()] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def appendRow(self, row_data):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(row_data)
        self.endInsertRows()

    def removeRow(self, row):
        if 0 <= row < self.rowCount():
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._data[row]
            self.endRemoveRows()
            return True
        return False

    def clear(self):
        """清空表格数据"""
        self.beginResetModel()
        self._data = []
        self.endResetModel()

# ========== 修复2：主窗口类 ==========
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # 1. 初始化数据库服务
        self.service = DBService()
        # 2. 初始化UI
        self.initUI()
        # 3. 加载学生数据
        self.load_student_data()

    def initUI(self):
        # 设置窗口基本属性
        self.setGeometry(0, 0, 900, 900)
        self.setWindowTitle("学生信息管理")

        # 中央部件
        self.central_widget = QWidget()  # 改为实例属性，方便其他方法访问
        self.setCentralWidget(self.central_widget)

        # ========== 顶部控件区域 ==========
        # 年级标签和输入框
        self.label_grade = QLabel("所属年级：", self.central_widget)
        self.label_grade.setGeometry(10, 30, 81, 21)
        self.label_grade.setFont(QFont("", 11))
        self.comboBox_grade = QComboBox(self.central_widget)
        self.comboBox_grade.setGeometry(100, 19, 81, 31)
        self.comboBox_grade.addItems(["大一", "大二","大三", "大四"])

        # 班级标签和输入框
        self.label_class = QLabel("所属班级：", self.central_widget)
        self.label_class.setGeometry(180, 30, 81, 21)
        self.label_class.setFont(QFont("", 11))

        self.lineEdit_class = QLineEdit(self.central_widget)
        self.lineEdit_class.setGeometry(270, 19, 91, 31)

        # 功能按钮
        self.btn_refresh = QPushButton("刷新", self.central_widget)
        self.btn_refresh.setGeometry(370, 20, 75, 31)
        self.btn_refresh.clicked.connect(self.on_refresh_click)

        self.btn_add = QPushButton("添加", self.central_widget)
        self.btn_add.setGeometry(450, 20, 75, 31)
        self.btn_add.clicked.connect(self.on_add_click)

        self.btn_modify = QPushButton("修改", self.central_widget)
        self.btn_modify.setGeometry(530, 20, 75, 31)
        self.btn_modify.clicked.connect(self.on_modify_click)

        self.btn_delete = QPushButton("删除", self.central_widget)
        self.btn_delete.setGeometry(610, 20, 75, 31)
        self.btn_delete.clicked.connect(self.on_delete_click)

        self.btn_quit = QPushButton("退出", self.central_widget)
        self.btn_quit.setGeometry(690, 20, 75, 31)
        self.btn_quit.clicked.connect(self.close)


        # ========== 表格区域：统一使用QTableWidget（更易上手） ==========
        # 修复3：创建QTableWidget并赋值为实例属性
        self.create_table_widget()

        # ========== 底部信息输入区域 ==========
        # 学生编号
        self.label_id = QLabel("学生编号：", self.central_widget)
        self.label_id.setGeometry(10, 420, 91, 21)
        self.label_id.setFont(QFont("", 11))

        self.lineEdit_id = QLineEdit(self.central_widget)
        self.lineEdit_id.setGeometry(100, 409, 81, 31)

        # 学生姓名
        self.label_name = QLabel("学生姓名：", self.central_widget)
        self.label_name.setGeometry(200, 420, 91, 21)
        self.label_name.setFont(QFont("", 11))

        self.lineEdit_name = QLineEdit(self.central_widget)
        self.lineEdit_name.setGeometry(290, 409, 101, 31)

        # 年龄
        self.label_age = QLabel("年龄：", self.central_widget)
        self.label_age.setGeometry(400, 420, 51, 21)
        self.label_age.setFont(QFont("", 11))

        self.lineEdit_age = QLineEdit(self.central_widget)
        self.lineEdit_age.setGeometry(450, 409, 81, 31)

        # 性别
        self.label_gender = QLabel("性别：", self.central_widget)
        self.label_gender.setGeometry(560, 420, 51, 21)
        self.label_gender.setFont(QFont("", 11))

        self.comboBox_gender = QComboBox(self.central_widget)
        self.comboBox_gender.setGeometry(630, 411, 67, 31)
        self.comboBox_gender.addItems(["男", "女"])

        # 联系电话
        self.label_phone = QLabel("联系电话：", self.central_widget)
        self.label_phone.setGeometry(30, 480, 91, 21)
        self.label_phone.setFont(QFont("", 11))

        self.lineEdit_phone = QLineEdit(self.central_widget)
        self.lineEdit_phone.setGeometry(130, 469, 201, 31)

        # 家庭住址
        self.label_address = QLabel("家庭住址：", self.central_widget)
        self.label_address.setGeometry(340, 480, 91, 21)
        self.label_address.setFont(QFont("", 11))

        self.lineEdit_address = QLineEdit(self.central_widget)
        self.lineEdit_address.setGeometry(430, 469, 321, 31)

        self.label_depart= QLabel("所属院系：", self.central_widget)
        self.label_depart.setGeometry(10, 530, 91, 21)
        self.label_depart.setFont(QFont("", 11))
        self.comboBox_depart = QComboBox(self.central_widget)
        self.comboBox_depart.setGeometry(100, 530, 300, 31)
        self.comboBox_depart.addItems(["信息工程学院", "生物工程学院", "文法学院", "艺术学院","外国语学院", "食品工程学院", "经济与管理学院", "机电工程学院"])

        self.label_major = QLabel("所属专业：", self.central_widget)
        self.label_major.setGeometry(10, 580, 91, 21)
        self.label_major.setFont(QFont("", 11))
        self.lineEdit_major = QLineEdit(self.central_widget)
        self.lineEdit_major.setGeometry(100, 580, 300, 31)

    def create_table_widget(self):
        """创建QTableWidget表格控件（实例属性）"""
        self.tableWidget = QTableWidget(self.central_widget)
        self.tableWidget.setGeometry(20, 90, 831, 311)
        # 设置表格属性
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

    def load_student_data(self):
        """加载学生视图数据到QTableWidget（修复列顺序）"""
        try:
            # 1. 执行视图查询（明确指定列顺序，避免依赖SELECT *）
            # 重点：按视图实际列顺序写SQL，确保和视图列一致
            view_sql = """
                   SELECT stuID, stuName, age, sex, phone, address, gradeName, className,departmentName,majorName
                   FROM tb_student ORDER BY stuID;
               """
            view_results = self.service.query(view_sql, )
            # 2. 清空表格
            self.tableWidget.setRowCount(0)
            if len(view_results) == 0:
                QMessageBox.information(self, "提示", "暂无学生视图数据")
                return
            # 3. 设置表格列数和表头（表头顺序不变，但数据映射要对应视图列）
            self.tableWidget.setColumnCount(10)
            headers = ["学生编号", "学生姓名", "年龄", "性别", "电话", "家庭住址", "所属年级", "所属班级","所属院系","所属专业"]
            self.tableWidget.setHorizontalHeaderLabels(headers)
            # 4. 填充表格数据
            for row_idx, row_data in enumerate(view_results):
                self.tableWidget.insertRow(row_idx)
                if isinstance(row_data, dict):

                    stu_id = str(row_data.get("stuID", ""))
                    stu_name = row_data.get("stuName", "")
                    stu_age = str(row_data.get("age", ""))
                    stu_gender = row_data.get("sex", "")
                    stu_phone = row_data.get("phone", "")
                    stu_address = row_data.get("address", "")
                    grade_name = row_data.get("gradeName", "")
                    class_name = row_data.get("className", "")
                    department = row_data.get("departmentName", "")
                    major = row_data.get("majorName", "")
                else:

                    stu_id = str(row_data[0]) if len(row_data) > 0 else ""
                    stu_name = row_data[1] if len(row_data) > 1 else ""
                    stu_age = str(row_data[2]) if (len(row_data) > 2 and row_data[2] is not None) else ""
                    stu_gender = row_data[3] if len(row_data) > 3 else ""
                    stu_phone = row_data[4] if len(row_data) > 4 else ""
                    stu_address = row_data[5] if len(row_data) > 5 else ""
                    grade_name = row_data[6] if len(row_data) > 6 else ""
                    class_name = row_data[7] if len(row_data) > 7 else ""
                    department = row_data[8] if len(row_data) > 8 else ""
                    major = row_data[9] if len(row_data) > 9 else ""

                # 填充单元格（对应表头顺序）
                self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(stu_id))  # 学生编号
                self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(stu_name))  # 学生姓名
                self.tableWidget.setItem(row_idx, 2, QTableWidgetItem(stu_age))  # 年龄
                self.tableWidget.setItem(row_idx, 3, QTableWidgetItem(stu_gender))  # 性别
                self.tableWidget.setItem(row_idx, 4, QTableWidgetItem(stu_phone))  # 电话
                self.tableWidget.setItem(row_idx, 5, QTableWidgetItem(stu_address))  # 家庭住址
                self.tableWidget.setItem(row_idx, 6, QTableWidgetItem(grade_name))
                self.tableWidget.setItem(row_idx, 7, QTableWidgetItem(class_name))
                self.tableWidget.setItem(row_idx, 8, QTableWidgetItem(department))
                self.tableWidget.setItem(row_idx, 9, QTableWidgetItem(major))

        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"错误信息：{str(e)}")
            import traceback
            print(traceback.format_exc())

    def on_refresh_click(self):
        """刷新按钮点击事件"""
        self.load_student_data()  # 重新加载数据
        self.clear_input_fields()
        QMessageBox.information(self, "提示", "数据已刷新")

    def on_add_click(self):
        """添加按钮点击事件（修复：向原始表插入+参数匹配）"""
        # 获取输入框数据
        stu_id = self.lineEdit_id.text().strip()
        name = self.lineEdit_name.text().strip()
        age = self.lineEdit_age.text().strip()
        gender = self.comboBox_gender.currentText()
        phone = self.lineEdit_phone.text().strip()
        address = self.lineEdit_address.text().strip()
        grade = self.comboBox_grade.currentText()
        cls = self.lineEdit_class.text().strip()
        department = self.comboBox_depart.currentText()
        major = self.lineEdit_major.text().strip()

        # 数据校验
        if not all([stu_id, name, age, grade, cls]):
            QMessageBox.warning(self, "提示", "请填写必填字段（编号、姓名、年龄、年级、班级）")
            return


        try:
            # SQL：向原始表tb_student插入，几 个 字段对应 几个?
            insert_sql = """
                INSERT INTO tb_student (stuID, stuName, age, sex, phone, address, gradeName, className,departmentName,majorName)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?);
            """
            # 参数：和?数量完全一致
            params = (stu_id, name, age, gender, phone, address, grade, cls,department,major)
            # 验证参数数量（调试用）
            print(f"SQL占位符数量：{insert_sql.count('?')}，参数数量：{len(params)}")

            self.service.update(insert_sql, params)

            # 刷新表格
            self.load_student_data()
            QMessageBox.information(self, "成功", "学生信息添加成功")
            self.clear_input_fields()
        except Exception as e:
            QMessageBox.critical(self, "添加失败", f"错误信息：{str(e)}")


    def on_modify_click(self):
        """修改按钮点击事件"""
        # 获取选中行
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "选择要修改的行")
            return
        row = self.tableWidget.currentRow()

        # 获取输入框数据
        grade = self.comboBox_grade.currentText()
        cls = self.lineEdit_class.text().strip()
        stu_id = self.lineEdit_id.text().strip()
        name = self.lineEdit_name.text().strip()
        age = self.lineEdit_age.text().strip()
        gender = self.comboBox_gender.currentText()
        phone = self.lineEdit_phone.text().strip()
        address = self.lineEdit_address.text().strip()
        department = self.comboBox_depart.currentText()
        major = self.lineEdit_major.text().strip()

        # 数据校验
        if not all([grade, cls, stu_id, name, age]):
            QMessageBox.warning(self, "提示", "请填写必填字段")
            return

        # 更新数据库和表格
        try:
            update_sql = """
                UPDATE tb_student 
                SET gradeName=?, className=?, stuName=?, age=?, sex=?, phone=?, address=?,department=?, major=?
                WHERE stuID=?;
            """
            self.service.update(update_sql, (grade, cls, name, age, gender, phone, address, stu_id,department, major))
            # 更新表格显示
            self.tableWidget.setItem(row, 0, QTableWidgetItem(stu_id))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(name))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(grade))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(cls))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(age))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(gender))
            self.tableWidget.setItem(row, 6, QTableWidgetItem(phone))
            self.tableWidget.setItem(row, 7, QTableWidgetItem(address))
            self.tableWidget.setItem(row, 8, QTableWidgetItem(department))
            self.tableWidget.setItem(row, 9, QTableWidgetItem(major))

            QMessageBox.information(self, "成功", "学生信息修改成功")
            self.clear_input_fields()
        except Exception as e:
            QMessageBox.critical(self, "修改失败", f"错误信息：{str(e)}")

    def on_delete_click(self):
        """删除按钮点击事件"""
        # 获取选中行
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "选择要删除的行")
            return
        row = self.tableWidget.currentRow()
        stu_id = self.tableWidget.item(row, 0).text()  # 获取选中行的学生编号

        # 确认删除
        reply = QMessageBox.question(self, "确认", f"是否确定删除学生编号{stu_id}的信息？",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # 删除数据库数据
        try:
            delete_sql = "DELETE FROM tb_student WHERE stuID = ?;"
            self.service.update(delete_sql, (stu_id,))
            # 删除表格行
            self.tableWidget.removeRow(row)
            QMessageBox.information(self, "成功", "学生信息删除成功")
            self.clear_input_fields()
        except Exception as e:
            QMessageBox.critical(self, "删除失败", f"错误信息：{str(e)}")

    def clear_input_fields(self):
        """清空所有输入框"""
        self.comboBox_grade.clear()
        self.lineEdit_class.clear()
        self.lineEdit_id.clear()
        self.lineEdit_name.clear()
        self.lineEdit_age.clear()
        self.comboBox_gender.setCurrentIndex(0)
        self.lineEdit_phone.clear()
        self.lineEdit_address.clear()

if __name__ == "__main__":
    # 创建应用程序实例
    app = QApplication(sys.argv)
    # 创建主窗口实例
    window = MainWindow()
    # 显示窗口
    window.show()
    # 运行应用程序
    sys.exit(app.exec_())