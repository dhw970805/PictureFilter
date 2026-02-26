#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Backend test script
Demonstrates the backend functionality
"""

import sys
import os
import logging
from pathlib import Path

# Add parent directory to path to import Backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from Backend import (
    import_folder,
    process_single_file,
    extract_exif_data,
    append_to_json,
    read_json_file,
    update_photo_metadata,
    ProgressTracker
)
from Backend.utils import is_supported_image_file, get_file_format, calculate_file_hash

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('backend_test.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


def test_utils():
    """测试工具函数"""
    logger.info("=" * 60)
    logger.info("Testing utility functions")
    logger.info("=" * 60)
    
    # 测试支持的格式
    test_files = [
        "test.jpg",
        "test.png",
        "test.cr2",
        "test.heic",
        "test.txt",
        "test.pdf"
    ]
    
    for file in test_files:
        is_supported = is_supported_image_file(file)
        file_format = get_file_format(file) if is_supported else "N/A"
        logger.info(f"  {file}: Supported={is_supported}, Format={file_format}")
    
    # 测试哈希计算
    test_hash = calculate_file_hash(
        "test.jpg",
        "/path/to/test.jpg",
        1024,
        "JPEG",
        "2024-02-26T14:35:22+08:00"
    )
    logger.info(f"\n  Test hash: {test_hash[:16]}...")
    
    logger.info("\n✓ Utility functions test completed\n")


def test_metadata_extraction():
    """测试元数据提取"""
    logger.info("=" * 60)
    logger.info("Testing metadata extraction")
    logger.info("=" * 60)
    
    # 查找测试图片文件
    test_image = None
    possible_locations = [
        "test_image.jpg",
        "sample.jpg",
        "../Frontend/Resources/sample.jpg",
        "../../sample.jpg"
    ]
    
    for location in possible_locations:
        if os.path.exists(location):
            test_image = os.path.abspath(location)
            break
    
    if test_image:
        logger.info(f"Using test image: {test_image}")
        
        # 提取元数据
        metadata = process_single_file(test_image, os.path.dirname(test_image))
        
        if metadata:
            logger.info("\n  File Info:")
            logger.info(f"    Name: {metadata.file_info.file_name}")
            logger.info(f"    Size: {metadata.file_info.file_size_bytes} bytes")
            logger.info(f"    Format: {metadata.file_info.file_format}")
            logger.info(f"    Hash: {metadata.file_info.hash[:16]}...")
            
            logger.info("\n  Image Info:")
            logger.info(f"    Dimensions: {metadata.image_info.width_px}x{metadata.image_info.height_px}")
            logger.info(f"    Aspect Ratio: {metadata.image_info.aspect_ratio}")
            logger.info(f"    Color Mode: {metadata.image_info.color_mode}")
            
            logger.info("\n  Camera Info:")
            logger.info(f"    Make: {metadata.camera_info.make}")
            logger.info(f"    Model: {metadata.camera_info.model}")
            logger.info(f"    ISO: {metadata.camera_info.iso}")
            logger.info(f"    Aperture: {metadata.camera_info.aperture}")
            
            logger.info("\n  EXIF Data:")
            logger.info(f"    Date: {metadata.exif_data.date_time_original}")
            logger.info(f"    Flash: {metadata.exif_data.flash_used}")
            
            logger.info("\n  GPS Info:")
            logger.info(f"    Coordinates: {metadata.gps_info.coordinates}")
            
            logger.info("\n✓ Metadata extraction test completed\n")
        else:
            logger.warning("Failed to extract metadata from test image\n")
    else:
        logger.warning("No test image found. Skipping metadata extraction test\n")
        logger.info("To test metadata extraction, place a sample image file in the project directory\n")


def test_json_operations():
    """测试JSON操作"""
    logger.info("=" * 60)
    logger.info("Testing JSON operations")
    logger.info("=" * 60)
    
    # 创建测试目录
    test_dir = "test_json_data"
    os.makedirs(test_dir, exist_ok=True)
    json_path = os.path.join(test_dir, "QualityRecord.json")
    
    # 清理旧文件
    if os.path.exists(json_path):
        os.remove(json_path)
    
    logger.info(f"Created test directory: {test_dir}")
    
    # 测试读取不存在的文件
    data = read_json_file(json_path)
    logger.info(f"  Reading non-existent file: {data}")
    
    # 测试创建新JSON文件
    from Backend.json_manager import create_json_structure
    new_data = create_json_structure(test_dir)
    logger.info(f"  Created new JSON structure with {len(new_data)} fields")
    
    # 测试写入文件
    from Backend.json_manager import write_json_file
    success = write_json_file(json_path, new_data, backup=False)
    logger.info(f"  Write JSON file: {success}")
    
    # 测试读取文件
    data = read_json_file(json_path)
    if data:
        logger.info(f"  Read JSON file successfully")
        logger.info(f"    Version: {data.get('version')}")
        logger.info(f"    Created: {data.get('created_time')}")
        logger.info(f"    Total photos: {data.get('total_photos')}")
    
    # 清理测试文件
    import shutil
    shutil.rmtree(test_dir)
    logger.info(f"\n✓ Cleaned up test directory\n")


def test_progress_tracker():
    """测试进度跟踪器"""
    logger.info("=" * 60)
    logger.info("Testing progress tracker")
    logger.info("=" * 60)
    
    tracker = ProgressTracker(10)
    logger.info(f"  Initialized with total: {tracker.total}")
    
    for i in range(10):
        tracker.update(success=(i % 3 != 0))  # 模拟每3个失败1个
        if i % 3 == 0:
            continue
        
        progress = tracker.get_progress()
        logger.info(f"  Progress {i+1}/10: {progress['percentage']:.1f}% - "
                   f"Imported: {progress['imported']}, Errors: {progress['errors']}")
    
    final_progress = tracker.get_progress()
    logger.info(f"\n  Final status:")
    logger.info(f"    Total: {final_progress['total']}")
    logger.info(f"    Processed: {final_progress['processed']}")
    logger.info(f"    Imported: {final_progress['imported']}")
    logger.info(f"    Errors: {final_progress['errors']}")
    logger.info(f"    Percentage: {final_progress['percentage']:.1f}%")
    
    logger.info("\n✓ Progress tracker test completed\n")


def test_folder_import():
    """测试文件夹导入"""
    logger.info("=" * 60)
    logger.info("Testing folder import")
    logger.info("=" * 60)
    
    # 查找测试文件夹
    test_folder = None
    possible_folders = [
        "test_photos",
        "sample_photos",
        "TestPhotos",
        "../test_photos",
        "../../test_photos"
    ]
    
    for folder in possible_folders:
        if os.path.exists(folder) and os.path.isdir(folder):
            test_folder = os.path.abspath(folder)
            break
    
    if test_folder:
        logger.info(f"Using test folder: {test_folder}")
        
        # 定义进度回调
        def progress_callback(progress):
            logger.info(f"  Progress: {progress['percentage']:.1f}% "
                       f"({progress['imported']} imported, {progress['errors']} errors)")
        
        # 导入文件夹
        result = import_folder(
            folder_path=test_folder,
            recursive=False,
            skip_existing=False,
            progress_callback=progress_callback,
            max_workers=2
        )
        
        logger.info(f"\n  Import result:")
        logger.info(f"    Success: {result['success']}")
        logger.info(f"    Total files: {result['total_files']}")
        logger.info(f"    Imported: {result['imported_files']}")
        logger.info(f"    Skipped: {result['skipped_files']}")
        logger.info(f"    Errors: {result['error_files']}")
        logger.info(f"    JSON file: {result['json_file_path']}")
        
        if result['errors']:
            logger.info(f"\n  Errors:")
            for error in result['errors'][:3]:  # 只显示前3个错误
                logger.info(f"    - {error}")
        
        logger.info("\n✓ Folder import test completed\n")
    else:
        logger.warning("No test folder found. Skipping folder import test")
        logger.info("To test folder import, create a folder named 'test_photos' with some image files\n")


def main():
    """主测试函数"""
    logger.info("\n" + "=" * 60)
    logger.info("Backend Test Suite")
    logger.info("=" * 60 + "\n")
    
    try:
        # 运行所有测试
        test_utils()
        test_metadata_extraction()
        test_json_operations()
        test_progress_tracker()
        test_folder_import()
        
        logger.info("=" * 60)
        logger.info("All tests completed!")
        logger.info("=" * 60 + "\n")
        
    except Exception as e:
        logger.error(f"\n✗ Test suite failed with error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())