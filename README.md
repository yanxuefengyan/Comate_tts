# 🎤 语音合成技能 - Comate AI编程助手变身"会说话的伙伴"

> 让您的编程工具真正"开口说话"，为AI助手赋予人声交互能力！

## 🎯 技能简介

这是一个基于阿里云千问语音合成API的Comate技能，专为让编程助手具备语音交互能力而设计。通过这项技能，您的AI编程助手可以：

- **语音播报代码审查结果** - 让AI大声朗读代码问题
- **有声编程教学** - 实时讲解编程概念和技巧  
- **智能语音助手** - 用语音与编程工具交互
- **个性化音色定制** - 定制您喜欢的AI助手声音

## 🎵 核心特性

### 🤖 编程助手语音化
- **代码朗读**: AI大声朗读代码片段，帮助理解复杂逻辑
- **错误播报**: 语音提示编译错误和代码问题
- **教程配音**: 为编程教程自动生成语音解说
- **交互反馈**: AI助手用语音回答编程问题

### 🔊 多音色支持
- **momo**: 温柔女声，适合教学讲解
- **Cherry**: 清晰女声，适合代码播报
- **Zhiyu**: 专业男声，适合正式汇报
- **更多音色**: 支持多种语言和场景适配

### ⚡ 灵活输出
- **MP3/WAV格式**: 支持高质量音频输出
- **实时流式**: 支持低延迟实时语音合成
- **批量处理**: 同时生成大量语音内容
- **声音定制**: 复刻个性化音色

## 🚀 快速开始

### 1. 环境配置
首先设置您的阿里云API Key：

```bash
# Windows
set DASHSCOPE_API_KEY=sk-您的API Key

# Linux/Mac
export DASHSCOPE_API_KEY="sk-您的API Key"
```

### 2. 基础使用
让AI朗读一段代码示例：

```bash
python scripts/text_to_speech.py "print('Hello, World!') 这是一个Python的打印语句" --voice momo
```

### 3. 编程示例
创建编程语音助手演示：

```bash
# 代码错误提示语音
python scripts/text_to_speech.py "第23行有语法错误，缺少冒号" --voice Cherry

# 编程概念讲解
python scripts/text_to_speech.py "函数式编程的核心是函数作为一等公民" --voice momo

# Git操作指导
python scripts/text_to_speech.py "执行git commit -m '修复bug'来提交更改" --voice Zhiyu
```

## 🔧 编程场景应用

### 代码审查语音化
```python
# 示例：生成代码审查语音反馈
def generate_code_review_voice(review_text):
    """将代码审查结果转为语音"""
    from scripts.text_to_speech import QwenTTSTool
    
    tts = QwenTTSTool()
    result = tts.synthesize(review_text, "momo", "Chinese")
    return result["audio_path"]

# 使用场景
review = """发现以下问题：
1. 变量命名不规范，建议使用驼峰命名法
2. 缺少异常处理，建议添加try-catch
3. 函数过长，建议拆分为小函数"""

audio_file = generate_code_review_voice(review)
```

### 编程教程语音生成
```bash
# 批量生成编程教程语音
python scripts/text_to_speech.py --batch tutorials.txt --voice momo
```

### IDE集成示例
创建IDE插件，在代码完成时语音提示：
```javascript
// VS Code扩展示例
const tts = require('./text_to_speech');

// 代码完成时语音提示
vscode.commands.registerCommand('extension.speakCompletion', () => {
    const message = "代码自动完成已应用，按Tab键确认";
    tts.synthesize(message, "Cherry");
});
```

## 🎨 进阶功能

### 个性化音色定制
使用您喜欢的音色配置：
```json
{
    "preferred_voice": "momo",
    "api_key": "sk-75de220bcb2d4291b23b9e46dc3331a1",
    "default_format": "mp3"
}
```

### 批量语音合成
一次处理多个编程提示：
```bash
# 创建编程提示文本文件
echo "欢迎使用编程语音助手" > prompts.txt
echo "当前项目包含10个Python文件" >> prompts.txt
echo "发现2个编译警告需要处理" >> prompts.txt

# 批量生成语音
python scripts/text_to_speech.py --batch prompts.txt --voice momo
```

## 📚 文件结构

```
.comate/skills/qwen-tts/
├── README.md              # 本文档
├── SKILL.md              # 技能规范
├── scripts/
│   ├── text_to_speech.py # 核心语音合成工具
│   └── batch_tts.py      # 批量处理脚本
├── user_config.json      # 用户个性化配置
└── output/               # 生成的语音文件
```

## 🔗 技术集成

### 与Comate AI助手集成
```python
# 在Comate技能中集成语音功能
from .scripts.text_to_speech import QwenTTSTool

class VoiceEnabledAI:
    def __init__(self):
        self.tts = QwenTTSTool()
    
    def speak_answer(self, text):
        """让AI用语音回答"""
        return self.tts.synthesize(text, "momo")
```

### Web应用集成
```html
<!-- 在网页中嵌入语音交互 -->
<button onclick="playProgrammingTip()">播放编程提示</button>
<script>
function playProgrammingTip() {
    // 调用后端语音合成API
    fetch('/api/tts?text=记得保存文件再运行代码&voice=momo')
        .then(response => response.blob())
        .then(audio => {
            const audioUrl = URL.createObjectURL(audio);
            new Audio(audioUrl).play();
        });
}
</script>
```

## 🎯 实际应用案例

### 1. 智能代码审查助手
- **功能**: 代码提交时自动生成语音审查报告
- **音色**: 使用专业音色进行正式审查
- **优势**: 提高代码审查的效率和趣味性

### 2. 编程学习伴侣
- **功能**: 为编程教程生成配套语音讲解
- **音色**: 选择亲和力强的教学音色
- **优势**: 多感官学习，提升理解效率

### 3. 开发环境语音提醒
- **功能**: 构建完成、测试通过等事件语音通知
- **音色**: 清晰的通知音色
- **优势**: 免打扰开发，重要事件不错过

## 🛠 故障排除

### 常见问题

**Q: API Key无效怎么办？**  
A: 确保正确设置环境变量，检查阿里云账户状态

**Q: 合成失败如何处理？**  
A: 检查网络连接，确认文本长度不超过限制

**Q: 如何选择合适的音色？**  
A: 试用不同音色，根据使用场景选择：
- 教学讲解：momo
- 代码播报：Cherry  
- 正式汇报：Zhiyu

## 📞 技术支持

如需技术帮助或功能建议，请参考：
- [技能详细文档](SKILL.md)
- [API参数说明](references/api-parameters.md)
- [故障排除指南](references/troubleshooting.md)

---

**让编程变得有声有色，让AI助手真正"开口说话"！** 🎤✨

通过这个技能，您可以为编程工作流添加语音交互维度，提升开发效率和乐趣。