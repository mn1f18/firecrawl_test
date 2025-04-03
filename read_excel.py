import pandas as pd

def read_urls_from_excel(file_path):
    """从Excel文件中读取URL列表"""
    try:
        df = pd.read_excel(file_path)
        
        # 检查必要的列是否存在
        if 'link' not in df.columns:
            print(f"错误: Excel文件中没有'link'列")
            return [], {}
        
        # 获取URL列表
        urls = df['link'].dropna().tolist()
        
        # 获取标签信息（如果存在）
        tags = {}
        if '标签' in df.columns:
            for index, row in df.iterrows():
                if pd.notna(row['link']) and pd.notna(row['标签']):
                    tags[row['link']] = row['标签']
        
        print(f"从Excel文件中读取了 {len(urls)} 个URL")
        return urls, tags
    
    except Exception as e:
        print(f"读取Excel文件时出错: {str(e)}")
        return [], {} 