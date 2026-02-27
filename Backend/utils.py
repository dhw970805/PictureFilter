#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility functions for backend operations
"""

import hashlib
import os
from pathlib import Path
from typing import List, Set, Optional
from datetime import datetime
import time
import uuid

# 支持的图片格式
SUPPORTED_FORMATS = {
    # 常见格式
    '.jpg', '.jpeg', '.jpe', '.jfif',
    '.png',
    '.bmp', '.dib',
    '.tif', '.tiff',
    '.gif',
    '.webp',
    '.avif',
    # HEIC/HEIF
    '.heic', '.heif',
    # RAW格式
    '.cr2', '.cr3',  # Canon
    '.nef', '.nrw',  # Nikon
    '.arw', '.srf', '.sr2',  # Sony
    '.dng',  # Adobe/Leica
    '.orf',  # Olympus
    '.pef',  # Pentax
    '.raf',  # Fujifilm
    '.rw2',  # Panasonic
}


def is_supported_image_file(file_path: str) -> bool:
    """
    检查文件是否为支持的图片格式
    
    Args:
        file_path: 文件路径
        
    Returns:
        是否为支持的图片格式
    """
    ext = Path(file_path).suffix.lower()
    return ext in SUPPORTED_FORMATS


def get_file_format(file_path: str) -> str:
    """
    获取文件格式（大写）
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件格式字符串（如 "JPEG", "PNG"）
    """
    ext = Path(file_path).suffix.lower()
    
    # 格式映射
    format_map = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.jpe': 'JPEG',
        '.jfif': 'JPEG',
        '.png': 'PNG',
        '.bmp': 'BMP',
        '.dib': 'BMP',
        '.tif': 'TIFF',
        '.tiff': 'TIFF',
        '.gif': 'GIF',
        '.webp': 'WebP',
        '.avif': 'AVIF',
        '.heic': 'HEIC',
        '.heif': 'HEIF',
        '.cr2': 'CR2',
        '.cr3': 'CR3',
        '.nef': 'NEF',
        '.nrw': 'NRW',
        '.arw': 'ARW',
        '.srf': 'SRF',
        '.sr2': 'SR2',
        '.dng': 'DNG',
        '.orf': 'ORF',
        '.pef': 'PEF',
        '.raf': 'RAF',
        '.rw2': 'RW2',
    }
    
    return format_map.get(ext, ext[1:].upper())


def get_file_extension(file_path: str) -> str:
    """
    获取文件扩展名（小写，不带点）
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件扩展名（如 "jpg", "png"）
    """
    return Path(file_path).suffix.lower()[1:]


def calculate_file_hash(
    file_name: str,
    file_path: str,
    file_size_bytes: int,
    file_format: str,
    creation_time: str
) -> str:
    """
    计算文件的SHA256哈希值
    
    Args:
        file_name: 文件名
        file_path: 文件路径
        file_size_bytes: 文件大小（字节）
        file_format: 文件格式
        creation_time: 创建时间
        
    Returns:
        SHA256哈希字符串
    """
    # 构建输入字符串
    input_string = f"{file_name}{file_path}{file_size_bytes}{file_format}{creation_time}"
    
    # 计算SHA256哈希
    hash_obj = hashlib.sha256(input_string.encode('utf-8'))
    return hash_obj.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小为人类可读格式
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        格式化后的文件大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_timestamps(file_path: str) -> tuple:
    """
    获取文件的创建和修改时间
    
    Args:
        file_path: 文件路径
        
    Returns:
        (creation_time, modification_time) 元组，格式为ISO 8601字符串
    """
    try:
        path = Path(file_path)
        
        # 获取修改时间
        mod_time = datetime.fromtimestamp(path.stat().st_mtime)
        modification_time = mod_time.isoformat()
        
        # 获取创建时间（Windows和Unix系统不同）
        if hasattr(path.stat(), 'st_ctime'):
            # Windows: st_ctime是创建时间
            # Unix: st_ctime是最后元数据变更时间
            if os.name == 'nt':
                creation_time = datetime.fromtimestamp(path.stat().st_ctime).isoformat()
            else:
                # Unix系统，尝试获取创建时间（可能不可用）
                creation_time = mod_time.isoformat()
        else:
            creation_time = mod_time.isoformat()
        
        return creation_time, modification_time
        
    except Exception as e:
        # 如果获取失败，返回当前时间
        now = datetime.now().isoformat()
        return now, now


def scan_folder(
    folder_path: str,
    recursive: bool = False,
    include_files: Optional[Set[str]] = None,
    ignore_folders: Optional[Set[str]] = None
) -> List[str]:
    """
    扫描文件夹，返回所有支持的图片文件路径
    
    Args:
        folder_path: 文件夹路径
        recursive: 是否递归扫描子文件夹
        include_files: 包含的文件集合（用于过滤重复）
        ignore_folders: 要忽略的文件夹名称集合
        
    Returns:
        图片文件路径列表
    """
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return []
    
    # 默认忽略 .thumbnails 文件夹
    if ignore_folders is None:
        ignore_folders = {'.thumbnails'}
    
    image_files = []
    
    # 检查路径是否在被忽略的文件夹中
    def should_ignore(path: Path) -> bool:
        """检查路径是否在被忽略的文件夹中"""
        # 检查路径的所有父目录
        for parent in path.parents:
            if parent.name in ignore_folders:
                return True
        return False
    
    if recursive:
        # 递归扫描
        for file_path in folder.rglob('*'):
            # 跳过被忽略的文件夹中的文件
            if should_ignore(file_path):
                continue
            
            if file_path.is_file() and is_supported_image_file(str(file_path)):
                if include_files is None or str(file_path) not in include_files:
                    image_files.append(str(file_path))
    else:
        # 单层扫描
        for file_path in folder.glob('*'):
            # 跳过被忽略的文件夹
            if file_path.parent.name in ignore_folders:
                continue
            
            if file_path.is_file() and is_supported_image_file(str(file_path)):
                if include_files is None or str(file_path) not in include_files:
                    image_files.append(str(file_path))
    
    return sorted(image_files)


def ensure_directory_exists(directory_path: str):
    """
    确保目录存在，不存在则创建
    
    Args:
        directory_path: 目录路径
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def safe_write_file(file_path: str, content: str, backup: bool = True, max_retries: int = 5, retry_delay: float = 0.1):
    """
    安全写入文件（使用临时文件+原子重命名，支持重试）
    
    Args:
        file_path: 文件路径
        content: 文件内容
        backup: 是否创建备份
        max_retries: 最大重试次数
        retry_delay: 重试延迟（秒）
    """
    path = Path(file_path)
    
    # 创建备份
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + '.bak')
        try:
            path.rename(backup_path)
        except Exception as e:
            # 如果备份失败，继续执行（可能是文件已被其他进程处理）
            pass
    
    # 使用UUID生成唯一的临时文件名
    unique_id = str(uuid.uuid4())[:8]
    temp_path = path.with_suffix(path.suffix + f'.tmp_{unique_id}')
    
    # 写入临时文件
    temp_path.write_text(content, encoding='utf-8')
    
    # 原子重命名，支持重试
    for attempt in range(max_retries):
        try:
            # 如果目标文件存在，先删除（Windows上的处理方式）
            if path.exists():
                try:
                    path.unlink()
                except:
                    pass
            
            # 尝试重命名
            temp_path.rename(path)
            return  # 成功
        except Exception as e:
            if attempt < max_retries - 1:
                # 等待后重试
                time.sleep(retry_delay)
            else:
                # 最后一次重试失败，删除临时文件
                try:
                    temp_path.unlink()
                except:
                    pass
                raise Exception(f"Failed to write file after {max_retries} attempts: {e}")
