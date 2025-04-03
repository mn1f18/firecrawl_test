from firecrawl.firecrawl import FirecrawlApp
import config
import json
import pandas as pd
from datetime import datetime
import time
import os
import random

class HomepageMonitor:
    def __init__(self, excel_path, cache_file="link_cache.json", new_links_file="new_links.json"):
        """初始化监控器"""
        self.app = FirecrawlApp(api_key=config.API_KEY)
        self.excel_path = excel_path
        self.cache_file = cache_file
        self.new_links_file = new_links_file
        self.link_history = self._load_link_history()

    def _load_link_history(self):
        """加载历史链接缓存"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"加载历史链接缓存时出错: {e}")
            return {}

    def _save_link_history(self):
        """保存历史链接缓存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.link_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史链接缓存时出错: {e}")

    def _save_new_links(self, new_links_data):
        """保存新发现的链接"""
        try:
            # 读取现有的新链接数据（如果存在）
            existing_data = {}
            if os.path.exists(self.new_links_file):
                with open(self.new_links_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)

            # 更新数据
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 生成batch_id
            batch_id = f"batch_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            if timestamp not in existing_data:
                # 为每个homepage_url的数据添加batch_id
                for homepage_url in new_links_data:
                    new_links_data[homepage_url]['batch_id'] = batch_id
                existing_data[timestamp] = new_links_data

            # 保存更新后的数据
            with open(self.new_links_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
                
            print(f"新链接已保存，批次ID: {batch_id}")
        except Exception as e:
            print(f"保存新链接时出错: {e}")

    def read_homepage_urls(self):
        """从Excel文件读取主页URL"""
        try:
            df = pd.read_excel(self.excel_path)
            # 确保必要的列存在
            if 'link' not in df.columns:
                raise ValueError("Excel文件中缺少'link'列")
            
            # 创建URL字典，包含备注和来源信息
            urls_info = {}
            for _, row in df.iterrows():
                url = row['link']
                info = {
                    'note': row.get('备注', ''),
                    'source': row.get('来源', '')
                }
                urls_info[url] = info
            
            return urls_info
        except Exception as e:
            print(f"读取Excel文件时出错: {e}")
            return {}

    def extract_links_from_page(self, url):
        """从页面提取链接"""
        max_retries = config.MAX_RETRIES
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                if retry_count > 0:
                    wait_time = config.RETRY_DELAY * (1 + retry_count)
                    print(f"第 {retry_count} 次重试，等待 {wait_time} 秒...")
                    time.sleep(wait_time)
                
                print(f"正在使用map方法获取 {url} 的链接...")
                
                # 使用map_url功能获取所有可访问的链接
                # 根据正确的API文档修改参数
                result = self.app.map_url(url, params={
                    'includeSubdomains': False,  # 包含子域名
                    'limit': 500,  # 增加链接获取上限
                    'timeout': 60000  # 超时时间（毫秒）
                })
                
                if result and 'links' in result:
                    # 移除自引用链接
                    links = [link for link in result['links'] if link != url]
                    
                    # 过滤掉一些不需要的路径
                    excluded_patterns = [
                        '/tag/', '/category/', '/author/',
                        '/search/', '/page/', '/wp-content/',
                        '/wp-admin/', '/wp-includes/',
                        '/login', '/register', '/account',
                        '.jpg', '.jpeg', '.png', '.gif',
                        '.css', '.js', '.xml', '.pdf',
                        'javascript:'
                    ]
                    
                    filtered_links = []
                    for link in links:
                        exclude = False
                        for pattern in excluded_patterns:
                            if pattern in link:
                                exclude = True
                                break
                        if not exclude:
                            filtered_links.append(link)
                    
                    if len(links) != len(result['links']):
                        print(f"移除了自引用链接: {url}")
                    
                    print(f"原始链接数量: {len(result['links'])}, 去除自引用后: {len(links)}, 过滤后: {len(filtered_links)}")
                    return filtered_links
                
                print("没有找到链接或返回结果为空")
                return []
                
            except Exception as e:
                print(f"从页面提取链接时出错 {url}: {e}")
                if "Rate limit exceeded" in str(e):
                    retry_count += 1
                    if retry_count <= max_retries:
                        # 从错误消息中提取等待时间
                        try:
                            error_str = str(e)
                            wait_info = error_str.split("please retry after ")[1].split("s,")[0]
                            wait_seconds = int(float(wait_info)) 
                            print(f"达到速率限制，等待 {wait_seconds} 秒后重试...")
                            time.sleep(wait_seconds)
                        except:
                            # 如果无法提取具体等待时间，使用递增等待
                            wait_time = 15 * retry_count  # 15, 30, 45 秒等
                            print(f"达到速率限制，等待 {wait_time} 秒后重试...")
                            time.sleep(wait_time)
                    else:
                        print(f"达到最大重试次数，放弃获取链接")
                        return []
                else:
                    # 对于非速率限制错误，尝试一次重试
                    if "timeout" in str(e).lower() and retry_count < max_retries:
                        retry_count += 1
                        wait_time = 10
                        print(f"请求超时，等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    else:
                        print(f"无法处理的错误，放弃获取链接")
                        return []
        
        return []

    def check_for_new_links(self):
        """检查新链接"""
        urls_info = self.read_homepage_urls()
        if not urls_info:
            print("没有找到要监控的URL")
            return

        new_links_found = {}
        
        # 统计信息
        total_urls = len(urls_info)
        processed_urls = 0
        total_new_links = 0
        
        for homepage_url, info in urls_info.items():
            processed_urls += 1
            print(f"\n正在检查主页 [{processed_urls}/{total_urls}]: {homepage_url}")
            print(f"备注: {info['note']}")
            
            try:
                # 获取当前页面的所有链接
                current_links = self.extract_links_from_page(homepage_url)
                print(f"发现 {len(current_links)} 个链接")
                
                # 获取这个主页的历史链接
                historical_links = self.link_history.get(homepage_url, [])
                print(f"历史链接数量: {len(historical_links)}")
                
                # 找出新链接
                new_links = [link for link in current_links if link not in historical_links]
                
                if new_links:
                    print(f"发现 {len(new_links)} 个新链接:")
                    # 限制显示的链接数量，避免输出过长
                    display_limit = min(10, len(new_links))
                    for i, link in enumerate(new_links[:display_limit]):
                        print(f"  - {link}")
                    
                    if len(new_links) > display_limit:
                        print(f"  ... 还有 {len(new_links) - display_limit} 个新链接未显示")
                    
                    # 更新历史记录
                    self.link_history[homepage_url] = list(set(historical_links + current_links))
                    print(f"历史链接更新至 {len(self.link_history[homepage_url])} 个")
                    
                    # 记录新链接
                    new_links_found[homepage_url] = {
                        'note': info['note'],
                        'source': info['source'],
                        'new_links': new_links,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    total_new_links += len(new_links)
                else:
                    print("没有发现新链接")
                
                # 每次检查后暂停较长时间，避免请求过于频繁
                if processed_urls < total_urls:  # 最后一个URL不需要等待
                    wait_time = config.BATCH_PAUSE_TIME + random.randint(5, 15)
                    print(f"等待 {wait_time} 秒后继续下一个URL...")
                    time.sleep(wait_time)
                
            except Exception as e:
                print(f"处理主页时出错 {homepage_url}: {e}")
                continue

        # 保存更新后的历史记录
        self._save_link_history()
        
        # 如果发现了新链接，保存它们
        if new_links_found:
            self._save_new_links(new_links_found)
            print(f"\n总计发现 {total_new_links} 个新链接，来自 {len(new_links_found)} 个网站")
        else:
            print("\n未发现任何新链接")

def main(interval_minutes=None):
    """主函数，可选择定时运行"""
    excel_path = "C:\\Python\\github\\firecrawl\\testhomepage.xlsx"
    monitor = HomepageMonitor(excel_path)
    
    def run_check():
        print(f"\n开始检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        monitor.check_for_new_links()
        print(f"检查完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if interval_minutes:
        print(f"设置为每 {interval_minutes} 分钟运行一次")
        while True:
            run_check()
            print(f"等待 {interval_minutes} 分钟后进行下一次检查...")
            time.sleep(interval_minutes * 60)
    else:
        run_check()

if __name__ == "__main__":
    # 设置为None表示只运行一次，或者设置分钟数进行定时运行
    # 例如：main(interval_minutes=60) 表示每小时运行一次
    main() 