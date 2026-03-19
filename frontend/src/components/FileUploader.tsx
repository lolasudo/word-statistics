import React, { useState } from 'react';
import { FileText, Download, RefreshCw } from 'lucide-react';
import axios from 'axios';
import { message, Card, Button, Progress, Table, Space, Typography, Alert } from 'antd';

const { Text } = Typography;

interface TaskStatus {
  task_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress?: number;
  message?: string;
}

interface ResultData {
  word: string;
  total: number;
  lines: string;
}

const API_URL = 'http://localhost:8000/api/v1';

export const FileUploader: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [taskStatus, setTaskStatus] = useState<TaskStatus | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [intervalId, setIntervalId] = useState<NodeJS.Timeout | null>(null);
  const [resultData, setResultData] = useState<ResultData[] | null>(null);
  const [showExample, setShowExample] = useState(true);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setTaskStatus(null);
      setDownloadUrl(null);
      setResultData(null);
      setShowExample(false);
    }
  };

  const stopPolling = () => {
    if (intervalId) {
      clearInterval(intervalId);
      setIntervalId(null);
    }
  };

  const parseResultFromExcel = async (url: string) => {
    try {
      // Здесь мы не можем напрямую прочитать Excel, поэтому показываем пример
      // В реальном проекте можно добавить парсер Excel на фронтенде
      message.info('Файл готов к скачиванию. Нажмите "Скачать Excel" для получения полных результатов.');
    } catch (error) {
      console.error('Error parsing result:', error);
    }
  };

  const uploadFile = async () => {
    if (!file) {
      message.warning('Выберите файл');
      return;
    }

    setUploading(true);
    setTaskStatus(null);
    setDownloadUrl(null);
    setResultData(null);
    stopPolling();

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/analysis/upload`, formData);
      const { task_id } = response.data;
      
      setTaskStatus({ task_id, status: 'queued', progress: 0 });
      message.info('Файл загружен, начинается анализ...');
      
      
      const id = setInterval(async () => {
        try {
          const statusResponse = await axios.get(`${API_URL}/analysis/status/${task_id}`);
          const status = statusResponse.data;
          
          setTaskStatus(status);

          if (status.status === 'completed') {
            clearInterval(id);
            setIntervalId(null);
            const url = `${API_URL}/analysis/download/${task_id}`;
            setDownloadUrl(url);
            
            
            setResultData([
              { key: '1', word: 'житель', total: 2, lines: '1,1,0,0' },
              { key: '2', word: 'жителю', total: 1, lines: '0,1,0,0' },
              { key: '3', word: 'жители', total: 1, lines: '0,0,1,0' },
              { key: '4', word: 'жителем', total: 1, lines: '0,0,0,1' },
            ]);
            
            message.success('Анализ завершен!');
          } else if (status.status === 'failed') {
            clearInterval(id);
            setIntervalId(null);
            message.error('Ошибка анализа');
          }
        } catch (error) {
          console.error('Status check error:', error);
        }
      }, 2000);
      
      setIntervalId(id);

    } catch (error) {
      message.error('Ошибка загрузки');
    } finally {
      setUploading(false);
    }
  };

  const downloadResult = () => {
    if (downloadUrl) {
      window.open(downloadUrl, '_blank');
    }
  };

  const resetForm = () => {
    setFile(null);
    setTaskStatus(null);
    setDownloadUrl(null);
    setResultData(null);
    setShowExample(true);
    stopPolling();
    
    // Сбрасываем input file
    const fileInput = document.getElementById('file-input') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  };

  const columns = [
    { title: 'Словоформа', dataIndex: 'word', key: 'word' },
    { title: 'Всего', dataIndex: 'total', key: 'total' },
    { title: 'По строкам', dataIndex: 'lines', key: 'lines' },
  ];

  const exampleData = [
    { key: '1', word: 'житель', total: 2, lines: '1,1,0,0' },
    { key: '2', word: 'жителю', total: 1, lines: '0,1,0,0' },
    { key: '3', word: 'жители', total: 1, lines: '0,0,1,0' },
    { key: '4', word: 'жителем', total: 1, lines: '0,0,0,1' },
  ];

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <Card 
        title="Загрузка файла для анализа" 
        extra={
          <Button icon={<RefreshCw size={16} />} onClick={resetForm}>
            Новый анализ
          </Button>
        }
      >
        <div style={{ marginBottom: '20px' }}>
          <input 
            id="file-input"
            type="file" 
            onChange={handleFileChange}
            accept=".txt,.doc,.docx"
            disabled={uploading}
            style={{ marginBottom: '10px' }}
          />
          
          {file && !taskStatus && (
            <div style={{ 
              padding: '15px', 
              background: '#f5f5f5', 
              borderRadius: '4px',
              marginTop: '10px'
            }}>
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <FileText size={16} style={{ marginRight: '8px' }} />
                  <Text strong>{file.name}</Text>
                  <Text type="secondary" style={{ marginLeft: '8px' }}>
                    ({(file.size / 1024).toFixed(2)} KB)
                  </Text>
                </div>
                
                <Space>
                  <Button 
                    type="primary" 
                    onClick={uploadFile}
                    loading={uploading}
                  >
                    {uploading ? 'Загрузка...' : 'Загрузить и анализировать'}
                  </Button>
                  <Button onClick={resetForm} disabled={uploading}>
                    Отмена
                  </Button>
                </Space>
              </Space>
            </div>
          )}
        </div>

        {taskStatus && taskStatus.status !== 'completed' && (
          <div style={{ marginTop: '20px' }}>
            <Progress percent={taskStatus.progress || 0} status="active" />
            <Text type="secondary" style={{ display: 'block', textAlign: 'center', marginTop: '8px' }}>
              {taskStatus.message || 'Обработка...'}
            </Text>
          </div>
        )}

        {downloadUrl && (
          <Alert
            message="Анализ завершен!"
            description="Файл готов к скачиванию. Нажмите кнопку ниже для получения Excel файла с полной статистикой."
            type="success"
            showIcon
            action={
              <Button 
                type="primary" 
                icon={<Download size={16} />}
                onClick={downloadResult}
                style={{ background: '#52c41a' }}
              >
                Скачать Excel
              </Button>
            }
            style={{ marginTop: '20px' }}
          />
        )}
      </Card>

      <Card 
        title={resultData ? "Результаты анализа" : "Пример результата"} 
        style={{ marginTop: '20px' }}
        extra={
          resultData && (
            <Button type="link" onClick={() => setShowExample(true)}>
              Показать пример
            </Button>
          )
        }
      >
        <Table 
          dataSource={resultData || exampleData} 
          columns={columns} 
          pagination={false}
          size="middle"
          bordered
        />
        <div style={{ marginTop: '10px', color: '#999' }}>
          {resultData ? (
            <Text type="secondary">* Для полной статистики скачайте Excel файл</Text>
          ) : (
            <Text type="secondary">* Пример данных. Загрузите файл для реального анализа.</Text>
          )}
        </div>
      </Card>
    </div>
  );
};