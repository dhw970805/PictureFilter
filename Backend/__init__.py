#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Backend package for PictureFilter
Handles photo import, metadata extraction, and JSON file management
"""

from .file_importer import import_folder, process_single_file, refresh_folder, check_duplicates, get_import_stats
from .metadata_extractor import extract_exif_data
from .json_manager import append_to_json, read_json_file, update_photo_metadata
from .models import (
    FileInfo, ImageInfo, CameraInfo, ExifData, 
    GPSInfo, AdditionalInfo, PhotoMetadata
)
from .exceptions import (
    FileImportError, UnsupportedFormatError, 
    FileCorruptedError, JsonWriteError
)
from .progress_tracker import ProgressTracker

__version__ = "1.0.0"
__all__ = [
    # Main functions
    'import_folder',
    'process_single_file',
    'refresh_folder',
    'check_duplicates',
    'get_import_stats',
    'extract_exif_data',
    'append_to_json',
    'read_json_file',
    'update_photo_metadata',
    # Models
    'FileInfo',
    'ImageInfo',
    'CameraInfo',
    'ExifData',
    'GPSInfo',
    'AdditionalInfo',
    'PhotoMetadata',
    # Exceptions
    'FileImportError',
    'UnsupportedFormatError',
    'FileCorruptedError',
    'JsonWriteError',
    # Utilities
    'ProgressTracker',
]