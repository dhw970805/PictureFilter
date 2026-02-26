#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract metadata from image files including EXIF data
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import logging

try:
    from PIL import Image, ExifTags, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from .models import (
    FileInfo, ImageInfo, CameraInfo, ExifData,
    GPSInfo, AdditionalInfo, PhotoMetadata
)
from .utils import (
    get_file_format, get_file_extension,
    calculate_file_hash, get_file_timestamps
)
from .exceptions import UnsupportedFormatError, FileCorruptedError

logger = logging.getLogger(__name__)


def extract_exif_data(file_path: str) -> Dict[str, Any]:
    """
    从图片文件中提取EXIF数据
    
    Args:
        file_path: 图片文件路径
        
    Returns:
        EXIF数据字典
    """
    if not PIL_AVAILABLE:
        logger.warning("PIL/Pillow not available, cannot extract EXIF data")
        return {}
    
    exif_data = {}
    
    try:
        with Image.open(file_path) as img:
            # 获取EXIF数据
            if hasattr(img, '_getexif'):
                exif = img._getexif()
                if exif is not None:
                    # 将EXIF标签ID转换为名称
                    for tag_id, value in exif.items():
                        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                        exif_data[tag_name] = value
    
    except Exception as e:
        logger.error(f"Error extracting EXIF from {file_path}: {e}")
    
    return exif_data


def extract_metadata(file_path: str, folder_path: str) -> Optional[PhotoMetadata]:
    """
    提取单个文件的完整元数据
    
    Args:
        file_path: 图片文件路径
        folder_path: 文件夹路径
        
    Returns:
        PhotoMetadata对象，失败返回None
    """
    try:
        file_info = extract_file_info(file_path)
        image_info = extract_image_info(file_path)
        camera_info = extract_camera_info(file_path)
        exif_data = extract_exif_info(file_path)
        gps_info = extract_gps_info(file_path)
        additional_info = extract_additional_info(file_path)
        
        metadata = PhotoMetadata(
            file_info=file_info,
            image_info=image_info,
            camera_info=camera_info,
            exif_data=exif_data,
            gps_info=gps_info,
            additional_info=additional_info,
            quality="未审查"
        )
        
        return metadata
        
    except Exception as e:
        logger.error(f"Error extracting metadata from {file_path}: {e}")
        return None


def extract_file_info(file_path: str) -> FileInfo:
    """
    提取文件基本信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        FileInfo对象
    """
    path = Path(file_path)
    
    # 获取文件名
    file_name = path.name
    
    # 获取文件大小
    file_size_bytes = path.stat().st_size
    
    # 获取文件格式和扩展名
    file_format = get_file_format(file_path)
    file_extension = get_file_extension(file_path)
    
    # 获取时间戳
    creation_time, modification_time = get_file_timestamps(file_path)
    
    # 计算哈希值
    hash_value = calculate_file_hash(
        file_name, file_path, file_size_bytes, file_format, creation_time
    )
    
    return FileInfo(
        file_name=file_name,
        file_path=file_path,
        file_size_bytes=file_size_bytes,
        file_format=file_format,
        file_extension=file_extension,
        creation_time=creation_time,
        modification_time=modification_time,
        hash=hash_value
    )


def extract_image_info(file_path: str) -> ImageInfo:
    """
    提取图片信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        ImageInfo对象
    """
    if not PIL_AVAILABLE:
        # 如果PIL不可用，返回默认值
        return ImageInfo(width_px=0, height_px=0)
    
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            
            # 计算宽高比
            aspect_ratio = width / height if height > 0 else None
            
            # 获取颜色模式
            color_mode = img.mode
            
            # 获取每样本位数
            bits_per_sample = None
            if hasattr(img, 'bits'):
                bits_per_sample = img.bits
            elif hasattr(img, 'info') and 'bits' in img.info:
                bits_per_sample = img.info['bits']
            
            return ImageInfo(
                width_px=width,
                height_px=height,
                aspect_ratio=aspect_ratio,
                color_mode=color_mode,
                bits_per_sample=bits_per_sample
            )
    
    except Exception as e:
        logger.error(f"Error extracting image info from {file_path}: {e}")
        return ImageInfo(width_px=0, height_px=0)


def extract_camera_info(file_path: str) -> CameraInfo:
    """
    提取相机信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        CameraInfo对象
    """
    exif = extract_exif_data(file_path)
    
    return CameraInfo(
        make=exif.get('Make'),
        model=exif.get('Model'),
        lens_make=exif.get('LensMake'),
        lens_model=exif.get('LensModel'),
        focal_length=exif.get('FocalLength'),
        aperture=exif.get('FNumber'),
        iso=exif.get('ISOSpeedRatings'),
        shutter_speed=exif.get('ExposureTime'),
        exposure_mode=exif.get('ExposureMode')
    )


def extract_exif_info(file_path: str) -> ExifData:
    """
    提取EXIF数据
    
    Args:
        file_path: 文件路径
        
    Returns:
        ExifData对象
    """
    exif = extract_exif_data(file_path)
    
    # 格式化日期时间
    date_time_original = exif.get('DateTimeOriginal')
    if date_time_original:
        try:
            # 尝试解析EXIF日期格式
            dt = datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S')
            date_time_original = dt.isoformat()
        except (ValueError, TypeError):
            pass
    
    # 处理闪光灯
    flash_used = None
    if 'Flash' in exif:
        flash_used = bool(exif['Flash'] & 1)
    
    return ExifData(
        date_time_original=date_time_original,
        orientation=exif.get('Orientation'),
        flash_used=flash_used,
        white_balance=exif.get('WhiteBalance'),
        metering_mode=exif.get('MeteringMode')
    )


def extract_gps_info(file_path: str) -> GPSInfo:
    """
    提取GPS信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        GPSInfo对象
    """
    exif = extract_exif_data(file_path)
    
    # GPS信息提取
    gps_info = {}
    
    # 获取GPS数据
    gps_data = exif.get('GPSInfo')
    if gps_data:
        # 提取纬度
        if 'GPSLatitude' in gps_data and 'GPSLatitudeRef' in gps_data:
            lat = gps_data['GPSLatitude']
            lat_ref = gps_data['GPSLatitudeRef']
            try:
                latitude = convert_gps_to_decimal(lat, lat_ref)
                gps_info['latitude'] = latitude
            except (ValueError, TypeError):
                pass
        
        # 提取经度
        if 'GPSLongitude' in gps_data and 'GPSLongitudeRef' in gps_data:
            lon = gps_data['GPSLongitude']
            lon_ref = gps_data['GPSLongitudeRef']
            try:
                longitude = convert_gps_to_decimal(lon, lon_ref)
                gps_info['longitude'] = longitude
            except (ValueError, TypeError):
                pass
        
        # 提取海拔
        if 'GPSAltitude' in gps_data:
            altitude = convert_rational(gps_data['GPSAltitude'])
            gps_info['altitude'] = altitude
        
        # 提取GPS时间
        if 'GPSDateStamp' in gps_data and 'GPSTimeStamp' in gps_data:
            try:
                date_str = gps_data['GPSDateStamp']
                time_tuple = gps_data['GPSTimeStamp']
                time_str = f"{int(time_tuple[0]):02d}:{int(time_tuple[1]):02d}:{int(time_tuple[2]):02d}"
                gps_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y:%m:%d %H:%M:%S")
                gps_info['gps_date_time'] = gps_datetime.isoformat()
            except (ValueError, TypeError):
                pass
    
    # 构建坐标字符串
    latitude = gps_info.get('latitude')
    longitude = gps_info.get('longitude')
    coordinates = None
    if latitude is not None and longitude is not None:
        coordinates = f"{latitude}, {longitude}"
    
    return GPSInfo(
        latitude=gps_info.get('latitude'),
        longitude=gps_info.get('longitude'),
        altitude=gps_info.get('altitude'),
        gps_date_time=gps_info.get('gps_date_time'),
        coordinates=coordinates
    )


def extract_additional_info(file_path: str) -> AdditionalInfo:
    """
    提取附加信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        AdditionalInfo对象
    """
    exif = extract_exif_data(file_path)
    
    return AdditionalInfo(
        color_space=exif.get('ColorSpace'),
        compression=exif.get('Compression'),
        software=exif.get('Software')
    )


def convert_gps_to_decimal(gps_tuple: tuple, ref: str) -> float:
    """
    将GPS坐标转换为十进制
    
    Args:
        gps_tuple: GPS坐标元组 (度, 分, 秒)
        ref: 参考方向 ('N', 'S', 'E', 'W')
        
    Returns:
        十进制坐标
    """
    degrees = convert_rational(gps_tuple[0])
    minutes = convert_rational(gps_tuple[1])
    seconds = convert_rational(gps_tuple[2])
    
    decimal = degrees + (minutes / 60) + (seconds / 3600)
    
    # 根据参考方向调整符号
    if ref in ['S', 'W']:
        decimal = -decimal
    
    return decimal


def convert_rational(rational) -> float:
    """
    转换有理数为浮点数
    
    Args:
        rational: 有理数 (可以是元组或单个值)
        
    Returns:
        浮点数
    """
    if isinstance(rational, tuple) and len(rational) == 2:
        return rational[0] / rational[1]
    return float(rational)