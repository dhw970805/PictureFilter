#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Thumbnail generation for photos
"""

import os
import logging
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)


def get_thumbnail_folder(folder_path: str) -> str:
    """
    获取缩略图文件夹路径
    
    Args:
        folder_path: 原始照片文件夹路径
        
    Returns:
        缩略图文件夹路径
    """
    return os.path.join(folder_path, ".thumbnails")


def get_thumbnail_path(file_path: str, thumbnail_size: Tuple[int, int] = (200, 200)) -> str:
    """
    获取缩略图文件路径
    
    Args:
        file_path: 原始照片文件路径
        thumbnail_size: 缩略图尺寸 (width, height)
        
    Returns:
        缩略图文件路径
    """
    # 获取文件信息
    folder_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    
    # 创建缩略图文件夹
    thumbnail_folder = get_thumbnail_folder(folder_path)
    os.makedirs(thumbnail_folder, exist_ok=True)
    
    # 创建缩略图文件名（包含尺寸信息）
    size_str = f"{thumbnail_size[0]}x{thumbnail_size[1]}"
    thumbnail_name = f"{file_name_without_ext}_{size_str}.jpg"
    
    return os.path.join(thumbnail_folder, thumbnail_name)


def generate_thumbnail(
    file_path: str,
    thumbnail_size: Tuple[int, int] = (200, 200),
    quality: int = 85,
    fit_mode: str = "cover"
) -> Optional[str]:
    """
    为单个图片文件生成缩略图
    
    Args:
        file_path: 原始图片文件路径
        thumbnail_size: 缩略图尺寸 (width, height)
        quality: JPEG质量 (1-100)
        fit_mode: 适配模式 ("cover", "contain", "fill")
        
    Returns:
        缩略图文件路径，失败返回None
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            return None
        
        # 检查是否是图片文件
        if not file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', 
                                            '.tiff', '.tif', '.webp', '.avif', '.heic', '.heif')):
            logger.warning(f"不支持的文件格式: {file_path}")
            return None
        
        # 获取缩略图路径
        thumbnail_path = get_thumbnail_path(file_path, thumbnail_size)
        
        # 如果缩略图已存在且比原文件新，直接返回
        if os.path.exists(thumbnail_path):
            orig_time = os.path.getmtime(file_path)
            thumb_time = os.path.getmtime(thumbnail_path)
            if thumb_time > orig_time:
                logger.debug(f"使用现有缩略图: {thumbnail_path}")
                return thumbnail_path
        
        # 打开图片
        with Image.open(file_path) as img:
            # 处理EXIF方向信息
            img = ImageOps.exif_transpose(img)
            
            # 根据适配模式处理图片
            if fit_mode == "cover":
                # 裁剪填充模式
                img = ImageOps.cover(img, thumbnail_size)
            elif fit_mode == "contain":
                # 包含模式
                img = ImageOps.contain(img, thumbnail_size)
            elif fit_mode == "fill":
                # 拉伸填充模式
                img = img.resize(thumbnail_size, Image.Resampling.LANCZOS)
            else:
                # 默认使用cover模式
                img = ImageOps.cover(img, thumbnail_size)
            
            # 转换为RGB模式（JPEG不支持RGBA）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存缩略图
            img.save(thumbnail_path, 'JPEG', quality=quality, optimize=True)
            logger.debug(f"生成缩略图: {thumbnail_path}")
            return thumbnail_path
    
    except Exception as e:
        logger.error(f"生成缩略图失败 {file_path}: {e}")
        return None


def generate_thumbnails_batch(
    file_paths: list,
    thumbnail_size: Tuple[int, int] = (200, 200),
    quality: int = 85,
    fit_mode: str = "cover",
    progress_callback: Optional[callable] = None
) -> dict:
    """
    批量生成缩略图
    
    Args:
        file_paths: 图片文件路径列表
        thumbnail_size: 缩略图尺寸 (width, height)
        quality: JPEG质量 (1-100)
        fit_mode: 适配模式 ("cover", "contain", "fill")
        progress_callback: 进度回调函数 (current, total, success_count, error_count)
        
    Returns:
        {
            "success": bool,
            "total_files": int,
            "success_count": int,
            "error_count": int,
            "thumbnails": dict  # {original_path: thumbnail_path}
        }
    """
    total = len(file_paths)
    success_count = 0
    error_count = 0
    thumbnails = {}
    
    for i, file_path in enumerate(file_paths):
        thumbnail_path = generate_thumbnail(
            file_path=file_path,
            thumbnail_size=thumbnail_size,
            quality=quality,
            fit_mode=fit_mode
        )
        
        if thumbnail_path:
            thumbnails[file_path] = thumbnail_path
            success_count += 1
        else:
            error_count += 1
        
        # 调用进度回调
        if progress_callback:
            progress_callback(i + 1, total, success_count, error_count)
    
    result = {
        "success": error_count == 0,
        "total_files": total,
        "success_count": success_count,
        "error_count": error_count,
        "thumbnails": thumbnails
    }
    
    logger.info(f"批量生成缩略图完成: {result}")
    return result


def clear_thumbnails(folder_path: str) -> bool:
    """
    清除指定文件夹的所有缩略图
    
    Args:
        folder_path: 原始照片文件夹路径
        
    Returns:
        是否成功
    """
    try:
        thumbnail_folder = get_thumbnail_folder(folder_path)
        
        if not os.path.exists(thumbnail_folder):
            logger.info(f"缩略图文件夹不存在: {thumbnail_folder}")
            return True
        
        # 删除缩略图文件夹及其内容
        for item in os.listdir(thumbnail_folder):
            item_path = os.path.join(thumbnail_folder, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
        
        logger.info(f"清除缩略图完成: {thumbnail_folder}")
        return True
    
    except Exception as e:
        logger.error(f"清除缩略图失败: {e}")
        return False


def get_thumbnail_cache_size(folder_path: str) -> int:
    """
    获取缩略图缓存大小（字节）
    
    Args:
        folder_path: 原始照片文件夹路径
        
    Returns:
        缩略图缓存大小（字节）
    """
    try:
        thumbnail_folder = get_thumbnail_folder(folder_path)
        
        if not os.path.exists(thumbnail_folder):
            return 0
        
        total_size = 0
        for item in os.listdir(thumbnail_folder):
            item_path = os.path.join(thumbnail_folder, item)
            if os.path.isfile(item_path):
                total_size += os.path.getsize(item_path)
        
        return total_size
    
    except Exception as e:
        logger.error(f"获取缩略图缓存大小失败: {e}")
        return 0