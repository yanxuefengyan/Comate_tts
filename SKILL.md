---
name: qwen-tts
description: "阿里云千问语音合成API集成技能。支持多语言音色合成、流式输出、声音复刻和声音设计功能。使用场景：(1)文本转语音合成 (2)多语言语音生成 (3)个性化音色定制 (4)流式语音播放"
---

# 阿里云千问语音合成技能

本技能提供完整的阿里云千问语音合成API集成，支持多种语音合成模式和音色定制功能。

## 核心功能

### 支持的模型
- **基础语音合成**: qwen3-tts-flash（推荐用于高频短文本场景）
- **指令控制语音**: qwen3-tts-instruct-flash（支持自然语言指令控制情感和语调）
- **声音复刻**: qwen3-tts-vc（基于音频样本音色复刻）
- **声音设计**: qwen3-tts-vd（基于文本描述创建音色）

### 部署模式
- **中国内地**: 北京地域，使用 `https://dashscope.aliyuncs.com/api/v1`
- **国际**: 新加坡地域，使用 `https://dashscope-intl.aliyuncs.com/api/v1`

## 快速开始

### 环境配置
设置API Key到环境变量：
```bash
export DASHSCOPE_API_KEY="sk-您的API Key"
```

### 基础使用示例
查看[基础示例](references/basic-examples.md)了解基础语音合成用法。

## 高级功能

### 1. 流式输出
支持实时语音合成输出，适用于实时播放场景。详见[流式合成指南](references/streaming-synthesis.md)。

### 2. 声音复刻
基于音频样本复刻音色，创建个性化语音。详见[声音复刻指南](references/voice-cloning.md)。

### 3. 声音设计
通过文本描述创建全新音色，无需音频样本。详见[声音设计指南](references/voice-design.md)。

### 4. 指令控制
使用自然语言指令控制语速、语调、情感表现等。

## 实用脚本

使用预置脚本来简化语音合成任务：

- [文本转语音合成器](scripts/text_to_speech.py) - 基础文本转语音
- [批量语音生成器](scripts/batch_tts.py) - 批量文本处理
- [音色管理工具](scripts/voice_manager.py) - 音色配置管理

## API参数参考

详见[API参数说明](references/api-parameters.md)了解完整参数列表和使用方法。

## 最佳实践

1. **音色选择**: 根据使用场景选择合适的预置音色
2. **文本优化**: 支持多种语言和方言混合输入
3. **流式应用**: 实时应用使用流式输出减少延迟
4. **成本优化**: 短文本使用flash模型，长文本考虑流式处理
5. **错误处理**: 集成完整的异常处理机制

## 故障排除

常见问题参见[故障排除指南](references/troubleshooting.md)。