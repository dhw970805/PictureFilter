import { useState } from 'react';
import { Collapse, Rate, Input, Space, Button, Divider, Tag, Empty } from 'antd';
import {
  InfoCircleOutlined,
  CameraOutlined,
  EnvironmentOutlined,
  StarFilled,
  RotateRightOutlined,
  RotateLeftOutlined,
  ScissorOutlined,
  CloseOutlined
} from '@ant-design/icons';

const { Panel } = Collapse;
const { TextArea } = Input;

function RightPanel({ selectedFiles, onClose }) {
  const [rating, setRating] = useState(4);
  const [note, setNote] = useState('');
  const [activeKey, setActiveKey] = useState(['1', '2', '3', '4']);

  // 模拟选中文件的数据
  const selectedPhoto = selectedFiles.length === 1 ? {
    name: 'photo_001.jpg',
    size: '3.2 MB',
    type: 'JPG',
    resolution: '3840x2160',
    modifiedDate: '2026/2/25',
    camera: 'Canon EOS R5',
    lens: 'RF 50mm f/1.2L',
    shutter: '1/125',
    aperture: 'f/2.8',
    iso: '400',
    gps: '31.2304° N, 121.4737° E'
  } : null;

  if (selectedFiles.length === 0) {
    return (
      <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div style={{ 
          padding: '12px 16px', 
          borderBottom: '1px solid var(--divider-color)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <span style={{ fontWeight: 'bold', fontSize: '14px', color: 'var(--text-primary)' }}>属性</span>
          <Button 
            type="text" 
            icon={<CloseOutlined />} 
            size="small"
            onClick={onClose}
          />
        </div>
        <div style={{ 
          flex: 1, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          padding: 20
        }}>
          <Empty 
            description="请选择一个文件查看属性"
            style={{ marginTop: 60 }}
          />
        </div>
      </div>
    );
  }

  if (selectedFiles.length > 1) {
    return (
      <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div style={{ 
          padding: '12px 16px', 
          borderBottom: '1px solid var(--divider-color)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <span style={{ fontWeight: 'bold', fontSize: '14px', color: 'var(--text-primary)' }}>属性</span>
          <Button 
            type="text" 
            icon={<CloseOutlined />} 
            size="small"
            onClick={onClose}
          />
        </div>
        <div style={{ 
          flex: 1, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          padding: 20
        }}>
          <Empty 
            description={`已选择 ${selectedFiles.length} 个文件`}
            style={{ marginTop: 60 }}
          />
        </div>
      </div>
    );
  }

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* 面板标题 */}
      <div style={{ 
        padding: '12px 16px', 
        borderBottom: '1px solid var(--divider-color)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <span style={{ fontWeight: 'bold', fontSize: '14px', color: 'var(--text-primary)' }}>属性</span>
        <Button 
          type="text" 
          icon={<CloseOutlined />} 
          size="small"
          onClick={onClose}
        />
      </div>

      {/* 面板内容 */}
      <div style={{ flex: 1, overflow: 'auto' }}>
        <Collapse
          activeKey={activeKey}
          onChange={setActiveKey}
          bordered={false}
          style={{ backgroundColor: 'transparent' }}
        >
          {/* 基本信息 */}
          <Panel 
            header={
              <Space>
                <InfoCircleOutlined />
                <span style={{ color: 'var(--text-primary)' }}>基本信息</span>
              </Space>
            } 
            key="1"
            style={{ border: 'none' }}
          >
            <div style={{ padding: '0 8px' }}>
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  文件名
                </div>
                <div style={{ fontSize: '12px', wordBreak: 'break-all', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.name}
                </div>
              </div>
              
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  大小
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.size}
                </div>
              </div>

              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  格式
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.type}
                </div>
              </div>

              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  分辨率
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.resolution}
                </div>
              </div>

              <div>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  修改日期
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.modifiedDate}
                </div>
              </div>
            </div>
          </Panel>

          <Divider style={{ margin: '8px 0' }} />

          {/* 元数据 */}
          <Panel 
            header={
              <Space>
                <CameraOutlined />
                <span style={{ color: 'var(--text-primary)' }}>元数据</span>
              </Space>
            } 
            key="2"
            style={{ border: 'none' }}
          >
            <div style={{ padding: '0 8px' }}>
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  相机型号
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.camera}
                </div>
              </div>

              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  镜头
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.lens}
                </div>
              </div>

              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  快门速度
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.shutter}
                </div>
              </div>

              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  光圈
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.aperture}
                </div>
              </div>

              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  ISO
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.iso}
                </div>
              </div>

              <div>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  GPS位置
                </div>
                <div style={{ fontSize: '12px', wordBreak: 'break-all', color: 'var(--text-primary)' }}>
                  {selectedPhoto?.gps}
                </div>
              </div>
            </div>
          </Panel>

          <Divider style={{ margin: '8px 0' }} />

          {/* 标签/评分 */}
          <Panel 
            header={
              <Space>
                <StarFilled />
                <span style={{ color: 'var(--text-primary)' }}>标签/评分</span>
              </Space>
            } 
            key="3"
            style={{ border: 'none' }}
          >
            <div style={{ padding: '0 8px' }}>
              <div style={{ marginBottom: 16 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 8 }}>
                  评分
                </div>
                <Rate 
                  value={rating} 
                  onChange={setRating}
                  style={{ fontSize: '16px' }}
                />
              </div>

              <div style={{ marginBottom: 16 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 8 }}>
                  标签
                </div>
                <Space wrap>
                  <Tag color="red">红色</Tag>
                  <Tag color="gold">黄色</Tag>
                  <Tag color="green">绿色</Tag>
                  <Tag color="blue">蓝色</Tag>
                  <Tag color="purple">紫色</Tag>
                  <Tag>+ 添加</Tag>
                </Space>
              </div>
            </div>
          </Panel>

          <Divider style={{ margin: '8px 0' }} />

          {/* 快速编辑 */}
          <Panel 
            header={
              <Space>
                <ScissorOutlined />
                <span style={{ color: 'var(--text-primary)' }}>快速编辑</span>
              </Space>
            } 
            key="4"
            style={{ border: 'none' }}
          >
            <div style={{ padding: '0 8px' }}>
              <div style={{ marginBottom: 16 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 8 }}>
                  旋转
                </div>
                <Space>
                  <Button 
                    icon={<RotateLeftOutlined />} 
                    size="small"
                    style={{ width: '100%' }}
                  >
                    逆时针
                  </Button>
                  <Button 
                    icon={<RotateRightOutlined />} 
                    size="small"
                    style={{ width: '100%' }}
                  >
                    顺时针
                  </Button>
                </Space>
              </div>

              <div style={{ marginBottom: 16 }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 8 }}>
                  裁剪
                </div>
                <Button 
                  icon={<ScissorOutlined />} 
                  size="small"
                  style={{ width: '100%' }}
                >
                  快速裁剪预览
                </Button>
              </div>

              <div>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 8 }}>
                  备注
                </div>
                <TextArea
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  placeholder="添加文件备注..."
                  autoSize={{ minRows: 3, maxRows: 6 }}
                  style={{ fontSize: '12px' }}
                />
              </div>
            </div>
          </Panel>
        </Collapse>
      </div>
    </div>
  );
}

export default RightPanel;