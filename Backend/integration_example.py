#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Integration example: Backend with Frontend
Demonstrates how to use the backend functionality in the frontend application
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Backend import import_folder, get_import_stats, ProgressTracker
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton, QApplication
from PyQt6.QtCore import Qt, QThread, pyqtSignal


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
        def progress_callback(progress):
            self.progress_updated.emit(progress)
        
        result = import_folder(
            folder_path=self.folder_path,
            recursive=self.recursive,
            progress_callback=progress_callback
        )
        
        self.import_completed.emit(result)


class FolderImportDialog(QWidget):
    """
    文件夹导入对话框示例
    展示如何在Qt应用中集成后端功能
    """
    
    def __init__(self):
        super().__init__()
        self.current_folder = None
        self.import_worker = None
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        self.setWindowTitle("文件夹导入 - 后端集成示例")
        self.setMinimumSize(600, 300)
        
        layout = QVBoxLayout(self)
        
        # 文件夹选择
        self.folder_label = QLabel("未选择文件夹")
        self.folder_label.setStyleSheet("color: #888; font-size: 14px;")
        layout.addWidget(self.folder_label)
        
        self.select_folder_btn = QPushButton("选择照片文件夹")
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.select_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QPushButton:pressed {
                background-color: #0064b0;
            }
        """)
        layout.addWidget(self.select_folder_btn)
        
        # 进度条
        self.progress_label = QLabel("")
        layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # 结果显示
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.result_label.setStyleSheet("font-size: 12px; color: #333;")
        layout.addWidget(self.result_label)
        
        layout.addStretch()
    
    def select_folder(self):
        """选择文件夹"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择照片文件夹",
            ""
        )
        
        if folder_path:
            self.current_folder = folder_path
            self.folder_label.setText(f"已选择: {folder_path}")
            self.folder_label.setStyleSheet("color: #333; font-size: 14px; font-weight: bold;")
            
            # 开始导入
            self.start_import()
    
    def start_import(self):
        """开始导入"""
        if not self.current_folder:
            return
        
        # 禁用按钮
        self.select_folder_btn.setEnabled(False)
        self.select_folder_btn.setText("导入中...")
        
        # 创建并启动工作线程
        self.import_worker = ImportWorker(self.current_folder, recursive=False)
        self.import_worker.progress_updated.connect(self.update_progress)
        self.import_worker.import_completed.connect(self.import_finished)
        self.import_worker.start()
    
    def update_progress(self, progress):
        """更新进度"""
        percentage = progress.get('percentage', 0)
        imported = progress.get('imported', 0)
        errors = progress.get('errors', 0)
        total = progress.get('total', 0)
        
        self.progress_bar.setValue(int(percentage))
        self.progress_label.setText(
            f"进度: {int(percentage)}% "
            f"({imported}/{total} 已导入, {errors} 错误)"
        )
    
    def import_finished(self, result):
        """导入完成"""
        # 恢复按钮
        self.select_folder_btn.setEnabled(True)
        self.select_folder_btn.setText("选择照片文件夹")
        
        # 显示结果
        success = result.get('success', False)
        total_files = result.get('total_files', 0)
        imported_files = result.get('imported_files', 0)
        skipped_files = result.get('skipped_files', 0)
        error_files = result.get('error_files', 0)
        errors = result.get('errors', [])
        json_file_path = result.get('json_file_path', '')
        
        result_text = f"""
导入结果:
--------
状态: {'成功' if success else '失败'}
总文件数: {total_files}
已导入: {imported_files}
已跳过: {skipped_files}
错误文件: {error_files}
JSON文件: {json_file_path}
"""
        
        if errors:
            result_text += "\n错误详情:\n"
            for error in errors[:5]:  # 只显示前5个错误
                result_text += f"  - {error}\n"
            if len(errors) > 5:
                result_text += f"  ... 还有 {len(errors) - 5} 个错误\n"
        
        self.result_label.setText(result_text)
        
        # 显示统计信息
        if success and json_file_path:
            stats = get_import_stats(self.current_folder)
            if stats:
                quality_stats = stats.get('quality_stats', {})
                stats_text = f"\n质量统计:\n"
                for quality, count in quality_stats.items():
                    stats_text += f"  {quality}: {count}\n"
                self.result_label.setText(self.result_label.text() + stats_text)
        
        # 显示消息框
        if success:
            QMessageBox.information(
                self,
                "导入完成",
                f"成功导入 {imported_files} 个文件！"
            )
        else:
            QMessageBox.warning(
                self,
                "导入完成",
                f"导入过程中遇到错误。已导入 {imported_files} 个文件。"
            )


def main():
    """主函数"""
    import logging
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = FolderImportDialog()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()