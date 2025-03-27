from firecrawl.firecrawl import FirecrawlApp
from config import API_KEY
import json
import pandas as pd
from datetime import datetime
import time

app = FirecrawlApp(api_key=API_KEY)

def load_urls_from_file(file_path):
    """从文件中加载URL列表"""
    urls = []
    print(f"尝试从文件加载URL: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"文件中共有 {len(lines)} 行")
            for i, line in enumerate(lines):
                original_line = line
                line = line.strip()
                print(f"第 {i+1} 行: '{original_line}' -> '{line}'")
                if line and not line.startswith('link') and line.startswith('http'):
                    urls.append(line)
                    print(f"  - 已添加URL: {line}")
                else:
                    print(f"  - 跳过行: {line}")
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
    
    return urls

def extract_content_from_urls(urls):
    """使用Firecrawl的extract功能从URL中提取内容"""
    results = {}
    
    for url in urls:
        print(f"正在处理: {url}")
        try:
            # 使用scrape_url方法提取结构化内容
            print(f"提交scrape请求，带有JSON提取选项...")
            
            # 定义提取schema
            schema = {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "文章标题"},
                    "content": {"type": "string", "description": "文章的完整正文内容"},
                    "publish_date": {"type": "string", "description": "发布日期"},
                    "source": {"type": "string", "description": "文章来源"}
                },
                "required": ["title", "content"]
            }
            
            # 使用scrape_url方法，带有jsonOptions
            try:
                # 先尝试只获取markdown格式
                print(f"尝试获取markdown格式内容...")
                scrape_result = app.scrape_url(
                    url, 
                    params={'formats': ['markdown']}
                )
                
                print(f"成功获取markdown内容!")
                
                # 打印返回的结构以便调试
                print(f"返回结构: {list(scrape_result.keys())}")
                
                # 保存markdown结果
                markdown_content = scrape_result.get("markdown", "")
                metadata = scrape_result.get("metadata", {})
                
                # 然后尝试使用jsonOptions提取结构化数据
                print(f"尝试提取结构化数据...")
                json_result = app.scrape_url(
                    url, 
                    params={
                        'formats': ['json'],
                        'jsonOptions': {
                            'schema': schema,
                            'prompt': "Extract the main body content of the article."
                        }
                    }
                )
                
                print(f"成功提取结构化数据!")
                print(f"JSON结构: {list(json_result.keys())}")
                
                # 获取json数据
                json_data = json_result.get("json", {})
                
                # 保存结果
                results[url] = {
                    "extract": {
                        "data": json_data
                    },
                    "markdown": markdown_content,
                    "metadata": metadata
                }
                
            except Exception as scrape_error:
                print(f"scrape_url出错: {str(scrape_error)}")
                # 如果超时，等待一段时间后重试
                if "timeout" in str(scrape_error).lower():
                    print(f"请求超时，等待30秒后重试...")
                    time.sleep(30)
                    
                    # 重试，只获取markdown
                    print(f"重试获取markdown...")
                    scrape_result = app.scrape_url(
                        url, 
                        params={'formats': ['markdown']}
                    )
                    
                    results[url] = {
                        "extract": {
                            "data": {}  # 空数据，因为提取失败
                        },
                        "markdown": scrape_result.get("markdown", ""),
                        "metadata": scrape_result.get("metadata", {})
                    }
                else:
                    raise scrape_error
            
            print(f"成功处理URL!")
            
        except Exception as e:
            results[url] = {
                "error": str(e)
            }
            print(f"处理失败: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("-" * 50)
    
    return results

def save_results(results):
    """保存结果到文件(JSON和Excel)"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存完整结果到JSON
    full_filename = f"firecrawl_full_results_{timestamp}.json"
    with open(full_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 保存提取的内容到单独JSON文件
    content_filename = f"firecrawl_extracted_content_{timestamp}.json"
    extracted_content = {}
    
    for url, data in results.items():
        if "extract" in data and "error" not in data:
            extracted_content[url] = data["extract"]
    
    with open(content_filename, "w", encoding="utf-8") as f:
        json.dump(extracted_content, f, ensure_ascii=False, indent=2)
    
    # 保存到Excel文件
    excel_filename = f"firecrawl_results_{timestamp}.xlsx"
    
    # 准备Excel数据
    excel_data = []
    for url, data in results.items():
        row = {"URL": url}
        
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
    print(f"Excel格式结果已保存到: {excel_filename}")

# 主函数
if __name__ == "__main__":
    print("开始使用Firecrawl提取网页内容...")
    
    # 硬编码URL列表，而不是从文件加载
    urls = [
        "https://cj.zhue.com.cn/xingye/2025/0325/398498.html",
        "https://www.zaobao.com/realtime/world/story20250325-6067441",
        "http://info.shippingchina.com/bluenews/index/detail/id/225469.html"
    ]
    print(f"使用硬编码的 {len(urls)} 个URL")
    
    # 提取内容
    results = extract_content_from_urls(urls)
    
    # 保存结果
    save_results(results)
    
    print("处理完成!") 