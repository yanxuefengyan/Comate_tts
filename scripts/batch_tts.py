#!/usr/bin/env python3
"""
批量语音合成工具
支持大文本文件的分割处理和批量合成
"""

import os
import sys
import argparse
import json
import time
from datetime import datetime
from text_to_speech import QwenTTSTool

class BatchTTSProcessor:
    def __init__(self, region="china"):
        """初始化批量处理器"""
        self.tts = QwenTTSTool(region)
        self.results = []
    
    def process_file(self, input_file: str, voice: str = "Cherry", 
                    max_length: int = 500, delay: float = 1.0) -> dict:
        """处理文本文件
        
        Args:
            input_file: 输入文件路径
            voice: 音色名称
            max_length: 单个文本最大长度
            delay: 请求间隔（秒）
            
        Returns:
            处理结果统计
        """
        
        # 读取文本文件
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return {"success": False, "error": str(e)}
        
        # 分割文本
        chunks = self._split_text(content, max_length)
        print(f"📊 文本分割完成，共{len(chunks)}个片段")
        
        # 创建输出目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"batch_output_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # 批量合成
        successful_chunks = 0
        for i, chunk in enumerate(chunks):
            print(f"\n🔄 处理片段 {i+1}/{len(chunks)}")
            print(f"文本: {chunk[:100]}{'...' if len(chunk) > 100 else ''}")
            
            try:
                audio_url = self.tts.synthesize(chunk, voice)
                
                if audio_url:
                    # 下载音频
                    filename = f"audio_{i+1:03d}.wav"
                    filepath = os.path.join(output_dir, filename)
                    
                    if self._download_audio(audio_url, filepath):
                        self.results.append({
                            "chunk_index": i + 1,
                            "text": chunk,
                            "audio_file": filepath,
                            "audio_url": audio_url,
                            "success": True
                        })
                        successful_chunks += 1
                        print(f"✅ 片段 {i+1} 处理成功")
                    else:
                        self.results.append({
                            "chunk_index": i + 1,
                            "text": chunk,
                            "success": False,
                            "error": "下载失败"
                        })
                else:
                    self.results.append({
                        "chunk_index": i + 1,
                        "text": chunk,
                        "success": False,
                        "error": "合成失败"
                    })
                
                # 延迟以避免频率限制
                if i < len(chunks) - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"❌ 处理片段 {i+1} 时出错: {e}")
                self.results.append({
                    "chunk_index": i + 1,
                    "text": chunk,
                    "success": False,
                    "error": str(e)
                })
        
        # 生成结果报告
        report = self._generate_report(output_dir, successful_chunks, len(chunks))
        
        return {
            "success": True,
            "output_dir": output_dir,
            "total_chunks": len(chunks),
            "successful_chunks": successful_chunks,
            "success_rate": successful_chunks / len(chunks) if chunks else 0,
            "report_file": report
        }
    
    def _split_text(self, text: str, max_length: int) -> list:
        """分割长文本为合适片段"""
        import re
        
        # 按句子分割
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += sentence + "。"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + "。"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _download_audio(self, url: str, filepath: str) -> bool:
        """下载音频文件"""
        try:
            import requests
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"❌ 下载失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 下载异常: {e}")
            return False
    
    def _generate_report(self, output_dir: str, success_count: int, total_count: int) -> str:
        """生成处理报告"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "output_directory": output_dir,
            "statistics": {
                "total_chunks": total_count,
                "successful_chunks": success_count,
                "failed_chunks": total_count - success_count,
                "success_rate": success_count / total_count if total_count > 0 else 0
            },
            "results": self.results
        }
        
        # 保存详细报告
        report_file = os.path.join(output_dir, "processing_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 生成摘要报告
        summary_file = os.path.join(output_dir, "summary.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("批量语音合成处理报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总片段数: {total_count}\n")
            f.write(f"成功片段: {success_count}\n")
            f.write(f"失败片段: {total_count - success_count}\n")
            f.write(f"成功率: {success_count/total_count*100:.1f}%\n")
            f.write(f"输出目录: {output_dir}\n")
        
        print(f"\n📊 处理报告已生成:")
        print(f"   - 详细报告: {report_file}")
        print(f"   - 摘要报告: {summary_file}")
        
        return report_file

def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description="批量语音合成工具")
    parser.add_argument("input_file", help="输入文本文件路径")
    parser.add_argument("--voice", "-v", default="Cherry", help="音色名称")
    parser.add_argument("--max-length", "-l", type=int, default=500, 
                       help="单个文本最大长度")
    parser.add_argument("--delay", "-d", type=float, default=1.0, 
                       help="请求间隔时间（秒）")
    parser.add_argument("--region", "-r", choices=["china", "international"], 
                       default="china", help="地域选择")
    
    args = parser.parse_args()
    
    # 检查文件存在
    if not os.path.exists(args.input_file):
        print(f"❌ 文件不存在: {args.input_file}")
        sys.exit(1)
    
    # 处理文件
    processor = BatchTTSProcessor(args.region)
    result = processor.process_file(
        args.input_file, 
        args.voice, 
        args.max_length, 
        args.delay
    )
    
    if result["success"]:
        stats = result["statistics"]
        print(f"\n🎉 批量处理完成!")
        print(f"   成功率: {stats['success_rate']*100:.1f}%")
        print(f"   输出目录: {result['output_dir']}")
    else:
        print(f"❌ 处理失败: {result.get('error', '未知错误')}")
        sys.exit(1)

if __name__ == "__main__":
    main()