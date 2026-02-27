#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JSON file management for storing photo metadata
"""

import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
import logging
import threading

from .models import PhotoMetadata
from .utils import safe_write_file, ensure_directory_exists
from .exceptions import JsonWriteError

logger = logging.getLogger(__name__)


def get_json_file_path(folder_path: str) -> str:
    """
    获取JSON文件的路径
    
    Args:
        folder_path: 文件夹路径
        
    Returns:
        JSON文件路径
    """
    return os.path.join(folder_path, "QualityRecord.json")


def create_json_structure(folder_path: str) -> Dict[str, Any]:
    """
    创建新的JSON结构
    
    Args:
        folder_path: 文件夹路径
        
    Returns:
        JSON结构字典
    """
    now = datetime.now().isoformat()
    
    return {
        "version": "1.0",
        "created_time": now,
        "last_updated": now,
        "folder_path": folder_path,
        "total_photos": 0,
        "photos": []
    }


def read_json_file(json_file_path: str) -> Optional[Dict[str, Any]]:
    """
    读取JSON文件
    
    Args:
        json_file_path: JSON文件路径
        
    Returns:
        JSON数据字典，文件不存在或读取失败返回None
    """
    if not os.path.exists(json_file_path):
        return None
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"Error reading JSON file {json_file_path}: {e}")
        return None


def write_json_file(json_file_path: str, data: Dict[str, Any], backup: bool = True) -> bool:
    """
    写入JSON文件
    
    Args:
        json_file_path: JSON文件路径
        data: 要写入的数据
        backup: 是否创建备份
        
    Returns:
        是否成功
    """
    try:
        # 更新时间戳
        data["last_updated"] = datetime.now().isoformat()
        data["total_photos"] = len(data.get("photos", []))
        
        # 确保目录存在
        ensure_directory_exists(os.path.dirname(json_file_path))
        
        # 写入文件
        json_content = json.dumps(data, ensure_ascii=False, indent=2)
        safe_write_file(json_file_path, json_content, backup=backup)
        
        return True
        
    except Exception as e:
        logger.error(f"Error writing JSON file {json_file_path}: {e}")
        raise JsonWriteError(f"Failed to write JSON file: {e}")


def append_to_json(
    json_file_path: str,
    photo_metadata: PhotoMetadata,
    create_if_not_exists: bool = True,
    backup: bool = True
) -> bool:
    """
    将照片元数据追加到JSON文件
    
    Args:
        json_file_path: JSON文件路径
        photo_metadata: 照片元数据对象
        create_if_not_exists: 文件不存在时是否创建
        backup: 是否创建备份
        
    Returns:
        是否成功
    """
    try:
        # 读取现有数据或创建新结构
        data = read_json_file(json_file_path)
        
        if data is None:
            if not create_if_not_exists:
                return False
            data = create_json_structure(os.path.dirname(json_file_path))
        
        # 添加照片元数据
        photo_dict = photo_metadata.to_dict()
        data["photos"].append(photo_dict)
        
        # 写回文件
        return write_json_file(json_file_path, data, backup=backup)
        
    except Exception as e:
        logger.error(f"Error appending to JSON file {json_file_path}: {e}")
        return False


def update_photo_metadata(
    json_file_path: str,
    file_hash: str,
    metadata_updates: Dict[str, Any],
    backup: bool = True
) -> bool:
    """
    更新照片的元数据
    
    Args:
        json_file_path: JSON文件路径
        file_hash: 文件哈希值（用于标识照片）
        metadata_updates: 要更新的元数据字段
        backup: 是否创建备份
        
    Returns:
        是否成功
    """
    try:
        # 读取现有数据
        data = read_json_file(json_file_path)
        if data is None:
            return False
        
        # 查找并更新照片
        updated = False
        for photo in data.get("photos", []):
            photo_metadata = photo.get("photo_metadata", {})
            file_info = photo_metadata.get("file_info", {})
            if file_info.get("hash") == file_hash:
                # 更新元数据
                for key, value in metadata_updates.items():
                    if key in photo_metadata:
                        photo_metadata[key] = value
                    elif key in photo:
                        photo[key] = value
                updated = True
                break
        
        if not updated:
            logger.warning(f"Photo with hash {file_hash} not found in JSON file")
            return False
        
        # 写回文件
        return write_json_file(json_file_path, data, backup=backup)
        
    except Exception as e:
        logger.error(f"Error updating photo metadata in {json_file_path}: {e}")
        return False


def get_photo_by_hash(json_file_path: str, file_hash: str) -> Optional[Dict[str, Any]]:
    """
    根据文件哈希值获取照片元数据
    
    Args:
        json_file_path: JSON文件路径
        file_hash: 文件哈希值
        
    Returns:
        照片元数据字典，未找到返回None
    """
    data = read_json_file(json_file_path)
    if data is None:
        return None
    
    for photo in data.get("photos", []):
        photo_metadata = photo.get("photo_metadata", {})
        file_info = photo_metadata.get("file_info", {})
        if file_info.get("hash") == file_hash:
            return photo
    
    return None


def get_all_photos(json_file_path: str) -> List[Dict[str, Any]]:
    """
    获取JSON文件中的所有照片
    
    Args:
        json_file_path: JSON文件路径
        
    Returns:
        照片元数据列表
    """
    data = read_json_file(json_file_path)
    if data is None:
        return []
    
    return data.get("photos", [])


def is_photo_exists(json_file_path: str, file_hash: str) -> bool:
    """
    检查照片是否已存在于JSON文件中
    
    Args:
        json_file_path: JSON文件路径
        file_hash: 文件哈希值
        
    Returns:
        是否存在
    """
    return get_photo_by_hash(json_file_path, file_hash) is not None


def merge_json_files(source_path: str, target_path: str, backup: bool = True) -> bool:
    """
    合并两个JSON文件
    
    Args:
        source_path: 源JSON文件路径
        target_path: 目标JSON文件路径
        backup: 是否创建备份
        
    Returns:
        是否成功
    """
    try:
        # 读取两个文件
        source_data = read_json_file(source_path)
        target_data = read_json_file(target_path)
        
        if source_data is None:
            logger.warning(f"Source JSON file {source_path} does not exist")
            return False
        
        # 如果目标文件不存在，直接复制源文件
        if target_data is None:
            ensure_directory_exists(os.path.dirname(target_path))
            json_content = json.dumps(source_data, ensure_ascii=False, indent=2)
            safe_write_file(target_path, json_content, backup=backup)
            return True
        
        # 获取已有的哈希集合
        existing_hashes = set()
        for photo in target_data.get("photos", []):
            photo_metadata = photo.get("photo_metadata", {})
            file_info = photo_metadata.get("file_info", {})
            if "hash" in file_info:
                existing_hashes.add(file_info["hash"])
        
        # 合并照片（跳过重复的）
        merged_count = 0
        for photo in source_data.get("photos", []):
            photo_metadata = photo.get("photo_metadata", {})
            file_info = photo_metadata.get("file_info", {})
            file_hash = file_info.get("hash")
            
            if file_hash and file_hash not in existing_hashes:
                target_data["photos"].append(photo)
                existing_hashes.add(file_hash)
                merged_count += 1
        
        logger.info(f"Merged {merged_count} photos from {source_path} to {target_path}")
        
        # 写回文件
        return write_json_file(target_path, target_data, backup=backup)
        
    except Exception as e:
        logger.error(f"Error merging JSON files: {e}")
        return False


class JsonFileManager:
    """
    JSON文件管理器，支持线程安全的操作
    """
    
    def __init__(self, json_file_path: str):
        """
        初始化JSON文件管理器
        
        Args:
            json_file_path: JSON文件路径
        """
        self.json_file_path = json_file_path
        self.lock = threading.Lock()
    
    def read(self) -> Optional[Dict[str, Any]]:
        """
        读取JSON文件（线程安全）
        
        Returns:
            JSON数据字典
        """
        with self.lock:
            return read_json_file(self.json_file_path)
    
    def write(self, data: Dict[str, Any], backup: bool = True) -> bool:
        """
        写入JSON文件（线程安全）
        
        Args:
            data: 要写入的数据
            backup: 是否创建备份
            
        Returns:
            是否成功
        """
        with self.lock:
            return write_json_file(self.json_file_path, data, backup=backup)
    
    def append(self, photo_metadata: PhotoMetadata, backup: bool = True) -> bool:
        """
        追加照片元数据（线程安全）
        
        Args:
            photo_metadata: 照片元数据对象
            backup: 是否创建备份
            
        Returns:
            是否成功
        """
        with self.lock:
            return append_to_json(self.json_file_path, photo_metadata, backup=backup)
    
    def update(self, file_hash: str, metadata_updates: Dict[str, Any], backup: bool = True) -> bool:
        """
        更新照片元数据（线程安全）
        
        Args:
            file_hash: 文件哈希值
            metadata_updates: 要更新的元数据字段
            backup: 是否创建备份
            
        Returns:
            是否成功
        """
        with self.lock:
            return update_photo_metadata(self.json_file_path, file_hash, metadata_updates, backup)
    
    def get_photo(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """
        获取照片元数据（线程安全）
        
        Args:
            file_hash: 文件哈希值
            
        Returns:
            照片元数据字典
        """
        with self.lock:
            return get_photo_by_hash(self.json_file_path, file_hash)
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        获取所有照片元数据（线程安全）
        
        Returns:
            照片元数据列表
        """
        with self.lock:
            return get_all_photos(self.json_file_path)
    
    def exists(self, file_hash: str) -> bool:
        """
        检查照片是否存在（线程安全）
        
        Args:
            file_hash: 文件哈希值
            
        Returns:
            是否存在
        """
        with self.lock:
            return is_photo_exists(self.json_file_path, file_hash)
    
    def get_stats(self) -> Optional[Dict[str, Any]]:
        """
        获取JSON文件统计信息（线程安全）
        
        Returns:
            统计信息字典
        """
        with self.lock:
            data = read_json_file(self.json_file_path)
            if data is None:
                return None
            
            photos = data.get("photos", [])
            
            # 统计质量标记
            quality_stats = {}
            for photo in photos:
                # quality现在是数组格式，如["过曝", "欠曝"]，需要统计每个标签
                quality_list = photo.get("photo_metadata", {}).get("quality", ["未审查"])
                if not quality_list:
                    quality_list = ["未审查"]
                # 遍历数组中的所有标签进行统计
                for quality in quality_list:
                    quality_stats[quality] = quality_stats.get(quality, 0) + 1
            
            return {
                "version": data.get("version"),
                "created_time": data.get("created_time"),
                "last_updated": data.get("last_updated"),
                "folder_path": data.get("folder_path"),
                "total_photos": data.get("total_photos", 0),
                "quality_stats": quality_stats
            }