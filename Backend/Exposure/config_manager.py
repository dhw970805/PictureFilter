#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration manager for exposure detection thresholds
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """管理曝光检测的配置文件"""
    
    def __init__(self, config_path: str = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，默认为Backend/Exposure/config/exposure_config.json
        """
        if config_path is None:
            # 获取当前文件所在目录
            current_dir = Path(__file__).parent
            config_path = os.path.join(current_dir, "config", "exposure_config.json")
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        try:
            if not os.path.exists(self.config_path):
                logger.warning(f"Config file not found at {self.config_path}, using default values")
                return self._get_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            logger.info(f"Loaded configuration from {self.config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading config file: {e}, using default values")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置
        
        Returns:
            默认配置字典
        """
        return {
            "version": "1.0",
            "description": "曝光检测阈值配置文件（默认值）",
            "last_updated": "2024-02-27",
            "overexposure": {
                "highlight_pixel_ratio_threshold": 0.05,
                "rgb_max_channel_ratio_threshold": 0.03,
                "histogram_highlight_ratio_threshold": 0.08,
                "connected_overexposed_area_threshold": 0.02
            },
            "underexposure": {
                "shadow_pixel_ratio_threshold": 0.15,
                "rgb_min_channel_ratio_threshold": 0.10,
                "histogram_shadow_ratio_threshold": 0.20,
                "average_brightness_threshold": 80.0
            }
        }
    
    def get_overexposure_config(self) -> Dict[str, float]:
        """
        获取过曝检测配置
        
        Returns:
            过曝检测阈值字典
        """
        return self.config.get("overexposure", self._get_default_config()["overexposure"])
    
    def get_underexposure_config(self) -> Dict[str, float]:
        """
        获取欠曝检测配置
        
        Returns:
            欠曝检测阈值字典
        """
        return self.config.get("underexposure", self._get_default_config()["underexposure"])
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取完整配置
        
        Returns:
            完整配置字典
        """
        return self.config.copy()
    
    def reload_config(self) -> None:
        """
        重新加载配置文件
        """
        self.config = self._load_config()
        logger.info("Configuration reloaded")
    
    def get_threshold(self, category: str, key: str) -> float:
        """
        获取特定的阈值
        
        Args:
            category: 类别（overexposure 或 underexposure）
            key: 阈值键名
            
        Returns:
            阈值值
        """
        category_config = self.config.get(category, {})
        if key not in category_config:
            default_config = self._get_default_config()
            category_config = default_config.get(category, {})
        
        return category_config.get(key, 0.0)