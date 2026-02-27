#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Underexposure detection module
"""

import cv2
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class UnderexposureDetector:
    """欠曝检测器"""
    
    def __init__(self, config: Dict[str, float]):
        """
        初始化欠曝检测器
        
        Args:
            config: 欠曝检测配置字典
        """
        self.config = config
        self.shadow_threshold = 50       # 暗部像素亮度阈值
        self.rgb_min_threshold = 30      # RGB通道最小值阈值
        self.histogram_shadow_min = 0    # 直方图暗部区域最小值
        self.histogram_shadow_max = 40   # 直方图暗部区域最大值
    
    def detect(self, image_path: str) -> Tuple[bool, Dict[str, any]]:
        """
        检测图片是否欠曝
        
        Args:
            image_path: 图片路径
            
        Returns:
            (是否欠曝, 检测结果字典)
        """
        try:
            # 读取图片（支持中文路径）
            import numpy as np
            from pathlib import Path
            
            # 将路径转换为字符串，确保正确处理中文
            image_path_str = str(image_path)
            
            # 使用 numpy 读取文件并解码，解决中文路径问题
            image_array = np.fromfile(image_path_str, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
            if image is None:
                logger.error(f"Failed to read image: {image_path}")
                return False, {"error": "Failed to read image"}
            
            # 转换为RGB格式
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # 计算总像素数
            total_pixels = image_rgb.shape[0] * image_rgb.shape[1]
            
            # 1. 检测暗部像素占比
            shadow_ratio = self._detect_shadow_pixel_ratio(image_rgb, total_pixels)
            
            # 2. 检测RGB通道最小值占比
            rgb_min_ratio = self._detect_rgb_min_channel_ratio(image_rgb, total_pixels)
            
            # 3. 检测直方图暗部区域占比
            histogram_shadow_ratio = self._detect_histogram_shadow_ratio(image_rgb, total_pixels)
            
            # 4. 检测平均亮度值
            average_brightness = self._detect_average_brightness(image_rgb)
            
            # 汇总检测结果
            results = {
                "shadow_pixel_ratio": shadow_ratio,
                "rgb_min_channel_ratio": rgb_min_ratio,
                "histogram_shadow_ratio": histogram_shadow_ratio,
                "average_brightness": average_brightness
            }
            
            # 判断是否欠曝（任一条件满足即判定为欠曝）
            is_underexposed = (
                shadow_ratio >= self.config["shadow_pixel_ratio_threshold"] or
                rgb_min_ratio >= self.config["rgb_min_channel_ratio_threshold"] or
                histogram_shadow_ratio >= self.config["histogram_shadow_ratio_threshold"] or
                average_brightness < self.config["average_brightness_threshold"]
            )
            
            return is_underexposed, results
            
        except Exception as e:
            logger.error(f"Error detecting underexposure for {image_path}: {e}")
            return False, {"error": str(e)}
    
    def _detect_shadow_pixel_ratio(self, image: np.ndarray, total_pixels: int) -> float:
        """
        检测暗部像素占比（亮度值 ≤ 50）
        
        Args:
            image: RGB图像数组
            total_pixels: 总像素数
            
        Returns:
            暗部像素占比
        """
        # 转换为灰度图计算亮度
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # 统计暗部像素数
        shadow_pixels = np.sum(gray <= self.shadow_threshold)
        
        ratio = shadow_pixels / total_pixels
        return ratio
    
    def _detect_rgb_min_channel_ratio(self, image: np.ndarray, total_pixels: int) -> float:
        """
        检测RGB通道最小值占比（单通道值 ≤ 30）
        
        Args:
            image: RGB图像数组
            total_pixels: 总像素数
            
        Returns:
            RGB通道最小值占比
        """
        # 分别检测R、G、B通道
        r_channel = image[:, :, 0]
        g_channel = image[:, :, 1]
        b_channel = image[:, :, 2]
        
        # 统计每个通道低于阈值的像素数
        r_min_pixels = np.sum(r_channel <= self.rgb_min_threshold)
        g_min_pixels = np.sum(g_channel <= self.rgb_min_threshold)
        b_min_pixels = np.sum(b_channel <= self.rgb_min_threshold)
        
        # 取三个通道的最大值
        max_channel_pixels = max(r_min_pixels, g_min_pixels, b_min_pixels)
        
        ratio = max_channel_pixels / total_pixels
        return ratio
    
    def _detect_histogram_shadow_ratio(self, image: np.ndarray, total_pixels: int) -> float:
        """
        检测直方图暗部区域占比（0-40区间）
        
        Args:
            image: RGB图像数组
            total_pixels: 总像素数
            
        Returns:
            直方图暗部区域占比
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # 计算直方图
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        
        # 统计暗部区域（0-40）的像素数
        shadow_pixels = np.sum(hist[self.histogram_shadow_min:self.histogram_shadow_max + 1])
        
        ratio = shadow_pixels / total_pixels
        return ratio
    
    def _detect_average_brightness(self, image: np.ndarray) -> float:
        """
        检测平均亮度值
        
        Args:
            image: RGB图像数组
            
        Returns:
            平均亮度值（0-255）
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # 计算平均亮度
        avg_brightness = np.mean(gray)
        
        return float(avg_brightness)