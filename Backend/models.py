#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data models for photo metadata
"""

from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any
from datetime import datetime


def serialize_value(value: Any) -> Any:
    """
    将值转换为JSON可序列化的格式
    
    处理特殊类型，如IFDRational、IFDTag等
    """
    if value is None:
        return None
    
    # 处理Pillow的特殊类型
    if hasattr(value, 'numerator') and hasattr(value, 'denominator'):
        # IFDRational 或其他有理数类型
        try:
            if value.denominator == 0:
                return str(value)
            return float(value.numerator) / float(value.denominator)
        except:
            return str(value)
    
    # 处理元组
    if isinstance(value, tuple):
        return [serialize_value(v) for v in value]
    
    # 处理列表
    if isinstance(value, list):
        return [serialize_value(v) for v in value]
    
    # 处理字典
    if isinstance(value, dict):
        return {k: serialize_value(v) for k, v in value.items()}
    
    # 处理datetime
    if isinstance(value, datetime):
        return value.isoformat()
    
    # 处理字节
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8', errors='ignore')
        except:
            return str(value)
    
    # 尝试直接转换
    try:
        return float(value)
    except (ValueError, TypeError):
        pass
    
    # 如果是其他类型，转换为字符串
    return str(value)


def serialize_dataclass(obj: Any) -> Dict:
    """
    将dataclass对象序列化为字典，处理特殊类型
    """
    if hasattr(obj, '__dataclass_fields__'):
        result = {}
        for field_name, field_value in obj.__dict__.items():
            result[field_name] = serialize_value(field_value)
        return result
    return serialize_value(obj)


@dataclass
class FileInfo:
    """文件信息"""
    file_name: str
    file_path: str
    file_size_bytes: int
    file_format: str
    file_extension: str
    creation_time: str
    modification_time: Optional[str] = None
    hash: str = ""


@dataclass
class ImageInfo:
    """图片信息"""
    width_px: int
    height_px: int
    aspect_ratio: Optional[float] = None
    color_mode: Optional[str] = None
    bits_per_sample: Optional[int] = None


@dataclass
class CameraInfo:
    """相机信息"""
    make: Optional[str] = None
    model: Optional[str] = None
    lens_make: Optional[str] = None
    lens_model: Optional[str] = None
    focal_length: Optional[str] = None
    aperture: Optional[str] = None
    iso: Optional[int] = None
    shutter_speed: Optional[str] = None
    exposure_mode: Optional[str] = None


@dataclass
class ExifData:
    """EXIF数据"""
    date_time_original: Optional[str] = None
    orientation: Optional[int] = None
    flash_used: Optional[bool] = None
    white_balance: Optional[str] = None
    metering_mode: Optional[str] = None


@dataclass
class GPSInfo:
    """GPS信息"""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    gps_date_time: Optional[str] = None
    coordinates: Optional[str] = None


@dataclass
class AdditionalInfo:
    """附加信息"""
    color_space: Optional[str] = None
    compression: Optional[str] = None
    software: Optional[str] = None


@dataclass
class PhotoMetadata:
    """照片元数据"""
    file_info: FileInfo
    image_info: ImageInfo
    camera_info: CameraInfo = field(default_factory=CameraInfo)
    exif_data: ExifData = field(default_factory=ExifData)
    gps_info: GPSInfo = field(default_factory=GPSInfo)
    additional_info: AdditionalInfo = field(default_factory=AdditionalInfo)
    quality: str = "未审查"
    
    def to_dict(self) -> Dict:
        """转换为字典格式，处理特殊类型"""
        return {
            "photo_metadata": {
                "file_info": serialize_dataclass(self.file_info),
                "image_info": serialize_dataclass(self.image_info),
                "camera_info": serialize_dataclass(self.camera_info),
                "exif_data": serialize_dataclass(self.exif_data),
                "gps_info": serialize_dataclass(self.gps_info),
                "additional_info": serialize_dataclass(self.additional_info),
                "quality": self.quality
            }
        }
