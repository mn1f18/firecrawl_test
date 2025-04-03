from firecrawl.firecrawl import FirecrawlApp
import config
import json
import pandas as pd
from datetime import datetime
import time
import os
import sys

class ContentExtractor:
    def __init__(self, valid_links_file=config.VALID_LINKS_FILE):
        """初始化内容提取器"""
        self.app = FirecrawlApp(api_key=config.API_KEY)
        self.valid_links_file = valid_links_file
        
    def load_valid_links(self, batch_id=None, timestamp=None):
        """加载已验证的有效链接
        
        参数:
            batch_id: 批次ID，如果指定则加载该批次的链接
            timestamp: 时间戳，如果指定则加载该时间戳的验证结果
        
        返回:
            有效链接列表，每个元素为字典 {url, source, note}
        """
        try:
            if not os.path.exists(self.valid_links_file):
                print(f"验证链接文件 {self.valid_links_file} 不存在")
                return []
                
            with open(self.valid_links_file, 'r', encoding='utf-8') as f:
                validation_data = json.load(f)
            
            if not validation_data:
                print("验证链接文件为空")
                return []
            
            # 确定要处理的时间戳
            target_timestamp = None
            if timestamp and timestamp in validation_data:
                target_timestamp = timestamp
            elif batch_id:
                # 查找包含指定batch_id的时间戳
                for ts, entry in validation_data.items():
                    if entry.get('batch_id') == batch_id:
                        target_timestamp = ts
                        break
            else:
                # 使用最新的时间戳
                target_timestamp = max(validation_data.keys())
            
            if not target_timestamp:
                print(f"找不到指定的批次ID或时间戳")
                return []
            
            print(f"使用时间戳 {target_timestamp} 的验证结果")
            validation_entry = validation_data[target_timestamp]
            validation_results = validation_entry.get('results', {})
            
            valid_links = []
            for homepage_url, homepage_data in validation_results.items():
                source = homepage_data.get('source', '')
                note = homepage_data.get('note', '')
                
                validated_links = homepage_data.get('validated_links', [])
                for link_data in validated_links:
                    url = link_data.get('url', '')
                    validation = link_data.get('validation', {})
                    
                    # 只提取有效的链接（is_valid为True且score较高的）
                    if validation.get('is_valid', False) and validation.get('score', 0) >= config.MIN_VALID_SCORE:
                        valid_links.append({
                            'url': url,
                            'source': source,
                            'note': note,
                            'score': validation.get('score', 0),
                            'reason': validation.get('reason', '')
                        })
            
            print(f"找到 {len(valid_links)} 个有效链接")
            return valid_links
            
        except Exception as e:
            print(f"加载验证链接时出错: {e}")
            import traceback
            traceback.print_exc()
            return []
            
    def extract_content_from_urls(self, valid_links):
        """从有效链接中提取内容"""
        if not valid_links:
            print("没有有效链接可处理")
            return {}
            
        results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 创建结果目录
        results_dir = f"extracted_content_{timestamp}"
        os.makedirs(results_dir, exist_ok=True)
        
        for i, link_data in enumerate(valid_links):
            url = link_data['url']
            print(f"\n[{i+1}/{len(valid_links)}] 正在处理: {url}")
            print(f"来源: {link_data['source']}, 备注: {link_data['note']}")
            print(f"验证分数: {link_data['score']}")
            
            try:
                # 使用config中的schema
                schema = config.CONTENT_SCHEMA
                
                try:
                    # 先尝试只获取markdown格式
                    print(f"尝试获取markdown格式内容...")
                    scrape_result = self.app.scrape_url(
                        url, 
                        params={'formats': ['markdown']}
                    )
                    
                    print(f"成功获取markdown内容!")
                    
                    # 保存markdown结果
                    markdown_content = scrape_result.get("markdown", "")
                    metadata = scrape_result.get("metadata", {})
                    
                    # 然后尝试使用jsonOptions提取结构化数据
                    print(f"尝试提取结构化数据...")
                    json_result = self.app.scrape_url(
                        url, 
                        params={
                            'formats': ['json'],
                            'jsonOptions': {
                                'schema': schema,
                                'prompt': "提取这篇农业新闻文章的完整内容，包括标题、正文、发布日期、来源、分类、作者和摘要。"
                            }
                        }
                    )
                    
                    print(f"成功提取结构化数据!")
                    
                    # 获取json数据
                    json_data = json_result.get("json", {})
                    
                    # 保存结果
                    results[url] = {
                        "extract": {
                            "data": json_data
                        },
                        "markdown": markdown_content,
                        "metadata": metadata,
                        "source": link_data['source'],
                        "note": link_data['note'],
                        "validation_score": link_data['score'],
                        "validation_reason": link_data['reason']
                    }
                    
                except Exception as scrape_error:
                    print(f"scrape_url出错: {str(scrape_error)}")
                    # 如果超时，等待一段时间后重试
                    if "timeout" in str(scrape_error).lower():
                        print(f"请求超时，等待{config.RETRY_WAIT_TIME}秒后重试...")
                        time.sleep(config.RETRY_WAIT_TIME)
                        
                        # 重试，只获取markdown
                        print(f"重试获取markdown...")
                        scrape_result = self.app.scrape_url(
                            url, 
                            params={'formats': ['markdown']}
                        )
                        
                        results[url] = {
                            "extract": {
                                "data": {}  # 空数据，因为提取失败
                            },
                            "markdown": scrape_result.get("markdown", ""),
                            "metadata": scrape_result.get("metadata", {}),
                            "source": link_data['source'],
                            "note": link_data['note'],
                            "validation_score": link_data['score'],
                            "validation_reason": link_data['reason']
                        }
                    else:
                        raise scrape_error
                
                print(f"成功处理URL!")
                
            except Exception as e:
                results[url] = {
                    "error": str(e),
                    "source": link_data['source'],
                    "note": link_data['note'],
                    "validation_score": link_data['score'],
                    "validation_reason": link_data['reason']
                }
                print(f"处理失败: {str(e)}")
                import traceback
                traceback.print_exc()
            
            print("-" * 50)
            
            # 每处理一个URL就保存一次结果
            self.save_interim_results(results, results_dir, i+1, len(valid_links))
            
            # 每处理N个URL后暂停一下，避免API限制
            if (i + 1) % config.BATCH_SIZE == 0 and i + 1 < len(valid_links):
                print(f"已处理 {i+1} 个URL，暂停 {config.BATCH_PAUSE_TIME} 秒...")
                time.sleep(config.BATCH_PAUSE_TIME)
        
        # 保存最终结果
        self.save_final_results(results, results_dir)
        
        return results, results_dir
    
    def save_interim_results(self, results, results_dir, current_count, total_count):
        """每处理一个URL后保存中间结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存到Excel文件
        excel_filename = os.path.join(results_dir, f"content_interim_results_{current_count}_of_{total_count}.xlsx")
        
        # 准备Excel数据
        excel_data = []
        for url, data in results.items():
            row = {
                "URL": url,
                "来源": data.get("source", ""),
                "备注": data.get("note", ""),
                "验证分数": data.get("validation_score", 0),
                "处理状态": "成功" if "error" not in data else "失败"
            }
            
            # 添加提取的结构化数据
            if "extract" in data and "error" not in data:
                extract_data = data["extract"]
                if "data" in extract_data:
                    for key, value in extract_data["data"].items():
                        row[key] = value
            
            # 添加错误信息(如果有)
            if "error" in data:
                row["错误信息"] = data["error"]
            
            # 添加元数据
            if "metadata" in data:
                for key, value in data["metadata"].items():
                    row[f"元数据_{key}"] = value
            
            # 添加原始markdown的前500个字符作为预览
            if "markdown" in data:
                row["Markdown预览"] = data["markdown"][:500] + "..." if len(data["markdown"]) > 500 else data["markdown"]
            
            excel_data.append(row)
        
        # 创建DataFrame并保存到Excel
        df = pd.DataFrame(excel_data)
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        
        print(f"已处理 {current_count}/{total_count} 个URL，中间结果已保存到: {excel_filename}")
        
    def save_final_results(self, results, results_dir):
        """保存最终结果到文件(JSON和Excel)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存完整结果到JSON
        full_filename = os.path.join(results_dir, f"content_full_results_{timestamp}.json")
        with open(full_filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 保存提取的内容到单独JSON文件
        content_filename = os.path.join(results_dir, f"content_extracted_data_{timestamp}.json")
        extracted_content = {}
        
        for url, data in results.items():
            if "extract" in data and "error" not in data:
                extracted_content[url] = data["extract"]
        
        with open(content_filename, "w", encoding="utf-8") as f:
            json.dump(extracted_content, f, ensure_ascii=False, indent=2)
        
        # 保存到Excel文件
        excel_filename = os.path.join(results_dir, f"content_final_results_{timestamp}.xlsx")
        
        # 准备Excel数据
        excel_data = []
        for url, data in results.items():
            row = {
                "URL": url,
                "来源": data.get("source", ""),
                "备注": data.get("note", ""),
                "验证分数": data.get("validation_score", 0),
                "验证理由": data.get("validation_reason", ""),
                "处理状态": "成功" if "error" not in data else "失败"
            }
            
            # 添加提取的结构化数据
            if "extract" in data and "error" not in data:
                extract_data = data["extract"]
                if "data" in extract_data:
                    for key, value in extract_data["data"].items():
                        row[key] = value
            
            # 添加错误信息(如果有)
            if "error" in data:
                row["错误信息"] = data["error"]
            
            # 添加元数据
            if "metadata" in data:
                for key, value in data["metadata"].items():
                    row[f"元数据_{key}"] = value
            
            # 添加原始markdown的前500个字符作为预览
            if "markdown" in data:
                row["Markdown预览"] = data["markdown"][:500] + "..." if len(data["markdown"]) > 500 else data["markdown"]
            
            excel_data.append(row)
        
        # 创建DataFrame并保存到Excel
        df = pd.DataFrame(excel_data)
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        
        print(f"完整结果已保存到: {full_filename}")
        print(f"提取的内容已保存到: {content_filename}")
        print(f"最终Excel结果已保存到: {excel_filename}")

def main():
    """主函数"""
    extractor = ContentExtractor()
    
    # 检查是否指定了批次ID
    batch_id = None
    timestamp = None
    
    if len(sys.argv) > 1:
        if sys.argv[1].startswith("batch_"):
            batch_id = sys.argv[1]
            print(f"使用指定的批次ID: {batch_id}")
        else:
            timestamp = sys.argv[1]
            print(f"使用指定的时间戳: {timestamp}")
    
    # 加载有效链接
    valid_links = extractor.load_valid_links(batch_id, timestamp)
    
    if not valid_links:
        print("没有找到有效的链接，程序退出")
        exit(1)
    
    print(f"准备处理 {len(valid_links)} 个有效链接")
    
    # 提取内容
    results, results_dir = extractor.extract_content_from_urls(valid_links)
    
    print(f"处理完成! 所有结果已保存到 {results_dir} 目录")

if __name__ == "__main__":
    main() 