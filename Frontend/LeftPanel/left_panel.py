"""
左侧面板组件
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QSplitter, QLabel, QSlider, QGroupBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QBrush, QColor


class LeftPanel(QWidget):
    """左侧面板组件"""
    
    # 信号定义
    folder_selected = pyqtSignal(str)  # 文件夹选择信号
    filter_changed = pyqtSignal(str)   # 筛选条件变化信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(100)  # 最小宽度100px
        self.default_width = 200   # 默认宽度200px
        self.resize(self.default_width, 400)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        # 设置样式
        self.setStyleSheet("""
            LeftPanel {
                background-color: #1A1A1A;
                border: none;
            }
        """)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建折叠面板容器
        self.create_navigation_panel(main_layout)
        self.create_filter_panel(main_layout)
        self.create_preview_size_panel(main_layout)
        
        # 添加弹性空间
        main_layout.addStretch()
    
    def create_navigation_panel(self, parent_layout):
        """创建导航面板"""
        # 导航组
        nav_group = QGroupBox("导航")
        nav_group.setStyleSheet(self.get_group_style())
        nav_layout = QVBoxLayout(nav_group)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        
        # 导航树
        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderHidden(True)
        self.nav_tree.setStyleSheet(self.get_tree_style())
        
        # 添加导航项
        self.add_navigation_items()
        
        # 连接信号
        self.nav_tree.itemClicked.connect(self.on_nav_item_clicked)
        
        nav_layout.addWidget(self.nav_tree)
        parent_layout.addWidget(nav_group)
    
    def create_filter_panel(self, parent_layout):
        """创建筛选面板"""
        # 筛选组
        filter_group = QGroupBox("筛选器")
        filter_group.setStyleSheet(self.get_group_style())
        filter_layout = QVBoxLayout(filter_group)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        
        # 按文件类型
        type_group = self.create_filter_type_group()
        filter_layout.addWidget(type_group)
        
        # 按日期
        date_group = self.create_filter_date_group()
        filter_layout.addWidget(date_group)
        
        # 按标签
        tag_group = self.create_filter_tag_group()
        filter_layout.addWidget(tag_group)
        
        parent_layout.addWidget(filter_group)
    
    def create_preview_size_panel(self, parent_layout):
        """创建预览尺寸面板"""
        # 预览尺寸组
        preview_group = QGroupBox("预览尺寸")
        preview_group.setStyleSheet(self.get_group_style())
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(10, 10, 10, 10)
        
        # 尺寸标签
        size_label = QLabel("50px")
        size_label.setStyleSheet(self.get_label_style())
        preview_layout.addWidget(size_label)
        
        # 滑块
        size_slider = QSlider(Qt.Orientation.Horizontal)
        size_slider.setMinimum(50)
        size_slider.setMaximum(500)
        size_slider.setValue(150)
        size_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        size_slider.setTickInterval(50)
        
        # 滑块样式
        size_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #333333;
                border-radius: 2px;
            }
            
            QSlider::handle:horizontal {
                width: 16px;
                height: 16px;
                background: #4A9EFF;
                border-radius: 8px;
                margin: -6px 0;
            }
            
            QSlider::handle:horizontal:hover {
                background: #3B99FF;
            }
        """)
        
        # 更新尺寸标签
        def update_size_label(value):
            size_label.setText(f"{value}px")
            # 这里可以发送信号到中央内容区更新缩略图大小
        
        size_slider.valueChanged.connect(update_size_label)
        preview_layout.addWidget(size_slider)
        
        # 尺寸值标签
        value_label = QLabel("150px")
        value_label.setStyleSheet(self.get_label_style())
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(value_label)
        
        # 连接信号更新值标签
        size_slider.valueChanged.connect(lambda v: value_label.setText(f"{v}px"))
        
        parent_layout.addWidget(preview_group)
    
    def add_navigation_items(self):
        """添加导航项"""
        # 快速访问
        quick_access = QTreeWidgetItem(["快速访问"])
        quick_access.setFont(0, QFont("微软雅黑", 11, QFont.Weight.Bold))
        
        desktop = QTreeWidgetItem(["桌面"])
        documents = QTreeWidgetItem(["文档"])
        pictures = QTreeWidgetItem(["图片"])
        
        quick_access.addChild(desktop)
        quick_access.addChild(documents)
        quick_access.addChild(pictures)
        
        self.nav_tree.addTopLevelItem(quick_access)
        
        # 最近访问
        recent = QTreeWidgetItem(["最近访问"])
        recent.setFont(0, QFont("微软雅黑", 11, QFont.Weight.Bold))
        
        # 添加最近访问的目录（示例）
        for i in range(5):
            item = QTreeWidgetItem([f"文件夹 {i+1}"])
            recent.addChild(item)
        
        self.nav_tree.addTopLevelItem(recent)
        
        # 收藏夹
        favorites = QTreeWidgetItem(["收藏夹"])
        favorites.setFont(0, QFont("微软雅黑", 11, QFont.Weight.Bold))
        
        # 添加收藏夹（示例）
        fav1 = QTreeWidgetItem(["项目 A"])
        fav2 = QTreeWidgetItem(["项目 B"])
        
        favorites.addChild(fav1)
        favorites.addChild(fav2)
        
        self.nav_tree.addTopLevelItem(favorites)
        
        # 展开所有项
        self.nav_tree.expandAll()
        
        # 设置默认选中项
        self.nav_tree.setCurrentItem(pictures)
    
    def create_filter_type_group(self):
        """创建按文件类型筛选组"""
        group = QGroupBox("按文件类型")
        group.setStyleSheet(self.get_group_style())
        layout = QVBoxLayout(group)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 文件类型列表（示例）
        file_types = [
            ("图片 (JPG/PNG/RAW)", True),
            ("视频 (MP4/MOV)", False),
            ("音频", False),
            ("文档", False),
            ("其他", False)
        ]
        
        self.type_checkboxes = []
        for text, checked in file_types:
            checkbox = QLabel(f"▶ {text}")
            checkbox.setStyleSheet(self.get_checkbox_style())
            if checked:
                checkbox.setText(f"▶ {text} ✓")
            checkbox.mousePressEvent = lambda e, cb=checkbox: self.on_type_checkbox_clicked(cb)
            layout.addWidget(checkbox)
            self.type_checkboxes.append(checkbox)
        
        return group
    
    def create_filter_date_group(self):
        """创建按日期筛选组"""
        group = QGroupBox("按日期")
        group.setStyleSheet(self.get_group_style())
        layout = QVBoxLayout(group)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 日期选项
        date_options = ["今天", "昨天", "本周", "本月", "自定义"]
        
        self.date_labels = []
        for option in date_options:
            label = QLabel(f"▶ {option}")
            label.setStyleSheet(self.get_checkbox_style())
            label.mousePressEvent = lambda e, lb=label: self.on_date_label_clicked(lb)
            layout.addWidget(label)
            self.date_labels.append(label)
        
        return group
    
    def create_filter_tag_group(self):
        """创建按标签筛选组"""
        group = QGroupBox("按标签")
        group.setStyleSheet(self.get_group_style())
        layout = QVBoxLayout(group)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 标签选项
        tags = [
            ("红色", "#FF4444"),
            ("黄色", "#FFD700"),
            ("绿色", "#44FF44"),
            ("蓝色", "#4444FF"),
            ("紫色", "#FF44FF"),
            ("自定义", "#CCCCCC")
        ]
        
        self.tag_labels = []
        for name, color in tags:
            label = QLabel(f"▶ {name}")
            label.setStyleSheet(self.get_checkbox_style())
            # 设置标签颜色
            label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    padding: 2px 0;
                }}
            """)
            label.mousePressEvent = lambda e, lb=label: self.on_tag_label_clicked(lb)
            layout.addWidget(label)
            self.tag_labels.append(label)
        
        return group
    
    def on_nav_item_clicked(self, item):
        """导航项点击处理"""
        if item.parent() is None:  # 顶级项
            return
        
        folder_path = item.text(0)
        self.folder_selected.emit(folder_path)
    
    def on_type_checkbox_clicked(self, label):
        """文件类型复选框点击处理"""
        if "✓" in label.text():
            label.setText(label.text().replace(" ✓", ""))
        else:
            label.setText(label.text() + " ✓")
    
    def on_date_label_clicked(self, label):
        """日期标签点击处理"""
        # 清除其他选中状态
        for lb in self.date_labels:
            if "▶" in lb.text():
                lb.setText(lb.text().replace("▶", "  "))
        
        # 设置当前选中
        if "▶" in label.text():
            label.setText(label.text().replace("▶", "  "))
        else:
            label.setText(label.text().replace("  ", "▶"))
        
        # 发送筛选信号
        filter_text = label.text().replace("▶", "").strip()
        self.filter_changed.emit(f"date:{filter_text}")
    
    def on_tag_label_clicked(self, label):
        """标签点击处理"""
        if "✓" in label.text():
            label.setText(label.text().replace(" ✓", ""))
        else:
            label.setText(label.text() + " ✓")
        
        # 发送筛选信号
        filter_text = label.text().replace("▶", "").replace(" ✓", "").strip()
        self.filter_changed.emit(f"tag:{filter_text}")
    
    def get_group_style(self):
        """获取组控件样式"""
        return """
            QGroupBox {
                font-weight: bold;
                color: #FFFFFF;
                border: none;
                padding-top: 10px;
                margin-top: 5px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
    
    def get_tree_style(self):
        """获取树控件样式"""
        return """
            QTreeWidget {
                background-color: #2A2A2A;
                border: none;
                color: #FFFFFF;
                font-size: 12px;
            }
            
            QTreeWidget::item {
                padding: 3px 2px;
            }
            
            QTreeWidget::item:hover {
                background-color: #333333;
            }
            
            QTreeWidget::item:selected {
                background-color: #4A9EFF;
                color: #FFFFFF;
            }
            
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {
                border-image: none;
                image: none;
            }
            
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {
                border-image: none;
                image: none;
            }
        """
    
    def get_label_style(self):
        """获取标签样式"""
        return """
            QLabel {
                color: #CCCCCC;
                font-size: 11px;
                background-color: transparent;
                border: none;
            }
        """
    
    def get_checkbox_style(self):
        """获取复选框样式"""
        return """
            QLabel {
                color: #CCCCCC;
                font-size: 12px;
                background-color: transparent;
                border: none;
                padding: 2px 0;
                cursor: pointer;
            }
            
            QLabel:hover {
                color: #FFFFFF;
                background-color: #2A2A2A;
            }
        """