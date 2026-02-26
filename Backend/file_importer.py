#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File import functionality for photo folders
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, List, Callable, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import PhotoMetadata
from .metadata_extractor import extract_metadata
from .json_manager import get_json_file_path, is_photo_exists, JsonFileManager
from .utils import scan_folder
from .progress_tracker import ProgressTracker
from .exceptions import FileImportError, UnsupportedFormatError, FileCorruptedError

logger = logging.getLogger(__name__)


def process_single_file(
    file_path: str,
    folder_path: str,
    skip_existing: bool = False,
    json_file_manager: Optional[JsonFileManager] = None
) -> Optional[PhotoMetadata]:
    """
    处理单个图片文件，提取元数据
    
    Args:
        file_path: 图片文件路径
        folder_path: 文件夹路径
        skip_existing: 是否跳过已存在的文件
        json_file_manager: JSON文件管理器对象
        
    Returns:
        包含元数据的PhotoMetadata对象，失败返回None
    """
    try:
        # 提取元数据
        metadata = extract_metadata(file_path, folder_path)
        
        if metadata is None:
            logger.error(f"Failed to extract metadata from {file_path}")
            return None
        
        # 检查是否已存在
        if skip_existing and json_file_manager:
            if json_file_manager.exists(metadata.file_info.hash):
                logger.info(f"Skipping existing file: {file_path}")
                return None
        
        return metadata
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return None


def import_folder(
    folder_path: str,
    recursive: bool = False,
    skip_existing: bool = True,
    file_filters: Optional[Dict] = None,
    progress_callback: Optional[Callable[[Dict], None]] = None,
    max_workers: int = 4
) -> Dict:
    """
    导入文件夹中的所有图片
    
    Args:
        folder_path: 文件夹路径
        recursive: 是否递归扫描子文件夹
        skip_existing: 是否跳过已存在的文件
        file_filters: 文件过滤条件
        progress_callback: 进度回调函数
        max_workers: 最大并发线程数
        
    Returns:
        {
            "success": bool,
            "total_files": int,
            "imported_files": int,
            "skipped_files": int,
            "error_files": int,
            "errors": List[str],
            "json_file_path": str
        }
    """
    # 验证文件夹路径
    if not os.path.exists(folder_path):
        return {
            "success": False,
            "total_files": 0,
            "imported_files": 0,
            "skipped_files": 0,
            "error_files": 0,
            "errors": [f"文件夹不存在: {folder_path}"],
            "json_file_path": None
        }
    
    if not os.path.isdir(folder_path):
        return {
            "success": False,
            "total_files": 0,
            "imported_files": 0,
            "skipped_files": 0,
            "error_files": 0,
            "errors": [f"路径不是文件夹: {folder_path}"],
            "json_file_path": None
        }
    
    # 获取JSON文件路径
    json_file_path = get_json_file_path(folder_path)
    
    # 初始化JSON文件管理器
    json_manager = JsonFileManager(json_file_path)
    
    # 获取已存在的文件哈希集合
    existing_hashes: Set[str] = set()
    if skip_existing:
        all_photos = json_manager.get_all()
        for photo in all_photos:
            photo_metadata = photo.get("photo_metadata", {})
            file_info = photo_metadata.get("file_info", {})
            file_hash = file_info.get("hash")
            if file_hash:
                existing_hashes.add(file_hash)
    
    # 扫描文件夹
    image_files = scan_folder(folder_path, recursive)
    
    if not image_files:
        logger.info(f"没有找到支持的图片文件在: {folder_path}")
        return {
            "success": True,
            "total_files": 0,
            "imported_files": 0,
            "skipped_files": 0,
            "error_files": 0,
            "errors": [],
            "json_file_path": json_file_path
        }
    
    # 过滤已存在的文件
    if skip_existing:
        files_to_process = []
        for file_path in image_files:
            metadata = extract_metadata(file_path, folder_path)
            if metadata and metadata.file_info.hash not in existing_hashes:
                files_to_process.append(file_path)
    else:
        files_to_process = image_files
    
    total_files = len(files_to_process)
    logger.info(f"找到 {len(image_files)} 个图片文件，需要处理 {total_files} 个")
    
    # 初始化进度跟踪器
    progress = ProgressTracker(total_files)
    
    # 错误列表
    errors = []
    
    # 使用线程池处理文件
    imported_count = 0
    skipped_count = 0
    error_count = 0
    
    # 收集所有元数据
    all_metadata = []
    
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交任务
            future_to_file = {
                executor.submit(
                    process_single_file,
                    file_path,
                    folder_path,
                    skip_existing,
                    None  # 不使用 json_manager，避免并发写入
                ): file_path
                for file_path in files_to_process
            }
            
            # 处理完成的任务
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                
                try:
                    metadata = future.result()
                    
                    if metadata is None:
                        # 文件被跳过或处理失败
                        progress.update(success=False, skipped=True)
                        skipped_count += 1
                    else:
                        # 成功提取元数据，收集到列表
                        all_metadata.append(metadata)
                        progress.update(success=True)
                        imported_count += 1
                        logger.debug(f"成功提取元数据: {file_path}")
                
                except Exception as e:
                    progress.update(success=False)
                    error_count += 1
                    error_msg = f"处理文件 {file_path} 时出错: {str(e)}"
                    errors.append(error_msg)
                    logger.error(error_msg)
                
                # 调用进度回调
                if progress_callback:
                    progress_callback(progress.get_progress())
        
        # 批量写入JSON文件（一次性写入所有元数据）
        if all_metadata:
            try:
                # 读取现有数据
                existing_data = json_manager.read()
                if existing_data is None:
                    from .json_manager import create_json_structure
                    existing_data = create_json_structure(folder_path)
                
                # 添加所有元数据
                for metadata in all_metadata:
                    photo_dict = metadata.to_dict()
                    existing_data["photos"].append(photo_dict)
                
                # 一次性写入
                from .json_manager import write_json_file
                if write_json_file(json_file_path, existing_data, backup=False):
                    logger.info(f"成功写入 {len(all_metadata)} 个照片元数据")
                else:
                    # 写入失败，将所有文件标记为错误
                    error_count += imported_count
                    imported_count = 0
                    for metadata in all_metadata:
                        errors.append(f"无法写入JSON: {metadata.file_info.file_path}")
            except Exception as e:
                # 写入失败，将所有文件标记为错误
                error_count += imported_count
                imported_count = 0
                error_msg = f"批量写入JSON文件时出错: {str(e)}"
                errors.append(error_msg)
                for metadata in all_metadata:
                    errors.append(f"无法写入JSON: {metadata.file_info.file_path}")
                logger.error(error_msg)
    
    except Exception as e:
        error_msg = f"导入过程中发生错误: {str(e)}"
        errors.append(error_msg)
        logger.error(error_msg)
    
    # 返回结果
    result = {
        "success": error_count == 0,
        "total_files": total_files,
        "imported_files": imported_count,
        "skipped_files": skipped_count,
        "error_files": error_count,
        "errors": errors,
        "json_file_path": json_file_path
    }
    
    logger.info(f"导入完成: {result}")
    return result


def refresh_folder(
    folder_path: str,
    recursive: bool = False,
    progress_callback: Optional[Callable[[Dict], None]] = None,
    max_workers: int = 4
) -> Dict:
    """
    刷新文件夹，检测新增或删除的文件
    
    Args:
        folder_path: 文件夹路径
        recursive: 是否递归扫描子文件夹
        progress_callback: 进度回调函数
        max_workers: 最大并发线程数
        
    Returns:
        导入结果字典
    """
    return import_folder(
        folder_path=folder_path,
        recursive=recursive,
        skip_existing=True,
        progress_callback=progress_callback,
        max_workers=max_workers
    )


def check_duplicates(folder_path: str) -> List[str]:
    """
    检查文件夹中的重复照片
    
    Args:
        folder_path: 文件夹路径
        
    Returns:
        重复的文件哈希值列表
    """
    json_file_path = get_json_file_path(folder_path)
    json_manager = JsonFileManager(json_file_path)
    
    all_photos = json_manager.get_all()
    
    # 统计哈希值
    hash_count = {}
    for photo in all_photos:
        photo_metadata = photo.get("photo_metadata", {})
        file_info = photo_metadata.get("file_info", {})
        file_hash = file_info.get("hash")
        if file_hash:
            hash_count[file_hash] = hash_count.get(file_hash, 0) + 1
    
    # 找出重复的哈希值
    duplicates = [hash_value for hash_value, count in hash_count.items() if count > 1]
    
    logger.info(f"找到 {len(duplicates)} 个重复的照片")
    
    return duplicates


def get_import_stats(folder_path: str) -> Optional[Dict]:
    """
    获取导入统计信息
    
    Args:
        folder_path: 文件夹路径
        
    Returns:
        统计信息字典
    """
    json_file_path = get_json_file_path(folder_path)
    json_manager = JsonFileManager(json_file_path)
    
    return json_manager.get_stats()