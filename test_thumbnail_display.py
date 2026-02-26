#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试缩略图显示问题
"""

import json
import os
import sys

# 添加Backend路径
sys.path.insert(0, 'Backend')
from json_manager import get_json_file_path

def check_json_structure(folder_path):
    """检查JSON文件结构"""
    print(f"检查文件夹: {folder_path}")
    print(f"文件夹是否存在: {os.path.exists(folder_path)}")
    
    json_path = get_json_file_path(folder_path)
    print(f"JSON文件路径: {json_path}")
    print(f"JSON文件是否存在: {os.path.exists(json_path)}")
    
    if not os.path.exists(json_path):
        print("❌ JSON文件不存在")
        return
    
    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    photos = data.get('photos', [])
    print(f"\n📊 照片数量: {len(photos)}")
    
    if not photos:
        print("❌ 没有照片数据")
        return
    
    # 检查第一张照片的数据结构
    print(f"\n📸 第一张照片数据结构:")
    photo = photos[0]
    print(f"  photo keys: {list(photo.keys())}")
    
    photo_metadata = photo.get('photo_metadata', {})
    print(f"  photo_metadata keys: {list(photo_metadata.keys())}")
    
    file_info = photo_metadata.get('file_info', {})
    print(f"\n📁 file_info 内容:")
    for key, value in file_info.items():
        print(f"    {key}: {value}")
    
    # 检查缩略图路径
    thumbnail_path = file_info.get('thumbnail_path', '')
    print(f"\n🖼️ 缩略图路径: {thumbnail_path}")
    print(f"  缩略图文件是否存在: {os.path.exists(thumbnail_path)}")
    
    if os.path.exists(thumbnail_path):
        file_size = os.path.getsize(thumbnail_path)
        print(f"  缩略图文件大小: {file_size} 字节")
    
    # 检查所有照片的缩略图
    print(f"\n📋 所有照片缩略图状态:")
    missing_thumbnails = []
    for i, photo in enumerate(photos):
        photo_metadata = photo.get('photo_metadata', {})
        file_info = photo_metadata.get('file_info', {})
        thumbnail_path = file_info.get('thumbnail_path', '')
        file_name = file_info.get('file_name', 'Unknown')
        exists = os.path.exists(thumbnail_path)
        
        status = "✅" if exists else "❌"
        print(f"  {status} {i+1}. {file_name}: {thumbnail_path}")
        
        if not exists:
            missing_thumbnails.append(file_name)
    
    if missing_thumbnails:
        print(f"\n⚠️  缺少缩略图的照片 ({len(missing_thumbnails)}):")
        for name in missing_thumbnails:
            print(f"    - {name}")
    else:
        print(f"\n✅ 所有照片的缩略图都存在")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = input("请输入导入的照片文件夹路径: ")
    
    check_json_structure(folder_path)