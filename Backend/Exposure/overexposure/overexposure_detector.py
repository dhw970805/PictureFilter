#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Overexposure detection module
"""

import cv2
import numpy as np
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class OverexposureDetector:
    """过曝检测器"""
    
    def __init__(self, config: Dict[str, float]):
        """
        初始化过曝检测器
        
        Args:
            config: 过曝检测配置字典
        """
        self.config = config
        self.high_light_threshold = 245  # 高光像素亮度阈值
        self.rgb_max_threshold = 250     # RGB通道最大值阈值
        self.histogram_highlight_min = 240  # 直方图高光区域最小值
        self.histogram_highlight_max = 255  # 直方图高光区域最大值
    
    def detect(self, image_path: str) -> Tuple[bool, Dict[str, any]]:
        """
        检测图片是否过曝
        
        Args:
            image_path: 图片路径
            
        Returns:
            (是否过曝, 检测结果字典)
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
            
            # 1. 检测高光像素占比
            highlight_ratio = self._detect_highlight_pixel_ratio(image_rgb, total_pixels)
            
            # 2. 检测RGB通道最大值占比
            rgb_max_ratio = self._detect_rgb_max_channel_ratio(image_rgb, total_pixels)
            
            # 3. 检测直方图高光区域占比
            histogram_highlight_ratio = self._detect_histogram_highlight_ratio(image_rgb, total_pixels)
            
            # 4. 检测过曝区域连通性（可选）
            connected_area_ratio = self._detect_connected_overexposed_area(image_rgb, total_pixels)
            
            # 汇总检测结果
            results = {
                "highlight_pixel_ratio": highlight_ratio,
                "rgb_max_channel_ratio": rgb_max_ratio,
                "histogram_highlight_ratio": histogram_highlight_ratio,
                "connected_overexposed_area_ratio": connected_area_ratio
            }
            
            # 判断是否过曝（任一条件满足即判定为过曝）
            is_overexposed = (
                highlight_ratio >= self.config["highlight_pixel_ratio_threshold"] or
                rgb_max_ratio >= self.config["rgb_max_channel_ratio_threshold"] or
                histogram_highlight_ratio >= self.config["histogram_highlight_ratio_threshold"]
            )
            
            return is_overexposed, results
            
        except Exception as e:
            logger.error(f"Error detecting overexposure for {image_path}: {e}")
            return False, {"error": str(e)}
    
    def _detect_highlight_pixel_ratio(self, image: np.ndarray, total_pixels: int) -> float:
        """
        检测高光像素占比（亮度值 ≥ 245）
        
        Args:
            image: RGB图像数组
            total_pixels: 总像素数
            
        Returns:
            高光像素占比
        """
        # 转换为灰度图计算亮度
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # 统计高光像素数
        highlight_pixels = np.sum(gray >= self.high_light_threshold)
        
        ratio = highlight_pixels / total_pixels
        return ratio
    
    def _detect_rgb_max_channel_ratio(self, image: np.ndarray, total_pixels: int) -> float:
        """
        检测RGB通道最大值占比（单通道值 ≥ 250）
        
        Args:
            image: RGB图像数组
            total_pixels: 总像素数
            
        Returns:
            RGB通道最大值占比
        """
        # 分别检测R、G、B通道
        r_channel = image[:, :, 0]
        g_channel = image[:, :, 1]
        b_channel = image[:, :, 2]
        
        # 统计每个通道超过阈值的像素数
        r_max_pixels = np.sum(r_channel >= self.rgb_max_threshold)
        g_max_pixels = np.sum(g_channel >= self.rgb_max_threshold)
        b_max_pixels = np.sum(b_channel >= self.rgb_max_threshold)
        
        # 取三个通道的最大值
        max_channel_pixels = max(r_max_pixels, g_max_pixels, b_max_pixels)
        
        ratio = max_channel_pixels / total_pixels
        return ratio
    
    def _detect_histogram_highlight_ratio(self, image: np.ndarray, total_pixels: int) -> float:
        """
        检测直方图高光区域占比（240-255区间）
        
        Args:
            image: RGB图像数组
            total_pixels: 总像素数
            
        Returns:
            直方图高光区域占比
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # 计算直方图
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        
        # 统计高光区域（240-255）的像素数
        highlight_pixels = np.sum(hist[self.histogram_highlight_min:self.histogram_highlight_max + 1])
        
        ratio = highlight_pixels / total_pixels
        return ratio
    
    def _detect_connected_overexposed_area(self, image: np.ndarray, total_pixels: int) -> float:
        """
        检测过曝区域连通性（大面积连续过曝）
        
        Args:
            image: RGB图像数组
            total_pixels: 总像素数
            
        Returns:
            最大连通过曝区域占比
        """
        try:
            # 转换为灰度图
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # 创建二值图像（高光区域为白色）
            _, binary = cv2.threshold(gray, self.high_light_threshold, 255, cv2.THRESH_BINARY)
            
            # 查找连通区域
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                binary, connectivity=8
            )
            
            # 找到最大的连通区域（忽略背景label=0）
            if num_labels > 1:
                areas = stats[1:, cv2.CC_STAT_AREA]  # 跳过背景
                max_area = np.max(areas)
                ratio = max_area / total_pixels
            else:
                ratio = 0.0
            
            return ratio
            
        except Exception as e:
            logger.warning(f"Error detecting connected overexposed area: {e}")
            return 0.0