# 流式合成指南

## 流式输出模式

流式输出允许实时接收语音合成数据，适合需要低延迟播放的场景。

## Python 流式输出

### 基础流式合成
```python
import os
import dashscope
import base64

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def stream_tts_realtime(text, voice="Cherry"):
    """实时流式语音合成"""
    
    responses = dashscope.MultiModalConversation.call(
        model="qwen3-tts-flash",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice=voice,
        stream=True
    )
    
    audio_chunks = []
    
    for response in responses:
        if response.status_code == 200:
            if hasattr(response.output, 'audio') and response.output.audio:
                # 处理音频数据
                audio_data = response.output.audio.data
                if audio_data:
                    decoded_audio = base64.b64decode(audio_data)
                    audio_chunks.append(decoded_audio)
                    print(f"收到音频数据块，大小: {len(decoded_audio)} bytes")
            
            # 检查是否合成完成
            if response.output.finish_reason == "stop":
                print("语音合成完成")
                
    # 合并所有音频块
    full_audio = b''.join(audio_chunks)
    return full_audio
```

### 实时播放示例
```python
import pyaudio
import io

def play_streaming_audio(text, voice="Cherry"):
    """实时播放流式音频"""
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                   channels=1,
                   rate=24000,  # 千问TTS标准采样率
                   output=True)
    
    responses = dashscope.MultiModalConversation.call(
        model="qwen3-tts-flash",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice=voice,
        stream=True
    )
    
    for response in responses:
        if response.status_code == 200 and hasattr(response.output, 'audio'):
            audio_data = response.output.audio.data
            if audio_data:
                decoded_audio = base64.b64decode(audio_data)
                stream.write(decoded_audio)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
```

## Java 流式输出

```java
import com.alibaba.dashscope.aigc.multimodalconversation.*;
import java.util.Base64;

public class StreamTTSExample {
    public static void streamSynthesis(String text, String voice) {
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-tts-flash")
                .text(text)
                .voice(voice)
                .stream(true)
                .build();
        
        MultiModalConversationResult result = MultiModalConversation.streamCall(param);
        
        // 处理流式响应
        for (MultiModalConversationOutput output : result.getOutputs()) {
            if (output.getAudio() != null && output.getAudio().getData() != null) {
                byte[] audioData = Base64.getDecoder().decode(output.getAudio().getData());
                System.out.println("收到音频数据块: " + audioData.length + " bytes");
            }
        }
    }
}
```

## 流式输出优势

### 优点
1. **低延迟**: 边合成边播放，减少等待时间
2. **内存友好**: 无需等待完整音频文件
3. **实时交互**: 适合语音助手等交互场景
4. **进度可控**: 可以监控合成进度

### 适用场景
- 实时语音助手
- 在线语音播报
- 交互式语音应用
- 长文本分段播报

## 性能优化建议

### 缓冲区设置
```python
# 优化缓冲区大小
BUFFER_SIZE = 4096  # 4KB缓冲区

# 分块处理长文本
def chunk_text_for_streaming(text, max_chars=200):
    """长文本分块处理"""
    import re
    sentences = re.split(r'[。！？.!?]', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence + "。"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + "。"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
```

### 错误处理
```python
def robust_stream_tts(text, voice="Cherry", max_retries=3):
    """带有重试机制的流式合成"""
    
    for attempt in range(max_retries):
        try:
            return stream_tts_realtime(text, voice)
        except Exception as e:
            print(f"第{attempt+1}次尝试失败: {e}")
            if attempt == max_retries - 1:
                raise e
```