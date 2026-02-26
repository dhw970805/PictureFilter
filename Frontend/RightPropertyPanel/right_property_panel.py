"""
右侧属性面板组件
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QLineEdit, QPushButton, QGroupBox, QSlider
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import sys


class RightPropertyPanel(QWidget):
    """右侧属性面板组件"""
    
    # 信号定义
    file_info_changed = pyqtSignal(dict)  # 文件信息变化信号
    tag_changed = pyqtSignal(str, str)    # 标签变化信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(200)  # 最小宽度200px
        self.default_width = 300   # 默认宽度300px
        self.resize(self.default_width, 400)
        self.current_file = None
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        # 设置样式
        if sys.platform == 'win32':
            self.setStyleSheet(f"""
                RightPropertyPanel {{
                    background-color: #1A1A1A;
                    border: none;
                }}
            """)
        else:  # macOS
            self.setStyleSheet(f"""
                RightPropertyPanel {{
                    background-color: #1E1E1E;
                    border: none;
                }}
            """)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        if sys.platform == 'win32':
            scroll_area.setStyleSheet(f"""
                QScrollArea {{
                    border: none;
                    background-color: #1A1A1A;
                }}
                
                QScrollBar::vertical {{
                    width: 8px;
                    background: #2A2A2A;
                    border: none;
                    margin: 0px 0px 0px 0px;
                }}
                
                QScrollBar::handle:vertical {{
                    background: #555555;
                    min-height: 20px;
                    border-radius: 4px;
                }}
                
                QScrollBar::handle:vertical:hover {{
                    background: #777777;
                }}
                
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}
            """)
        else:  # macOS
            scroll_area.setStyleSheet(f"""
                QScrollArea {{
                    border: none;
                    background-color: #1E1E1E;
                }}
                
                QScrollBar::vertical {{
                    width: 8px;
                    background: #2E2E2E;
                    border: none;
                    margin: 0px 0px 0px 0px;
                }}
                
                QScrollBar::handle:vertical {{
                    background: #555555;
                    min-height: 20px;
                    border-radius: 4px;
                }}
                
                QScrollBar::handle:vertical:hover {{
                    background: #777777;
                }}
                
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}
            """)
        
        # 创建内容窗口
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(16)  # 模块间距16px
        
        # 创建各个模块
        self.basic_info_group = self.create_basic_info_group()
        content_layout.addWidget(self.basic_info_group)
        
        self.metadata_group = self.create_metadata_group()
        content_layout.addWidget(self.metadata_group)
        
        self.tag_rating_group = self.create_tag_rating_group()
        content_layout.addWidget(self.tag_rating_group)
        
        self.quick_edit_group = self.create_quick_edit_group()
        content_layout.addWidget(self.quick_edit_group)
        
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
    
    def create_basic_info_group(self):
        """创建基本信息模块"""
        group = QGroupBox("基本信息")
        
        if sys.platform == 'win32':
            group.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #FFFFFF;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1A1A1A;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)
        else:  # macOS
            group.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #F5F5F7;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1E1E1E;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # 基本信息
        basic_info = [
            ("文件名:", "未选择文件"),
            ("大小:", "--"),
            ("格式:", "--"),
            ("分辨率:", "--"),
            ("修改日期:", "--")
        ]
        
        self.basic_info_labels = {}
        for label_text, value_text in basic_info:
            # 标签行布局
            row_layout = QHBoxLayout()
            
            # 标签 - 根据设计规范使用次级文字颜色
            label = QLabel(label_text)
            label.setStyleSheet("color: #CCCCCC; font-size: 12px;")
            label.setFixedWidth(60)
            row_layout.addWidget(label)
            
            # 值 - 根据设计规范使用主文字颜色
            value = QLabel(value_text)
            value.setStyleSheet("color: #FFFFFF; font-size: 12px;")
            value.setWordWrap(True)
            row_layout.addWidget(value)
            
            layout.addLayout(row_layout)
            
            # 保存引用
            self.basic_info_labels[label_text.replace(":", "")] = value
        
        return group
    
    def create_metadata_group(self):
        """创建元数据模块"""
        group = QGroupBox("元数据")
        
        if sys.platform == 'win32':
            group.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #FFFFFF;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1A1A1A;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)
        else:  # macOS
            group.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #F5F5F7;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1E1E1E;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # EXIF信息
        exif_section = self.create_exif_section()
        layout.addWidget(exif_section)
        
        # GPS信息
        gps_section = self.create_gps_section()
        layout.addWidget(gps_section)
        
        return group
    
    def create_exif_section(self):
        """创建EXIF信息部分"""
        frame = QFrame()
        
        if sys.platform == 'win32':
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #1E1E1E;
                    border-radius: 4px;
                    border: 1px solid #333333;
                }}
            """)
        else:  # macOS
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #252525;
                    border-radius: 4px;
                    border: 1px solid #3A3A3A;
                }}
            """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # 标题
        title = QLabel("EXIF信息")
        title.setStyleSheet("color: #4A9EFF; font-size: 11px; font-weight: bold;")
        layout.addWidget(title)
        
        # EXIF信息项
        exif_info = [
            ("相机型号:", "Canon EOS 5D Mark IV"),
            ("镜头:", "EF 24-70mm f/2.8L USM"),
            ("光圈:", "f/2.8"),
            ("快门速度:", "1/250s"),
            ("ISO:", "100"),
            ("焦距:", "50mm"),
            ("白平衡:", "自动")
        ]
        
        self.exif_labels = {}
        for label_text, value_text in exif_info:
            # 标签行布局
            row_layout = QHBoxLayout()
            
            # 标签 - 使用次级文字颜色
            label = QLabel(label_text)
            label.setStyleSheet("color: #CCCCCC; font-size: 11px;")
            label.setFixedWidth(70)
            row_layout.addWidget(label)
            
            # 值 - 使用主文字颜色
            value = QLabel(value_text)
            value.setStyleSheet("color: #FFFFFF; font-size: 11px;")
            value.setWordWrap(True)
            row_layout.addWidget(value)
            
            layout.addLayout(row_layout)
            
            # 保存引用
            self.exif_labels[label_text.replace(":", "")] = value
        
        return frame
    
    def create_gps_section(self):
        """创建GPS信息部分"""
        frame = QFrame()
        
        if sys.platform == 'win32':
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #1E1E1E;
                    border-radius: 4px;
                    border: 1px solid #333333;
                }}
            """)
        else:  # macOS
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #252525;
                    border-radius: 4px;
                    border: 1px solid #3A3A3A;
                }}
            """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # 标题
        title = QLabel("GPS信息")
        title.setStyleSheet("color: #4A9EFF; font-size: 11px; font-weight: bold;")
        layout.addWidget(title)
        
        # GPS信息项
        gps_info = [
            ("纬度:", "39.9042° N"),
            ("经度:", "116.4074° E"),
            ("海拔:", "43.5m"),
            ("精度:", "±5m")
        ]
        
        self.gps_labels = {}
        for label_text, value_text in gps_info:
            # 标签行布局
            row_layout = QHBoxLayout()
            
            # 标签 - 使用次级文字颜色
            label = QLabel(label_text)
            label.setStyleSheet("color: #CCCCCC; font-size: 11px;")
            label.setFixedWidth(70)
            row_layout.addWidget(label)
            
            # 值 - 使用主文字颜色
            value = QLabel(value_text)
            value.setStyleSheet("color: #FFFFFF; font-size: 11px;")
            value.setWordWrap(True)
            row_layout.addWidget(value)
            
            layout.addLayout(row_layout)
            
            # 保存引用
            self.gps_labels[label_text.replace(":", "")] = value
        
        return frame
    
    def create_tag_rating_group(self):
        """创建标签/评分模块"""
        group = QGroupBox("标签/评分")
        
        if sys.platform == 'win32':
            group.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #FFFFFF;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1A1A1A;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)
        else:  # macOS
            group.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #F5F5F7;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1E1E1E;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # 评分部分
        rating_frame = QFrame()
        
        if sys.platform == 'win32':
            rating_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #1E1E1E;
                    border-radius: 4px;
                    border: 1px solid #333333;
                }}
            """)
        else:  # macOS
            rating_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #252525;
                    border-radius: 4px;
                    border: 1px solid #3A3A3A;
                }}
            """)
        
        rating_layout = QVBoxLayout(rating_frame)
        rating_layout.setContentsMargins(12, 12, 12, 12)
        
        # 评分标题
        rating_title = QLabel("评分")
        rating_title.setStyleSheet("color: #4A9EFF; font-size: 11px; font-weight: bold;")
        rating_layout.addWidget(rating_title)
        
        # 评分滑块
        self.rating_slider = QSlider(Qt.Orientation.Horizontal)
        self.rating_slider.setMinimum(1)
        self.rating_slider.setMaximum(5)
        self.rating_slider.setValue(3)
        self.rating_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.rating_slider.setTickInterval(1)
        
        self.rating_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 4px;
                background: #333333;
                border-radius: 2px;
            }}
            
            QSlider::handle:horizontal {{
                width: 16px;
                height: 16px;
                background: #FFD700;
                border-radius: 8px;
                margin: -6px 0;
            }}
            
            QSlider::handle:horizontal:hover {{
                background: #FFA500;
            }}
        """)
        
        # 评分显示
        self.rating_display = QLabel("⭐⭐⭐")
        self.rating_display.setStyleSheet("color: #FFFFFF; font-size: 14px; text-align: center;")
        self.rating_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 连接信号
        self.rating_slider.valueChanged.connect(self.on_rating_changed)
        
        rating_layout.addWidget(self.rating_slider)
        rating_layout.addWidget(self.rating_display)
        layout.addWidget(rating_frame)
        
        # 标签部分
        tags_frame = QFrame()
        
        if sys.platform == 'win32':
            tags_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #1E1E1E;
                    border-radius: 4px;
                    border: 1px solid #333333;
                }}
            """)
        else:  # macOS
            tags_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #252525;
                    border-radius: 4px;
                    border: 1px solid #3A3A3A;
                }}
            """)
        
        tags_layout = QVBoxLayout(tags_frame)
        tags_layout.setContentsMargins(12, 12, 12, 12)
        
        # 标题
        tags_title = QLabel("标签")
        tags_title.setStyleSheet("color: #4A9EFF; font-size: 11px; font-weight: bold;")
        tags_layout.addWidget(tags_title)
        
        # 标签网格
        tags_layout_grid = QHBoxLayout()
        tags_layout_grid.setSpacing(8)
        
        # 预设标签
        preset_tags = [
            ("红色", "#FF4444", "🔴"),
            ("黄色", "#FFD700", "🟡"),
            ("绿色", "#44FF44", "🟢"),
            ("蓝色", "#4444FF", "🔵"),
            ("紫色", "#FF44FF", "🟣"),
            ("自定义", "#CCCCCC", "⚙️")
        ]
        
        self.tag_buttons = []
        for name, color, icon in preset_tags:
            tag_btn = QPushButton(f"{icon} {name}")
            tag_btn.setFixedSize(70, 28)
            
            if sys.platform == 'win32':
                tag_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: #FFFFFF;
                        border: none;
                        border-radius: 4px;
                        font-size: 10px;
                        font-weight: bold;
                    }}
                    
                    QPushButton:hover {{
                        opacity: 0.8;
                    }}
                    
                    QPushButton:pressed {{
                        opacity: 0.6;
                    }}
                    
                    QPushButton:checked {{
                        border: 2px solid #FFFFFF;
                    }}
                """)
            else:  # macOS
                tag_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: #FFFFFF;
                        border: none;
                        border-radius: 4px;
                        font-size: 10px;
                        font-weight: bold;
                    }}
                    
                    QPushButton:hover {{
                        opacity: 0.8;
                    }}
                    
                    QPushButton:pressed {{
                        opacity: 0.6;
                    }}
                    
                    QPushButton:checked {{
                        border: 2px solid #FFFFFF;
                    }}
                """)
            
            tag_btn.setCheckable(True)
            
            # 连接信号
            tag_btn.clicked.connect(lambda checked, n=name: self.on_tag_clicked(n, checked))
            
            tags_layout_grid.addWidget(tag_btn)
            self.tag_buttons.append(tag_btn)
        
        tags_layout.addLayout(tags_layout_grid)
        layout.addWidget(tags_frame)
        
        return group
    
    def create_quick_edit_group(self):
        """创建快速编辑模块"""
        group = QGroupBox("快速编辑")
        
        if sys.platform == 'win32':
            group.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #FFFFFF;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1A1A1A;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)
        else:  # macOS
            group.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #F5F5F7;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1E1E1E;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # 旋转按钮
        rotate_layout = QHBoxLayout()
        rotate_layout.setSpacing(8)
        
        rotate_left_btn = QPushButton("↺ 左转90°")
        rotate_left_btn.setFixedSize(100, 32)
        
        if sys.platform == 'win32':
            rotate_left_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #404040;
                    border-radius: 4px;
                    font-size: 11px;
                }}
                
                QPushButton:hover {{
                    background-color: #404040;
                    border-color: #555555;
                }}
                
                QPushButton:pressed {{
                    background-color: #2A2A2A;
                }}
            """)
        else:  # macOS
            rotate_left_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #3A3A3A;
                    color: #FFFFFF;
                    border: 1px solid #4A4A4A;
                    border-radius: 4px;
                    font-size: 11px;
                }}
                
                QPushButton:hover {{
                    background-color: #4A4A4A;
                    border-color: #555555;
                }}
                
                QPushButton:pressed {{
                    background-color: #2E2E2E;
                }}
            """)
        
        rotate_layout.addWidget(rotate_left_btn)
        
        rotate_right_btn = QPushButton("↻ 右转90°")
        rotate_right_btn.setFixedSize(100, 32)
        
        if sys.platform == 'win32':
            rotate_right_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #404040;
                    border-radius: 4px;
                    font-size: 11px;
                }}
                
                QPushButton:hover {{
                    background-color: #404040;
                    border-color: #555555;
                }}
                
                QPushButton:pressed {{
                    background-color: #2A2A2A;
                }}
            """)
        else:  # macOS
            rotate_right_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #3A3A3A;
                    color: #FFFFFF;
                    border: 1px solid #4A4A4A;
                    border-radius: 4px;
                    font-size: 11px;
                }}
                
                QPushButton:hover {{
                    background-color: #4A4A4A;
                    border-color: #555555;
                }}
                
                QPushButton:pressed {{
                    background-color: #2E2E2E;
                }}
            """)
        
        rotate_layout.addWidget(rotate_right_btn)
        
        layout.addLayout(rotate_layout)
        
        # 裁剪按钮
        crop_btn = QPushButton("✂️ 裁剪")
        crop_btn.setFixedSize(210, 32)
        
        if sys.platform == 'win32':
            crop_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #404040;
                    border-radius: 4px;
                    font-size: 11px;
                }}
                
                QPushButton:hover {{
                    background-color: #404040;
                    border-color: #555555;
                }}
                
                QPushButton:pressed {{
                    background-color: #2A2A2A;
                }}
            """)
        else:  # macOS
            crop_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #3A3A3A;
                    color: #FFFFFF;
                    border: 1px solid #4A4A4A;
                    border-radius: 4px;
                    font-size: 11px;
                }}
                
                QPushButton:hover {{
                    background-color: #4A4A4A;
                    border-color: #555555;
                }}
                
                QPushButton:pressed {{
                    background-color: #2E2E2E;
                }}
            """)
        
        layout.addWidget(crop_btn)
        
        # 备注区域
        notes_label = QLabel("备注:")
        notes_label.setStyleSheet("color: #CCCCCC; font-size: 12px;")
        layout.addWidget(notes_label)
        
        self.notes_text = QLineEdit()
        self.notes_text.setPlaceholderText("添加备注...")
        
        if sys.platform == 'win32':
            self.notes_text.setStyleSheet(f"""
                QLineEdit {{
                    background-color: #2A2A2A;
                    color: #FFFFFF;
                    border: 1px solid #404040;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 12px;
                }}
                
                QLineEdit:focus {{
                    border-color: #4A9EFF;
                }}
            """)
        else:  # macOS
            self.notes_text.setStyleSheet(f"""
                QLineEdit {{
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                    border: 1px solid #4A4A4A;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 12px;
                }}
                
                QLineEdit:focus {{
                    border-color: #3B99FF;
                }}
            """)
        
        # 连接信号
        self.notes_text.textChanged.connect(self.on_notes_changed)
        
        layout.addWidget(self.notes_text)
        
        return group
    
    def update_file_info(self, file_info):
        """更新文件信息"""
        self.current_file = file_info
        
        # 更新基本信息
        if "name" in file_info:
            self.basic_info_labels["文件名"].setText(file_info["name"])
        if "size" in file_info:
            self.basic_info_labels["大小"].setText(file_info["size"])
        if "format" in file_info:
            self.basic_info_labels["格式"].setText(file_info["format"])
        if "resolution" in file_info:
            self.basic_info_labels["分辨率"].setText(file_info["resolution"])
        if "date" in file_info:
            self.basic_info_labels["修改日期"].setText(file_info["date"])
        
        # 更新EXIF信息
        if "exif" in file_info:
            exif_data = file_info["exif"]
            if "camera" in exif_data:
                self.exif_labels["相机型号"].setText(exif_data["camera"])
            if "lens" in exif_data:
                self.exif_labels["镜头"].setText(exif_data["lens"])
            if "aperture" in exif_data:
                self.exif_labels["光圈"].setText(exif_data["aperture"])
            if "shutter" in exif_data:
                self.exif_labels["快门速度"].setText(exif_data["shutter"])
            if "iso" in exif_data:
                self.exif_labels["ISO"].setText(exif_data["iso"])
            if "focal_length" in exif_data:
                self.exif_labels["焦距"].setText(exif_data["focal_length"])
            if "wb" in exif_data:
                self.exif_labels["白平衡"].setText(exif_data["wb"])
        
        # 更新GPS信息
        if "gps" in file_info:
            gps_data = file_info["gps"]
            if "lat" in gps_data:
                self.gps_labels["纬度"].setText(gps_data["lat"])
            if "lon" in gps_data:
                self.gps_labels["经度"].setText(gps_data["lon"])
            if "altitude" in gps_data:
                self.gps_labels["海拔"].setText(gps_data["altitude"])
            if "accuracy" in gps_data:
                self.gps_labels["精度"].setText(gps_data["accuracy"])
        
        # 更新备注
        if "notes" in file_info:
            self.notes_text.setText(file_info["notes"])
    
    def on_rating_changed(self, value):
        """评分变化处理"""
        stars = "⭐" * value
        self.rating_display.setText(stars)
        
        # 发送信号
        file_info = self.current_file or {}
        file_info["rating"] = value
        self.file_info_changed.emit(file_info)
    
    def on_tag_clicked(self, tag_name, checked):
        """标签点击处理"""
        # 发送信号
        file_info = self.current_file or {}
        if "tags" not in file_info:
            file_info["tags"] = []
        
        if checked:
            if tag_name not in file_info["tags"]:
                file_info["tags"].append(tag_name)
        else:
            if tag_name in file_info["tags"]:
                file_info["tags"].remove(tag_name)
        
        self.file_info_changed.emit(file_info)
    
    def on_notes_changed(self, text):
        """备注变化处理"""
        if self.current_file:
            self.current_file["notes"] = text
            self.file_info_changed.emit(self.current_file)
    
    def get_group_style(self):
        """获取组控件样式"""
        if sys.platform == 'win32':
            return f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #FFFFFF;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1A1A1A;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """
        else:  # macOS
            return f"""
                QGroupBox {{
                    font-weight: bold;
                    color: #F5F5F7;
                    border: none;
                    padding-top: 10px;
                    margin-top: 5px;
                    background-color: #1E1E1E;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """