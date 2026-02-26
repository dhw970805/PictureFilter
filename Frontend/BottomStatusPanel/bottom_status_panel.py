"""
底部状态栏组件
"""

from PyQt6.QtWidgets import QStatusBar, QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class BottomStatusPanel(QStatusBar):
    """底部状态栏组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(24)
        self.setup_ui()
        
        # 加载状态计时器
        self.load_timer = QTimer()
        self.load_timer.timeout.connect(self.update_load_status)
        self.current_load_count = 0
        self.total_files = 0
    
    def setup_ui(self):
        """设置UI界面"""
        # 设置状态栏样式
        self.setStyleSheet("""
            QStatusBar {
                background-color: #1A1A1A;
                border: none;
                color: #CCCCCC;
                font-size: 11px;
            }
            
            QStatusBar::item {
                border: none;
            }
        """)
        
        # 创建右侧容器
        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 10, 0)
        right_layout.setSpacing(15)
        
        # 当前路径标签
        self.path_label = QLabel("桌面 > 图片")
        self.path_label.setStyleSheet("color: #CCCCCC; font-size: 11px;")
        right_layout.addWidget(self.path_label)
        
        # 文件统计标签
        self.stats_label = QLabel("共 0 个文件，选中 0 个")
        self.stats_label.setStyleSheet("color: #CCCCCC; font-size: 11px;")
        right_layout.addWidget(self.stats_label)
        
        # 预览模式标签
        self.mode_label = QLabel("网格视图 | 缩略图大小：150px")
        self.mode_label.setStyleSheet("color: #CCCCCC; font-size: 11px;")
        right_layout.addWidget(self.mode_label)
        
        # 加载状态标签
        self.load_label = QLabel("")
        self.load_label.setStyleSheet("color: #4A9EFF; font-size: 11px;")
        right_layout.addWidget(self.load_label)
        
        # 添加到状态栏
        self.addPermanentWidget(right_container)
    
    def update_path(self, path):
        """更新当前路径"""
        self.path_label.setText(path)
    
    def update_stats(self, total_files, selected_files=0):
        """更新文件统计"""
        self.stats_label.setText(f"共 {total_files} 个文件，选中 {selected_files} 个")
        self.total_files = total_files
    
    def update_mode(self, view_mode, thumbnail_size=150):
        """更新预览模式"""
        mode_text = f"{view_mode}视图 | 缩略图大小：{thumbnail_size}px"
        self.mode_label.setText(mode_text)
    
    def start_loading(self, total_files):
        """开始加载"""
        self.current_load_count = 0
        self.total_files = total_files
        self.load_label.setText(f"正在加载：0/{total_files}")
        self.load_timer.start(100)  # 每100ms更新一次
    
    def update_load_status(self):
        """更新加载状态"""
        self.current_load_count += 1
        if self.current_load_count <= self.total_files:
            self.load_label.setText(f"正在加载：{self.current_load_count}/{self.total_files}")
            
            if self.current_load_count >= self.total_files:
                self.load_timer.stop()
                self.load_label.setText("加载完成")
                # 3秒后隐藏加载状态
                QTimer.singleShot(3000, lambda: self.load_label.setText(""))
        else:
            self.load_timer.stop()
            self.load_label.setText("加载完成")
            # 3秒后隐藏加载状态
            QTimer.singleShot(3000, lambda: self.load_label.setText(""))
    
    def stop_loading(self):
        """停止加载"""
        self.load_timer.stop()
        self.load_label.setText("加载完成")
        # 3秒后隐藏加载状态
        QTimer.singleShot(3000, lambda: self.load_label.setText(""))