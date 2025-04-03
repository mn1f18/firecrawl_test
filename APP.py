import os
import sys
import argparse
from datetime import datetime
import time
import json
import logging

# 从各个模块导入功能
from step_1_homepage_monitor import HomepageMonitor
from step_2_link_validator import LinkValidator
from step_3_content_extraction import ContentExtractor
import config

def setup_logging():
    """设置日志记录"""
    # 创建logger
    logger = logging.getLogger('AgriNews')
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # 创建文件处理器
    fh = logging.FileHandler(config.LOG_FILE, encoding='utf-8')
    fh.setLevel(getattr(logging, config.LOG_LEVEL))

    # 创建控制台处理器
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, config.LOG_LEVEL))

    # 创建格式器
    formatter = logging.Formatter(config.LOG_FORMAT)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 添加处理器到logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

class AgriNewsApp:
    def __init__(self):
        """初始化应用"""
        # 设置日志
        self.logger = setup_logging()
        self.logger.info("初始化农业新闻处理应用...")
        
        self.homepage_monitor = HomepageMonitor(
            excel_path=config.HOMEPAGE_EXCEL_PATH,
            cache_file=config.LINKS_CACHE_FILE,
            new_links_file=config.NEW_LINKS_FILE
        )
        
        self.link_validator = LinkValidator(
            new_links_file=config.NEW_LINKS_FILE,
            valid_links_file=config.VALID_LINKS_FILE
        )
        
        self.content_extractor = ContentExtractor(
            valid_links_file=config.VALID_LINKS_FILE
        )
        
        # 当前批次ID
        self.current_batch_id = None
        self.logger.info("应用初始化完成")
    
    def run_homepage_monitor(self):
        """运行步骤1：监控主页并提取链接"""
        self.logger.info("="*30)
        self.logger.info("步骤1: 开始监控主页并提取链接...")
        self.logger.info("="*30)
        
        try:
            # 运行链接监控
            self.homepage_monitor.check_for_new_links()
            
            # 从结果中提取批次ID
            with open(config.NEW_LINKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 获取最新的时间戳
            if data:
                latest_timestamp = max(data.keys())
                latest_data = data[latest_timestamp]
                
                # 提取批次ID
                for homepage_url, homepage_data in latest_data.items():
                    if 'batch_id' in homepage_data:
                        self.current_batch_id = homepage_data['batch_id']
                        break
                
                if self.current_batch_id:
                    self.logger.info(f"步骤1完成！提取到批次ID: {self.current_batch_id}")
                else:
                    self.logger.warning("步骤1完成，但未找到批次ID")
            else:
                self.logger.warning("步骤1完成，但没有发现新链接")
                
        except Exception as e:
            self.logger.error(f"步骤1执行出错: {str(e)}", exc_info=True)
        
        return self.current_batch_id
    
    def run_link_validator(self, batch_id=None):
        """运行步骤2：验证链接有效性"""
        self.logger.info("="*30)
        self.logger.info("步骤2: 开始验证链接有效性...")
        self.logger.info("="*30)
        
        try:
            # 如果没有指定批次ID，使用当前批次ID
            if not batch_id and self.current_batch_id:
                batch_id = self.current_batch_id
                
            # 检查是否有批次ID
            if not batch_id:
                self.logger.warning("没有有效的批次ID，跳过链接验证步骤")
                return False
                
            # 验证链接
            self.link_validator.validate_links_by_batch(batch_id)
            
            self.logger.info("步骤2完成！")
            return True
            
        except Exception as e:
            self.logger.error(f"步骤2执行出错: {str(e)}", exc_info=True)
            return False
    
    def run_content_extraction(self, batch_id=None):
        """运行步骤3：提取内容"""
        self.logger.info("="*30)
        self.logger.info("步骤3: 开始提取内容...")
        self.logger.info("="*30)
        
        try:
            # 如果没有指定批次ID，使用当前批次ID
            if not batch_id and self.current_batch_id:
                batch_id = self.current_batch_id
                
            # 检查是否有批次ID
            if not batch_id:
                self.logger.warning("没有有效的批次ID，跳过内容提取步骤")
                return False
                
            # 加载有效链接
            valid_links = self.content_extractor.load_valid_links(batch_id)
            
            if not valid_links:
                self.logger.warning("没有找到有效的链接，步骤3无法继续")
                return False
            
            # 提取内容
            results, results_dir = self.content_extractor.extract_content_from_urls(valid_links)
            
            self.logger.info(f"步骤3完成！结果保存在 {results_dir} 目录")
            return results_dir
            
        except Exception as e:
            self.logger.error(f"步骤3执行出错: {str(e)}", exc_info=True)
            return False
    
    def run_full_pipeline(self, batch_id=None):
        """运行完整的处理流程"""
        self.logger.info("="*50)
        self.logger.info("启动农业新闻处理流程...")
        self.logger.info("="*50)
        
        start_time = datetime.now()
        self.logger.info(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 步骤1：监控主页
            if not batch_id:
                self.logger.info("执行步骤1: 主页监控...")
                batch_id = self.run_homepage_monitor()
                
                # 如果步骤1没有发现新链接，停止流程
                if not batch_id:
                    self.logger.warning("没有发现新链接，流程结束")
                    return None
            else:
                self.logger.info(f"使用指定的批次ID: {batch_id}，跳过步骤1")
                self.current_batch_id = batch_id
            
            # 步骤2：验证链接
            self.logger.info("执行步骤2: 链接验证...")
            if not self.run_link_validator(batch_id):
                self.logger.error("链接验证失败，流程结束")
                return None
            
            # 步骤3：提取内容
            self.logger.info("执行步骤3: 内容提取...")
            results_dir = self.run_content_extraction(batch_id)
            if not results_dir:
                self.logger.error("内容提取失败，流程结束")
                return None
            
            # 汇总结果
            end_time = datetime.now()
            duration = end_time - start_time
            
            self.logger.info("="*50)
            self.logger.info("农业新闻处理流程已完成！")
            self.logger.info(f"批次ID: {batch_id}")
            self.logger.info(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.logger.info(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.logger.info(f"总耗时: {duration}")
            self.logger.info(f"最终结果保存位置: {results_dir}")
            self.logger.info("="*50)
            
            return results_dir
            
        except Exception as e:
            self.logger.error(f"执行过程中出错: {str(e)}", exc_info=True)
            return None

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="农业新闻处理应用")
    parser.add_argument("--step", type=int, choices=[1, 2, 3], 
                        help="指定要运行的步骤编号(1:主页监控, 2:链接验证, 3:内容提取)")
    parser.add_argument("--batch", type=str, help="指定批次ID")
    parser.add_argument("--timestamp", type=str, help="指定时间戳")
    parser.add_argument("--all", action="store_true", help="运行完整流程")
    
    args = parser.parse_args()
    
    app = AgriNewsApp()
    
    # 根据命令行参数执行相应的步骤
    if args.all:
        app.run_full_pipeline(args.batch)
    elif args.step == 1:
        app.run_homepage_monitor()
    elif args.step == 2:
        app.run_link_validator(args.batch)
    elif args.step == 3:
        if args.timestamp:
            valid_links = app.content_extractor.load_valid_links(batch_id=args.batch, timestamp=args.timestamp)
            if valid_links:
                app.content_extractor.extract_content_from_urls(valid_links)
            else:
                print("没有找到有效的链接，无法提取内容。")
        else:
            app.run_content_extraction(args.batch)
    else:
        # 默认运行完整流程
        app.run_full_pipeline(args.batch)

if __name__ == "__main__":
    main() 