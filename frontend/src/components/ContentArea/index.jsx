import { useState, useEffect } from 'react';
import { Row, Col, Table, Spin, Tag, Tooltip, Space } from 'antd';
import {
  PictureOutlined,
  CloseCircleOutlined,
  StarFilled
} from '@ant-design/icons';

// 模拟照片数据
const mockPhotos = Array.from({ length: 24 }, (_, i) => ({
  id: i + 1,
  name: `photo_${String(i + 1).padStart(3, '0')}.jpg`,
  size: `${(Math.random() * 5 + 1).toFixed(1)} MB`,
  type: 'JPG',
  resolution: `${3840}x${2160}`,
  modifiedDate: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toLocaleDateString(),
  rating: Math.floor(Math.random() * 5) + 1,
  tags: ['红色', '绿色', '蓝色'][Math.floor(Math.random() * 3)],
  status: ['good', 'bad', 'review'][Math.floor(Math.random() * 3)],
  issues: {
    blur: Math.random() > 0.7,
    closedEyes: Math.random() > 0.8,
    exposure: Math.random() > 0.75,
    expression: Math.random() > 0.8
  }
}));

function ContentArea({ viewMode, thumbnailSize, selectedFiles, setSelectedFiles, setFileStats }) {
  const [loading, setLoading] = useState(true);
  const [hoveredPhoto, setHoveredPhoto] = useState(null);

  useEffect(() => {
    // 模拟加载
    const timer = setTimeout(() => {
      setLoading(false);
      setFileStats({ total: mockPhotos.length, selected: selectedFiles.length });
    }, 1000);
    return () => clearTimeout(timer);
  }, [selectedFiles.length, setFileStats]);

  const handlePhotoClick = (photo, event) => {
    event.stopPropagation();
    if (selectedFiles.includes(photo.id)) {
      setSelectedFiles(selectedFiles.filter(id => id !== photo.id));
    } else {
      setSelectedFiles([...selectedFiles, photo.id]);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'good': return '#52c41a';
      case 'bad': return '#ff4d4f';
      case 'review': return '#faad14';
      default: return '#d9d9d9';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'good': return '优质';
      case 'bad': return '废片';
      case 'review': return '待审查';
      default: return '未知';
    }
  };

  // 网格视图
  const GridView = () => (
    <div style={{ padding: '16px', height: '100%', overflow: 'auto', background: 'var(--background-color)' }}>
      <Row gutter={[10, 10]}>
        {mockPhotos.map((photo) => (
          <Col key={photo.id}>
            <div
              style={{
                width: thumbnailSize,
                cursor: 'pointer',
                position: 'relative'
              }}
              onClick={(e) => handlePhotoClick(photo, e)}
              onMouseEnter={() => setHoveredPhoto(photo.id)}
              onMouseLeave={() => setHoveredPhoto(null)}
            >
              {/* 缩略图 */}
              <div
                style={{
                  width: thumbnailSize,
                  height: thumbnailSize,
                  border: selectedFiles.includes(photo.id) 
                    ? `2px solid var(--primary-color)` 
                    : '2px solid transparent',
                  borderRadius: 4,
                  overflow: 'hidden',
                  background: 'var(--divider-color)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  position: 'relative'
                }}
              >
                <PictureOutlined style={{ fontSize: thumbnailSize / 3, color: 'var(--text-tertiary)' }} />
                
                {/* 状态标签 */}
                <div style={{
                  position: 'absolute',
                  top: 4,
                  right: 4,
                  padding: '2px 6px',
                  borderRadius: 4,
                  fontSize: '10px',
                  color: 'white',
                  background: getStatusColor(photo.status),
                  zIndex: 1
                }}>
                  {getStatusText(photo.status)}
                </div>

                {/* 问题标记 */}
                {(photo.issues.blur || photo.issues.closedEyes || photo.issues.exposure || photo.issues.expression) && (
                  <div style={{
                    position: 'absolute',
                    top: 4,
                    left: 4,
                    display: 'flex',
                    gap: 2,
                    zIndex: 1
                  }}>
                    {photo.issues.blur && <Tooltip title="模糊"><CloseCircleOutlined style={{ color: '#ff4d4f', fontSize: 14 }} /></Tooltip>}
                    {photo.issues.closedEyes && <Tooltip title="闭眼"><CloseCircleOutlined style={{ color: '#ff4d4f', fontSize: 14 }} /></Tooltip>}
                  </div>
                )}

                {/* 评分 */}
                <div style={{
                  position: 'absolute',
                  bottom: 4,
                  left: 4,
                  display: 'flex',
                  gap: 2,
                  zIndex: 1
                }}>
                  {Array.from({ length: 5 }).map((_, i) => (
                    <StarFilled 
                      key={i} 
                      style={{ 
                        fontSize: 12, 
                        color: i < photo.rating ? '#faad14' : '#d9d9d9' 
                      }} 
                    />
                  ))}
                </div>
              </div>

              {/* 文件名 */}
              <div
                style={{
                  marginTop: 4,
                  fontSize: '11px',
                  textAlign: 'center',
                  color: 'var(--text-primary)',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  maxWidth: thumbnailSize
                }}
              >
                {photo.name}
              </div>
            </div>
          </Col>
        ))}
      </Row>
    </div>
  );

  // 列表视图
  const ListView = () => {
    const columns = [
      {
        title: '缩略图',
        dataIndex: 'id',
        key: 'thumbnail',
        width: 80,
        render: () => (
          <div style={{
            width: 50,
            height: 50,
            background: 'var(--divider-color)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: 4
          }}>
            <PictureOutlined style={{ fontSize: 24, color: 'var(--text-tertiary)' }} />
          </div>
        )
      },
      {
        title: '名称',
        dataIndex: 'name',
        key: 'name',
        sorter: (a, b) => a.name.localeCompare(b.name)
      },
      {
        title: '大小',
        dataIndex: 'size',
        key: 'size',
        width: 100,
        sorter: (a, b) => parseFloat(a.size) - parseFloat(b.size)
      },
      {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
        width: 80
      },
      {
        title: '分辨率',
        dataIndex: 'resolution',
        key: 'resolution',
        width: 120
      },
      {
        title: '修改日期',
        dataIndex: 'modifiedDate',
        key: 'modifiedDate',
        width: 120,
        sorter: (a, b) => new Date(a.modifiedDate) - new Date(b.modifiedDate)
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: 100,
        render: (status) => (
          <Tag color={getStatusColor(status)}>
            {getStatusText(status)}
          </Tag>
        )
      }
    ];

    const rowSelection = {
      selectedRowKeys: selectedFiles,
      onChange: setSelectedFiles
    };

    return (
      <div style={{ padding: 16, background: 'var(--background-color)' }}>
        <Table
          rowSelection={rowSelection}
          columns={columns}
          dataSource={mockPhotos}
          rowKey="id"
          pagination={{
            pageSize: 20,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 个文件`
          }}
          size="small"
        />
      </div>
    );
  };

  // 详情视图
  const DetailView = () => (
    <div style={{ padding: 16, height: '100%', overflow: 'auto', background: 'var(--background-color)' }}>
      <Row gutter={16}>
        {mockPhotos.map((photo) => (
          <Col key={photo.id} span={24} style={{ marginBottom: 16 }}>
            <div
              style={{
                display: 'flex',
                gap: 16,
                padding: 16,
                border: selectedFiles.includes(photo.id) 
                  ? `2px solid var(--primary-color)` 
                  : '1px solid var(--divider-color)',
                borderRadius: 8,
                cursor: 'pointer',
                background: 'var(--panel-background)'
              }}
              onClick={(e) => handlePhotoClick(photo, e)}
            >
              {/* 左侧预览图 */}
              <div
                style={{
                  width: 400,
                  height: 300,
                  background: 'var(--divider-color)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  borderRadius: 4,
                  flexShrink: 0
                }}
              >
                <PictureOutlined style={{ fontSize: 80, color: 'var(--text-tertiary)' }} />
              </div>

              {/* 右侧信息 */}
              <div style={{ flex: 1, overflow: 'hidden' }}>
                <h3 style={{ marginBottom: 12, color: 'var(--text-primary)' }}>{photo.name}</h3>
                <Row gutter={[16, 8]}>
                  <Col span={8}>
                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>大小</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>{photo.size}</div>
                  </Col>
                  <Col span={8}>
                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>类型</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>{photo.type}</div>
                  </Col>
                  <Col span={8}>
                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>分辨率</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>{photo.resolution}</div>
                  </Col>
                  <Col span={8}>
                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>修改日期</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>{photo.modifiedDate}</div>
                  </Col>
                  <Col span={8}>
                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>状态</div>
                    <Tag color={getStatusColor(photo.status)}>
                      {getStatusText(photo.status)}
                    </Tag>
                  </Col>
                  <Col span={8}>
                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>评分</div>
                    <div>
                      {Array.from({ length: 5 }).map((_, i) => (
                        <StarFilled 
                          key={i} 
                          style={{ 
                            fontSize: 14, 
                            color: i < photo.rating ? '#faad14' : '#d9d9d9' 
                          }} 
                        />
                      ))}
                    </div>
                  </Col>
                </Row>

                {/* 问题列表 */}
                {(photo.issues.blur || photo.issues.closedEyes || photo.issues.exposure || photo.issues.expression) && (
                  <div style={{ marginTop: 16 }}>
                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: 8 }}>检测到的问题</div>
                    <Space wrap>
                      {photo.issues.blur && <Tag color="red">模糊</Tag>}
                      {photo.issues.closedEyes && <Tag color="red">闭眼</Tag>}
                      {photo.issues.exposure && <Tag color="orange">曝光问题</Tag>}
                      {photo.issues.expression && <Tag color="orange">表情不佳</Tag>}
                    </Space>
                  </div>
                )}
              </div>
            </div>
          </Col>
        ))}
      </Row>
    </div>
  );

  if (loading) {
    return (
      <div style={{ 
        height: '100%', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        background: 'var(--background-color)'
      }}>
        <Spin size="large" tip="正在加载照片..." />
      </div>
    );
  }

  return (
    <div style={{ height: '100%', background: 'var(--background-color)' }}>
      {viewMode === 'grid' && <GridView />}
      {viewMode === 'list' && <ListView />}
      {viewMode === 'detail' && <DetailView />}
    </div>
  );
}

export default ContentArea;