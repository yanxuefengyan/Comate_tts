# 故障排除指南

## 常见问题及解决方法

### 1. API认证失败

**问题现象**: 
- 401 Unauthorized 错误
- "Invalid API Key" 错误信息

**解决方法**:
1. 检查环境变量是否设置正确
```bash
# 检查环境变量
echo $DASHSCOPE_API_KEY

# 设置环境变量（Linux/Mac）
export DASHSCOPE_API_KEY="sk-your-api-key"

# Windows PowerShell
$env:DASHSCOPE_API_KEY="sk-your-api-key"
```

2. 验证API Key格式是否正确（应以 `sk-` 开头）
3. 检查API Key是否在有效期内
4. 确认地域选择正确（中国内地 vs 国际）

### 2. 文本长度限制

**问题现象**:
- 400 Bad Request 错误
- "Text too long" 错误信息

**解决方法**:
1. 分割长文本
```python
def split_long_text(text, max_length=500):
    """分割长文本为合适片段"""
    import re
    sentences = re.split(r'[。！？.!?]', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + "。"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + "。"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
```

### 3. 流式输出问题

**问题现象**:
- 流式响应数据不完整
- 音频播放有中断

**解决方法**:
1. 增加缓冲区处理
```python
def robust_stream_handler(responses):
    """健壮的流式处理"""
    audio_chunks = []
    
    for response in responses:
        if response.status_code == 200:
            if hasattr(response.output, 'audio') and response.output.audio:
                try:
                    audio_data = response.output.audio.data
                    if audio_data:
                        decoded_audio = base64.b64decode(audio_data)
                        audio_chunks.append(decoded_audio)
                except Exception as e:
                    print(f"处理音频块时出错: {e}")
                    continue
    
    return b''.join(audio_chunks)
```

### 4. 音色不可用

**问题现象**:
- 指定的音色返回错误
- 语音合成质量不佳

**解决方法**:
1. 使用推荐的音色
```python
# 推荐音色选择
def get_recommended_voice(scenario):
    """根据场景推荐音色"""
    recommendations = {
        "business": "Yunxi",      # 商务场景
        "education": "Zhiyu",     # 教育场景
        "entertainment": "Xiaoxiao",  # 娱乐场景
        "navigation": "Cherry",   # 导航场景
        "default": "Cherry"       # 默认音色
    }
    return recommendations.get(scenario, "Cherry")
```

### 5. 网络连接问题

**问题现象**:
- 请求超时
- 连接中断

**解决方法**:
1. 增加重试机制
```python
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_retry_session(retries=3, backoff_factor=0.3):
    """创建带重试的会话"""
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
```

### 6. 音频文件下载问题

**问题现象**:
- 音频URL失效
- 下载文件损坏

**解决方法**:
1. 立即下载音频文件
```python
def download_audio_with_retry(url, filepath, max_retries=3):
    """带重试的音频下载"""
    session = create_retry_session(max_retries)
    
    for attempt in range(max_retries):
        try:
            response = session.get(url, timeout=30)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"下载失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"下载尝试 {attempt+1} 失败: {e}")
            if attempt == max_retries - 1:
                return False
    
    return False
```

## 性能优化建议

### 1. 批量处理优化
```python
# 使用延迟避免频率限制
import time

def batch_process_with_delay(texts, delay=1.0):
    """带延迟的批量处理"""
    results = []
    
    for i, text in enumerate(texts):
        result = synthesize_speech(text)
        results.append(result)
        
        # 添加延迟
        if i < len(texts) - 1:
            time.sleep(delay)
    
    return results
```

### 2. 内存优化
```python
# 流式处理大文件
def process_large_text_streaming(text_file_path):
    """流式处理大文本文件"""
    with open(text_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                # 使用流式合成
                audio_data = stream_synthesis(line)
                # 立即处理或保存音频数据
                process_audio_chunk(audio_data)
```

### 3. 错误恢复
```python
def robust_synthesis(text, fallback_voice="Cherry"):
    """健壮的语音合成"""
    try:
        # 首选音色
        result = synthesize_speech(text, "preferred_voice")
        if result:
            return result
    except Exception as e:
        print(f"首选音色失败: {e}")
    
    # 回退到默认音色
    try:
        return synthesize_speech(text, fallback_voice)
    except Exception as e:
        print(f"回退音色也失败: {e}")
        return None
```

## 调试技巧

### 1. 启用详细日志
```python
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_synthesis(text):
    """带调试信息的合成"""
    logger.debug(f"开始合成文本: {text}")
    
    try:
        result = synthesize_speech(text)
        logger.debug("合成成功")
        return result
    except Exception as e:
        logger.error(f"合成失败: {e}")
        return None
```

### 2. 请求监控
```python
import time

def timed_synthesis(text):
    """计时语音合成"""
    start_time = time.time()
    
    result = synthesize_speech(text)
    
    elapsed = time.time() - start_time
    print(f"合成耗时: {elapsed:.2f}秒")
    
    return result
```