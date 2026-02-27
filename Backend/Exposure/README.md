# 曝光检测模块 (Exposure Detection Module)

## 概述

本模块用于检测图片的过曝和欠曝情况，为人像摄影废片过滤工具提供质量筛查功能。

## 功能特性

### 1. 过曝检测 (Overexposure Detection)
- 高光像素占比检测（亮度值 ≥ 245）
- RGB通道最大值占比检测（单通道值 ≥ 250）
- 直方图高光区域占比检测（240-255区间）
- 过曝区域连通性检测（大面积连续过曝）

### 2. 欠曝检测 (Underexposure Detection)
- 暗部像素占比检测（亮度值 ≤ 50）
- RGB通道最小值占比检测（单通道值 ≤ 30）
- 直方图暗部区域占比检测（0-40区间）
- 平均亮度值检测

### 3. 配置管理
- 支持本地配置文件存储所有阈值
- 程序启动时自动加载配置
- 支持运行时重新加载配置

## 目录结构

```
Backend/Exposure/
├── __init__.py                      # 模块初始化文件
├── exposure_detector.py             # 主检测器类
├── config_manager.py               # 配置管理器
├── config/                         # 配置文件目录
│   ├── __init__.py
│   └── exposure_config.json        # 曝光检测配置文件
├── overexposure/                   # 过曝检测模块
│   ├── __init__.py
│   └── overexposure_detector.py    # 过曝检测器
├── underexposure/                  # 欠曝检测模块
│   ├── __init__.py
│   └── underexposure_detector.py  # 欠曝检测器
├── test_exposure_detection.py      # 测试脚本
└── README.md                       # 本文档
```

## 配置文件说明

配置文件位于 `Backend/Exposure/config/exposure_config.json`，包含以下内容：

### 过曝检测阈值
- `highlight_pixel_ratio_threshold`: 高光像素占比阈值（默认: 0.05, 即5%）
- `rgb_max_channel_ratio_threshold`: RGB通道最大值占比阈值（默认: 0.03, 即3%）
- `histogram_highlight_ratio_threshold`: 直方图高光区域占比阈值（默认: 0.08, 即8%）
- `connected_overexposed_area_threshold`: 连通过曝区域占比阈值（默认: 0.02, 即2%）

### 欠曝检测阈值
- `shadow_pixel_ratio_threshold`: 暗部像素占比阈值（默认: 0.15, 即15%）
- `rgb_min_channel_ratio_threshold`: RGB通道最小值占比阈值（默认: 0.10, 即10%）
- `histogram_shadow_ratio_threshold`: 直方图暗部区域占比阈值（默认: 0.20, 即20%）
- `average_brightness_threshold`: 平均亮度阈值（默认: 80.0）

## 使用方法

### 1. 基本使用

```python
from Backend.Exposure import ExposureDetector

# 初始化检测器
detector = ExposureDetector()

# 检测单张图片
result = detector.detect_single_image("path/to/image.jpg")

print(f"质量标签: {result['quality']}")
print(f"是否过曝: {result['is_overexposed']}")
print(f"是否欠曝: {result['is_underexposed']}")
```

### 2. 批量检测

```python
# 检测文件夹中所有图片
results = detector.detect_folder("path/to/folder")

# 统计结果
quality_counts = {}
for result in results:
    quality = result['quality']
    quality_counts[quality] = quality_counts.get(quality, 0) + 1

print(quality_counts)
```

### 3. 更新JSON文件

```python
# 检测并更新JSON文件中的质量字段
json_file_path = "path/to/QualityRecord.json"
success, quality = detector.update_json_quality(json_file_path, "path/to/image.jpg")

# 批量更新文件夹
stats = detector.update_folder_json_quality(
    json_file_path,
    "path/to/folder",
    max_workers=4
)

print(f"总计: {stats['total']}")
print(f"成功: {stats['success']}")
print(f"失败: {stats['failed']}")
print(f"质量统计: {stats['quality_stats']}")
```

### 4. 配置管理

```python
from Backend.Exposure import ConfigManager

# 加载配置
config_manager = ConfigManager()
config = config_manager.get_config()

# 获取特定阈值
overexposure_config = config_manager.get_overexposure_config()
underexposure_config = config_manager.get_underexposure_config()

# 重新加载配置
detector.reload_config()
```

## 质量标签说明

检测完成后，图片会被标记为以下质量标签之一：

- **合格**: 既不过曝也不欠曝
- **过曝**: 检测到过曝
- **欠曝**: 检测到欠曝
- **过曝,欠曝**: 同时检测到过曝和欠曝
- **检测失败**: 检测过程中出现错误
- **未审查**: 尚未进行检测

## 技术栈

- **OpenCV**: 图像处理和计算机视觉
- **NumPy**: 数值计算和数组操作
- **Python 3.7+**: 编程语言

## 性能优化

1. **多线程处理**: 支持批量检测时的多线程处理，可配置线程数
2. **并行检测**: 过曝和欠曝检测并行执行
3. **高效算法**: 使用向量化操作和优化的图像处理算法

## 测试

运行测试脚本：

```bash
cd Backend/Exposure
python test_exposure_detection.py
```

测试脚本包含以下测试用例：
- 配置文件加载测试
- 单张图片检测测试
- 文件夹批量检测测试
- 配置重载测试

## 注意事项

1. **配置文件路径**: 默认配置文件位于 `Backend/Exposure/config/exposure_config.json`，可自定义路径
2. **图片格式**: 支持 JPG、JPEG、PNG、BMP、TIFF、WEBP 等常见格式
3. **内存使用**: 批量检测大量图片时，注意内存使用情况，可适当调整 `max_workers` 参数
4. **日志记录**: 模块使用 Python logging 模块记录运行信息和错误

## 扩展性

本模块设计具有良好的扩展性，可以：

1. 添加新的检测指标
2. 自定义质量标签判定逻辑
3. 集成其他图像质量评估算法
4. 支持配置文件的动态更新

## 版本历史

- **v1.0** (2024-02-27): 初始版本
  - 实现过曝检测
  - 实现欠曝检测
  - 实现配置文件管理
  - 实现JSON文件更新功能
  - 支持批量检测和多线程处理

## 作者

PictureFilter 项目组

## 许可证

本项目采用开源许可证，详见项目根目录的 LICENSE 文件。