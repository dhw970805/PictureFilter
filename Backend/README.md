# Backend 模块文档

## 概述

Backend 模块提供了图片导入、元数据提取和 JSON 文件管理功能，是 PictureFilter 项目的核心后端组件。

## 功能特性

### 1. 图片导入
- 支持多种图片格式（JPG、PNG、BMP、TIFF、GIF、WebP、AVIF、HEIC、HEIF）
- 支持 RAW 格式（CR2、CR3、NEF、NRW、ARW、SRF、SR2、DNG、ORF、PEF、RAF、RW2）
- 支持递归扫描子文件夹
- 自动过滤非图片文件
- 基于哈希值的重复检测
- 进度跟踪和实时反馈

### 2. 元数据提取
- 文件基本信息（名称、大小、格式、创建时间等）
- 图片信息（尺寸、宽高比、颜色模式等）
- 相机信息（制造商、型号、镜头、ISO、光圈、快门等）
- EXIF 数据（拍摄时间、闪光灯、白平衡等）
- GPS 信息（经纬度、海拔、时间戳等）
- 附加信息（色彩空间、压缩方式、软件等）

### 3. JSON 文件管理
- 自动在照片文件夹创建 `QualityRecord.json`
- 支持增量更新（追加新记录）
- 支持元数据更新
- 线程安全的文件操作
- 备份机制
- 统计信息查询

## 项目结构

```
Backend/
├── __init__.py              # 包初始化和公共接口
├── models.py                # 数据模型定义
├── exceptions.py            # 自定义异常类
├── progress_tracker.py      # 进度跟踪器
├── utils.py                 # 工具函数
├── metadata_extractor.py     # 元数据提取器
├── json_manager.py          # JSON 文件管理器
├── file_importer.py         # 文件导入器
├── requirements.txt          # 依赖项
├── test_backend.py          # 后端测试脚本
├── integration_example.py    # 前端集成示例
└── README.md               # 本文档
```

## 安装

### 依赖项

```bash
pip install -r Backend/requirements.txt
```

必需依赖：
- Pillow >= 10.0.0

可选依赖（用于扩展功能）：
- rawpy >= 0.18.0 (RAW 格式支持)
- pillow-heif >= 0.13.0 (HEIC/HEIF 格式支持)
- exifread >= 3.0.0 (额外的 EXIF 提取)

## 使用方法

### 1. 导入文件夹

```python
from Backend import import_folder

# 定义进度回调
def progress_callback(progress):
    print(f"进度: {progress['percentage']:.1f}%")

# 导入文件夹
result = import_folder(
    folder_path="/path/to/photos",
    recursive=True,  # 递归扫描子文件夹
    skip_existing=True,  # 跳过已存在的文件
    progress_callback=progress_callback,
    max_workers=4  # 并发线程数
)

print(f"导入完成: {result['imported_files']} 个文件")
```

### 2. 处理单个文件

```python
from Backend import process_single_file

# 处理单个图片文件
metadata = process_single_file(
    file_path="/path/to/photo.jpg",
    folder_path="/path/to/photos"
)

if metadata:
    print(f"文件名: {metadata.file_info.file_name}")
    print(f"尺寸: {metadata.image_info.width_px}x{metadata.image_info.height_px}")
    print(f"相机: {metadata.camera_info.make} {metadata.camera_info.model}")
```

### 3. 读取和更新 JSON

```python
from Backend import read_json_file, update_photo_metadata

# 读取 JSON 文件
data = read_json_file("/path/to/photos/QualityRecord.json")

# 更新照片元数据
update_photo_metadata(
    json_file_path="/path/to/photos/QualityRecord.json",
    file_hash="abc123...",
    metadata_updates={"quality": "优质"}
)
```

### 4. 获取统计信息

```python
from Backend import get_import_stats

stats = get_import_stats("/path/to/photos")
print(f"总照片数: {stats['total_photos']}")
print(f"质量统计: {stats['quality_stats']}")
```

## 数据模型

### PhotoMetadata

完整的照片元数据对象，包含以下子对象：

- **FileInfo**: 文件基本信息
- **ImageInfo**: 图片信息
- **CameraInfo**: 相机信息
- **ExifData**: EXIF 数据
- **GPSInfo**: GPS 信息
- **AdditionalInfo**: 附加信息
- **quality**: 质量标记（字符串）

### JSON 文件结构

```json
{
  "version": "1.0",
  "created_time": "2024-02-26T14:35:22+08:00",
  "last_updated": "2024-02-26T15:30:45+08:00",
  "folder_path": "/path/to/photos",
  "total_photos": 150,
  "photos": [
    {
      "photo_metadata": {
        "file_info": { ... },
        "image_info": { ... },
        "camera_info": { ... },
        "exif_data": { ... },
        "gps_info": { ... },
        "additional_info": { ... },
        "quality": "未审查"
      }
    }
  ]
}
```

## 前端集成

### 使用 QThread 进行后台导入

```python
from PyQt6.QtCore import QThread, pyqtSignal
from Backend import import_folder

class ImportWorker(QThread):
    progress_updated = pyqtSignal(dict)
    import_completed = pyqtSignal(dict)
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
    
    def run(self):
        def progress_callback(progress):
            self.progress_updated.emit(progress)
        
        result = import_folder(
            folder_path=self.folder_path,
            progress_callback=progress_callback
        )
        self.import_completed.emit(result)
```

完整示例请参考 `integration_example.py`。

## 测试

运行测试脚本：

```bash
python Backend/test_backend.py
```

测试包括：
- 工具函数测试
- 元数据提取测试
- JSON 操作测试
- 进度跟踪器测试
- 文件夹导入测试

## API 参考

### 主要函数

#### `import_folder(folder_path, recursive=False, skip_existing=True, file_filters=None, progress_callback=None, max_workers=4)`

导入文件夹中的所有图片。

**参数:**
- `folder_path`: 文件夹路径
- `recursive`: 是否递归扫描子文件夹
- `skip_existing`: 是否跳过已存在的文件
- `file_filters`: 文件过滤条件（可选）
- `progress_callback`: 进度回调函数
- `max_workers`: 最大并发线程数

**返回:**
- 导入结果字典

#### `process_single_file(file_path, folder_path, skip_existing=False, json_file_manager=None)`

处理单个图片文件，提取元数据。

**参数:**
- `file_path`: 图片文件路径
- `folder_path`: 文件夹路径
- `skip_existing`: 是否跳过已存在的文件
- `json_file_manager`: JSON 文件管理器对象

**返回:**
- PhotoMetadata 对象，失败返回 None

#### `extract_exif_data(file_path)`

从图片文件中提取 EXIF 数据。

**参数:**
- `file_path`: 图片文件路径

**返回:**
- EXIF 数据字典

#### `append_to_json(json_file_path, photo_metadata, create_if_not_exists=True, backup=True)`

将照片元数据追加到 JSON 文件。

**参数:**
- `json_file_path`: JSON 文件路径
- `photo_metadata`: 照片元数据对象
- `create_if_not_exists`: 文件不存在时是否创建
- `backup`: 是否创建备份

**返回:**
- 是否成功

#### `read_json_file(json_file_path)`

读取 JSON 文件。

**参数:**
- `json_file_path`: JSON 文件路径

**返回:**
- JSON 数据字典，文件不存在或读取失败返回 None

#### `update_photo_metadata(json_file_path, file_hash, metadata_updates, backup=True)`

更新照片的元数据。

**参数:**
- `json_file_path`: JSON 文件路径
- `file_hash`: 文件哈希值
- `metadata_updates`: 要更新的元数据字段
- `backup`: 是否创建备份

**返回:**
- 是否成功

## 错误处理

Backend 模块定义了以下异常类：

- `FileImportError`: 文件导入异常
- `UnsupportedFormatError`: 不支持的文件格式异常
- `FileCorruptedError`: 文件损坏异常
- `JsonWriteError`: JSON 写入异常

示例：

```python
from Backend import import_folder
from Backend.exceptions import FileImportError

try:
    result = import_folder("/path/to/photos")
except FileImportError as e:
    print(f"导入失败: {e}")
```

## 性能优化

1. **多线程处理**: 使用线程池并发处理多个文件
2. **增量更新**: 跳过已存在的文件，避免重复处理
3. **文件锁机制**: 线程安全的 JSON 文件操作
4. **备份机制**: 写入前创建备份，防止数据丢失
5. **进度反馈**: 实时更新导入进度

## 日志

Backend 模块使用 Python 标准库 `logging` 进行日志记录。

配置日志：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='photo_import.log',
    filemode='a'
)
```

## 扩展功能

### 添加新的图片格式支持

在 `Backend/utils.py` 的 `SUPPORTED_FORMATS` 集合中添加新的扩展名。

### 自定义元数据提取

在 `Backend/metadata_extractor.py` 中扩展 `extract_metadata` 函数。

## 注意事项

1. **文件权限**: 确保对目标文件夹有读取权限
2. **磁盘空间**: 确保 JSON 文件有足够的写入空间
3. **并发限制**: 大量文件导入时，适当调整 `max_workers` 参数
4. **RAW 文件处理**: RAW 文件可能需要额外的依赖库
5. **HEIC/HEIF 文件**: 需要安装 `pillow-heif` 库

## 许可证

本项目遵循与 PictureFilter 主项目相同的许可证。

## 贡献

欢迎提交问题和拉取请求！

## 联系方式

如有问题，请通过 GitHub Issues 联系。