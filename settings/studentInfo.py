import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QComboBox,
                               QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QStatusBar)
from PySide2.QtGui import QFont
# 注意：确保你的 DBService 类能正常工作，提供 query 方法执行SQL查询
from main import DBService  # 根据你的实际路径调整
from PySide2.QtCore import Qt

# 主窗口类（学生信息查询系统）
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initComboBoxData()
        self.service = DBService()
        self.all_student_data = []  # 存储所有学生数据的属性
        self.load_studentInfo_data()

    def initUI(self):
        # 窗口基本属性
        self.setGeometry(100, 100, 900, 700)  # 调整初始位置，避免贴边
        self.setWindowTitle("学生信息查询")

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ========== 查询筛选区域 ==========
        # 选择查询列表标签与下拉框
        self.label_query_type = QLabel("选择查询列表:", central_widget)
        self.label_query_type.setGeometry(10, 20, 130, 31)
        self.label_query_type.setFont(QFont("", 11))
        self.comboBox_query_type = QComboBox(central_widget)
        self.comboBox_query_type.setGeometry(140, 20, 191, 30)

        # 查询关键字标签与下拉框
        self.label_keyword = QLabel("查询关键字:", central_widget)
        self.label_keyword.setGeometry(340, 20, 135, 31)
        self.label_keyword.setFont(QFont("", 11))
        self.comboBox_keyword = QComboBox(central_widget)
        self.comboBox_keyword.setGeometry(450, 20, 180, 30)

        # 功能按钮
        self.btn_query = QPushButton("查询", central_widget)
        self.btn_query.setGeometry(640, 10, 61, 41)
        self.btn_query.clicked.connect(self.on_query_click)

        self.btn_reset = QPushButton("重置", central_widget)  # 新增重置按钮
        self.btn_reset.setGeometry(720, 10, 61, 41)
        self.btn_reset.clicked.connect(self.on_reset_click)

        self.btn_quit = QPushButton("退出", central_widget)
        self.btn_quit.setGeometry(800, 10, 61, 41)
        self.btn_quit.clicked.connect(self.close)

        # ========== 表格显示区域 ==========
        self.tableWidget = QTableWidget(central_widget)
        self.tableWidget.setGeometry(20, 61, 850, 580)  # 加宽表格，适配更多列
        # 设置表格自动调整列宽
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # ========== 状态栏 ==========
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("就绪 - 请选择查询条件后点击查询")

    def initComboBoxData(self):
        """初始化查询下拉框数据"""
        # 查询类型（选择查询列表）
        self.comboBox_query_type.addItems([
            "按年级查询",
            "按班级查询",
            "按姓名查询",
            "按性别查询",
            "按学院查询"
        ])

        # 对应查询关键字（根据查询类型动态匹配，先初始化默认关键字）
        self.keyword_map = {
            "按年级查询": ["大一", "大二", "大三", "大四"],
            "按班级查询": ["一班", "二班", "三班", "四班", "五班", "六班", "七班", "八班", "九班", "十班", "十一班",
                           "十二班"],
            "按姓名查询": ["江离", "江只", "江零", "江林", "江小"],
            "按性别查询": ["男", "女"],
            "按学院查询": ["信息工程学院", "生物工程学院", "文法学院", "艺术学院", "外国语学院", "食品工程学院",
                           "经济与管理学院", "机电工程学院"],
        }

        # 绑定查询类型变化事件，动态更新关键字下拉框
        self.comboBox_query_type.currentTextChanged.connect(self.update_keyword_combo)
        # 初始化默认关键字（按年级查询的关键字）
        self.update_keyword_combo(self.comboBox_query_type.currentText())

    def update_keyword_combo(self, query_type):
        """根据查询类型更新关键字下拉框"""
        self.comboBox_keyword.clear()
        keywords = self.keyword_map.get(query_type, [])
        self.comboBox_keyword.addItems(keywords)

    def load_studentInfo_data(self):
        """加载学生视图数据到QTableWidget，并保存所有数据到属性"""
        try:
            # 1. 执行视图查询（明确指定列顺序）
            view_sql = """
                   SELECT stuID, stuName, age, sex, phone, address, gradeName, className,departmentName,majorName
                   FROM tb_student ORDER BY stuID;
               """
            view_results = self.service.query(view_sql)

            # 2. 保存所有学生数据到实例属性
            self.all_student_data = view_results

            # 3. 填充表格
            self.fill_table_data(view_results)

            if len(view_results) == 0:
                QMessageBox.information(self, "提示", "暂无学生视图数据")
                self.statusbar.showMessage("就绪 - 暂无学生数据")
            else:
                self.statusbar.showMessage(f"就绪 - 共加载 {len(view_results)} 条学生数据")

        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"错误信息：{str(e)}")
            import traceback
            print(traceback.format_exc())

    def fill_table_data(self, data):
        """通用的表格数据填充方法"""
        # 清空表格
        self.tableWidget.setRowCount(0)

        if not data:
            return

        # 设置表格列数和表头
        self.tableWidget.setColumnCount(10)
        headers = ["学生编号", "学生姓名", "年龄", "性别", "电话", "家庭住址", "所属年级", "所属班级", "所属院系",
                   "所属专业"]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # 填充表格数据
        for row_idx, row_data in enumerate(data):
            self.tableWidget.insertRow(row_idx)
            # 确保数据长度足够，避免索引越界
            for col_idx in range(min(len(row_data), 10)):
                item = QTableWidgetItem(str(row_data[col_idx]) if row_data[col_idx] is not None else "")
                item.setTextAlignment(Qt.AlignCenter)  # 文字居中显示
                self.tableWidget.setItem(row_idx, col_idx, item)

    def on_query_click(self):
        """查询按钮点击事件：根据条件筛选数据"""
        # 获取查询条件
        query_type = self.comboBox_query_type.currentText()
        keyword = self.comboBox_keyword.currentText()

        if not keyword:
            self.statusbar.showMessage("请选择查询关键字")
            return

        # 根据查询类型筛选数据（修正列索引）
        filtered_data = []
        for row in self.all_student_data:
            if len(row) < 8:  # 数据完整性校验
                continue

            if query_type == "按年级查询" and row[6] == keyword:  # 年级在第7列（索引6）
                filtered_data.append(row)
            elif query_type == "按班级查询" and row[7] == keyword:  # 班级在第8列（索引7）
                filtered_data.append(row)
            elif query_type == "按姓名查询" and row[1] == keyword:  # 姓名在第2列（索引1）
                filtered_data.append(row)
            elif query_type == "按性别查询" and row[3] == keyword:  # 性别在第4列（索引3）
                filtered_data.append(row)
            elif query_type == "按学院查询" and row[8] == keyword:  # 学院在第9列（索引8）
                filtered_data.append(row)

        # 填充筛选后的数据
        self.fill_table_data(filtered_data)

        # 更新状态栏提示
        if filtered_data:
            self.statusbar.showMessage(f"查询成功 - 共找到 {len(filtered_data)} 条匹配数据")
        else:
            self.statusbar.showMessage("查询结果为空 - 未找到匹配数据")
            QMessageBox.information(self, "查询提示", "未找到匹配的学生信息")

    def on_reset_click(self):
        """重置按钮点击事件：恢复显示所有数据"""
        self.fill_table_data(self.all_student_data)
        # 重置下拉框到默认值
        self.comboBox_query_type.setCurrentIndex(0)
        self.statusbar.showMessage(f"已重置 - 显示所有 {len(self.all_student_data)} 条学生数据")

if __name__ == "__main__":
    # 创建应用实例
    app = QApplication(sys.argv)
    # 创建主窗口实例
    window = MainWindow()
    # 显示窗口
    window.show()
    # 运行应用
    sys.exit(app.exec_())