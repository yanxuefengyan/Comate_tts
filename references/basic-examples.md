# 基础示例

## Python 基础示例

### 非流式输出
```python
import os
import dashscope

# 配置API端点（中国内地）
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def text_to_speech(text, voice="Cherry", language="Chinese"):
    """基础文本转语音合成"""
    response = dashscope.MultiModalConversation.call(
        model="qwen3-tts-flash",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice=voice,
        language_type=language,
        stream=False
    )
    
    if response.status_code == 200:
        audio_url = response.output.audio.url
        print(f"音频文件URL: {audio_url}")
        return audio_url
    else:
        print(f"合成失败: {response.message}")
        return None

# 使用示例
text = "欢迎使用阿里云千问语音合成服务"
audio_url = text_to_speech(text)
```

### 流式输出示例
```python
def stream_text_to_speech(text, voice="Cherry"):
    """流式文本转语音合成"""
    responses = dashscope.MultiModalConversation.call(
        model="qwen3-tts-flash",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice=voice,
        stream=True
    )
    
    for response in responses:
        if response.status_code == 200:
            if hasattr(response.output, 'audio') and response.output.audio:
                audio_data = response.output.audio.data
                # 处理音频数据（base64编码）
                print(f"收到音频数据块")
        else:
            print(f"合成错误: {response.message}")
```

## Java 基础示例

```java
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

public class TTSExample {
    public static String synthesizeSpeech(String text, String voice, String language) {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-tts-flash")
                .text(text)
                .voice(voice)
                .languageType(language)
                .build();
        
        MultiModalConversationResult result = conv.call(param);
        return result.getOutput().getAudio().getUrl();
    }
}
```

## 常用音色列表

### 女性音色
- `"Cherry"` - 甜美女声
- `"Zhiyu"` - 知性女声  
- `"Zhiyu2"` - 知性女声（优化版）
- `"Xiaoxiao"` - 活泼女声

### 男性音色
- `"Yunxi"` - 沉稳男声
- `"Yunyang"` - 阳刚男声
- `"Yunye"` - 温和男声

### 方言音色
- `"Xiaobei"` - 东北方言
- `"Xiaoning"` - 四川方言

## 语言支持

- `"Chinese"` - 中文
- `"English"` - 英文
- `"Japanese"` - 日文
- `"Korean"` - 韩文
- `"French"` - 法文
- `"German"` - 德文
- `"Spanish"` - 西班牙文
- `"Russian"` - 俄文