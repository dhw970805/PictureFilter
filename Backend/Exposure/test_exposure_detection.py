#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for exposure detection
"""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Exposure import ExposureDetector, ConfigManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_config_loading():
    """Test configuration loading"""
    logger.info("=== Testing Configuration Loading ===")
    
    config_manager = ConfigManager()
    config = config_manager.get_config()
    
    logger.info(f"Configuration version: {config['version']}")
    logger.info(f"Overexposure config: {config['overexposure']}")
    logger.info(f"Underexposure config: {config['underexposure']}")
    
    logger.info("✓ Configuration loaded successfully\n")


def test_single_image_detection(image_path: str):
    """Test single image detection"""
    logger.info("=== Testing Single Image Detection ===")
    
    if not os.path.exists(image_path):
        logger.error(f"Image file not found: {image_path}")
        return
    
    detector = ExposureDetector()
    result = detector.detect_single_image(image_path)
    
    logger.info(f"Image: {image_path}")
    logger.info(f"Quality: {result['quality']}")
    logger.info(f"Overexposed: {result['is_overexposed']}")
    logger.info(f"Underexposed: {result['is_underexposed']}")
    
    if 'overexposure_details' in result and 'error' not in result['overexposure_details']:
        details = result['overexposure_details']
        logger.info(f"  - Highlight pixel ratio: {details['highlight_pixel_ratio']:.4f}")
        logger.info(f"  - RGB max channel ratio: {details['rgb_max_channel_ratio']:.4f}")
        logger.info(f"  - Histogram highlight ratio: {details['histogram_highlight_ratio']:.4f}")
    
    if 'underexposure_details' in result and 'error' not in result['underexposure_details']:
        details = result['underexposure_details']
        logger.info(f"  - Shadow pixel ratio: {details['shadow_pixel_ratio']:.4f}")
        logger.info(f"  - RGB min channel ratio: {details['rgb_min_channel_ratio']:.4f}")
        logger.info(f"  - Histogram shadow ratio: {details['histogram_shadow_ratio']:.4f}")
        logger.info(f"  - Average brightness: {details['average_brightness']:.2f}")
    
    logger.info("✓ Single image detection completed\n")


def test_folder_detection(folder_path: str):
    """Test folder detection"""
    logger.info("=== Testing Folder Detection ===")
    
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        logger.error(f"Invalid folder: {folder_path}")
        return
    
    detector = ExposureDetector()
    results = detector.detect_folder(folder_path)
    
    logger.info(f"Found {len(results)} images")
    
    # Count quality types
    quality_counts = {}
    for result in results:
        quality = result.get('quality', 'unknown')
        quality_counts[quality] = quality_counts.get(quality, 0) + 1
    
    for quality, count in quality_counts.items():
        logger.info(f"  {quality}: {count}")
    
    logger.info("✓ Folder detection completed\n")


def test_config_reload():
    """Test configuration reload"""
    logger.info("=== Testing Configuration Reload ===")
    
    detector = ExposureDetector()
    
    # Get initial config
    initial_config = detector.get_current_config()
    logger.info("Initial configuration loaded")
    
    # Reload config
    detector.reload_config()
    logger.info("Configuration reloaded")
    
    # Get new config
    new_config = detector.get_current_config()
    logger.info("New configuration loaded")
    
    logger.info("✓ Configuration reload test completed\n")


def main():
    """Main test function"""
    logger.info("=" * 60)
    logger.info("Exposure Detection Test Suite")
    logger.info("=" * 60 + "\n")
    
    # Test 1: Configuration loading
    test_config_loading()
    
    # Test 2: Single image detection (requires a test image)
    # Uncomment and provide a valid image path to test
    # test_image_path = "path/to/test/image.jpg"
    # test_single_image_detection(test_image_path)
    
    # Test 3: Folder detection (requires a test folder)
    # Uncomment and provide a valid folder path to test
    # test_folder_path = "path/to/test/folder"
    # test_folder_detection(test_folder_path)
    
    # Test 4: Configuration reload
    test_config_reload()
    
    logger.info("=" * 60)
    logger.info("All tests completed!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()