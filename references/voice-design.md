# 声音设计指南

声音设计功能通过文本描述创建全新音色，无需音频样本即可生成定制化语音。

## 声音设计流程

### 1. 创建音色描述
```python
import os
import dashscope

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def create_voice_by_design(voice_description, voice_name="designed_voice"):
    """通过文本描述设计音色"""
    
    response = dashscope.audio.voice_design.create_voice(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3-tts-vd-2026-01-26",
        voice_name=voice_name,
        description=voice_description
    )
    
    if response.status_code == 200:
        voice_id = response.output.voice_id
        preview_url = response.output.preview_audio.url
        print(f"音色设计成功，音色ID: {voice_id}")
        print(f"预览音频: {preview_url}")
        return voice_id, preview_url
    else:
        print(f"音色设计失败: {response.message}")
        return None, None
```

### 2. 使用设计音色合成语音
```python
def synthesize_with_designed_voice(text, voice_id):
    """使用设计音色进行语音合成"""
    
    response = dashscope.MultiModalConversation.call(
        model="qwen3-tts-vd-2026-01-26",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        custom_voice_id=voice_id,
        stream=False
    )
    
    if response.status_code == 200:
        audio_url = response.output.audio.url
        print(f"使用设计音色合成成功: {audio_url}")
        return audio_url
    else:
        print(f"合成失败: {response.message}")
        return None
```

## 音色描述技巧

### 基础属性描述
```python
# 标准音色描述模板
voice_descriptions = {
    "专业男声": "成年男性声音，语速中等偏慢，音调稳重有磁性，适合播报新闻和严肃内容",
    "活泼女声": "年轻女性声音，音调较高且富有活力，语速较快，适合儿童内容和娱乐播报",
    "标准播报": "标准播音员音色，中性语调，发音清晰准确，适合正式场合和商务应用",
    "温和女声": "温柔的女性声音，语速缓慢，音调柔和，适合睡前故事和冥想指导"
}
```

### 详细参数描述
```python
def create_detailed_voice_description(age, gender, tone, speed, style):
    """创建详细的音色描述"""
    
    description = f"""
    创建一个{age}年龄段的{gender}音色。
    音色特征：{tone}，语速{speed}。
    风格特点：{style}。
    发音清晰自然，适合{style}场景使用。
    """.strip()
    
    return description

# 示例使用
description = create_detailed_voice_description(
    age="青年",
    gender="男性", 
    tone="音调适中带温暖磁性",
    speed="中等偏快",
    style="知识分享和播客录音"
)
```

## 质量优化

### 预览试听
```python
def preview_and_confirm_voice(voice_description, test_text="欢迎试用我们的语音服务"):
    """预览并确认音色效果"""
    
    voice_id, preview_url = create_voice_by_design(voice_description)
    
    if voice_id:
        print("音色创建成功，正在生成测试音频...")
        
        # 等待音色可用
        import time
        time.sleep(10)  # 等待音色处理完成
        
        # 使用新音色合成测试文本
        test_audio = synthesize_with_designed_voice(test_text, voice_id)
        
        if test_audio:
            print("测试音频生成成功，请试听效果")
            return voice_id, test_audio
        else:
            print("测试音频生成失败")
            return None, None
    
    return None, None
```

### 批量音色生成
```python
class VoiceDesigner:
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.designed_voices = {}
    
    def design_multiple_voices(self, voice_specs):
        """批量设计多个音色"""
        
        for spec in voice_specs:
            print(f"正在设计音色: {spec['name']}")
            
            voice_id, preview_url = create_voice_by_design(
                spec['description'], 
                spec['name']
            )
            
            if voice_id:
                self.designed_voices[spec['name']] = {
                    'voice_id': voice_id,
                    'preview_url': preview_url,
                    'description': spec['description']
                }
                print(f"音色 {spec['name']} 设计完成")
        
        return self.designed_voices
```

## 应用场景指南

### 品牌音色设计
```python
# 企业品牌音色
brand_voice_descriptions = {
    "科技品牌": "专业可靠的音色，语速适中，音调稳定，适合科技产品介绍和知识分享",
    "教育机构": "亲切耐心的音色，语速清晰缓慢，适合教学内容和知识普及",
    "娱乐应用": "活泼有趣的音色，语速稍快，富有情感表现力，适合娱乐内容"
}
```

### 角色音色设计
```python
# 角色音色定制
character_voices = {
    "智能助手": "友好亲切的音色，语速流畅自然，带有温馨感，适合日常对话",
    "导航播报": "清晰干脆的音色，发音准确，语速稳定，适合导航和提示信息",
    "有声读物": "富有表现力的音色，情感丰富，语速有变化，适合故事讲述"
}
```

## 成本控制建议

### 预览机制
1. 先创建音色并获取预览音频
2. 试听满意后再用于大批量合成
3. 不满意可重新设计，避免无效调用

### 批量优化
1. 一次性设计多个相关音色
2. 建立音色库重复使用
3. 定期评估音色使用效果