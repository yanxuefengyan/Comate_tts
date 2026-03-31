#!/usr/bin/env python3
"""
阿里云千问语音合成技能使用示例
"""

import os
import sys

# 添加技能脚本路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from text_to_speech import QwenTTSTool
from voice_manager import VoiceManager

def demo_basic_tts():
    """基础语音合成演示"""
    print("🎤 基础语音合成演示")
    print("=" * 50)
    
    # 初始化TTS工具
    tts = QwenTTSTool("china")
    
    # 测试文本
    test_texts = [
        "欢迎使用阿里云千问语音合成服务",
        "这是一个测试语音合成的示例",
        "语音合成技术让机器能够自然地说话"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. 合成文本: {text}")
        audio_url = tts.synthesize(text, "Cherry")
        if audio_url:
            print(f"   音频URL: {audio_url}")

def demo_voice_manager():
    """音色管理演示"""
    print("\n🎵 音色管理演示")
    print("=" * 50)
    
    # 初始化音色管理器
    manager = VoiceManager()
    
    # 列出所有音色
    voices = manager.list_voices()
    manager.print_voice_table(voices)
    
    # 场景推荐
    scenarios = ["business", "education", "entertainment"]
    for scenario in scenarios:
        recommended = manager.recommend_voice(scenario)
        if recommended:
            print(f"\n💡 {scenario}场景推荐音色: {recommended['name']}")
            print(f"   描述: {recommended['description']}")

def demo_scenario_usage():
    """场景化使用演示"""
    print("\n🚀 场景化使用演示")
    print("=" * 50)
    
    tts = QwenTTSTool("china")
    
    # 商务场景
    business_text = "尊敬的客户，感谢您选择我们的服务。我们致力于为您提供最优质的解决方案。"
    print("\n📊 商务场景演示")
    print(f"文本: {business_text}")
    tts.synthesize(business_text, "Yunxi")
    
    # 教育场景
    education_text = "同学们好，今天我们来学习语音合成技术的基本原理和应用场景。"
    print("\n📚 教育场景演示") 
    print(f"文本: {education_text}")
    tts.synthesize(education_text, "Zhiyu")
    
    # 娱乐场景
    entertainment_text = "大家好！欢迎来到今天的节目，让我们开始这个有趣的冒险吧！"
    print("\n🎮 娱乐场景演示")
    print(f"文本: {entertainment_text}")
    tts.synthesize(entertainment_text, "Xiaoxiao")

def main():
    """主演示函数"""
    
    # 检查API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ 请设置 DASHSCOPE_API_KEY 环境变量")
        print("   例如: export DASHSCOPE_API_KEY=\"sk-your-api-key\"")
        return
    
    print("🌟 阿里云千问语音合成技能演示")
    print("=" * 60)
    
    # 运行演示
    demo_basic_tts()
    demo_voice_manager()
    
    # 询问是否继续场景演示
    input("\n按回车键继续场景演示...")
    demo_scenario_usage()
    
    print("\n🎉 演示完成!")
    print("\n📖 更多功能请查看技能文档:")
    print("   - 流式合成: references/streaming-synthesis.md")
    print("   - 声音复刻: references/voice-cloning.md") 
    print("   - 声音设计: references/voice-design.md")

if __name__ == "__main__":
    main()