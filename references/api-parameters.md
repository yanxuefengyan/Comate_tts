# API参数说明

## 核心参数

### model (必需)
指定使用的TTS模型：
- `qwen3-tts-flash`: 基础语音合成，适合高频短文本
- `qwen3-tts-instruct-flash`: 支持指令控制，可调节情感语调
- `qwen3-tts-vc-2026-01-22`: 声音复刻模型
- `qwen3-tts-vd-2026-01-26`: 声音设计模型

### text (必需)
要合成的文本内容：
- 支持多语言混合输入
- 最大长度：2000字符
- 建议分段处理长文本

### voice
音色选择：
```python
# 预置音色
"Cherry"    # 甜美女声
"Zhiyu"     # 知性女声  
"Zhiyu2"    # 知性女声优化版
"Xiaoxiao"  # 活泼女声
"Yunxi"     # 沉稳男声
"Yunyang"   # 阳刚男声
"Yunye"     # 温和男声

# 方言音色
"Xiaobei"   # 东北方言
"Xiaoning"  # 四川方言

# 英文音色
"Aria"      # 英文女声
"Kenny"     # 英文男声
```

### language_type
文本语言类型：
- `"Chinese"` - 中文
- `"English"` - 英文
- `"Japanese"` - 日文
- `"Korean"` - 韩文
- `"French"` - 法文
- `"German"` - 德文
- `"Spanish"` - 西班牙文
- `"Russian"` - 俄文

### stream
是否使用流式输出：
- `False` (默认): 返回完整音频URL
- `True`: 流式输出音频数据

## 高级参数

### instructions (指令控制)
仅适用于 `qwen3-tts-instruct-flash` 模型：
```python
# 情感控制
instructions="开心愉快的语气，语速稍快"
instructions="温柔舒缓的语调，适合睡前故事"

# 角色控制  
instructions="模拟新闻播报员的专业语气"
instructions="用儿童故事讲解员的活泼语调"

# 技术参数控制
instructions="语速较快，音调较高，带有上扬感"
```

### optimize_instructions
优化指令效果：
- `True`: 启用指令优化
- `False` (默认): 不优化

### custom_voice_id
自定义音色ID（声音复刻/设计）：
- 声音复刻：上传音频后返回的voice_id
- 声音设计：创建音色后返回的voice_id

## 常用参数组合

### 基础中文合成
```python
params = {
    "model": "qwen3-tts-flash",
    "text": "欢迎使用语音合成服务",
    "voice": "Cherry", 
    "language_type": "Chinese",
    "stream": False
}
```

### 英文语音合成
```python
params = {
    "model": "qwen3-tts-flash", 
    "text": "Hello, welcome to our service",
    "voice": "Aria",
    "language_type": "English"
}
```

### 情感化语音
```python
params = {
    "model": "qwen3-tts-instruct-flash",
    "text": "今天是个好天气，我们出去玩吧！",
    "voice": "Xiaoxiao",
    "instructions": "开心兴奋的语气，语速较快",
    "optimize_instructions": True
}
```

### 流式语音合成
```python
params = {
    "model": "qwen3-tts-flash",
    "text": "实时语音播报内容",
    "voice": "Cherry",
    "stream": True
}
```

## 响应格式

### 非流式响应
```json
{
  "output": {
    "audio": {
      "url": "https://audio-url.com/audio.wav"
    }
  },
  "usage": {
    "total_tokens": 100
  },
  "request_id": "request-id-123"
}
```

### 流式响应
```json
{
  "output": {
    "audio": {
      "data": "base64-encoded-audio-data"
    },
    "finish_reason": "stop"
  }
}
```

## 错误代码

常见HTTP状态码：
- `200`: 成功
- `400`: 请求参数错误
- `401`: 认证失败
- `429`: 频率限制
- `500`: 服务器错误

## 最佳实践参数配置

### 根据场景选择模型
```python
# 短文本播报
short_text_params = {
    "model": "qwen3-tts-flash",
    "max_length": 200
}

# 情感化内容
emotional_params = {
    "model": "qwen3-tts-instruct-flash", 
    "instructions": "根据内容自动调整",
    "optimize_instructions": True
}

# 实时交互
realtime_params = {
    "model": "qwen3-tts-flash",
    "stream": True
}
```