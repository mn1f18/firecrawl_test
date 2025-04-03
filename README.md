# 农业新闻处理系统

这是一个用于监控农业新闻网站、提取新链接、验证链接有效性并提取内容的自动化处理系统。系统分为三个主要步骤，可以单独运行或作为完整流程运行。

## 功能特点

- **主页监控**：定期检查指定的农业新闻网站主页，提取并过滤链接
- **链接验证**：使用AI判断链接是否指向有效的农业新闻文章
- **内容提取**：从验证为有效的链接中提取结构化内容
- **批次处理**：所有处理都基于批次ID进行，便于追踪和管理
- **灵活配置**：所有配置集中在一个文件中，便于调整

## 项目结构

```
├── config.py                     # 配置文件，包含API密钥和其他设置
├── APP.py                        # 主应用，整合了三个步骤的功能
├── step_1_homepage_monitor.py    # 步骤1：主页监控和链接提取
├── step_2_link_validator.py      # 步骤2：链接有效性验证
├── step_3_content_extraction.py  # 步骤3：内容提取
├── testhomepage.xlsx             # 包含要监控的主页URL列表的Excel文件
├── link_cache.json               # 历史链接缓存
├── new_links.json                # 新发现的链接
└── new_links_valid.json          # 验证后的链接
```

## 安装与配置

1. 安装所需依赖：
   ```bash
   pip install firecrawl-py pandas openpyxl dashscope
   ```

2. 在`config.py`中配置您的API密钥：
   - Firecrawl API密钥
   - 阿里云通义千问API密钥

3. 准备主页URL列表：
   在`testhomepage.xlsx`文件中添加要监控的网站URL，文件应包含以下列：
   - `link`: 网站URL（必需）
   - `备注`: 网站说明（可选）
   - `来源`: 网站来源信息（可选）

## 使用方法

### 完整流程

运行完整的处理流程（包括所有三个步骤）：

```bash
python APP.py
```

### 使用特定批次ID

指定批次ID运行流程（跳过步骤1）：

```bash
python APP.py --batch batch_20250403114912
```

### 单独运行特定步骤

运行步骤1（主页监控和链接提取）：

```bash
python APP.py --step 1
```

运行步骤2（链接验证），可选指定批次ID：

```bash
python APP.py --step 2 --batch batch_20250403114912
```

运行步骤3（内容提取），可选指定批次ID或时间戳：

```bash
python APP.py --step 3 --batch batch_20250403114912
```

或使用时间戳：

```bash
python APP.py --step 3 --timestamp "2025-04-03 11:49:12"
```

## 工作流程

1. **步骤1: 主页监控**
   - 从Excel文件加载主页URL
   - 提取并过滤链接
   - 与历史链接比较，找出新链接
   - 为每批次链接分配批次ID
   - 保存新链接到JSON文件

2. **步骤2: 链接验证**
   - 加载特定批次的链接
   - 使用AI验证每个链接的有效性
   - 为每个链接分配验证分数和理由
   - 保存验证结果到JSON文件

3. **步骤3: 内容提取**
   - 加载验证为有效的链接（分数>=70）
   - 使用Firecrawl API提取网页内容
   - 将内容转换为结构化数据
   - 保存结果到Excel和JSON文件

## 注意事项

- Firecrawl API使用JSON格式提取结构化数据会消耗更多的API积分（每页5积分 vs 普通提取每页1积分）
- 所有步骤都支持批次ID，确保数据在各个步骤之间的一致性
- 错误处理机制确保单个链接的失败不会影响整体流程

## 自定义与扩展

- 修改`config.py`中的设置以调整系统行为
- 在`step_1_homepage_monitor.py`中修改`filter_valid_links`方法可以自定义链接过滤规则
- 在`step_2_link_validator.py`中修改验证提示词可以调整链接验证标准
- 在`step_3_content_extraction.py`中修改内容提取schema可以调整提取的内容结构 