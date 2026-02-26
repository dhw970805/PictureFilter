#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Custom exceptions for the backend module
"""


class FileImportError(Exception):
    """文件导入异常"""
    pass


class UnsupportedFormatError(Exception):
    """不支持的文件格式异常"""
    pass


class FileCorruptedError(Exception):
    """文件损坏异常"""
    pass


class JsonWriteError(Exception):
    """JSON写入异常"""
    pass