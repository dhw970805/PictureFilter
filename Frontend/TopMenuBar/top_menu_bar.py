"""
顶部菜单栏组件
"""

from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtCore import Qt
import sys


class TopMenuBar(QMenuBar):
    """顶部菜单栏组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        # 设置字体
        if sys.platform == 'win32':
            font = QFont("微软雅黑", 12)
            self.setStyleSheet(f"""
                QMenuBar {{
                    background-color: #1A1A1A;
                    color: #FFFFFF;
                    border: none;
                }}
                
                QMenuBar::item {{
                    background-color: transparent;
                    padding: 4px 8px;
                    border-radius: 4px;
                }}
                
                QMenuBar::item:selected {{
                    background-color: #4A9EFF;
                    color: #FFFFFF;
                }}
                
                QMenuBar::item:hover {{
                    background-color: #2A2A2A;
                    color: #FFFFFF;
                }}
                
                QMenu {{
                    background-color: #1A1A1A;
                    color: #FFFFFF;
                    border: 1px solid #333333;
                    border-radius: 4px;
                    padding: 4px;
                }}
                
                QMenu::item {{
                    background-color: transparent;
                    padding: 6px 20px 6px 20px;
                    border-radius: 4px;
                    margin: 2px;
                }}
                
                QMenu::item:selected {{
                    background-color: #4A9EFF;
                    color: #FFFFFF;
                }}
                
                QMenu::item:hover {{
                    background-color: #2A2A2A;
                    color: #FFFFFF;
                }}
                
                QMenu::separator {{
                    height: 1px;
                    background-color: #333333;
                    margin: 4px 8px;
                }}
                
                QMenu::indicator:non-exclusive:checked {{
                    image: url();
                    width: 18px;
                    height: 18px;
                    background-color: #4A9EFF;
                    border-radius: 3px;
                }}
                
                QMenu::indicator:exclusive:checked {{
                    image: url();
                    width: 18px;
                    height: 18px;
                    background-color: #4A9EFF;
                    border-radius: 3px;
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
            """)
        else:  # macOS
            font = QFont("SF Pro", 12)
            self.setStyleSheet(f"""
                QMenuBar {{
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                    border: none;
                }}
                
                QMenuBar::item {{
                    background-color: transparent;
                    padding: 4px 8px;
                    border-radius: 4px;
                }}
                
                QMenuBar::item:selected {{
                    background-color: #3B99FF;
                    color: #FFFFFF;
                }}
                
                QMenuBar::item:hover {{
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                }}
                
                QMenu {{
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                    border: 1px solid #3A3A3A;
                    border-radius: 4px;
                    padding: 4px;
                }}
                
                QMenu::item {{
                    background-color: transparent;
                    padding: 6px 20px 6px 20px;
                    border-radius: 4px;
                    margin: 2px;
                }}
                
                QMenu::item:selected {{
                    background-color: #3B99FF;
                    color: #FFFFFF;
                }}
                
                QMenu::item:hover {{
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                }}
                
                QMenu::separator {{
                    height: 1px;
                    background-color: #3A3A3A;
                    margin: 4px 8px;
                }}
                
                QMenu::indicator:non-exclusive:checked {{
                    image: url();
                    width: 18px;
                    height: 18px;
                    background-color: #3B99FF;
                    border-radius: 3px;
                }}
                
                QMenu::indicator:exclusive:checked {{
                    image: url();
                    width: 18px;
                    height: 18px;
                    background-color: #3B99FF;
                    border-radius: 3px;
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
            """)
        
        self.setFont(font)
        
        # 创建菜单
        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.create_filter_menu()
        self.create_tools_menu()
        self.create_help_menu()
    
    def create_file_menu(self):
        """创建文件菜单"""
        file_menu = self.addMenu("文件(&F)")
        
        # 新建文件夹
        new_folder = QAction("新建文件夹(&N)", self)
        new_folder.setShortcut("Ctrl+N")
        file_menu.addAction(new_folder)
        
        file_menu.addSeparator()
        
        # 导入
        import_action = QAction("导入(&I)", self)
        import_action.setShortcut("Ctrl+I")
        file_menu.addAction(import_action)
        
        # 导出
        export_action = QAction("导出(&E)", self)
        export_action.setShortcut("Ctrl+E")
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # 批量重命名
        batch_rename = QAction("批量重命名(&R)", self)
        batch_rename.setShortcut("Ctrl+R")
        file_menu.addAction(batch_rename)
    
    def create_edit_menu(self):
        """创建编辑菜单"""
        edit_menu = self.addMenu("编辑(&E)")
        
        # 复制
        copy_action = QAction("复制(&C)", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)
        
        # 粘贴
        paste_action = QAction("粘贴(&P)", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        # 批量修改
        batch_edit = QAction("批量修改(&B)", self)
        batch_edit.setShortcut("Ctrl+B")
        edit_menu.addAction(batch_edit)
        
        edit_menu.addSeparator()
        
        # 偏好设置
        preferences = QAction("偏好设置(&P)", self)
        preferences.setShortcut("Ctrl+,")
        edit_menu.addAction(preferences)
    
    def create_view_menu(self):
        """创建视图菜单"""
        view_menu = self.addMenu("视图(&V)")
        
        # 列表视图
        list_view = QAction("列表视图(&L)", self)
        list_view.setShortcut("Ctrl+1")
        list_view.setCheckable(True)
        list_view.setChecked(False)
        view_menu.addAction(list_view)
        
        # 网格视图
        grid_view = QAction("网格视图(&G)", self)
        grid_view.setShortcut("Ctrl+2")
        grid_view.setCheckable(True)
        grid_view.setChecked(True)
        view_menu.addAction(grid_view)
        
        # 详情视图
        detail_view = QAction("详情视图(&D)", self)
        detail_view.setShortcut("Ctrl+3")
        detail_view.setCheckable(True)
        detail_view.setChecked(False)
        view_menu.addAction(detail_view)
        
        view_menu.addSeparator()
        
        # 缩放
        zoom_in = QAction("放大(&I)", self)
        zoom_in.setShortcut("Ctrl++")
        view_menu.addAction(zoom_in)
        
        zoom_out = QAction("缩小(&O)", self)
        zoom_out.setShortcut("Ctrl+-")
        view_menu.addAction(zoom_out)
        
        view_menu.addSeparator()
        
        # 面板
        panel_menu = view_menu.addMenu("面板(&P)")
        
        # 左侧面板
        left_panel = QAction("左侧面板(&L)", self)
        left_panel.setCheckable(True)
        left_panel.setChecked(True)
        panel_menu.addAction(left_panel)
        
        # 右侧面板
        right_panel = QAction("右侧面板(&R)", self)
        right_panel.setCheckable(True)
        right_panel.setChecked(True)
        panel_menu.addAction(right_panel)
        
        # 底部状态栏
        status_bar = QAction("底部状态栏(&S)", self)
        status_bar.setCheckable(True)
        status_bar.setChecked(True)
        panel_menu.addAction(status_bar)
        
        panel_menu.addSeparator()
        
        # 重置布局
        reset_layout = QAction("重置布局(&R)", self)
        reset_layout.setShortcut("Ctrl+Shift+R")
        view_menu.addAction(reset_layout)
    
    def create_filter_menu(self):
        """创建筛选菜单"""
        filter_menu = self.addMenu("筛选(&S)")
        
        # 按类型
        type_filter = QAction("按类型(&T)", self)
        type_filter.setShortcut("Ctrl+T")
        filter_menu.addAction(type_filter)
        
        # 按日期
        date_filter = QAction("按日期(&D)", self)
        date_filter.setShortcut("Ctrl+D")
        filter_menu.addAction(date_filter)
        
        # 按大小
        size_filter = QAction("按大小(&S)", self)
        size_filter.setShortcut("Ctrl+Shift+S")
        filter_menu.addAction(size_filter)
        
        # 按标签
        tag_filter = QAction("按标签(&A)", self)
        tag_filter.setShortcut("Ctrl+A")
        filter_menu.addAction(tag_filter)
    
    def create_tools_menu(self):
        """创建工具菜单"""
        tools_menu = self.addMenu("工具(&T)")
        
        # 批量处理
        batch_process = QAction("批量处理(&B)", self)
        batch_process.setShortcut("Ctrl+B")
        tools_menu.addAction(batch_process)
        
        # 元数据编辑
        metadata_edit = QAction("元数据编辑(&M)", self)
        metadata_edit.setShortcut("Ctrl+M")
        tools_menu.addAction(metadata_edit)
        
        tools_menu.addSeparator()
        
        # 插件管理
        plugin_manager = QAction("插件管理(&P)", self)
        plugin_manager.setShortcut("Ctrl+P")
        tools_menu.addAction(plugin_manager)
    
    def create_help_menu(self):
        """创建帮助菜单"""
        help_menu = self.addMenu("帮助(&H)")
        
        # 教程
        tutorial = QAction("教程(&T)", self)
        help_menu.addAction(tutorial)
        
        # 关于
        about = QAction("关于(&A)", self)
        about.setShortcut("F1")
        help_menu.addAction(about)
        
        # 检查更新
        check_update = QAction("检查更新(&C)", self)
        help_menu.addAction(check_update)