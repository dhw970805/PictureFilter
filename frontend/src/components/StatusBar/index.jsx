import { Space, Button, Tooltip, Tag } from 'antd';
import {
  AppstoreOutlined,
  UnorderedListOutlined,
  EyeOutlined,
  EyeInvisibleOutlined
} from '@ant-design/icons';

function StatusBar({ currentPath, fileStats, viewMode, thumbnailSize, rightPanelVisible, setRightPanelVisible }) {
  const getViewModeText = (mode) => {
    switch (mode) {
      case 'grid': return '网格视图';
      case 'list': return '列表视图';
      case 'detail': return '详情视图';
      default: return '未知视图';
    }
  };

  const getViewModeIcon = (mode) => {
    switch (mode) {
      case 'grid': return <AppstoreOutlined />;
      case 'list': return <UnorderedListOutlined />;
      case 'detail': return <EyeOutlined />;
      default: return <AppstoreOutlined />;
    }
  };

  return (
    <div style={{ 
      width: '100%', 
      display: 'flex', 
      justifyContent: 'space-between',
      alignItems: 'center',
      fontSize: '11px',
      color: 'var(--text-secondary)'
    }}>
      {/* 左侧信息 */}
      <Space size="large">
        {/* 当前路径 */}
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <span style={{ color: 'var(--text-tertiary)' }}>路径:</span>
          <span style={{ color: 'var(--text-primary)' }}>{currentPath}</span>
        </span>

        {/* 文件统计 */}
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <span style={{ color: 'var(--text-tertiary)' }}>共</span>
          <span style={{ color: 'var(--primary-color)', fontWeight: 'bold' }}>{fileStats.total}</span>
          <span style={{ color: 'var(--text-tertiary)' }}>个文件</span>
          {fileStats.selected > 0 && (
            <>
              <span style={{ color: 'var(--text-tertiary)' }}>, 选中</span>
              <span style={{ color: 'var(--primary-color)', fontWeight: 'bold' }}>{fileStats.selected}</span>
              <span style={{ color: 'var(--text-tertiary)' }}>个</span>
            </>
          )}
        </span>
      </Space>

      {/* 右侧信息 */}
      <Space size="large">
        {/* 视图模式 */}
        <Tooltip title={getViewModeText(viewMode)}>
          <span style={{ display: 'flex', alignItems: 'center', gap: 4, cursor: 'pointer' }}>
            {getViewModeIcon(viewMode)}
            <span>{getViewModeText(viewMode)}</span>
          </span>
        </Tooltip>

        {/* 缩略图大小 */}
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <span style={{ color: 'var(--text-tertiary)' }}>缩略图:</span>
          <span style={{ color: 'var(--primary-color)' }}>{thumbnailSize}px</span>
        </span>

        {/* 右侧面板开关 */}
        <Tooltip title={rightPanelVisible ? '隐藏属性面板' : '显示属性面板'}>
          <Button
            type="text"
            size="small"
            icon={rightPanelVisible ? <EyeOutlined /> : <EyeInvisibleOutlined />}
            onClick={() => setRightPanelVisible(!rightPanelVisible)}
            style={{ 
              fontSize: '11px',
              height: 20,
              color: 'var(--text-secondary)',
              padding: '0 4px'
            }}
          />
        </Tooltip>
      </Space>
    </div>
  );
}

export default StatusBar;