import { Menu } from 'antd';
import {
  FileOutlined,
  EditOutlined,
  EyeOutlined,
  FilterOutlined,
  ToolOutlined,
  QuestionCircleOutlined
} from '@ant-design/icons';

const { SubMenu } = Menu;

function MenuBar() {
  return (
    <Menu mode="horizontal" style={{ border: 'none' }}>
      <SubMenu key="file" icon={<FileOutlined />} title="文件(F)">
        <Menu.Item key="new-folder">新建文件夹</Menu.Item>
        <Menu.Item key="import">导入</Menu.Item>
        <Menu.Item key="export">导出</Menu.Item>
        <Menu.Item key="batch-rename">批量重命名</Menu.Item>
      </SubMenu>

      <SubMenu key="edit" icon={<EditOutlined />} title="编辑(E)">
        <Menu.Item key="copy">复制</Menu.Item>
        <Menu.Item key="paste">粘贴</Menu.Item>
        <Menu.Item key="batch-edit">批量修改</Menu.Item>
        <Menu.Item key="preferences">偏好设置</Menu.Item>
      </SubMenu>

      <SubMenu key="view" icon={<EyeOutlined />} title="视图(V)">
        <Menu.Item key="view-grid">网格视图</Menu.Item>
        <Menu.Item key="view-list">列表视图</Menu.Item>
        <Menu.Item key="view-detail">详情视图</Menu.Item>
        <Menu.Item key="zoom-in">放大</Menu.Item>
        <Menu.Item key="zoom-out">缩小</Menu.Item>
      </SubMenu>

      <SubMenu key="filter" icon={<FilterOutlined />} title="筛选(S)">
        <Menu.Item key="filter-type">按类型</Menu.Item>
        <Menu.Item key="filter-date">按日期</Menu.Item>
        <Menu.Item key="filter-size">按大小</Menu.Item>
        <Menu.Item key="filter-tag">按标签</Menu.Item>
      </SubMenu>

      <SubMenu key="tools" icon={<ToolOutlined />} title="工具(T)">
        <Menu.Item key="batch-process">批量处理</Menu.Item>
        <Menu.Item key="metadata-edit">元数据编辑</Menu.Item>
        <Menu.Item key="plugin-manage">插件管理</Menu.Item>
      </SubMenu>

      <SubMenu key="help" icon={<QuestionCircleOutlined />} title="帮助(H)">
        <Menu.Item key="tutorial">教程</Menu.Item>
        <Menu.Item key="about">关于</Menu.Item>
        <Menu.Item key="check-update">检查更新</Menu.Item>
      </SubMenu>
    </Menu>
  );
}

export default MenuBar;