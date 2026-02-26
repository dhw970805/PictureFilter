#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主应用程序入口
根据FrontEndImplement.md设计实现图片过滤工具的用户界面
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QSizePolicy, QFileDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# 添加 Backend 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from TopMenuBar.top_menu_bar import TopMenuBar
from ToolBar.tool_bar import ToolBar
from LeftPanel.left_panel import LeftPanel
from CenterContentArea.center_content_area import CenterContentArea
from RightPropertyPanel.right_property_panel import RightPropertyPanel
from BottomStatusPanel.bottom_status_panel import BottomStatusPanel


class ImportWorker(QThread):
    """
    后台导入工作线程
    """
    progress_updated = pyqtSignal(dict)
    import_completed = pyqtSignal(dict)
    
    def __init__(self, folder_path, recursive=False):
        super().__init__()
        self.folder_path = folder_path
        self.recursive = recursive
    
    def run(self):
        """执行导入操作"""
        from Backend import import_folder
        
        def progress_callback(progress):
            self.progress_updated.emit(progress)
        
        result = import_folder(
            folder_path=self.folder_path,
            recursive=self.recursive,
            skip_existing=True,
            progress_callback=progress_callback
        )
        
        self.import_completed.emit(result)


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
        
        # 导入工作线程
        self.import_worker = None
        
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
        # 连接菜单栏导入信号
        self.top_menu_bar.import_folder_requested.connect(self.on_import_folder_requested)
        
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
    
    def on_import_folder_requested(self):
        """导入文件夹请求处理"""
        # 如果正在导入，则忽略
        if self.import_worker and self.import_worker.isRunning():
            return
        
        # 选择文件夹
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择照片文件夹",
            ""
        )
        
        if not folder_path:
            return
        
        # 更新状态栏
        self.bottom_status_bar.update_path(f"导入: {folder_path}")
        # 使用 load_label 显示导入状态
        self.bottom_status_bar.load_label.setText("正在导入...")
        
        # 创建并启动导入工作线程
        self.import_worker = ImportWorker(folder_path, recursive=True)
        self.import_worker.progress_updated.connect(self.on_import_progress)
        self.import_worker.import_completed.connect(self.on_import_completed)
        self.import_worker.start()
    
    def on_import_progress(self, progress):
        """导入进度更新"""
        percentage = progress.get('percentage', 0)
        imported = progress.get('imported', 0)
        errors = progress.get('errors', 0)
        total = progress.get('total', 0)
        
        # 更新状态栏
        status_text = f"导入中: {int(percentage)}% ({imported}/{total} 已导入, {errors} 错误)"
        self.bottom_status_bar.load_label.setText(status_text)
        
        print(f"导入进度: {status_text}")
    
    def on_import_completed(self, result):
        """导入完成"""
        success = result.get('success', False)
        total_files = result.get('total_files', 0)
        imported_files = result.get('imported_files', 0)
        skipped_files = result.get('skipped_files', 0)
        error_files = result.get('error_files', 0)
        errors = result.get('errors', [])
        
        # 更新状态栏
        if success:
            status_text = f"导入完成: {imported_files} 个文件"
            self.bottom_status_bar.load_label.setText(status_text)
            self.bottom_status_bar.update_stats(imported_files, 0)
        else:
            status_text = f"导入失败: {error_files} 个错误"
            self.bottom_status_bar.load_label.setText(status_text)
        
        # 打印结果
        print(f"\n导入结果:")
        print(f"  状态: {'成功' if success else '失败'}")
        print(f"  总文件数: {total_files}")
        print(f"  已导入: {imported_files}")
        print(f"  已跳过: {skipped_files}")
        print(f"  错误文件: {error_files}")
        
        if errors:
            print(f"\n错误详情:")
            for error in errors[:5]:  # 只显示前5个错误
                print(f"  - {error}")
            if len(errors) > 5:
                print(f"  ... 还有 {len(errors) - 5} 个错误")
        
        # 显示导入统计
        json_file_path = result.get('json_file_path', '')
        if success and json_file_path:
            from Backend import get_import_stats
            stats = get_import_stats(result.get('folder_path', ''))
            if stats:
                print(f"\n统计信息:")
                print(f"  总照片数: {stats.get('total_photos', 0)}")
                quality_stats = stats.get('quality_stats', {})
                if quality_stats:
                    print(f"  质量统计:")
                    for quality, count in quality_stats.items():
                        print(f"    {quality}: {count}")
        
        # 清理工作线程
        self.import_worker = None


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