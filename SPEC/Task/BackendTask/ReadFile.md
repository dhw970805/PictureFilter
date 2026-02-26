# 读取照片的详细实现

## 1. 功能要求

### 1.1 核心功能
1. **文件夹导入**
   - 只能选择文件夹，一次性导入文件夹内的所有文件
   - 支持递归扫描子文件夹（可配置）
   - 记录文件夹路径信息到导航栏

2. **文件格式支持**
   - 支持常见图片格式：JPG、JPEG、PNG、BMP、TIFF、GIF
   - 支持相机处理格式：HEIC、HEIF、WebP、AVIF
   - 支持RAW格式：CR2、NEF、ARW、DNG、ORF、PEF、RAF、RW2
   - 自动过滤非图片文件

3. **文件管理**
   - 导入文件并非复制照片的副本，而是将文件夹信息记录到导航栏中
   - 保存原始文件夹路径，不修改原始文件
   - 支持刷新文件夹（检测新增或删除的文件）

4. **元数据记录**
   - 导入文件后，在照片的文件夹目录建立一个JSON文件，文件名为`QualityRecord.json`
   - 记录所有照片的元数据信息
   - 每导入一张照片，就记录该照片的元数据信息，并在JSON文件里添加该照片的元数据信息

5. **实时更新**
   - 支持增量更新：新导入的照片追加到JSON文件
   - 支持检测文件变化：文件修改时更新元数据
   - 提供进度反馈：显示导入进度和已处理文件数量

### 1.2 扩展功能
1. **重复检测**
   - 基于hash值检测重复照片
   - 可选择跳过或覆盖重复记录

2. **文件过滤**
   - 支持按文件大小过滤（最小/最大限制）
   - 支持按日期范围过滤
   - 支持按文件名模式过滤（正则表达式）

3. **导入验证**
   - 检查文件是否可读
   - 验证文件完整性
   - 提供错误文件列表和原因

4. **前端集成**
   - 集成到前端的文件->导入 选项中。 

## 2. 技术实现

### 2.1 技术栈
- **Python 3.14+**
- **Pillow (PIL)**: 图片读取和基础元数据提取
- **ExifRead** 或 **Pillow.ExifTags**: EXIF数据提取
- **rawpy**: RAW格式文件支持
- **heif-imageio**: HEIC/HEIF格式支持
- **hashlib**: SHA256哈希计算
- **json**: JSON文件读写
- **pathlib**: 路径操作
- **typing**: 类型注解

### 2.2 支持的图片格式
#### 常见格式
- JPEG (.jpg, .jpeg, .jpe, .jfif)
- PNG (.png)
- BMP (.bmp, .dib)
- TIFF (.tif, .tiff)
- GIF (.gif)
- WebP (.webp)
- AVIF (.avif)

#### 相机格式
- HEIC (.heic, .heif) - iOS设备
- RAW格式：
  - Canon: .cr2, .cr3
  - Nikon: .nef, .nrw
  - Sony: .arw, .srf, .sr2
  - Adobe: .dng
  - Olympus: .orf
  - Pentax: .pef
  - Fujifilm: .raf
  - Panasonic: .rw2
  - Leica: .dng, .rwl

### 2.3 实现流程

#### 2.3.1 导入流程
```
1. 用户选择文件夹
   ↓
2. 扫描文件夹（递归或单层）
   ↓
3. 过滤非图片文件
   ↓
4. 逐个处理图片文件
   ↓
5. 读取文件基本信息
   ↓
6. 提取EXIF和相机元数据
   ↓
7. 提取图片尺寸信息
   ↓
8. 计算SHA256哈希
   ↓
9. 构建元数据字典
   ↓
10. 追加到JSON文件
   ↓
11. 更新进度状态
   ↓
12. 返回导入结果统计
```

#### 2.3.2 JSON文件管理
- **文件位置**: 与照片文件夹同级目录
- **文件名**: `QualityRecord.json`
- **更新策略**: 
  - 如果文件不存在，创建新文件
  - 如果文件存在，追加新记录
  - 使用文件锁机制防止并发写入冲突
  - 备份机制：每次更新前备份旧文件

### 2.4 数据结构设计

#### 2.4.1 完整JSON结构
```json
{
  "version": "1.0",
  "created_time": "2024-02-26T14:35:22+08:00",
  "last_updated": "2024-02-26T15:30:45+08:00",
  "folder_path": "D:/PictureFilter/Photos",
  "total_photos": 150,
  "photos": [
    {
      "photo_metadata": {
        "file_info": {
          "file_name": "DSC00123.jpg",
          "file_path": "D:/PictureFilter/Photos/DSC00123.jpg",
          "file_size_bytes": 5242880,
          "file_format": "JPEG",
          "file_extension": "jpg",
          "creation_time": "2024-02-26T14:35:22+08:00",
          "modification_time": "2024-02-26T14:35:22+08:00",
          "hash": "a1b2c3d4e5f6..."
        },
        "image_info": {
          "width_px": 5472,
          "height_px": 3648,
          "aspect_ratio": 1.5,
          "color_mode": "RGB",
          "bits_per_sample": 8
        },
        "camera_info": {
          "make": "Canon",
          "model": "Canon EOS R5",
          "lens_make": "Canon",
          "lens_model": "RF 50mm f/1.2L USM",
          "focal_length": "50mm",
          "aperture": "f/1.8",
          "iso": 400,
          "shutter_speed": "1/200s",
          "exposure_mode": "Manual"
        },
        "exif_data": {
          "date_time_original": "2024-02-26T14:35:22+08:00",
          "orientation": 1,
          "flash_used": false,
          "white_balance": "Auto",
          "metering_mode": "Evaluative"
        },
        "gps_info": {
          "latitude": 31.2304,
          "longitude": 121.4737,
          "altitude": 5.2,
          "gps_date_time": "2024-02-26T14:35:22Z",
          "coordinates": "31.2304, 121.4737"
        },
        "additional_info": {
          "color_space": "sRGB",
          "compression": "JPEG",
          "software": "Adobe Photoshop"
        },
        "quality": "未审查"
      }
    }
  ]
}
```

#### 2.4.2 详细字段说明

##### file_info（文件信息）
| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| file_name | string | 文件名（含扩展名） | DSC00123.jpg |
| file_path | string | 完整文件路径 | D:/PictureFilter/Photos/DSC00123.jpg |
| file_size_bytes | integer | 文件大小（字节） | 5242880 |
| file_format | string | 文件格式大写 | JPEG |
| file_extension | string | 文件扩展名（小写） | jpg |
| creation_time | string | ISO 8601格式创建时间 | 2024-02-26T14:35:22+08:00 |
| modification_time | string | ISO 8601格式修改时间 | 2024-02-26T14:35:22+08:00 |
| hash | string | SHA256哈希值（唯一标识） | a1b2c3d4... |

##### image_info（图片信息）
| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| width_px | integer | 图片宽度（像素） | 5472 |
| height_px | integer | 图片高度（像素） | 3648 |
| aspect_ratio | float | 宽高比 | 1.5 |
| color_mode | string | 颜色模式 | RGB |
| bits_per_sample | integer | 每样本位数 | 8 |

##### camera_info（相机信息）
| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| make | string | 相机制造商 | Canon |
| model | string | 相机型号 | Canon EOS R5 |
| lens_make | string | 镜头制造商 | Canon |
| lens_model | string | 镜头型号 | RF 50mm f/1.2L USM |
| focal_length | string | 焦距 | 50mm |
| aperture | string | 光圈值 | f/1.8 |
| iso | integer | ISO感光度 | 400 |
| shutter_speed | string | 快门速度 | 1/200s |
| exposure_mode | string | 曝光模式 | Manual |

##### exif_data（EXIF数据）
| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| date_time_original | string | 拍摄时间 | 2024-02-26T14:35:22+08:00 |
| orientation | integer | 方向值 | 1 |
| flash_used | boolean | 是否使用闪光灯 | false |
| white_balance | string | 白平衡模式 | Auto |
| metering_mode | string | 测光模式 | Evaluative |

##### gps_info（GPS信息）
| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| latitude | float | 纬度 | 31.2304 |
| longitude | float | 经度 | 121.4737 |
| altitude | float | 海拔（米） | 5.2 |
| gps_date_time | string | GPS时间戳 | 2024-02-26T14:35:22Z |
| coordinates | string | 经纬度字符串 | 31.2304, 121.4737 |

##### additional_info（附加信息）
| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| color_space | string | 色彩空间 | sRGB |
| compression | string | 压缩方式 | JPEG |
| software | string | 编辑软件 | Adobe Photoshop |

##### quality（质量标记）
| 值 | 说明 |
|----|----|
| 未审查 | 默认值，尚未进行质量检测 |
| 过曝 | 曝光过度 |
| 过暗 | 曝光不足 |
| 闭眼 | 检测到闭眼 |
| 模糊 | 图片模糊 |
| 表情不佳 | 表情不自然 |
| 需复核 | 机器检测不确定，需要人工复核 |
| 优质 | 检测通过，质量良好 |

## 3. 数据结构说明

### 3.1 核心字段说明

1. **quality字段**
   - 用途：标记图片的质量检测结果
   - 可能值：
     - 未审查（默认值）
     - 过曝
     - 过暗
     - 闭眼
     - 模糊
     - 表情不佳
     - 需复核
     - 优质
   - 初始状态：在执行图片质量审查之前，quality字段默认为"未审查"

2. **空值处理**
   - 如果照片的某些元数据为空，则对应字段的值保留为空（null或{}）
   - 嵌套对象如果完全为空，设为`{}`

3. **hash字段计算**
   - 算法：SHA256
   - 输入字符串：`file_name + file_path + file_size_bytes + file_format + creation_time`
   - 用途：作为照片的唯一标识，用于检测重复文件
   - 示例：`sha256("DSC00123.jpgD:/PictureFilter/Photos/DSC00123.jpg5242880JPEG2024-02-26T14:35:22+08:00")`

### 3.2 字段优先级

#### 必需字段（所有文件都必须有）
- file_info: file_name, file_path, file_size_bytes, file_format, file_extension, creation_time, hash
- image_info: width_px, height_px

#### 可选字段（部分文件可能有）
- file_info: modification_time
- image_info: aspect_ratio, color_mode, bits_per_sample
- camera_info: 所有字段
- exif_data: 所有字段
- gps_info: 所有字段
- additional_info: 所有字段

### 3.3 JSON版本管理

#### 版本号
- 当前版本：1.0
- 存储位置：根级字段 `version`
- 用途：便于后续升级数据结构时的兼容性处理

#### 时间戳
- `created_time`: JSON文件创建时间
- `last_updated`: JSON文件最后更新时间

#### 统计信息
- `folder_path`: 记录的文件夹路径
- `total_photos`: 照片总数

## 4. 接口设计

### 4.1 主要函数接口

#### 4.1.1 导入文件夹
```python
def import_folder(
    folder_path: str,
    recursive: bool = False,
    file_filters: Optional[Dict] = None,
    progress_callback: Optional[Callable] = None
) -> Dict:
    """
    导入文件夹中的所有图片
    
    Args:
        folder_path: 文件夹路径
        recursive: 是否递归扫描子文件夹
        file_filters: 文件过滤条件
        progress_callback: 进度回调函数
        
    Returns:
        {
            "success": bool,
            "total_files": int,
            "imported_files": int,
            "skipped_files": int,
            "error_files": int,
            "errors": List[str],
            "json_file_path": str
        }
    """
```

#### 4.1.2 处理单个文件
```python
def process_single_file(
    file_path: str,
    folder_path: str
) -> Optional[Dict]:
    """
    处理单个图片文件，提取元数据
    
    Args:
        file_path: 图片文件路径
        folder_path: 文件夹路径
        
    Returns:
        包含元数据的字典，失败返回None
    """
```

#### 4.1.3 提取EXIF数据
```python
def extract_exif_data(file_path: str) -> Dict:
    """
    从图片文件中提取EXIF数据
    
    Args:
        file_path: 图片文件路径
        
    Returns:
        EXIF数据字典
    """
```

#### 4.1.4 计算文件哈希
```python
def calculate_file_hash(
    file_name: str,
    file_path: str,
    file_size_bytes: int,
    file_format: str,
    creation_time: str
) -> str:
    """
    计算文件的SHA256哈希值
    
    Args:
        file_name: 文件名
        file_path: 文件路径
        file_size_bytes: 文件大小
        file_format: 文件格式
        creation_time: 创建时间
        
    Returns:
        SHA256哈希字符串
    """
```

#### 4.1.5 写入JSON文件
```python
def append_to_json(
    json_file_path: str,
    photo_metadata: Dict,
    create_if_not_exists: bool = True
) -> bool:
    """
    将照片元数据追加到JSON文件
    
    Args:
        json_file_path: JSON文件路径
        photo_metadata: 照片元数据
        create_if_not_exists: 文件不存在时是否创建
        
    Returns:
        是否成功
    """
```

### 4.2 数据模型

```python
from dataclasses import dataclass, asdict
from typing import Optional, Dict
from datetime import datetime

@dataclass
class FileInfo:
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
    width_px: int
    height_px: int
    aspect_ratio: Optional[float] = None
    color_mode: Optional[str] = None
    bits_per_sample: Optional[int] = None

@dataclass
class CameraInfo:
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
    date_time_original: Optional[str] = None
    orientation: Optional[int] = None
    flash_used: Optional[bool] = None
    white_balance: Optional[str] = None
    metering_mode: Optional[str] = None

@dataclass
class GPSInfo:
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    gps_date_time: Optional[str] = None
    coordinates: Optional[str] = None

@dataclass
class AdditionalInfo:
    color_space: Optional[str] = None
    compression: Optional[str] = None
    software: Optional[str] = None

@dataclass
class PhotoMetadata:
    file_info: FileInfo
    image_info: ImageInfo
    camera_info: CameraInfo
    exif_data: ExifData
    gps_info: GPSInfo
    additional_info: AdditionalInfo
    quality: str = "未审查"
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "photo_metadata": {
                "file_info": asdict(self.file_info),
                "image_info": asdict(self.image_info),
                "camera_info": asdict(self.camera_info),
                "exif_data": asdict(self.exif_data),
                "gps_info": asdict(self.gps_info),
                "additional_info": asdict(self.additional_info),
                "quality": self.quality
            }
        }
```

## 5. 错误处理

### 5.1 异常类型

```python
class FileImportError(Exception):
    """文件导入异常"""
    pass

class UnsupportedFormatError(Exception):
    """不支持的文件格式异常"""
    pass

class FileCorruptedError(Exception):
    """文件损坏异常"""
    pass

class PermissionError(Exception):
    """权限异常"""
    pass

class JsonWriteError(Exception):
    """JSON写入异常"""
    pass
```

### 5.2 错误处理策略

1. **文件读取错误**
   - 记录错误文件路径和原因
   - 跳过该文件，继续处理下一个
   - 不中断整个导入流程

2. **格式不支持**
   - 检查文件扩展名
   - 尝试读取文件头验证
   - 跳过不支持的文件

3. **文件损坏**
   - 尝试部分读取
   - 记录损坏信息
   - 标记为错误文件

4. **JSON写入失败**
   - 重试机制（最多3次）
   - 使用临时文件+原子重命名
   - 失败时保留备份文件

5. **并发写入**
   - 使用文件锁
   - 检测文件锁定状态
   - 等待或跳过

### 5.3 错误日志

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='photo_import.log',
    filemode='a'
)

logger = logging.getLogger('PhotoImporter')
```

## 6. 性能优化

### 6.1 批量处理优化

1. **多线程处理**
   - 使用线程池处理多个文件
   - 限制并发数（建议：CPU核心数的2倍）
   - 使用队列管理任务

2. **I/O优化**
   - 批量读取文件
   - 使用内存映射大文件
   - 异步写入JSON文件

3. **缓存机制**
   - 缓存已处理的文件元数据
   - 检测文件修改时间，避免重复处理
   - 使用LRU缓存策略

### 6.2 内存管理

1. **及时释放资源**
   - 处理完立即关闭文件句柄
   - 使用上下文管理器（with语句）

2. **大文件处理**
   - 流式读取，避免一次性加载到内存
   - 分块处理RAW文件

3. **限制内存占用**
   - 设置最大并发处理数量
   - 监控内存使用情况

### 6.3 进度反馈

```python
class ProgressTracker:
    def __init__(self, total: int):
        self.total = total
        self.processed = 0
        self.errors = 0
        
    def update(self, success: bool = True):
        """更新进度"""
        self.processed += 1
        if not success:
            self.errors += 1
            
    def get_progress(self) -> Dict:
        """获取当前进度"""
        return {
            "total": self.total,
            "processed": self.processed,
            "success": self.processed - self.errors,
            "errors": self.errors,
            "percentage": (self.processed / self.total) * 100 if self.total > 0 else 0
        }
```

## 7. 测试要求

### 7.1 单元测试

1. **文件哈希计算测试**
   - 测试相同输入产生相同哈希
   - 测试不同输入产生不同哈希
   - 测试边界情况

2. **元数据提取测试**
   - 测试各种格式的元数据提取
   - 测试无EXIF数据的处理
   - 测试损坏文件的处理

3. **JSON读写测试**
   - 测试新文件创建
   - 测试追加写入
   - 测试并发写入
   - 测试损坏JSON的恢复

### 7.2 集成测试

1. **完整导入流程测试**
   - 测试空文件夹
   - 测试大量文件（1000+）
   - 测试嵌套文件夹
   - 测试混合格式文件

2. **错误场景测试**
   - 测试权限不足
   - 测试磁盘空间不足
   - 测试文件被占用

3. **性能测试**
   - 测试导入速度
   - 测试内存占用
   - 测试并发性能

### 7.3 测试数据

准备测试用文件夹结构：
```
TestPhotos/
├── normal/
│   ├── test1.jpg
│   ├── test2.png
│   └── test3.heic
├── raw/
│   ├── canon.cr2
│   ├── nikon.nef
│   └── sony.arw
├── corrupted/
│   └── broken.jpg
├── subfolder/
│   └── nested.jpg
└── non_image/
    ├── text.txt
    └── document.pdf
```

## 8. 实现注意事项

### 8.1 编码规范

1. **代码风格**
   - 遵循PEP 8规范
   - 使用类型注解（type hints）
   - 编写完整的docstring

2. **命名规范**
   - 函数名：小写下划线（snake_case）
   - 类名：大驼峰（PascalCase）
   - 常量：全大写下划线（UPPER_SNAKE_CASE）

### 8.2 安全考虑

1. **路径安全**
   - 验证路径有效性
   - 防止路径遍历攻击
   - 使用pathlib处理路径

2. **数据验证**
   - 验证输入参数
   - 防止注入攻击
   - 限制文件大小

3. **异常处理**
   - 不暴露敏感信息
   - 记录详细的错误日志
   - 提供友好的错误提示

### 8.3 兼容性

1. **跨平台兼容**
   - 使用pathlib处理路径分隔符
   - 考虑Windows和Linux的差异
   - 测试不同操作系统

2. **格式兼容**
   - 处理不同版本的EXIF标准
   - 处理不同相机的元数据差异
   - 提供默认值处理

## 9. 后续扩展

### 9.1 可能的扩展功能

1. **视频支持**
   - 扩展支持视频格式（MP4, MOV, AVI）
   - 提取视频元数据（时长、分辨率、编码）

2. **云端同步**
   - 支持从云存储导入
   - 支持元数据同步到云端

3. **数据库支持**
   - 除了JSON，支持SQLite等数据库
   - 提供更高效的查询

4. **AI元数据**
   - 使用AI自动添加标签
   - 识别照片中的人物和场景

### 9.2 性能提升方向

1. **C++扩展**
   - 对性能关键的代码使用C++扩展
   - 使用Cython加速

2. **GPU加速**
   - 利用GPU进行图像处理
   - 使用CUDA或OpenCL

3. **分布式处理**
   - 支持多台机器协同处理
   - 使用消息队列分发任务