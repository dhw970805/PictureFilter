import { Button, Space, Tooltip, Segmented, Slider } from 'antd';
import {
  ArrowLeftOutlined,
  ArrowRightOutlined,
  ReloadOutlined,
  AppstoreOutlined,
  UnorderedListOutlined,
  InfoCircleOutlined,
  SortAscendingOutlined,
  FilterOutlined,
  ThunderboltOutlined
} from '@ant-design/icons';

function Toolbar({ viewMode, setViewMode, thumbnailSize, setThumbnailSize }) {
  return (
    <Space size="small" style={{ width: '100%', justifyContent: 'space-between' }}>
      <Space size="small">
        {/* 导航按钮 */}
        <Tooltip title="返回 (Alt+←)">
          <Button icon={<ArrowLeftOutlined />} size="small" style={{ width: 32, height: 32 }} />
        </Tooltip>
        <Tooltip title="前进 (Alt+→)">
          <Button icon={<ArrowRightOutlined />} size="small" style={{ width: 32, height: 32 }} />
        </Tooltip>
        <Tooltip title="刷新 (F5)">
          <Button icon={<ReloadOutlined />} size="small" style={{ width: 32, height: 32 }} />
        </Tooltip>

        {/* 分隔线 */}
        <div style={{ width: 1, height: 20, background: 'var(--divider-color)', margin: '0 4px' }} />

        {/* 视图切换 */}
        <Segmented
          size="small"
          value={viewMode}
          onChange={setViewMode}
          options={[
            { value: 'grid', icon: <AppstoreOutlined />, label: '网格' },
            { value: 'list', icon: <UnorderedListOutlined />, label: '列表' },
            { value: 'detail', icon: <InfoCircleOutlined />, label: '详情' }
          ]}
        />
      </Space>

      <Space size="small">
        {/* 缩略图大小滑块 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>缩略图大小</span>
          <Slider
            min={50}
            max={300}
            value={thumbnailSize}
            onChange={setThumbnailSize}
            style={{ width: 120 }}
            tooltip={{ formatter: (value) => `${value}px` }}
          />
        </div>

        {/* 分隔线 */}
        <div style={{ width: 1, height: 20, background: 'var(--divider-color)', margin: '0 4px' }} />

        {/* 排序 */}
        <Tooltip title="排序 (Ctrl+S)">
          <Button icon={<SortAscendingOutlined />} size="small">排序</Button>
        </Tooltip>

        {/* 筛选 */}
        <Tooltip title="筛选 (Ctrl+F)">
          <Button icon={<FilterOutlined />} size="small">筛选</Button>
        </Tooltip>

        {/* 批量处理 */}
        <Tooltip title="批量处理 (Ctrl+B)">
          <Button icon={<ThunderboltOutlined />} size="small" type="primary">批量处理</Button>
        </Tooltip>
      </Space>
    </Space>
  );
}

export default Toolbar;