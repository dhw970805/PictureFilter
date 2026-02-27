"""
快捷工具栏组件
"""

from PyQt6.QtWidgets import QToolBar, QWidget, QSizePolicy
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, pyqtSignal


class ToolBar(QToolBar):
    """快捷工具栏组件"""
    
    # 定义信号
    refresh_requested = pyqtSignal()  # 刷新请求信号
    screening_requested = pyqtSignal()  # 筛查请求信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)  # 工具栏高度40px
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        # 设置工具栏样式
        self.setStyleSheet("""
            QToolBar {
                background-color: transparent;
                border: none;
                spacing: 4px;
                padding: 4px;
            }
            
            QToolBar::handle {
                width: 0px;
            }
            
            QToolButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                width: 32px;
                height: 32px;
                icon-size: 20px;
            }
            
            QToolButton:hover {
                background-color: #2A2A2A;
            }
            
            QToolButton:pressed {
                background-color: #3A3A3A;
            }
            
            QToolButton:checked {
                background-color: #3A3A3A;
                border: 1px solid #4A9EFF;
            }
        """)
        
        # 添加工具按钮
        self.create_buttons()
    
    def create_buttons(self):
        """创建工具按钮"""
        # 返回按钮
        back_action = QAction("返回", self)
        back_action.setShortcut("Alt+Left")
        back_action.setToolTip("返回上一文件夹 (Alt+←)")
        self.addAction(back_action)
        
        # 前进按钮
        forward_action = QAction("前进", self)
        forward_action.setShortcut("Alt+Right")
        forward_action.setToolTip("前进下一文件夹 (Alt+→)")
        self.addAction(forward_action)
        
        self.addSeparator()
        
        # 刷新按钮
        refresh_action = QAction("刷新", self)
        refresh_action.setShortcut("F5")
        refresh_action.setToolTip("刷新当前目录 (F5)")
        refresh_action.triggered.connect(self.refresh_requested.emit)  # 连接刷新信号
        self.addAction(refresh_action)
        
        self.addSeparator()
        
        # 视图切换按钮
        grid_view_action = QAction("网格视图", self)
        grid_view_action.setShortcut("Ctrl+1")
        grid_view_action.setCheckable(True)
        grid_view_action.setChecked(True)
        grid_view_action.setToolTip("网格视图 (Ctrl+1)")
        self.addAction(grid_view_action)
        
        list_view_action = QAction("列表视图", self)
        list_view_action.setShortcut("Ctrl+2")
        list_view_action.setCheckable(True)
        list_view_action.setToolTip("列表视图 (Ctrl+2)")
        self.addAction(list_view_action)
        
        self.addSeparator()
        
        # 排序按钮
        sort_action = QAction("排序", self)
        sort_action.setShortcut("Ctrl+S")
        sort_action.setToolTip("排序选项 (Ctrl+S)")
        self.addAction(sort_action)
        
        # 筛选按钮
        filter_action = QAction("筛选", self)
        filter_action.setShortcut("Ctrl+F")
        filter_action.setToolTip("打开筛选面板 (Ctrl+F)")
        self.addAction(filter_action)
        
        self.addSeparator()
        
        # 批量处理按钮
        batch_action = QAction("批量处理", self)
        batch_action.setShortcut("Ctrl+B")
        batch_action.setToolTip("批量处理 (Ctrl+B)")
        self.addAction(batch_action)
        
        # 添加弹性空间，将筛查按钮推到最右侧
        self.addSeparator()
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.addWidget(spacer)
        
        # 筛查按钮（最右侧）
        screening_action = QAction("筛查", self)
        screening_action.setToolTip("筛查照片")
        screening_action.triggered.connect(self.screening_requested.emit)  # 连接筛查信号
        self.addAction(screening_action)
    
    def get_action(self, action_name):
        """获取指定的动作"""
        for action in self.actions():
            if action.text() == action_name:
                return action
        return None