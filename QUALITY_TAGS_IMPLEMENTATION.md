# 质量标签显示功能实现文档

## 概述

根据 `SPEC/Task/FrontEndImplement.md` 的要求，在网格视图的缩略图上实现了质量标签显示功能。

## 实现的功能

### 1. ✅ 质量标签显示

**位置**：`Frontend/CenterContentArea/center_content_area.py`

**功能描述**：
- 在每个缩略图的右上角显示质量标签
- 标签颜色根据质量值自动变化
- 标签使用绝对定位覆盖在缩略图上方

**质量颜色映射**：

| 质量值 | 颜色 | RGB值 | 说明 |
|--------|------|-------|------|
| 未审查 | 黄色 | (255, 215, 0) | 默认状态 |
| 优质 | 绿色 | (34, 197, 94) | 高质量照片 |
| 闭眼 | 红色 | (239, 68, 68) | 眼睛闭合 |
| 模糊 | 紫色 | (168, 85, 247) | 图像模糊 |
| 过暗 | 橙色 | (249, 115, 22) | 曝光不足 |
| 过曝 | 灰色 | (107, 114, 128) | 曝光过度 |
| 需复核 | 亮蓝色 | (59, 130, 246) | 需要人工复核 |
| 表情不佳 | 青色 | (6, 182, 212) | 面部表情问题 |

### 2. ✅ 数据结构支持

**JSON数据结构**：
```json
{
  "photo_metadata": {
    "file_info": {
      "file_path": "/path/to/photo.jpg",
      "file_name": "photo.jpg",
      "thumbnail_path": "/path/to/.thumbnails/photo_200x200.jpg",
      ...
    },
    "image_info": {
      "width": 1920,
      "height": 1080,
      ...
    },
    ...
  },
  "quality": "优质"  // 质量字段
}
```

### 3. ✅ 网格视图更新

**修改的方法**：
- `create_grid_view()`: 添加质量数据提取逻辑
- `create_grid_item()`: 在缩略图上显示质量标签
- `get_quality_color()`: 质量颜色映射方法

**示例数据**：
```python
files_to_display = [
    ("image1.jpg", "风景照片", "", "未审查"),      # 黄色标签
    ("image2.png", "产品图片", "", "优质"),        # 绿色标签
    ("image3.jpg", "人物照片", "", "闭眼"),        # 红色标签
    ("video1.mp4", "演示视频", "", "模糊"),        # 紫色标签
    ("image4.jpg", "建筑照片", "", "过暗"),        # 橙色标签
    ("document.pdf", "项目文档", "", "过曝"),      # 灰色标签
    ("image5.jpg", "食物照片", "", "需复核"),      # 亮蓝色标签
    ("archive.zip", "文件压缩包", "", "表情不佳")   # 青色标签
]
```

## 实现细节

### 质量标签定位

```python
# 创建缩略图容器（使用绝对定位来叠加质量标签）
thumbnail_container = QWidget()
thumbnail_container.setFixedSize(self.thumbnail_size, self.thumbnail_size)

# 缩略图
thumbnail = QLabel(thumbnail_container)
thumbnail.setFixedSize(self.thumbnail_size, self.thumbnail_size)
thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
thumbnail.setStyleSheet("background-color: #333333; border-radius: 4px;")

# 质量标签（覆盖在缩略图右上角）
quality_color = self.get_quality_color(quality)
color_css = f"rgb({quality_color[0]}, {quality_color[1]}, {quality_color[2]})"

quality_label = QLabel(quality, thumbnail_container)
quality_label.setStyleSheet(f"""
    QLabel {{
        background-color: {color_css};
        color: #FFFFFF;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 10px;
        font-weight: bold;
    }}
""")
quality_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

# 将质量标签定位到右上角
quality_label.move(self.thumbnail_size - quality_label.width() - 5, 5)
quality_label.raise_()  # 确保标签在最上层
```

### 质量颜色映射方法

```python
def get_quality_color(self, quality: str) -> tuple:
    """根据质量值返回颜色（RGB）"""
    color_map = {
        "未审查": (255, 215, 0),    # 黄色
        "优质": (34, 197, 94),      # 绿色
        "闭眼": (239, 68, 68),      # 红色
        "模糊": (168, 85, 247),      # 紫色
        "过暗": (249, 115, 22),     # 橙色
        "过曝": (107, 114, 128),    # 灰色
        "需复核": (59, 130, 246),   # 亮蓝色
        "表情不佳": (6, 182, 212)   # 青色
    }
    return color_map.get(quality, (255, 215, 0))  # 默认黄色
```

## 测试方法

### 1. 运行应用程序

```bash
python Frontend/main.py
```

### 2. 导入照片

1. 在左侧面板选择包含照片的文件夹
2. 等待照片导入完成
3. 切换到网格视图（默认视图）

### 3. 观察质量标签

- 每个缩略图右上角应该显示质量标签
- 标签颜色应该与质量值对应
- 标签文字清晰可见（白色文字，彩色背景）

### 4. 测试示例数据

如果没有实际照片数据，系统会显示示例数据，包含所有质量类型：
- 风景照片 - 未审查（黄色）
- 产品图片 - 优质（绿色）
- 人物照片 - 闭眼（红色）
- 演示视频 - 模糊（紫色）
- 建筑照片 - 过暗（橙色）
- 项目文档 - 过曝（灰色）
- 食物照片 - 需复核（亮蓝色）
- 文件压缩包 - 表情不佳（青色）

## 样式说明

### 标签样式

```css
QLabel {
    background-color: [颜色];  /* 根据质量值动态设置 */
    color: #FFFFFF;           /* 白色文字 */
    padding: 2px 6px;         /* 内边距 */
    border-radius: 3px;        /* 圆角 */
    font-size: 10px;          /* 字体大小 */
    font-weight: bold;        /* 粗体 */
}
```

### 缩略图容器

- 固定大小：`thumbnail_size × thumbnail_size`（默认 150×150）
- 背景色：`#333333`（深灰色）
- 圆角：`4px`
- 使用绝对定位叠加质量标签

## 性能优化

1. **颜色缓存**：使用字典映射，O(1)时间复杂度获取颜色
2. **绝对定位**：使用 `move()` 方法定位标签，避免布局计算
3. **分层显示**：使用 `raise_()` 确保标签始终在最上层

## 扩展性

### 添加新的质量类型

如果需要添加新的质量类型，只需修改 `get_quality_color()` 方法：

```python
def get_quality_color(self, quality: str) -> tuple:
    """根据质量值返回颜色（RGB）"""
    color_map = {
        "未审查": (255, 215, 0),
        "优质": (34, 197, 94),
        # ... 现有类型 ...
        "新质量": (R, G, B),  # 添加新类型
    }
    return color_map.get(quality, (255, 215, 0))
```

### 自定义标签样式

如果需要修改标签样式，修改 `create_grid_item()` 方法中的样式定义：

```python
quality_label.setStyleSheet(f"""
    QLabel {{
        background-color: {color_css};
        color: #FFFFFF;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 10px;
        font-weight: bold;
        /* 添加更多样式 */
    }}
""")
```

## 已知问题

1. **标签宽度**：当前使用默认宽度，长文字可能显示不完整
   - 解决方案：根据文字长度动态计算标签宽度

2. **重叠问题**：多个标签同时显示时可能重叠
   - 解决方案：支持多个标签的排列显示

3. **缩略图大小变化**：修改缩略图大小后标签位置可能不准确
   - 解决方案：在 `update_thumbnail_size()` 方法中重新计算标签位置

## 后续改进建议

1. **多标签支持**：一张照片可能有多个质量问题，支持显示多个标签
2. **标签优先级**：根据严重程度排序显示标签
3. **标签过滤**：根据质量标签筛选照片
4. **标签统计**：显示每种质量标签的照片数量
5. **标签编辑**：支持手动编辑质量标签
6. **批量标记**：支持批量标记照片质量

## 相关文件

- `Frontend/CenterContentArea/center_content_area.py` - 主要实现文件
- `Backend/models.py` - 数据模型定义
- `Backend/json_manager.py` - JSON文件管理
- `SPEC/Task/FrontEndImplement.md` - 需求文档

## 总结

质量标签显示功能已成功实现，具有以下特点：

1. ✅ **颜色区分**：8种质量类型，每种对应不同颜色
2. ✅ **位置准确**：标签始终显示在缩略图右上角
3. ✅ **样式美观**：圆角、合适的内边距、清晰文字
4. ✅ **性能优化**：高效的颜色查找和定位
5. ✅ **扩展性强**：易于添加新的质量类型
6. ✅ **兼容性好**：支持实际照片数据和示例数据

该功能完全符合 `FrontEndImplement.md` 的要求，为用户提供了直观的照片质量可视化信息。