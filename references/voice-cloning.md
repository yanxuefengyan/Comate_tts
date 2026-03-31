# 声音复刻指南

声音复刻功能基于音频样本创建个性化音色，支持将现有音频的音色特征应用于新的语音合成。

## 声音复刻流程

### 1. 上传音频样本
```python
import os
import dashscope

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def upload_voice_sample(audio_file_path, voice_name="custom_voice"):
    """上传音频样本用于声音复刻"""
    
    response = dashscope.audio.voice_clone.upload_voice_sample(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        voice_name=voice_name,
        audio_file=audio_file_path
    )
    
    if response.status_code == 200:
        voice_id = response.output.voice_id
        print(f"声音样本上传成功，音色ID: {voice_id}")
        return voice_id
    else:
        print(f"上传失败: {response.message}")
        return None
```

### 2. 使用复刻音色合成语音
```python
def synthesize_with_cloned_voice(text, voice_id):
    """使用复刻音色进行语音合成"""
    
    response = dashscope.MultiModalConversation.call(
        model="qwen3-tts-vc-2026-01-22",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        custom_voice_id=voice_id,  # 使用复刻音色
        stream=False
    )
    
    if response.status_code == 200:
        audio_url = response.output.audio.url
        print(f"使用复刻音色合成成功: {audio_url}")
        return audio_url
    else:
        print(f"合成失败: {response.message}")
        return None
```

## 音频样本要求

### 技术规格
- **格式**: WAV、MP3、M4A
- **时长**: 30秒 - 5分钟
- **采样率**: 16kHz - 48kHz
- **声道**: 单声道或立体声
- **内容**: 清晰的语音，无明显噪音

### 最佳实践
1. **音频质量**: 使用高质量录音设备
2. **环境安静**: 避免背景噪音
3. **语音清晰**: 自然流畅的朗读
4. **内容多样**: 包含不同音节和语调

## 批量复刻管理

```python
class VoiceCloneManager:
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.voices = {}
    
    def clone_voice_from_files(self, file_paths, voice_name):
        """从多个音频文件复刻音色"""
        
        for i, file_path in enumerate(file_paths):
            print(f"处理第{i+1}个音频文件: {file_path}")
            voice_id = upload_voice_sample(file_path, f"{voice_name}_{i}")
            if voice_id:
                self.voices[f"{voice_name}_{i}"] = voice_id
        
        return self.voices
    
    def list_cloned_voices(self):
        """查看所有复刻音色"""
        
        response = dashscope.audio.voice_clone.list_voices(
            api_key=self.api_key
        )
        
        if response.status_code == 200:
            voices = response.output.voices
            for voice in voices:
                print(f"音色ID: {voice.voice_id}, 名称: {voice.voice_name}")
            return voices
        else:
            print(f"获取音色列表失败: {response.message}")
            return []
```

## 质量评估与优化

### 试听评估
```python
def evaluate_cloned_voice(voice_id, test_texts):
    """评估复刻音色效果"""
    
    results = []
    for i, text in enumerate(test_texts):
        print(f"测试第{i+1}个文本: {text}")
        audio_url = synthesize_with_cloned_voice(text, voice_id)
        if audio_url:
            results.append({
                "text": text,
                "audio_url": audio_url,
                "success": True
            })
        else:
            results.append({
                "text": text,
                "success": False
            })
    
    return results
```

### 优化建议
1. **样本多样性**: 使用不同场景的音频样本
2. **音色一致性**: 确保样本音色相似
3. **处理噪声**: 预处理降噪音频
4. **时长控制**: 保持适当样本时长