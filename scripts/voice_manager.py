#!/usr/bin/env python3
"""
音色管理工具
管理和配置阿里云千问语音合成音色
"""

import os
import json
import argparse
from typing import Dict, List, Optional

class VoiceManager:
    """音色管理器"""
    
    def __init__(self, config_file="voice_config.json"):
        self.config_file = config_file
        self.voices = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载音色配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 加载配置失败: {e}")
        
        # 默认音色配置
        return self._get_default_voices()
    
    def _get_default_voices(self) -> Dict:
        """获取默认音色配置"""
        return {
            "standard": {
                "description": "标准音色配置",
                "voices": {
                    "Cherry": {
                        "name": "Cherry",
                        "description": "甜美女声，适合大多数场景",
                        "language": "Chinese",
                        "gender": "female",
                        "recommended": True
                    },
                    "Zhiyu": {
                        "name": "Zhiyu", 
                        "description": "知性女声，适合知识分享",
                        "language": "Chinese",
                        "gender": "female"
                    },
                    "Yunxi": {
                        "name": "Yunxi",
                        "description": "沉稳男声，适合正式场合",
                        "language": "Chinese", 
                        "gender": "male"
                    },
                    "Xiaoxiao": {
                        "name": "Xiaoxiao",
                        "description": "活泼女声，适合娱乐内容",
                        "language": "Chinese",
                        "gender": "female"
                    }
                }
            },
            "international": {
                "description": "多语言音色配置",
                "voices": {
                    "Aria": {
                        "name": "Aria",
                        "description": "标准英语女声",
                        "language": "English",
                        "gender": "female"
                    },
                    "Kenny": {
                        "name": "Kenny",
                        "description": "标准英语男声",
                        "language": "English",
                        "gender": "male"
                    }
                }
            }
        }
    
    def list_voices(self, category: Optional[str] = None) -> List[Dict]:
        """列出所有可用音色"""
        voices_list = []
        
        for cat_name, cat_data in self.voices.items():
            if category and cat_name != category:
                continue
                
            for voice_name, voice_data in cat_data["voices"].items():
                voice_data["category"] = cat_name
                voices_list.append(voice_data)
        
        return voices_list
    
    def get_voice(self, voice_name: str) -> Optional[Dict]:
        """获取特定音色信息"""
        for cat_data in self.voices.values():
            if voice_name in cat_data["voices"]:
                return cat_data["voices"][voice_name]
        return None
    
    def recommend_voice(self, scenario: str, language: str = "Chinese") -> Optional[Dict]:
        """根据场景推荐音色"""
        
        # 场景映射
        scenario_mapping = {
            "business": ["Yunxi", "Zhiyu"],
            "education": ["Zhiyu", "Yunxi"], 
            "entertainment": ["Xiaoxiao", "Cherry"],
            "navigation": ["Cherry", "Yunxi"],
            "storytelling": ["Xiaoxiao", "Cherry"]
        }
        
        recommended_voices = scenario_mapping.get(scenario.lower(), ["Cherry"])
        
        for voice_name in recommended_voices:
            voice = self.get_voice(voice_name)
            if voice and voice.get("language") == language:
                return voice
        
        # 如果没有匹配语言，返回第一个推荐音色
        if recommended_voices:
            return self.get_voice(recommended_voices[0])
        
        return None
    
    def add_custom_voice(self, category: str, voice_data: Dict):
        """添加自定义音色"""
        if category not in self.voices:
            self.voices[category] = {
                "description": f"自定义{category}音色",
                "voices": {}
            }
        
        voice_name = voice_data["name"]
        self.voices[category]["voices"][voice_name] = voice_data
        self._save_config()
        print(f"✅ 添加自定义音色: {voice_name}")
    
    def create_scenario_profile(self, scenario: str, voices: List[str]):
        """创建场景音色配置"""
        profile = {
            "scenario": scenario,
            "description": f"{scenario}场景音色配置",
            "recommended_voices": voices,
            "created_at": str(os.path.getctime(__file__))
        }
        
        # 保存到配置文件
        if "profiles" not in self.voices:
            self.voices["profiles"] = {}
        
        self.voices["profiles"][scenario] = profile
        self._save_config()
        print(f"✅ 创建场景配置: {scenario}")
    
    def _save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.voices, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
    
    def print_voice_table(self, voices: List[Dict]):
        """打印音色表格"""
        if not voices:
            print("❌ 没有可用的音色")
            return
        
        print("\n🎤 可用音色列表")
        print("=" * 80)
        print(f"{'名称':<12} {'语言':<8} {'性别':<6} {'推荐':<6} {'描述'}")
        print("-" * 80)
        
        for voice in voices:
            name = voice["name"]
            language = voice.get("language", "-")
            gender = voice.get("gender", "-")
            recommended = "✅" if voice.get("recommended") else ""
            description = voice.get("description", "")
            
            print(f"{name:<12} {language:<8} {gender:<6} {recommended:<6} {description}")
        
        print("=" * 80)

def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description="音色管理工具")
    parser.add_argument("command", choices=["list", "get", "recommend", "add", "profile"], 
                       help="操作命令")
    parser.add_argument("--category", "-c", help="音色分类")
    parser.add_argument("--voice", "-v", help="音色名称")
    parser.add_argument("--scenario", "-s", help="使用场景")
    parser.add_argument("--language", "-l", default="Chinese", help="语言类型")
    parser.add_argument("--config", default="voice_config.json", help="配置文件路径")
    
    args = parser.parse_args()
    
    manager = VoiceManager(args.config)
    
    if args.command == "list":
        voices = manager.list_voices(args.category)
        manager.print_voice_table(voices)
    
    elif args.command == "get":
        if not args.voice:
            print("❌ 请使用 --voice 指定音色名称")
            return
        
        voice = manager.get_voice(args.voice)
        if voice:
            print(f"\n🎤 音色详情: {args.voice}")
            print(json.dumps(voice, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 音色不存在: {args.voice}")
    
    elif args.command == "recommend":
        if not args.scenario:
            print("❌ 请使用 --scenario 指定使用场景")
            return
        
        voice = manager.recommend_voice(args.scenario, args.language)
        if voice:
            print(f"\n💡 场景推荐: {args.scenario}")
            print(f"推荐音色: {voice['name']}")
            print(f"描述: {voice['description']}")
            print(f"语言: {voice.get('language', '中文')}")
        else:
            print(f"❌ 没有找到适合场景'{args.scenario}'的音色")
    
    elif args.command == "add":
        print("🚧 此功能需要手动实现自定义音色添加")
        print("请参考声音复刻和声音设计功能")
    
    elif args.command == "profile":
        if not args.scenario:
            print("❌ 请使用 --scenario 指定场景名称")
            return
        
        # 示例：为常见场景创建配置
        scenario_profiles = {
            "business": ["Yunxi", "Zhiyu"],
            "education": ["Zhiyu", "Cherry"],
            "entertainment": ["Xiaoxiao", "Cherry"]
        }
        
        if args.scenario in scenario_profiles:
            manager.create_scenario_profile(args.scenario, scenario_profiles[args.scenario])
        else:
            print(f"❌ 未知场景: {args.scenario}")

if __name__ == "__main__":
    main()