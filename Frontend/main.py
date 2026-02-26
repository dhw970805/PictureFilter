#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主应用程序入口
根据FrontEndImplement.md设计实现图片过滤工具的用户界面
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QSizePolicy
from PyQt6.QtCore import Qt

from TopMenuBar.top_menu_bar import TopMenuBar
from ToolBar.tool_bar import ToolBar
from LeftPanel.left_panel import LeftPanel
from CenterContentArea.center_content_area import CenterContentArea
from RightPropertyPanel.right_property_panel import RightPropertyPanel
from BottomStatusPanel.bottom_status_panel import BottomStatusPanel


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("PictureFilter - 图片过滤工具")
        self.setMinimumSize(1280, 720)  # 最低分辨率1280×720
        
        # 设置应用程序信息
        self.application = QApplication.instance()
        if self.application:
            self.application.setApplicationName("PictureFilter")
            self.application.setApplicationVersion("1.0.0")
        
        # 创建主界面
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建顶部布局（包含工具栏）
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        
        # 添加菜单栏
        self.top_menu_bar = TopMenuBar()
        self.setMenuBar(self.top_menu_bar)
        
        # 添加工具栏
        self.tool_bar = ToolBar()
        top_layout.addWidget(self.tool_bar)
        
        # 创建分割器用于调整左侧面板、中央内容区和右侧面板的大小
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)  # 防止面板被完全折叠
        
        # 添加左侧面板
        self.left_panel = LeftPanel()
        self.left_panel.setMinimumWidth(100)  # 左侧面板最小宽度
        splitter.addWidget(self.left_panel)
        
        # 添加中央内容区
        self.center_content_area = CenterContentArea()
        self.center_content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        splitter.addWidget(self.center_content_area)
        
        # 添加右侧属性面板
        self.right_property_panel = RightPropertyPanel()
        self.right_property_panel.setMinimumWidth(200)  # 右侧面板最小宽度
        splitter.addWidget(self.right_property_panel)
        
        # 设置初始比例 (左侧:中央:右侧 = 1:8:1)
        splitter.setStretchFactor(0, 1)  # 左侧面板
        splitter.setStretchFactor(1, 8)  # 中央内容区
        splitter.setStretchFactor(2, 1)  # 右侧面板
        
        # 添加分割器到顶部布局
        top_layout.addWidget(splitter)
        
        # 创建底部布局
        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        
        # 添加状态栏
        self.bottom_status_bar = BottomStatusPanel()
        self.setStatusBar(self.bottom_status_bar)
        
        # 组合布局
        main_layout.addLayout(top_layout)
        
        # 连接信号
        self.connect_signals()
    
    def connect_signals(self):
        """连接组件信号"""
        # 连接中央内容区信号
        self.center_content_area.file_selected.connect(self.on_file_selected)
        self.center_content_area.file_opened.connect(self.on_file_opened)
        
        # 连接左侧面板信号
        self.left_panel.folder_selected.connect(self.on_folder_selected)
        self.left_panel.filter_changed.connect(self.on_filter_changed)
        
        # 连接右侧属性面板信号
        self.right_property_panel.file_info_changed.connect(self.on_file_info_changed)
        
        # 连接工具栏视图切换信号
        grid_action = self.tool_bar.get_action("网格视图")
        if grid_action:
            grid_action.triggered.connect(lambda: self.center_content_area.switch_view("grid"))
        
        list_action = self.tool_bar.get_action("列表视图")
        if list_action:
            list_action.triggered.connect(lambda: self.center_content_area.switch_view("list"))
    
    def on_file_selected(self, filename):
        """文件选择处理"""
        print(f"选中文件: {filename}")
        
        # 更新状态栏
        self.bottom_status_bar.update_stats(8, 1)  # 假设有8个文件，选中1个
        
        # 更新右侧属性面板
        file_info = {
            "name": filename,
            "size": "2.5 MB",
            "format": "JPG",
            "resolution": "1920×1080",
            "date": "2024-01-15",
            "exif": {
                "camera": "Canon EOS 5D Mark IV",
                "lens": "EF 24-70mm f/2.8L USM",
                "aperture": "f/2.8",
                "shutter": "1/250s",
                "iso": "100",
                "focal_length": "50mm",
                "wb": "自动"
            },
            "gps": {
                "lat": "39.9042° N",
                "lon": "116.4074° E",
                "altitude": "43.5m",
                "accuracy": "±5m"
            }
        }
        self.right_property_panel.update_file_info(file_info)
    
    def on_file_opened(self, filename):
        """文件打开处理"""
        print(f"打开文件: {filename}")
    
    def on_folder_selected(self, folder_path):
        """文件夹选择处理"""
        print(f"选择文件夹: {folder_path}")
        self.bottom_status_bar.update_path(f"桌面 > {folder_path}")
    
    def on_filter_changed(self, filter_text):
        """筛选条件变化处理"""
        print(f"筛选条件变化: {filter_text}")
    
    def on_file_info_changed(self, file_info):
        """文件信息变化处理"""
        print(f"文件信息更新: {file_info}")


def main():
    """主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 设置应用程序样式表
    app.setStyleSheet("""
        QMainWindow {
            background-color: #000000;
        }
        
        QWidget {
            color: #FFFFFF;
        }
    """)
    
    # 创建主窗口
    window = MainWindow()
    
    # 显示主窗口
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()