#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单测试脚本，验证各个组件是否可以正确导入和初始化
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # 测试导入各个组件
    from TopMenuBar.top_menu_bar import TopMenuBar
    from ToolBar.tool_bar import ToolBar
    from LeftPanel.left_panel import LeftPanel
    from CenterContentArea.center_content_area import CenterContentArea
    from RightPropertyPanel.right_property_panel import RightPropertyPanel
    from BottomStatusPanel.bottom_status_panel import BottomStatusPanel
    
    print("✓ 所有组件导入成功")
    
    # 测试创建各个组件（不显示GUI）
    print("测试创建组件...")
    
    # 这些测试不需要显示GUI，只是验证组件可以创建
    menu_bar = TopMenuBar()
    print("✓ 顶部菜单栏创建成功")
    
    tool_bar = ToolBar()
    print("✓ 工具栏创建成功")
    
    left_panel = LeftPanel()
    print("✓ 左侧面板创建成功")
    
    center_area = CenterContentArea()
    print("✓ 中央内容区创建成功")
    
    right_panel = RightPropertyPanel()
    print("✓ 右侧属性面板创建成功")
    
    status_bar = BottomStatusPanel()
    print("✓ 底部状态栏创建成功")
    
    print("\n🎉 所有组件测试通过！")
    print("应用程序可以正常构建，但需要在有GUI的环境中运行")
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ 其他错误: {e}")
    sys.exit(1)