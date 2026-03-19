import React from 'react';
import { FileUploader } from './components/FileUploader';
import { Layout, Typography } from 'antd';
import 'antd/dist/reset.css';

const { Header, Content } = Layout;
const { Title } = Typography;

function App() {
  return (
    <Layout className="min-h-screen">
      <Header style={{ background: '#1677ff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Title level={3} style={{ color: 'white', margin: 0 }}>
          Анализ словоформ слова "житель"
        </Title>
      </Header>
      <Content style={{ padding: '24px' }}>
        <FileUploader />
      </Content>
    </Layout>
  );
}

export default App;