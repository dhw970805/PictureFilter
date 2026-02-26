"""
中央内容区组件
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QPixmap, QFont, QCursor, QMouseEvent
import os


class CenterContentArea(QWidget):
    """中央内容区组件"""
    
    # 信号定义
    file_selected = pyqtSignal(str)  # 文件选择信号
    file_opened = pyqtSignal(str)    # 文件打开信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_view = "grid"  # 当前视图模式
        self.thumbnail_size = 150    # 缩略图大小
        self.selected_files = []      # 选中的文件列表
        self.sort_order = {}          # 列表排序状态
        self.grid_columns = 4         # 网格列数
        self.photos_data = []         # 照片数据列表
        self.current_folder_path = None  # 当前文件夹路径
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        # 设置样式
        self.setStyleSheet("""
            CenterContentArea {
                background-color: #1A1A1A;
                border: none;
            }
        """)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建视图切换区域
        self.view_toolbar = self.create_view_toolbar()
        main_layout.addWidget(self.view_toolbar)
        
        # 创建内容区域
        self.content_container = QScrollArea()
        self.content_container.setWidgetResizable(True)
        self.content_container.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.content_container.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 设置滚动条样式
        self.content_container.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollBar:vertical {
                width: 8px;
                background: #2A2A2A;
                border: none;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                height: 8px;
                background: #2A2A2A;
                border: none;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle:horizontal {
                background: #555555;
                min-width: 20px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #777777;
            }
            
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        # 创建内容窗口
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: #1A1A1A;
            }
        """)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(10)
        
        # 设置初始视图
        self.switch_view("grid")
        
        self.content_container.setWidget(self.content_widget)
        main_layout.addWidget(self.content_container)
    
    def create_view_toolbar(self):
        """创建视图工具栏"""
        toolbar = QFrame()
        toolbar.setFixedHeight(36)
        toolbar.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border-bottom: 1px solid #404040;
            }
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(20)
        
        # 视图模式标签
        view_label = QLabel("视图模式:")
        view_label.setStyleSheet("color: #CCCCCC; font-size: 12px;")
        layout.addWidget(view_label)
        
        # 视图切换按钮
        self.grid_btn = self.create_view_button("网格视图", True)
        self.list_btn = self.create_view_button("列表视图", False)
        self.detail_btn = self.create_view_button("详情视图", False)
        
        layout.addWidget(self.grid_btn)
        layout.addWidget(self.list_btn)
        layout.addWidget(self.detail_btn)
        
        layout.addStretch()
        
        # 文件统计标签
        self.stats_label = QLabel("共 0 个文件")
        self.stats_label.setStyleSheet("color: #CCCCCC; font-size: 12px;")
        layout.addWidget(self.stats_label)
        
        return toolbar
    
    def create_view_button(self, text, checked):
        """创建视图切换按钮"""
        btn = QLabel(text)
        btn.setFixedSize(80, 28)
        btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if checked:
            btn.setStyleSheet("""
                QLabel {
                    background-color: #4A9EFF;
                    color: #FFFFFF;
                    font-size: 12px;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)
        else:
            btn.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    color: #CCCCCC;
                    font-size: 12px;
                    border: 1px solid #404040;
                    border-radius: 4px;
                    padding: 5px;
                }
                
                QLabel:hover {
                    background-color: #333333;
                    border-color: #555555;
                }
            """)
        
        # 视图类型映射
        view_mapping = {
            "网格视图": "grid",
            "列表视图": "list",
            "详情视图": "detail"
        }
        
        view_type = view_mapping.get(text)
        if view_type:
            btn.mousePressEvent = lambda e, vt=view_type: self.switch_view(vt)
        
        # 设置光标样式为手型
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn
    
    def switch_view(self, view_type):
        """切换视图模式"""
        self.current_view = view_type
        
        # 更新按钮状态
        if view_type == "grid":
            self._update_button_style(self.grid_btn, True)
            self._update_button_style(self.list_btn, False)
            self._update_button_style(self.detail_btn, False)
        elif view_type == "list":
            self._update_button_style(self.grid_btn, False)
            self._update_button_style(self.list_btn, True)
            self._update_button_style(self.detail_btn, False)
        elif view_type == "detail":
            self._update_button_style(self.grid_btn, False)
            self._update_button_style(self.list_btn, False)
            self._update_button_style(self.detail_btn, True)
        
        # 强制清空内容布局
        self._force_clear_layout()
        
        # 根据视图类型创建相应的内容
        if view_type == "grid":
            self.create_grid_view()
        elif view_type == "list":
            self.create_list_view()
        elif view_type == "detail":
            self.create_detail_view()
    
    def _force_clear_layout(self):
        """强制清空布局"""
        # 逐个移除并删除所有子部件
        items = []
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            items.append(item)
        
        # 删除所有部件
        for item in items:
            if item.widget():
                widget = item.widget()
                # 从布局中移除
                if widget.parent():
                    widget.setParent(None)
                # 删除部件
                widget.deleteLater()
            
            if item.layout():
                layout = item.layout()
                # 递归删除布局中的部件
                while layout.count():
                    sub_item = layout.takeAt(0)
                    if sub_item.widget():
                        sub_widget = sub_item.widget()
                        if sub_widget.parent():
                            sub_widget.setParent(None)
                        sub_widget.deleteLater()
                # 删除布局
                layout.deleteLater()
        
        # 强制更新
        self.content_widget.update()
        self.content_widget.repaint()
    
    def _update_button_style(self, button, is_active):
        """更新按钮样式"""
        if is_active:
            button.setStyleSheet("""
                QLabel {
                    background-color: #4A9EFF;
                    color: #FFFFFF;
                    font-size: 12px;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)
        else:
            button.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    color: #CCCCCC;
                    font-size: 12px;
                    border: 1px solid #404040;
                    border-radius: 4px;
                    padding: 5px;
                }
                
                QLabel:hover {
                    background-color: #333333;
                    border-color: #555555;
                }
            """)
    
    def _clear_content_layout(self):
        """清空内容布局"""
        # 确保删除所有小部件
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                # 确保小部件从父级布局中移除
                if item.widget().parent() == self.content_widget:
                    item.widget().setParent(None)
                item.widget().deleteLater()
        
        # 强制重新布局
        self.content_widget.update()
        self.content_widget.repaint()
    
    def create_grid_view(self):
        """创建网格视图"""
        # 创建主网格布局容器
        grid_container = QFrame()
        grid_container.setStyleSheet("""
            QFrame {
                background-color: #1A1A1A;
            }
        """)
        
        # 创建网格布局
        grid_layout = QVBoxLayout(grid_container)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(0)
        
        # 创建滚动容器
        scroll_container = QScrollArea()
        scroll_container.setWidgetResizable(True)
        scroll_container.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_container.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_container.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollBar:horizontal {
                height: 8px;
                background: #2A2A2A;
                border: none;
            }
            
            QScrollBar::handle:horizontal {
                background: #555555;
                min-width: 20px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #777777;
            }
            
            QScrollBar:vertical {
                width: 8px;
                background: #2A2A2A;
                border: none;
            }
            
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
        """)
        
        # 创建网格内容区域
        grid_content = QWidget()
        grid_content_layout = QVBoxLayout(grid_content)
        grid_content_layout.setContentsMargins(10, 10, 10, 10)
        grid_content_layout.setSpacing(10)
        
        # 创建网格容器，使用QGridLayout实现自动换行
        grid_widget = QWidget()
        grid_widget_layout = QGridLayout(grid_widget)
        grid_widget_layout.setContentsMargins(0, 0, 0, 0)
        grid_widget_layout.setSpacing(10)
        
        # 更新列数（根据缩略图大小）
        self.grid_columns = max(1, 1000 // (self.thumbnail_size + 20))
        
        # 使用实际照片数据或示例数据
        files_to_display = []
        if self.photos_data:
            print(f"🔍 正在处理 {len(self.photos_data)} 张照片的数据")
            for i, photo_data in enumerate(self.photos_data):
                # 检查数据结构
                photo_metadata = photo_data.get("photo_metadata", {})
                if not photo_metadata:
                    print(f"⚠️  照片 {i+1} 缺少 photo_metadata，尝试直接从 photo_data 读取")
                    file_info = photo_data.get("file_info", {})
                else:
                    file_info = photo_metadata.get("file_info", {})
                
                file_path = file_info.get("file_path", "")
                file_name = file_info.get("file_name", "")
                thumbnail_path = file_info.get("thumbnail_path", "")
                
                print(f"  {i+1}. {file_name}")
                print(f"     文件路径: {file_path}")
                print(f"     缩略图路径: {thumbnail_path}")
                
                files_to_display.append((file_path, file_name, thumbnail_path))
            
            print(f"✅ 准备显示 {len(files_to_display)} 张照片")
        else:
            print("ℹ️  没有照片数据，使用示例数据")
            # 使用示例数据
            files_to_display = [
                ("image1.jpg", "风景照片", ""),
                ("image2.png", "产品图片", ""),
                ("image3.jpg", "人物照片", ""),
                ("video1.mp4", "演示视频", ""),
                ("image4.jpg", "建筑照片", ""),
                ("document.pdf", "项目文档", ""),
                ("image5.jpg", "食物照片", ""),
                ("archive.zip", "文件压缩包", ""),
                ("image6.jpg", "动物照片", ""),
                ("image7.jpg", "花朵照片", ""),
                ("image8.jpg", "汽车照片", ""),
                ("image9.jpg", "天空照片", ""),
                ("image10.jpg", "山峰照片", ""),
                ("image11.jpg", "海洋照片", ""),
                ("image12.jpg", "森林照片", "")
            ]
        
        # 添加统计标签
        self.stats_label.setText(f"共 {len(files_to_display)} 个文件")
        
        for i, (file_path, name, thumbnail_path) in enumerate(files_to_display):
            file_item = self.create_grid_item(file_path, name, thumbnail_path)
            row = i // self.grid_columns
            col = i % self.grid_columns
            grid_widget_layout.addWidget(file_item, row, col)
        
        # 添加网格容器到布局
        grid_content_layout.addWidget(grid_widget)
        grid_content_layout.addStretch()
        
        # 设置滚动内容
        scroll_container.setWidget(grid_content)
        grid_layout.addWidget(scroll_container)
        
        # 添加到内容布局
        self.content_layout.addWidget(grid_container)
    
    def create_list_view(self):
        """创建列表视图"""
        # 创建表格
        self.list_table = QTableWidget()
        self.list_table.setColumnCount(6)
        self.list_table.setHorizontalHeaderLabels(["缩略图", "名称", "大小", "修改日期", "类型", "分辨率"])
        self.list_table.horizontalHeader().setStretchLastSection(True)
        self.list_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.list_table.verticalHeader().setVisible(False)
        self.list_table.setAlternatingRowColors(False)
        self.list_table.setStyleSheet("""
            QTableWidget {
                background-color: #2A2A2A;
                border: none;
                gridline-color: #333333;
            }
            
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #333333;
            }
            
            QTableWidget::item:selected {
                background-color: #4A9EFF;
                color: #FFFFFF;
            }
            
            QHeaderView::section {
                background-color: #2A2A2A;
                color: #CCCCCC;
                padding: 5px;
                border: none;
                border-bottom: 1px solid #404040;
                font-weight: normal;
            }
            
            QHeaderView::section:hover {
                background-color: #333333;
            }
            
            QHeaderView::section:pressed {
                background-color: #4A9EFF;
                color: #FFFFFF;
            }
        """)
        
        # 设置行高
        self.list_table.verticalHeader().setDefaultSectionSize(50)
        
        # 添加示例数据
        sample_files = [
            ("image1.jpg", "风景照片.jpg", "2.5 MB", "2024-01-15", "JPG", "1920×1080"),
            ("image2.png", "产品图片.png", "1.8 MB", "2024-01-14", "PNG", "1280×720"),
            ("image3.jpg", "人物照片.jpg", "3.2 MB", "2024-01-13", "JPG", "2560×1440"),
            ("video1.mp4", "演示视频.mp4", "15.6 MB", "2024-01-12", "MP4", "1920×1080"),
            ("image4.jpg", "建筑照片.jpg", "2.1 MB", "2024-01-11", "JPG", "1440×900")
        ]
        
        self.list_table.setRowCount(len(sample_files))
        
        for row, (filename, name, size, date, type_, resolution) in enumerate(sample_files):
            # 缩略图
            thumb_label = QLabel()
            thumb_label.setFixedSize(50, 50)
            thumb_label.setStyleSheet("background-color: #333333; border-radius: 4px;")
            thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            thumb_label.setText("📷")
            
            self.list_table.setCellWidget(row, 0, thumb_label)
            
            # 名称
            name_item = QTableWidgetItem(name)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.list_table.setItem(row, 1, name_item)
            
            # 大小
            size_item = QTableWidgetItem(size)
            size_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.list_table.setItem(row, 2, size_item)
            
            # 修改日期
            date_item = QTableWidgetItem(date)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.list_table.setItem(row, 3, date_item)
            
            # 类型
            type_item = QTableWidgetItem(type_)
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.list_table.setItem(row, 4, type_item)
            
            # 分辨率
            resolution_item = QTableWidgetItem(resolution)
            resolution_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.list_table.setItem(row, 5, resolution_item)
        
        # 连接排序信号
        self.list_table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        
        # 连接选择信号
        self.list_table.itemSelectionChanged.connect(self.on_list_selection_changed)
        
        # 添加到内容布局
        self.content_layout.addWidget(self.list_table)
    
    def create_detail_view(self):
        """创建详情视图"""
        # 创建主布局
        detail_layout = QHBoxLayout()
        detail_layout.setSpacing(20)
        
        # 左侧预览区
        preview_frame = QFrame()
        preview_frame.setFixedWidth(400)
        preview_frame.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border-radius: 4px;
            }
        """)
        
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        
        # 大图预览
        self.preview_image = QLabel()
        self.preview_image.setFixedSize(360, 360)
        self.preview_image.setStyleSheet("background-color: #333333; border-radius: 4px;")
        self.preview_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_image.setText("🖼️\n大图预览")
        
        preview_layout.addWidget(self.preview_image)
        preview_layout.addStretch()
        
        # 右侧信息区
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border-radius: 4px;
            }
        """)
        
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 20, 20, 20)
        
        # 基本信息
        info_group = self.create_info_group("基本信息")
        info_layout.addWidget(info_group)
        
        # 元数据
        metadata_group = self.create_info_group("元数据")
        info_layout.addWidget(metadata_group)
        
        # 标签/评分
        tag_group = self.create_info_group("标签/评分")
        info_layout.addWidget(tag_group)
        
        info_layout.addStretch()
        
        # 添加到布局
        detail_layout.addWidget(preview_frame)
        detail_layout.addWidget(info_frame)
        detail_layout.addStretch()
        
        # 添加到内容布局
        self.content_layout.addLayout(detail_layout)
    
    def create_grid_item(self, file_path, name, thumbnail_path):
        """创建网格视图项"""
        item_frame = QFrame()
        item_frame.setFixedSize(self.thumbnail_size + 20, self.thumbnail_size + 60)
        item_frame.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border-radius: 4px;
                border: 2px solid transparent;
            }
            
            QFrame:hover {
                background-color: #333333;
            }
            
            QFrame:selected {
                border: 2px solid #4A9EFF;
            }
        """)
        
        # 设置右键菜单
        item_frame.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        item_frame.customContextMenuRequested.connect(lambda pos: self.show_grid_context_menu(pos, file_path, item_frame))
        
        item_layout = QVBoxLayout(item_frame)
        item_layout.setContentsMargins(10, 10, 10, 10)
        item_layout.setSpacing(5)
        
        # 缩略图
        thumbnail = QLabel()
        thumbnail.setFixedSize(self.thumbnail_size, self.thumbnail_size)
        thumbnail.setStyleSheet("background-color: #333333; border-radius: 4px;")
        thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 尝试加载缩略图
        if thumbnail_path and os.path.exists(thumbnail_path):
            pixmap = QPixmap(thumbnail_path)
            if not pixmap.isNull():
                # 缩放缩略图以适应显示
                scaled_pixmap = pixmap.scaled(
                    self.thumbnail_size,
                    self.thumbnail_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                thumbnail.setPixmap(scaled_pixmap)
            else:
                self._set_default_thumbnail(thumbnail, file_path)
        else:
            self._set_default_thumbnail(thumbnail, file_path)
        
        item_layout.addWidget(thumbnail)
        
        # 文件名
        name_label = QLabel(name)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: #FFFFFF; font-size: 11px;")
        item_layout.addWidget(name_label)
        
        # 添加点击事件
        item_frame.mousePressEvent = lambda e: self.on_grid_item_clicked(file_path, item_frame, e)
        item_frame.mouseDoubleClickEvent = lambda e: self.on_grid_item_double_clicked(file_path)
        
        return item_frame
    
    def _set_default_thumbnail(self, thumbnail_label, file_path):
        """设置默认缩略图（图标）"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # 根据文件扩展名设置图标
        if file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv']:
            icon = "🎬"
            category = "视频"
        elif file_ext in ['.pdf', '.doc', '.docx', '.txt']:
            icon = "📄"
            category = "文档"
        elif file_ext in ['.zip', '.rar', '.7z', '.tar']:
            icon = "📦"
            category = "其他"
        else:
            icon = "🖼️"
            category = "图片"
        
        thumbnail_label.setText(icon)
        return category
    
    def create_info_group(self, title):
        """创建信息组"""
        group = QFrame()
        group.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border-radius: 4px;
                border: 1px solid #333333;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #4A9EFF; font-size: 12px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 信息项
        if title == "基本信息":
            info_items = [
                ("文件名:", "示例文件.jpg"),
                ("大小:", "2.5 MB"),
                ("格式:", "JPEG"),
                ("分辨率:", "1920×1080"),
                ("创建时间:", "2024-01-15 14:30:00"),
                ("修改时间:", "2024-01-15 15:45:00")
            ]
        elif title == "元数据":
            info_items = [
                ("相机型号:", "Canon EOS 5D Mark IV"),
                ("镜头:", "EF 24-70mm f/2.8L USM"),
                ("光圈:", "f/2.8"),
                ("快门速度:", "1/250s"),
                ("ISO:", "100"),
                ("焦距:", "50mm")
            ]
        else:  # 标签/评分
            info_items = [
                ("标签:", "风景, 户外, 自然"),
                ("评分:", "⭐⭐⭐⭐☆ (4/5)"),
                ("筛选条件:", "无")
            ]
        
        for label_text, value_text in info_items:
            # 标签
            label = QLabel(label_text)
            label.setStyleSheet("color: #CCCCCC; font-size: 11px;")
            layout.addWidget(label)
            
            # 值
            value = QLabel(value_text)
            value.setStyleSheet("color: #FFFFFF; font-size: 11px;")
            layout.addWidget(value)
        
        return group
    
    def show_grid_context_menu(self, pos, filename, item_frame):
        """显示网格项右键菜单"""
        # 创建菜单
        context_menu = QMenu(self)
        
        # 添加菜单项
        open_action = QAction("打开", self)
        open_action.triggered.connect(lambda: self.on_grid_item_double_clicked(filename))
        
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(lambda: print(f"删除文件: {filename}"))
        
        rename_action = QAction("重命名", self)
        rename_action.triggered.connect(lambda: print(f"重命名文件: {filename}"))
        
        select_all_action = QAction("全选", self)
        select_all_action.triggered.connect(self.select_all_files)
        
        deselect_all_action = QAction("取消全选", self)
        deselect_all_action.triggered.connect(self.deselect_all_files)
        
        # 添加菜单项
        context_menu.addAction(open_action)
        context_menu.addSeparator()
        context_menu.addAction(delete_action)
        context_menu.addAction(rename_action)
        context_menu.addSeparator()
        context_menu.addAction(select_all_action)
        context_menu.addAction(deselect_all_action)
        
        # 显示菜单
        global_pos = item_frame.mapToGlobal(pos)
        context_menu.exec(global_pos)
    
    def on_grid_item_clicked(self, filename, item_frame, event):
        """网格项点击处理"""
        # 保存事件用于判断Ctrl键
        self._last_mouse_event = event
        
        # 检查是否按下了Ctrl键（多选）
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # 切换选中状态
            if item_frame.is_grid_item and item_frame.is_selected:
                item_frame.setStyleSheet("""
                    QFrame {
                        background-color: #2A2A2A;
                        border-radius: 4px;
                        border: 2px solid transparent;
                    }
                    
                    QFrame:hover {
                        background-color: #333333;
                    }
                """)
                item_frame.is_selected = False
                if filename in self.selected_files:
                    self.selected_files.remove(filename)
            else:
                item_frame.is_grid_item = True
                item_frame.is_selected = True
                item_frame.setStyleSheet("""
                    QFrame {
                        background-color: #2A2A1A;
                        border-radius: 4px;
                        border: 2px solid #4A9EFF;
                    }
                """)
                if filename not in self.selected_files:
                    self.selected_files.append(filename)
        else:
            # 单选模式
            for child in self.content_widget.findChildren(QFrame):
                if hasattr(child, 'is_grid_item') and child.is_grid_item:
                    child.setStyleSheet("""
                        QFrame {
                            background-color: #2A2A2A;
                            border-radius: 4px;
                            border: 2px solid transparent;
                        }
                        
                        QFrame:hover {
                            background-color: #333333;
                        }
                    """)
                    child.is_selected = False
            
            # 设置当前选中
            item_frame.is_grid_item = True
            item_frame.is_selected = True
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: #2A2A1A;
                    border-radius: 4px;
                    border: 2px solid #4A9EFF;
                }
            """)
            
            # 添加到选中列表
            self.selected_files = [filename]
        
        # 发送信号
        self.file_selected.emit(filename)
    
    def on_grid_item_double_clicked(self, filename):
        """网格项双击处理"""
        self.file_opened.emit(filename)
    
    def on_header_clicked(self, column):
        """表头点击处理 - 列表排序"""
        # 获取当前排序状态
        current_order = self.sort_order.get(column, "none")
        
        # 确定新排序顺序
        if current_order == "none" or current_order == "desc":
            new_order = "asc"
        else:
            new_order = "desc"
        
        # 更新排序状态
        self.sort_order[column] = new_order
        
        # 这里应该根据列进行实际的数据排序
        # 简单实现：切换当前选中项（仅作为演示）
        print(f"按列{column}排序，排序方式: {new_order}")
        
        # 更新表头样式
        header = self.list_table.horizontalHeader()
        for i in range(self.list_table.columnCount()):
            if i == column:
                if new_order == "asc":
                    header.setStyleSheet(f"""
                        QHeaderView::section:{{{i}}} {{
                            background-color: #4A9EFF;
                            color: #FFFFFF;
                            padding: 5px;
                            border: none;
                            border-bottom: 1px solid #404040;
                            font-weight: normal;
                        }}
                    """)
                else:
                    header.setStyleSheet(f"""
                        QHeaderView::section:{{{i}}} {{
                            background-color: #4A9EFF;
                            color: #FFFFFF;
                            padding: 5px;
                            border: none;
                            border-bottom: 1px solid #404040;
                            font-weight: normal;
                        }}
                    """)
            else:
                header.setStyleSheet(f"""
                    QHeaderView::section:{{{i}}} {{
                        background-color: #2A2A2A;
                        color: #CCCCCC;
                        padding: 5px;
                        border: none;
                        border-bottom: 1px solid #404040;
                        font-weight: normal;
                    }}
                """)
    
    def on_list_selection_changed(self):
        """列表选择变化处理"""
        selected_items = self.list_table.selectedItems()
        if selected_items:
            filename = self.list_table.item(selected_items[0].row(), 1).text()
            self.file_selected.emit(filename)
    
    def select_all_files(self):
        """全选文件"""
        if self.current_view == "grid":
            for child in self.content_widget.findChildren(QFrame):
                if hasattr(child, 'is_grid_item'):
                    child.is_grid_item = True
                    child.is_selected = True
                    child.setStyleSheet("""
                        QFrame {
                            background-color: #2A2A1A;
                            border-radius: 4px;
                            border: 2px solid #4A9EFF;
                        }
                    """)
                    if hasattr(child, 'filename') and child.filename not in self.selected_files:
                        self.selected_files.append(child.filename)
    
    def deselect_all_files(self):
        """取消全选"""
        if self.current_view == "grid":
            for child in self.content_widget.findChildren(QFrame):
                if hasattr(child, 'is_grid_item'):
                    child.is_selected = False
                    child.setStyleSheet("""
                        QFrame {
                            background-color: #2A2A2A;
                            border-radius: 4px;
                            border: 2px solid transparent;
                        }
                        
                        QFrame:hover {
                            background-color: #333333;
                        }
                    """)
            self.selected_files = []
    
    def update_thumbnail_size(self, size):
        """更新缩略图大小"""
        self.thumbnail_size = size
        if self.current_view == "grid":
            self.switch_view("grid")
    
    def load_photos(self, folder_path):
        """
        从JSON文件加载照片数据
        
        Args:
            folder_path: 照片文件夹路径
        """
        import json
        from Backend.json_manager import get_json_file_path
        
        print(f"\n📁 load_photos 被调用")
        print(f"   文件夹路径: {folder_path}")
        
        # 保存当前文件夹路径
        self.current_folder_path = folder_path
        
        # 获取JSON文件路径
        json_file_path = get_json_file_path(folder_path)
        
        print(f"   JSON文件路径: {json_file_path}")
        print(f"   JSON文件存在: {os.path.exists(json_file_path)}")
        
        # 读取JSON文件
        self.photos_data = []
        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    photos = data.get('photos', [])
                    self.photos_data = photos
                    print(f"\n✅ 成功加载 {len(photos)} 个照片")
                    
                    if photos:
                        print(f"   第一张照片的keys: {list(photos[0].keys())}")
                        photo_metadata = photos[0].get('photo_metadata', {})
                        if photo_metadata:
                            print(f"   photo_metadata keys: {list(photo_metadata.keys())}")
                            file_info = photo_metadata.get('file_info', {})
                            print(f"   file_info keys: {list(file_info.keys())}")
                            print(f"   thumbnail_path: {file_info.get('thumbnail_path', 'N/A')}")
            except Exception as e:
                print(f"❌ 读取JSON文件失败: {e}")
                import traceback
                traceback.print_exc()
                self.photos_data = []
        else:
            print(f"❌ JSON文件不存在: {json_file_path}")
            self.photos_data = []
        
        print(f"\n📊 photos_data 长度: {len(self.photos_data)}")
        
        # 刷新当前视图
        print("🔄 刷新视图...")
        self.switch_view(self.current_view)
        print("✅ 视图刷新完成\n")
