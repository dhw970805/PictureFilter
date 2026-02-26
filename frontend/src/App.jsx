import { useState } from 'react';
import { Layout } from 'antd';
import MenuBar from './components/MenuBar';
import Toolbar from './components/Toolbar';
import LeftPanel from './components/LeftPanel';
import ContentArea from './components/ContentArea';
import RightPanel from './components/RightPanel';
import StatusBar from './components/StatusBar';
import './styles/global.css';

const { Header, Content, Footer, Sider } = Layout;

function App() {
  const [leftPanelCollapsed, setLeftPanelCollapsed] = useState(false);
  const [rightPanelVisible, setRightPanelVisible] = useState(true);
  const [viewMode, setViewMode] = useState('grid'); // grid, list, detail
  const [thumbnailSize, setThumbnailSize] = useState(150);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [currentPath, setCurrentPath] = useState('桌面 > 图片 > 旅行');
  const [fileStats, setFileStats] = useState({ total: 0, selected: 0 });

  return (
    <Layout style={{ height: '100vh', overflow: 'hidden' }}>
      {/* 顶部菜单栏 */}
      <Header style={{ 
        height: 'var(--menu-height)', 
        padding: 0, 
        lineHeight: 'var(--menu-height)',
        background: 'var(--panel-background)',
        borderBottom: '1px solid var(--divider-color)'
      }}>
        <MenuBar />
      </Header>

      {/* 快捷工具栏 */}
      <div style={{ 
        height: 'var(--toolbar-height)', 
        background: 'var(--panel-background)',
        borderBottom: '1px solid var(--divider-color)',
        display: 'flex',
        alignItems: 'center',
        padding: '0 16px'
      }}>
        <Toolbar 
          viewMode={viewMode}
          setViewMode={setViewMode}
          thumbnailSize={thumbnailSize}
          setThumbnailSize={setThumbnailSize}
        />
      </div>

      <Layout>
        {/* 左侧面板 */}
        <Sider
          width={leftPanelCollapsed ? 0 : 200}
          collapsible
          collapsed={leftPanelCollapsed}
          onCollapse={setLeftPanelCollapsed}
          style={{ 
            background: 'var(--panel-background)',
            borderRight: '1px solid var(--divider-color)',
            overflow: 'auto'
          }}
          trigger={null}
        >
          <LeftPanel collapsed={leftPanelCollapsed} />
        </Sider>

        {/* 中央内容区 */}
        <Content style={{ 
          flex: 1,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <ContentArea 
            viewMode={viewMode}
            thumbnailSize={thumbnailSize}
            selectedFiles={selectedFiles}
            setSelectedFiles={setSelectedFiles}
            setFileStats={setFileStats}
          />
        </Content>

        {/* 右侧属性面板 */}
        {rightPanelVisible && (
          <Sider
            width={300}
            style={{ 
              background: 'var(--panel-background)',
              borderLeft: '1px solid var(--divider-color)',
              overflow: 'auto'
            }}
          >
            <RightPanel 
              selectedFiles={selectedFiles}
              onClose={() => setRightPanelVisible(false)}
            />
          </Sider>
        )}
      </Layout>

      {/* 底部状态栏 */}
      <Footer style={{ 
        height: 'var(--statusbar-height)', 
        padding: '0 16px',
        lineHeight: 'var(--statusbar-height)',
        background: 'var(--panel-background)',
        borderTop: '1px solid var(--divider-color)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <StatusBar 
          currentPath={currentPath}
          fileStats={fileStats}
          viewMode={viewMode}
          thumbnailSize={thumbnailSize}
          rightPanelVisible={rightPanelVisible}
          setRightPanelVisible={setRightPanelVisible}
        />
      </Footer>
    </Layout>
  );
}

export default App;