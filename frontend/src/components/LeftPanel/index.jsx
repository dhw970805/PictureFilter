import { useState } from 'react';
import { Collapse, Tree, Slider, Space, Tag, Radio, Divider } from 'antd';
import {
  FolderOutlined,
  DesktopOutlined,
  FileTextOutlined,
  PictureOutlined,
  ClockCircleOutlined,
  StarOutlined,
  FilterOutlined
} from '@ant-design/icons';

const { Panel } = Collapse;
const { DirectoryTree } = Tree;

function LeftPanel({ collapsed }) {
  const [activeKey, setActiveKey] = useState(['1', '2', '3']);
  const [thumbnailSize, setThumbnailSize] = useState(150);

  // 模拟文件树数据
  const treeData = [
    {
      title: '快速访问',
      key: '0-0',
      icon: <DesktopOutlined />,
      children: [
        { title: '桌面', key: '0-0-0', icon: <DesktopOutlined /> },
        { title: '文档', key: '0-0-1', icon: <FileTextOutlined /> },
        { title: '图片', key: '0-0-2', icon: <PictureOutlined />, isLeaf: false },
        { title: '下载', key: '0-0-3', icon: <FolderOutlined /> },
      ],
    },
    {
      title: '最近访问',
      key: '0-1',
      icon: <ClockCircleOutlined />,
      children: [
        { title: '旅行照片', key: '0-1-0' },
        { title: '人像摄影', key: '0-1-1' },
        { title: '婚礼拍摄', key: '0-1-2' },
      ],
    },
    {
      title: '收藏夹',
      key: '0-2',
      icon: <StarOutlined />,
      children: [
        { title: '精选作品', key: '0-2-0' },
        { title: '客户项目', key: '0-2-1' },
      ],
    },
  ];

  return (
    <div style={{ 
      padding: '8px 0',
      display: collapsed ? 'none' : 'block' 
    }}>
      <Collapse
        activeKey={activeKey}
        onChange={setActiveKey}
        bordered={false}
        style={{ backgroundColor: 'transparent' }}
      >
        {/* 导航栏 */}
        <Panel 
          header={
            <Space>
              <FolderOutlined />
              <span>导航栏</span>
            </Space>
          } 
          key="1"
          style={{ border: 'none' }}
        >
          <DirectoryTree
            multiple
            defaultExpandAll
            treeData={treeData}
            style={{ fontSize: '12px' }}
          />
        </Panel>

        <Divider style={{ margin: '8px 0' }} />

        {/* 筛选器 */}
        <Panel 
          header={
            <Space>
              <FilterOutlined />
              <span>筛选器</span>
            </Space>
          } 
          key="2"
          style={{ border: 'none' }}
        >
          <div style={{ marginBottom: 16 }}>
            <div style={{ marginBottom: 8, fontSize: '12px', color: 'var(--text-secondary)' }}>
              文件类型
            </div>
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Radio.Group defaultValue="all" size="small" style={{ width: '100%' }}>
                <Space direction="vertical" size="small" style={{ width: '100%' }}>
                  <Radio value="all">全部</Radio>
                  <Radio value="image">
                    <Space>
                      <PictureOutlined />
                      图片
                    </Space>
                  </Radio>
                  <Radio value="raw">
                    <Space>
                      <FileTextOutlined />
                      RAW格式
                    </Space>
                  </Radio>
                </Space>
              </Radio.Group>
            </Space>
          </div>

          <div style={{ marginBottom: 16 }}>
            <div style={{ marginBottom: 8, fontSize: '12px', color: 'var(--text-secondary)' }}>
              日期
            </div>
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Tag color="blue" style={{ margin: '2px 0', cursor: 'pointer' }}>今天</Tag>
              <Tag style={{ margin: '2px 0', cursor: 'pointer' }}>昨天</Tag>
              <Tag style={{ margin: '2px 0', cursor: 'pointer' }}>本周</Tag>
              <Tag style={{ margin: '2px 0', cursor: 'pointer' }}>本月</Tag>
            </Space>
          </div>

          <div>
            <div style={{ marginBottom: 8, fontSize: '12px', color: 'var(--text-secondary)' }}>
              标签
            </div>
            <Space wrap>
              <Tag color="red" style={{ cursor: 'pointer' }}>红色</Tag>
              <Tag color="gold" style={{ cursor: 'pointer' }}>黄色</Tag>
              <Tag color="green" style={{ cursor: 'pointer' }}>绿色</Tag>
              <Tag color="blue" style={{ cursor: 'pointer' }}>蓝色</Tag>
              <Tag color="purple" style={{ cursor: 'pointer' }}>紫色</Tag>
            </Space>
          </div>
        </Panel>

        <Divider style={{ margin: '8px 0' }} />

        {/* 预览尺寸 */}
        <Panel 
          header={
            <Space>
              <PictureOutlined />
              <span>预览尺寸</span>
            </Space>
          } 
          key="3"
          style={{ border: 'none' }}
        >
          <div style={{ padding: '0 8px' }}>
            <Slider
              min={50}
              max={500}
              value={thumbnailSize}
              onChange={setThumbnailSize}
              tooltip={{ formatter: (value) => `${value}px` }}
            />
            <div style={{ 
              textAlign: 'center', 
              fontSize: '11px', 
              color: 'var(--text-secondary)',
              marginTop: 8 
            }}>
              当前: {thumbnailSize}px
            </div>
          </div>
        </Panel>
      </Collapse>
    </div>
  );
}

export default LeftPanel;