#!/usr/bin/env python3
"""
阿里云千问语音合成工具
支持基础文本转语音、批量处理和流式输出
"""

import os
import sys
import argparse
import dashscope
from typing import Optional, List

class QwenTTSTool:
    def __init__(self, region="china"):
        """初始化语音合成工具"""
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")
        
        # 配置API端点
        if region == "china":
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
        else:
            dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
    
    def synthesize(self, text: str, voice: str = "Cherry", 
                  language: str = "Chinese", 
                  model: str = "qwen3-tts-flash",
                  stream: bool = False,
                  output_format: str = "mp3") -> Optional[dict]:
        """基础语音合成
        
        Args:
            text: 要合成的文本
            voice: 音色名称
            language: 语言类型
            model: 使用的模型
            stream: 是否使用流式输出
            output_format: 输出格式，支持wav/mp3
            
        Returns:
            包含音频URL和路径的字典
        """
        try:
            response = dashscope.MultiModalConversation.call(
                model=model,
                api_key=self.api_key,
                text=text,
                voice=voice,
                language_type=language,
                stream=stream
            )
            
            if response.status_code == 200:
                if stream:
                    # 流式输出处理
                    audio_data = self._handle_stream_response(response)
                    return audio_data
                else:
                    # 非流式输出
                    audio_url = response.output.audio.url
                    print(f"合成成功: {audio_url}")
                    
                    # 下载音频文件
                    result = self._download_audio(audio_url, output_format)
                    return {
                        "success": True,
                        "audio_url": audio_url,
                        "audio_path": result,
                        "format": output_format
                    }
            else:
                print(f"合成失败: {response.message}")
                return {"success": False, "error": response.message}
                
        except Exception as e:
            print(f"调用异常: {e}")
            return {"success": False, "error": str(e)}
    
    def _download_audio(self, audio_url: str, output_format: str = "mp3") -> str:
        """下载音频文件到本地"""
        import requests
        
        # 创建输出目录
        os.makedirs("output", exist_ok=True)
        
        # 生成文件名
        import uuid
        filename = f"{uuid.uuid4().hex[:8]}.{output_format}"
        filepath = os.path.join("output", filename)
        
        try:
            response = requests.get(audio_url)
            response.raise_for_status()
            
            # 写入文件
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            print(f"音频已保存: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"下载失败: {e}")
            raise
    
    def _handle_stream_response(self, response):
        """处理流式响应"""
        import base64
        
        audio_chunks = []
        for resp in response:
            if resp.status_code == 200:
                if hasattr(resp.output, 'audio') and resp.output.audio:
                    audio_data = resp.output.audio.data
                    if audio_data:
                        decoded_audio = base64.b64decode(audio_data)
                        audio_chunks.append(decoded_audio)
                        print(f"收到音频数据块: {len(decoded_audio)} bytes")
        
        if audio_chunks:
            full_audio = b''.join(audio_chunks)
            print(f"流式合成完成，总大小: {len(full_audio)} bytes")
            return full_audio
        
        return None
    
    def batch_synthesize(self, texts: List[str], voice: str = "Cherry", 
                        output_dir: str = "output") -> List[str]:
        """批量语音合成
        
        Args:
            texts: 文本列表
            voice: 音色名称
            output_dir: 输出目录
            
        Returns:
            成功合成的音频URL列表
        """
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        for i, text in enumerate(texts):
            print(f"\\n处理第{i+1}/{len(texts)}个文本...")
            print(f"文本: {text[:50]}{'...' if len(text) > 50 else ''}")
            
            result = self.synthesize(text, voice, output_format="mp3")
            if result and result["success"]:
                results.append(result)
                print(f"音频已保存: {result['audio_path']}")
        
        print(f"\\n批量合成完成，成功: {len(results)}/{len(texts)}")
        return results

def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description="阿里云千问语音合成工具")
    parser.add_argument("text", nargs="?", help="要合成的文本内容")
    parser.add_argument("--voice", "-v", default="Cherry", help="音色名称（默认: Cherry）")
    parser.add_argument("--language", "-l", default="Chinese", help="语言类型（默认: Chinese）")
    parser.add_argument("--model", "-m", default="qwen3-tts-flash", help="模型名称")
    parser.add_argument("--stream", "-s", action="store_true", help="使用流式输出")
    parser.add_argument("--format", "-f", choices=["wav", "mp3"], default="mp3", 
                       help="输出格式（默认: mp3）")
    parser.add_argument("--batch", "-b", help="批量处理文本文件路径")
    parser.add_argument("--region", "-r", choices=["china", "international"], 
                       default="china", help="地域选择")
    
    args = parser.parse_args()
    
    # 初始化工具
    try:
        tts = QwenTTSTool(args.region)
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    
    # 批量处理模式
    if args.batch:
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
            
            if not texts:
                print("文本文件为空")
                sys.exit(1)
                
            print(f"批量处理 {len(texts)} 个文本")
            tts.batch_synthesize(texts, args.voice)
            
        except FileNotFoundError:
            print(f"文件不存在: {args.batch}")
            sys.exit(1)
    
    # 单文本处理模式
    elif args.text:
        result = tts.synthesize(
            args.text, 
            args.voice, 
            args.language, 
            args.model,
            args.stream,
            args.format
        )
        
        if not result or not result.get("success"):
            sys.exit(1)
            
        print(f"MP3文件已生成: {result['audio_path']}")
    
    else:
        # 交互模式
        print("阿里云千问语音合成工具")
        print("输入文本进行语音合成（输入'quit'退出）")
        
        while True:
            try:
                text = input("\\n请输入文本: ").strip()
                if text.lower() == 'quit':
                    break
                if not text:
                    continue
                    
                tts.synthesize(text, args.voice, args.language, args.model)
                
            except KeyboardInterrupt:
                print("\\n再见!")
                break
                if not text:
                    continue
                    
                tts.synthesize(text, args.voice, args.language, args.model)
                
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break

if __name__ == "__main__":
    main()