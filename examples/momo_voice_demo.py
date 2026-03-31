#!/usr/bin/env python3
"""
momo音色专用演示 - 为您的个性化设置定制
"""

import os
import sys

# 添加技能脚本路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from text_to_speech import QwenTTSTool

def setup_momo_environment():
    """设置momo音色的专属环境"""
    
    # 设置您的API Key
    os.environ["DASHSCOPE_API_KEY"] = "sk-75de220bcb2d4291b23b9e46dc3331a1"
    
    print("✅ 已设置您的API Key")
    print("🎵 使用音色: momo")
    print("🌍 地域: 中国内地")
    
    return "momo"

def test_momo_voice():
    """测试momo音色效果"""
    print("\n🎤 momo音色效果测试")
    print("=" * 40)
    
    tts = QwenTTSTool("china")
    
    # 测试不同场景的文本
    test_scenarios = [
        {
            "name": "日常问候",
            "text": "你好，很高兴为您服务！今天过得怎么样？"
        },
        {
            "name": "信息播报", 
            "text": "欢迎使用阿里云语音合成服务，我是您的语音助手momo。"
        },
        {
            "name": "情感表达",
            "text": "今天天气真好，阳光明媚，让人心情愉快！"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n📝 {scenario['name']}:")
        print(f"   文本: {scenario['text']}")
        
        audio_url = tts.synthesize(scenario['text'], "momo")
        if audio_url:
            print(f"   ✅ 合成成功: {audio_url}")
        else:
            print("   ❌ 合成失败")

def momo_batch_demo():
    """momo音色批量演示"""
    print("\n📦 momo音色批量处理演示")
    print("=" * 40)
    
    # 创建测试文本
    test_texts = [
        "欢迎使用momo音色进行语音合成。",
        "这个声音非常自然亲切，适合多种场景。",
        "无论是日常对话还是信息播报都很合适。",
        "感谢您选择momo作为您的首选音色。"
    ]
    
    # 创建输出目录
    output_dir = "./momo_demo_output"
    os.makedirs(output_dir, exist_ok=True)
    
    tts = QwenTTSTool("china")
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n处理第{i}个文本: {text}")
        
        audio_url = tts.synthesize(text, "momo")
        if audio_url:
            # 下载音频文件
            try:
                import requests
                response = requests.get(audio_url)
                filename = f"momo_demo_{i}.wav"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"   ✅ 音频已保存: {filepath}")
            except Exception as e:
                print(f"   ⚠️ 下载失败: {e}")

def create_momo_quick_script():
    """创建momo音色快速使用脚本"""
    
    script_content = '''#!/usr/bin/env python3
"""
momo音色快速使用脚本
专门为您喜爱的momo音色定制
"""

import os
import sys

# 设置您的配置
os.environ["DASHSCOPE_API_KEY"] = "sk-75de220bcb2d4291b23b9e46dc3331a1"

# 添加技能路径
sys.path.append("scripts")

from text_to_speech import QwenTTSTool

def momo_speak(text):
    """使用momo音色合成语音"""
    tts = QwenTTSTool("china")
    return tts.synthesize(text, "momo")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        print(f"使用momo音色合成: {text}")
        audio_url = momo_speak(text)
        if audio_url:
            print(f"音频URL: {audio_url}")
    else:
        print("用法: python momo_quick.py <要合成的文本>")
'''
    
    # 保存快速脚本
    script_path = os.path.join(os.path.dirname(__file__), "momo_quick.py")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\n⚡ 已创建快速使用脚本: {script_path}")
    print("   用法: python momo_quick.py '要合成的文本'")

def main():
    """主演示函数"""
    
    print("🌟 momo音色专属演示")
    print("=" * 50)
    
    # 设置环境
    preferred_voice = setup_momo_environment()
    
    # 运行演示
    test_momo_voice()
    
    # 询问是否继续批量演示
    input("\n按回车键继续批量处理演示...")
    momo_batch_demo()
    
    # 创建快速脚本
    create_momo_quick_script()
    
    print("\n🎯 您的个性化配置:")
    print("   • API Key: 已设置")
    print("   • 首选音色: momo") 
    print("   • 地域: 中国内地")
    print("   • 快速脚本: momo_quick.py")
    
    print("\n💡 使用建议:")
    print("   1. 直接运行 momo_quick.py 进行快速合成")
    print("   2. 使用 scripts/text_to_speech.py 进行高级功能")
    print("   3. 查看 references/ 目录了解更多功能")

if __name__ == "__main__":
    main()