import os
import json
import sys
from datetime import datetime
from urllib.parse import urlparse
import dashscope
from dashscope import Generation
import config

# 设置环境变量和API密钥
os.environ['DASHSCOPE_API_KEY'] = config.DASHSCOPE_API_KEY
dashscope.api_key = config.DASHSCOPE_API_KEY
MODEL_ID = config.DASHSCOPE_MODEL_ID  # 从配置中使用模型ID

class LinkValidator:
    def __init__(self, new_links_file=config.NEW_LINKS_FILE, valid_links_file=config.VALID_LINKS_FILE):
        """初始化链接验证器"""
        self.new_links_file = new_links_file
        self.valid_links_file = valid_links_file
        self.validation_prompt = """
你是一个专门评估链接是否为有效农业新闻链接的 AI 助手。请基于以下信息判断：

URL: {url}
链接文本: {link_text}
URL 路径: {url_path}

任务：判断此链接是否指向有效的农业新闻文章，并给出 0-100 的分数。
有效农业新闻链接的特征：
1. 指向具体新闻文章（而非主页、栏目页或聚合页）
2. URL 路径通常包含日期（例如 /2023/04/02/）或文章标识符（例如 /article-id-123）
3. 链接文本类似新闻标题（简洁、描述性强，非泛泛的"点击这里"）
4. 不包含非文章路径（如 /tag/, /login/, /search/, /category/）
5. 有效农业新闻有时也会和天气, 政策，农业相关主体（如JBS minerva, marfrig），进出口汇率 等有关

评分标准：
- 完全符合特征：80-100 分
- 部分符合（如有标题但路径不明确）：50-79 分
- 不符合或无法判断：0-49 分

直接返回以下 JSON 格式结果：
{{"score": 分数值(0-100), "is_valid": true/false, "reason": "简要分析原因"}}
"""

    def _load_new_links(self, batch_id=None):
        """加载链接数据
        
        参数:
            batch_id: 如果指定，则加载特定批次的链接；否则加载最新的一批
        """
        try:
            with open(self.new_links_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if batch_id:
                    # 查找特定批次ID的数据
                    for timestamp, batch_data in data.items():
                        # 检查每个主页的数据
                        for homepage_url, homepage_data in batch_data.items():
                            if 'batch_id' in homepage_data and homepage_data['batch_id'] == batch_id:
                                print(f"找到批次 {batch_id} 的数据，时间戳: {timestamp}")
                                return timestamp, batch_data
                    
                    print(f"未找到批次ID为 {batch_id} 的数据")
                    return None, None
                else:
                    # 获取最新的时间戳
                    latest_timestamp = max(data.keys())
                    print(f"加载最新批次的数据，时间戳: {latest_timestamp}")
                    return latest_timestamp, data[latest_timestamp]
        except Exception as e:
            print(f"加载新链接文件时出错: {e}")
            return None, None

    def _save_valid_links(self, validation_results, batch_id=None):
        """保存验证结果"""
        try:
            # 读取现有的验证结果（如果存在）
            existing_data = {}
            if os.path.exists(self.valid_links_file):
                with open(self.valid_links_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)

            # 添加新的验证结果
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 构建结果条目
            result_entry = {
                'batch_id': batch_id if batch_id else "未知批次",
                'timestamp': timestamp,
                'results': validation_results
            }
            
            # 使用时间戳作为键保存结果
            existing_data[timestamp] = result_entry

            # 保存更新后的数据
            with open(self.valid_links_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            print(f"验证结果已保存到 {self.valid_links_file}")
            if batch_id:
                print(f"已完成批次 {batch_id} 的验证")
        except Exception as e:
            print(f"保存验证结果时出错: {e}")

    def validate_link(self, url, link_text=""):
        """使用Qwen API验证单个链接"""
        try:
            parsed_url = urlparse(url)
            url_path = parsed_url.path

            # 准备提示词
            prompt = self.validation_prompt.format(
                url=url,
                link_text=link_text,
                url_path=url_path
            )

            print(f"正在验证链接: {url}")
            # 使用更简单的方式调用通义千问API
            response = Generation.call(
                model=MODEL_ID,
                prompt=prompt,
                temperature=0.1,
                max_tokens=1500,
                top_p=0.8
            )

            if response.status_code == 200:
                try:
                    # 从响应中提取内容
                    content = response.output.text
                    print(f"API响应: {content[:100]}...")  # 仅打印开头部分，避免过长
                    
                    # 尝试从内容中提取JSON
                    try:
                        # 查找第一个 { 和最后一个 } 之间的内容
                        start = content.find('{')
                        end = content.rfind('}') + 1
                        if start != -1 and end != 0:
                            json_str = content[start:end]
                            result = json.loads(json_str)
                            return result
                        else:
                            print("响应中没有找到JSON格式的内容")
                            # 创建默认结果
                            return {
                                "score": 0,
                                "is_valid": False,
                                "reason": "无法解析API响应"
                            }
                    except json.JSONDecodeError as e:
                        print(f"JSON解析错误: {str(e)}")
                        print(f"尝试解析的内容: {content}")
                        # 创建默认结果
                        return {
                            "score": 0,
                            "is_valid": False,
                            "reason": "JSON解析失败"
                        }
                except Exception as e:
                    print(f"处理API响应时出错: {str(e)}")
                    return None
            else:
                print(f"API调用失败: {response.status_code}")
                if hasattr(response, 'code'):
                    print(f"错误代码: {response.code}")
                if hasattr(response, 'message'):
                    print(f"错误信息: {response.message}")
                return None

        except Exception as e:
            print(f"验证链接时出错 {url}: {str(e)}")
            return None

    def validate_links_by_batch(self, batch_id=None):
        """验证特定批次的链接
        
        参数:
            batch_id: 批次ID，如果为None则验证最新一批
        """
        timestamp, links_data = self._load_new_links(batch_id)
        if not links_data:
            print("没有找到要验证的链接数据")
            return

        print(f"\n开始验证 {timestamp} 的链接")
        # 确定当前正在处理的批次ID
        current_batch_id = batch_id
        if not current_batch_id:
            # 如果未指定批次ID，尝试从数据中获取
            for homepage_url, data in links_data.items():
                if 'batch_id' in data:
                    current_batch_id = data['batch_id']
                    print(f"使用从数据中获取的批次ID: {current_batch_id}")
                    break
        
        validation_results = {}

        for homepage_url, data in links_data.items():
            print(f"\n检查来自 {data.get('note', '未知来源')} 的链接:")
            valid_links = []
            
            # 确保new_links字段存在
            if 'new_links' not in data:
                print(f"警告: {homepage_url} 没有 'new_links' 字段")
                continue
                
            for link in data['new_links']:
                result = self.validate_link(link)
                
                if result:
                    print(f"验证结果: 分数={result['score']}, 有效={result['is_valid']}")
                    print(f"原因: {result['reason']}")
                    
                    valid_links.append({
                        'url': link,
                        'validation': result
                    })
                else:
                    print(f"链接验证失败")

            validation_results[homepage_url] = {
                'note': data.get('note', ''),
                'source': data.get('source', ''),
                'validated_links': valid_links,
                'original_timestamp': timestamp
            }

        # 保存验证结果
        self._save_valid_links(validation_results, current_batch_id)

def main():
    """主函数"""
    validator = LinkValidator()
    
    # 检查是否指定了批次ID
    if len(sys.argv) > 1:
        batch_id = sys.argv[1]
        print(f"使用指定的批次ID: {batch_id}")
        validator.validate_links_by_batch(batch_id)
    else:
        print("未指定批次ID，将验证最新一批链接")
        validator.validate_links_by_batch()

if __name__ == "__main__":
    main() 