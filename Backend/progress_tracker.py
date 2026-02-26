#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Progress tracking for file import operations
"""

from typing import Dict, Optional


class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self, total: int = 0):
        """
        初始化进度跟踪器
        
        Args:
            total: 总文件数
        """
        self.total = total
        self.processed = 0
        self.errors = 0
        self.skipped = 0
    
    def update(self, success: bool = True, skipped: bool = False):
        """
        更新进度
        
        Args:
            success: 是否成功处理
            skipped: 是否跳过
        """
        self.processed += 1
        if skipped:
            self.skipped += 1
        elif not success:
            self.errors += 1
    
    def set_total(self, total: int):
        """设置总数"""
        self.total = total
    
    def get_progress(self) -> Dict:
        """
        获取当前进度
        
        Returns:
            进度信息字典
        """
        imported = self.processed - self.errors - self.skipped
        
        return {
            "total": self.total,
            "processed": self.processed,
            "imported": imported,
            "errors": self.errors,
            "skipped": self.skipped,
            "percentage": (self.processed / self.total * 100) if self.total > 0 else 0
        }
    
    def get_percentage(self) -> float:
        """
        获取完成百分比
        
        Returns:
            完成百分比 (0-100)
        """
        if self.total == 0:
            return 0.0
        return (self.processed / self.total) * 100
    
    def is_complete(self) -> bool:
        """
        检查是否完成
        
        Returns:
            是否完成
        """
        return self.processed >= self.total and self.total > 0
    
    def reset(self):
        """重置进度"""
        self.processed = 0
        self.errors = 0
        self.skipped = 0