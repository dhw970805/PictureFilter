#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main exposure detection module combining overexposure and underexposure detection
"""

from typing import Dict, Tuple, Optional, List
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from .config_manager import ConfigManager
from .overexposure import OverexposureDetector
from .underexposure import UnderexposureDetector

logger = logging.getLogger(__name__)


class ExposureDetector:
    """曝光检测器（主类）"""
    
    def __init__(self, config_path: str = None):
        """
        初始化曝光检测器
        
        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        self.config_manager = ConfigManager(config_path)
        
        # 初始化检测器
        overexposure_config = self.config_manager.get_overexposure_config()
        underexposure_config = self.config_manager.get_underexposure_config()
        
        self.overexposure_detector = OverexposureDetector(overexposure_config)
        self.underexposure_detector = UnderexposureDetector(underexposure_config)
        
        logger.info("ExposureDetector initialized")
    
    def detect_single_image(self, image_path: str) -> Dict[str, any]:
        """
        检测单张图片的曝光情况
        
        Args:
            image_path: 图片路径
            
        Returns:
            检测结果字典
        """
        # 检测过曝
        is_overexposed, overexposure_results = self.overexposure_detector.detect(image_path)
        
        # 检测欠曝
        is_underexposed, underexposure_results = self.underexposure_detector.detect(image_path)
        
        # 确定质量标签（拆分成数组，每个标签独立）
        quality_list = []
        if is_overexposed:
            quality_list.append("过曝")
        if is_underexposed:
            quality_list.append("欠曝")
        if not quality_list:
            quality_list.append("合格")
        
        # 汇总结果
        result = {
            "image_path": image_path,
            "quality_list": quality_list,
            "is_overexposed": is_overexposed,
            "is_underexposed": is_underexposed,
            "overexposure_details": overexposure_results,
            "underexposure_details": underexposure_results
        }
        
        return result
    
    def detect_batch_images(
        self,
        image_paths: List[str],
        max_workers: int = 4
    ) -> List[Dict[str, any]]:
        """
        批量检测图片的曝光情况（多线程）
        
        Args:
            image_paths: 图片路径列表
            max_workers: 最大线程数
            
        Returns:
            检测结果列表
        """
        results = []
        
        logger.info(f"Starting batch detection for {len(image_paths)} images")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_path = {
                executor.submit(self.detect_single_image, path): path
                for path in image_paths
            }
            
            # 收集结果
            completed = 0
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1
                    
                    if completed % 10 == 0:
                        logger.info(f"Completed {completed}/{len(image_paths)} images")
                        
                except Exception as e:
                    logger.error(f"Error processing {path}: {e}")
                    results.append({
                        "image_path": path,
                        "quality": "检测失败",
                        "error": str(e)
                    })
        
        logger.info(f"Batch detection completed: {len(results)} images processed")
        return results
    
    def detect_folder(
        self,
        folder_path: str,
        extensions: List[str] = None,
        max_workers: int = 4
    ) -> List[Dict[str, any]]:
        """
        检测文件夹中所有图片的曝光情况
        
        Args:
            folder_path: 文件夹路径
            extensions: 支持的图片扩展名列表
            max_workers: 最大线程数
            
        Returns:
            检测结果列表
        """
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp']
        
        folder = Path(folder_path)
        if not folder.exists() or not folder.is_dir():
            logger.error(f"Invalid folder path: {folder_path}")
            return []
        
        # 收集所有图片文件
        image_paths = []
        for ext in extensions:
            image_paths.extend([str(p) for p in folder.glob(f"*{ext}")])
            image_paths.extend([str(p) for p in folder.glob(f"*{ext.upper()}")])
        
        if not image_paths:
            logger.warning(f"No images found in {folder_path}")
            return []
        
        logger.info(f"Found {len(image_paths)} images in {folder_path}")
        
        # 批量检测
        results = self.detect_batch_images(image_paths, max_workers)
        
        return results
    
    def update_json_quality(
        self,
        json_file_path: str,
        image_path: str
    ) -> Tuple[bool, str]:
        """
        检测图片并更新JSON文件中的质量字段
        
        Args:
            json_file_path: JSON文件路径
            image_path: 图片路径
            
        Returns:
            (是否成功, 质量标签)
        """
        try:
            # 检测图片
            result = self.detect_single_image(image_path)
            quality_list = result["quality_list"]
            
            # 导入json_manager（避免循环导入）
            from ..json_manager import update_photo_metadata, get_photo_by_hash
            from ..utils import calculate_file_hash_from_path
            
            # 计算文件哈希
            file_hash = calculate_file_hash_from_path(image_path)
            
            # 更新JSON文件（quality字段为标签数组）
            success = update_photo_metadata(
                json_file_path,
                file_hash,
                {"quality": quality_list}
            )
            
            if success:
                logger.info(f"Updated quality for {image_path}: {quality_list}")
                return True, quality_list
            else:
                logger.error(f"Failed to update quality for {image_path}")
                return False, quality_list
                
        except Exception as e:
            logger.error(f"Error updating JSON quality: {e}")
            return False, ["检测失败"]
    
    def update_folder_json_quality(
        self,
        json_file_path: str,
        folder_path: str,
        extensions: List[str] = None,
        max_workers: int = 4
    ) -> Dict[str, any]:
        """
        检测文件夹中所有图片并更新JSON文件
        
        Args:
            json_file_path: JSON文件路径
            folder_path: 文件夹路径
            extensions: 支持的图片扩展名列表
            max_workers: 最大线程数
            
        Returns:
            统计结果字典
        """
        # 检测文件夹中的图片
        results = self.detect_folder(folder_path, extensions, max_workers)
        
        if not results:
            return {
                "total": 0,
                "success": 0,
                "failed": 0,
                "quality_stats": {}
            }
        
        # 统计结果
        stats = {
            "total": len(results),
            "success": 0,
            "failed": 0,
            "quality_stats": {}
        }
        
        # 更新JSON文件
        from ..json_manager import update_photo_metadata
        from ..utils import calculate_file_hash_from_path
        
        for result in results:
            if "error" in result:
                stats["failed"] += 1
                continue
            
            try:
                file_hash = calculate_file_hash_from_path(result["image_path"])
                quality_list = result["quality_list"]
                
                success = update_photo_metadata(
                    json_file_path,
                    file_hash,
                    {"quality": quality_list}
                )
                
                if success:
                    stats["success"] += 1
                    # 统计每个标签
                    for quality in quality_list:
                        stats["quality_stats"][quality] = stats["quality_stats"].get(quality, 0) + 1
                else:
                    stats["failed"] += 1
                    
            except Exception as e:
                logger.error(f"Error updating {result['image_path']}: {e}")
                stats["failed"] += 1
        
        logger.info(f"Quality update completed: {stats}")
        return stats
    
    def reload_config(self) -> None:
        """
        重新加载配置文件
        """
        self.config_manager.reload_config()
        
        # 重新初始化检测器
        overexposure_config = self.config_manager.get_overexposure_config()
        underexposure_config = self.config_manager.get_underexposure_config()
        
        self.overexposure_detector = OverexposureDetector(overexposure_config)
        self.underexposure_detector = UnderexposureDetector(underexposure_config)
        
        logger.info("Configuration and detectors reloaded")
    
    def get_current_config(self) -> Dict[str, any]:
        """
        获取当前配置
        
        Returns:
            配置字典
        """
        return {
            "overexposure": self.config_manager.get_overexposure_config(),
            "underexposure": self.config_manager.get_underexposure_config()
        }