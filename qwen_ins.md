
在阿里云上创建了一个智能应用（Application）后，你可以通过阿里云 Model Studio 提供的 API 来调用它。以下是如何在 Python 中调用应用 ID 为 abf27f9eb6f742ff8f8fcf4d9c8dbb15、选用模型为 qwen-plus 的智能应用的步骤和代码示例。
前提条件
获取 API Key：
登录阿里云 Model Studio 控制台。

转到“API-KEY”页面，点击“创建 API Key”，生成一个密钥。

将 API Key 保存下来，建议设置为环境变量以提高安全性。

安装依赖：
确保已安装 Python 和 requests 库：
bash

pip install requests

API 端点：
调用应用的 HTTP 端点为：https://dashscope-intl.aliyuncs.com/api/v1/apps/{YOUR_APP_ID}/completion

Python 调用代码
以下是一个简单的 Python 脚本，用于调用你的智能应用：
python

import requests
import json
import os

# 配置
API_KEY = os.getenv("DASHSCOPE_API_KEY")  # 建议从环境变量读取 API Key
APP_ID = "abf27f9eb6f742ff8f8fcf4d9c8dbb15"  # 你的应用 ID
ENDPOINT = f"https://dashscope-intl.aliyuncs.com/api/v1/apps/{APP_ID}/completion"

# 如果未设置环境变量，可直接在此处硬编码（不推荐）
# API_KEY = "your-api-key-here"

# 请求头
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 请求体
payload = {
    "input": {
        "prompt": "请告诉我今天的天气如何？"  # 替换为你想输入的提示
    },
    "parameters": {
        "model": "qwen-plus"  # 指定模型为 qwen-plus
    },
    "debug": {}  # 可选：调试参数
}

# 发送请求
try:
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        print("返回结果：")
        print(json.dumps(result, ensure_ascii=False, indent=4))
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print(response.text)
except Exception as e:
    print(f"请求异常：{e}")

代码说明
API Key 配置：
推荐将 API Key 设置为环境变量：
bash

export DASHSCOPE_API_KEY="your-api-key-here"

然后在 Python 中通过 os.getenv("DASHSCOPE_API_KEY") 获取。

如果不使用环境变量，可以直接在代码中填入 API_KEY（但不安全）。

请求参数：
input.prompt：你发送给应用的输入文本，可以根据需求修改。

parameters.model：指定使用 qwen-plus 模型。

debug：可选字段，用于调试，留空即可。

返回结果：
如果成功，API 会返回 JSON 格式的响应，包含应用的输出。

示例输出可能如下：
json

{
  "output": {
    "text": "今天的天气晴朗，温度在20-25摄氏度之间。",
    "finish_reason": "stop",
    "session_id": "xxx"
  },
  "usage": {
    "models": [
      {
        "model_id": "qwen-plus",
        "input_tokens": 10,
        "output_tokens": 20
      }
    ]
  },
  "request_id": "yyy"
}

注意事项
权限检查：
确保你的 API Key 有权限访问该应用。如果遇到 Model.AccessDenied 错误，可能是子工作空间的 API Key 无法访问默认工作空间的应用，需联系阿里云账户管理员授权。

模型确认：
你指定了 qwen-plus，但应用的实际配置可能覆盖此参数。如果应用内部已绑定其他模型，API 会优先使用应用配置的模型。

调试：
如果请求失败，检查 response.text 中的错误信息，或在 payload 中添加 "debug": {"verbose": true} 获取更多日志。

文档参考：
更多细节可参考阿里云官方文档：调用应用 API。
https://help.aliyun.com/zh/model-studio/what-is-model-studio





QwQ 模型介绍
商业版模型
基于 Qwen2.5 模型训练的 QwQ 推理模型，通过强化学习大幅度提升了模型推理能力。模型数学代码等核心指标（AIME 24/25、LiveCodeBench）以及部分通用指标（IFEval、LiveBench等）达到DeepSeek-R1 满血版水平。相较于开源版，商业版具有最新的能力和改进。


qwq-plus-2025-03-05

又称qwq-plus-0305
快照版

开源版模型
基于 Qwen2.5-32B 模型训练的 QwQ 推理模型，于2025年3月6日发布。通过强化学习大幅度提升了模型推理能力。模型数学代码等核心指标（AIME 24/25、LiveCodeBench）以及部分通用指标（IFEval、LiveBench等）达到DeepSeek-R1 满血版水平，各指标均显著超过同样基于 Qwen2.5-32B 的 DeepSeek-R1-Distill-Qwen-32B。


模型名称

上下文长度

最大输入

最大思维链长度

最大回复长度

输入成本

输出成本

免费额度

（注）

（Token数）

（每千Token）

qwq-32b

131,072

98,304

32,768

8,192

0.002元

0.006元

100万 Token

有效期：百炼开通后180天内

并发限流请参考限流。
快速开始
API 使用前提：已获取API Key并完成配置API Key到环境变量。如果通过SDK调用，需要安装 OpenAI 或 DashScope SDK（DashScope Java SDK 版本需要不低于2.18.2）。

重要
QwQ 模型当前仅支持通过流式输出方式调用。

如果您使用 DashScope 方式调用 QwQ 模型：

incremental_output 参数默认为 true，且不支持设置为 false，仅支持增量流式返回；

response_format参数默认为"message"。

OpenAI兼容DashScope
PythonNode.jsHTTP
示例代码
 
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用百炼API Key替换：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复

# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qwq-32b",  # 此处以 qwq-32b 为例，可按需更换模型名称
    messages=[
        {"role": "user", "content": "9.9和9.11谁大"}
    ],
    # QwQ 模型仅支持流式输出方式调用
    stream=True,
    # 解除以下注释会在最后一个chunk返回Token使用量
    # stream_options={
    #     "include_usage": True
    # }
)

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
返回结果
 
====================思考过程====================

嗯，用户问的是9.9和9.11谁大。首先我要确定这两个数字的具体含义，因为有时候在不同的上下文中可能会有不同的解释。不过通常来说，这里的数字应该是指十进制的小数，也就是数学上的数值比较。

首先，我需要比较这两个小数的大小。9.9和9.11。先看整数部分，都是9，所以整数部分相同。接下来比较小数部分。小数点后的第一位，9.9的小数点后第一位是9，而9.11的小数点后第一位是1。这时候，9比1大，所以9.9的小数部分在第一位就已经更大了，那么整个数自然更大。不过，可能有人会疑惑，因为9.11的小数点后有两位，而9.9只有两位？或者说是不是应该补零来比较？

比如，9.9可以写成9.90，而9.11是9.11，这样比较的话，第二位小数的话，9.90的第二位是0，而9.11的是1，这时候第二位的话，0比1小。不过这时候第一位已经分出胜负了，第一位9比1大，所以不管后面的小数位如何，第一位已经决定了。因此，9.9比9.11大。

不过，也有可能用户在这里的写法有其他意思，比如9.9和9.11可能指的是日期，比如9月9日和9月11日，这样的话比较的话，9.11会更大，因为11日比9日晚。但通常数字比较的话，如果没有特别说明是日期的话，应该按数值来比较。不过用户的问题用的是“谁大”，也就是数值大小，而不是日期先后，所以应该还是数值比较。

再仔细检查一遍，9.9和9.11的数值比较：

9.9 = 9 + 0.9 = 9.900...

9.11 = 9 + 0.11 = 9.110...

比较的时候，先比较整数部分，都是9，相同。然后比较小数点后的第一位，0.9的十分位是9，而0.11的十分位是1，所以9.9的十分位更大，因此整个数更大。后面的百分位虽然9.11有1，但因为十分位已经分出高下了，所以不影响结果。

所以结论应该是9.9比9.11大。不过可能有人会因为小数点后的位数不同而产生混淆，比如认为9.11有两位小数，所以更精确或者数值更大，但其实不是的，数值的大小不取决于小数点后的位数，而是每一位的数值比较。

比如，比如比较1.5和1.499，虽然1.499有三位小数，但数值上还是小于1.5。同理，9.9虽然写成一位小数，但等价于9.90，所以比9.11大。

不过，也有可能用户在这里的写法有其他意思，比如货币单位？比如9.9元和9.11元，这时候同样是9.9元更多。或者其他的上下文，但如果没有特别说明的话，应该按数值比较。

所以最终结论是9.9比9.11大。不过，为了确保正确，再举个例子，比如用分数来比较：

9.9 = 99/10 = 9.9

9.11 = 911/100 = 9.11

将它们通分比较：

99/10 = 990/100

911/100 = 911/100

显然，990 > 911，所以9.9更大。

这样确认下来，答案应该是9.9更大。不过用户可能在输入时有笔误，或者有其他意图，但按照常规数学比较的话，结论应该是正确的。
====================完整回复====================

9.9比9.11大。以下是详细分析：

1. **整数部分比较**：  
   两个数的整数部分均为 **9**，因此整数部分相等。

2. **小数部分比较**：  
   - **第一位小数**：  
     9.9 的小数点后第一位是 **9**，而 9.11 的小数点后第一位是 **1**。  
     **9 > 1**，因此仅凭这一位即可判断 **9.9 > 9.11**。

   - **后续小数位**（补充说明）：  
     即使补零为相同位数（如 9.9 = 9.90），比较第二位小数时：  
     - 9.90 的第二位是 **0**，而 9.11 的第二位是 **1**。  
     但此时第一位小数已分出胜负，后续位数不影响最终结果。

3. **分数形式验证**：  
   - 9.9 = \( \frac{99}{10} = \frac{990}{100} \)  
   - 9.11 = \( \frac{911}{100} \)  
   显然，\( 990 > 911 \)，因此 **9.9 > 9.11**。

**结论**：  
在数值大小比较中，**9.9 大于 9.11**。
多轮对话
QwQ 模型 API 默认不会记录您的历史对话信息。多轮对话功能可以让大模型“拥有记忆”，满足如追问、信息采集等需要连续交流的场景。您在使用 QwQ 模型时，会接收到reasoning_content字段（思考过程）与content（回复内容），您可以将content字段通过{'role': 'assistant', 'content':拼接后的流式输出content}添加到上下文，无需添加reasoning_content字段。

OpenAI兼容DashScope
您可以通过 OpenAI SDK 或 OpenAI 兼容的 HTTP 方式使用多轮对话功能。

PythonNode.jsHTTP
示例代码
 
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用百炼API Key替换：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复

messages = []
conversation_idx = 1
while True:
    print("="*20+f"第{conversation_idx}轮对话"+"="*20)
    conversation_idx += 1
    user_msg = {"role": "user", "content": input("请输入你的消息：")}
    messages.append(user_msg)
    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model="qwq-32b",  # 此处以 qwq-32b 为例，可按需更换模型名称
        messages=messages,
        # QwQ 模型仅支持流式输出方式调用
        stream=True
    )
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    for chunk in completion:
        # 如果chunk.choices为空，则打印usage
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
        else:
            delta = chunk.choices[0].delta
            # 打印思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                print(delta.reasoning_content, end='', flush=True)
                reasoning_content += delta.reasoning_content
            else:
                # 开始回复
                if delta.content != "" and is_answering is False:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                    is_answering = True
                # 打印回复过程
                print(delta.content, end='', flush=True)
                answer_content += delta.content
    messages.append({"role": "assistant", "content": answer_content})
    print("\n")
    # print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
    # print(reasoning_content)
    # print("=" * 20 + "完整回复" + "=" * 20 + "\n")
    # print(answer_content)
Function Calling（工具调用）
QwQ 模型在回答需要实时信息的问题时效果不佳。您可以使用 Function Calling 功能，通过引入外部工具，使得 QwQ 模型可以与外部世界进行交互。

QwQ 模型会在思考完成后进行工具调用信息的输出，tool_choice参数只支持设置为"auto"（默认值，表示由模型自主选择工具）或"none"（强制模型不选择工具）。
OpenAI兼容DashScope
PythonNode.jsHTTP
示例代码
 
import os
from openai import OpenAI

# 初始化OpenAI客户端，配置阿里云DashScope服务
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 从环境变量读取API密钥
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 定义可用工具列表
tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}  # 无需参数
        }
    },  
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {  
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]  # 必填参数
            }
        }
    }
]

# 定义问题，请不要设置 System Message
messages = [{"role": "user", "content": input("请输入问题：")}]
completion = client.chat.completions.create(
    model="qwq-plus",  # 此处以qwq-plus为例，可更换为其它qwq模型
    messages=messages,
    tools=tools,
    parallel_tool_calls=True,
    stream=True,
    # 解除注释后，可以获取到token消耗信息
    # stream_options={
    #     "include_usage": True
    # }
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
tool_info = []          # 存储工具调用信息
is_answering = False   # 判断是否结束思考过程并开始回复
print("="*20+"思考过程"+"="*20)
for chunk in completion:
    if not chunk.choices:
        # 处理用量统计信息
        print("\n"+"="*20+"Usage"+"="*20)
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 处理AI的思考过程（链式推理）
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
            reasoning_content += delta.reasoning_content
            print(delta.reasoning_content,end="",flush=True)  # 实时输出思考过程
            
        # 处理最终回复内容
        else:
            if not is_answering:  # 首次进入回复阶段时打印标题
                is_answering = True
                print("\n"+"="*20+"回复内容"+"="*20)
            if delta.content is not None:
                answer_content += delta.content
                print(delta.content,end="",flush=True)  # 流式输出回复内容
            
            # 处理工具调用信息（支持并行工具调用）
            if delta.tool_calls is not None:
                for tool_call in delta.tool_calls:
                    index = tool_call.index  # 工具调用索引，用于并行调用
                    
                    # 动态扩展工具信息存储列表
                    while len(tool_info) <= index:
                        tool_info.append({})
                    
                    # 收集工具调用ID（用于后续函数调用）
                    if tool_call.id:
                        tool_info[index]['id'] = tool_info[index].get('id', '') + tool_call.id
                    
                    # 收集函数名称（用于后续路由到具体函数）
                    if tool_call.function and tool_call.function.name:
                        tool_info[index]['name'] = tool_info[index].get('name', '') + tool_call.function.name
                    
                    # 收集函数参数（JSON字符串格式，需要后续解析）
                    if tool_call.function and tool_call.function.arguments:
                        tool_info[index]['arguments'] = tool_info[index].get('arguments', '') + tool_call.function.arguments
            
print(f"\n"+"="*19+"工具调用信息"+"="*19)
if not tool_info:
    print("没有工具调用")
else:
    print(tool_info)
返回结果
输入“四个直辖市的天气”，得到以下返回结果：

 
请输入问题：四个直辖市的天气
====================思考过程====================
好的，用户问的是四个直辖市的天气。首先，我需要明确中国的四个直辖市分别是哪几个。北京、上海、天津和重庆，对吧？所以用户需要这四个城市的天气情况。

接下来，我需要调用获取天气的函数get_current_weather，每个城市都要单独查询。不过这个函数每次只能查询一个地点，所以得分别调用四次。首先，我应该检查函数的参数是否需要其他信息，但根据描述，参数只需要location，类型是字符串，比如城市名。所以应该没问题。

然后，我需要确保每个城市的名称正确。比如北京应该用“北京市”，上海是“上海市”，天津是“天津市”，重庆的话可能是“重庆市”或者直接“重庆”，但为了统一，可能用全称更好。用户可能希望得到每个城市的当前天气，所以需要依次调用四次函数。

不过，用户可能希望一次性得到所有四个直辖市的天气，但根据工具的限制，可能需要多次调用。这时候可能需要分四次调用，然后把结果汇总。所以在回复里，我应该生成四个tool_call，每个对应一个城市。

另外，还要注意用户是否可能有其他意图，比如是否只需要今天的天气还是未来几天的？不过根据问题描述，函数是获取当前天气，所以应该没问题。不需要额外处理。

最后，确保每个tool_call的格式正确，参数正确，名称正确。然后按顺序生成四个调用，这样用户就能得到所有四个直辖市的天气数据了。
====================回复内容====================

===================工具调用信息===================
[{'id': 'call_0bfdb95b784e46fab218c0', 'name': 'get_current_weather', 'arguments': '{"location": "北京市"}'}, {'id': 'call_9631576c3ccd419f8d8bc7', 'name': 'get_current_weather', 'arguments': '{"location": "上海市"}'}, {'id': 'call_d862b1bfe8374d2d97f508', 'name': 'get_current_weather', 'arguments': '{"location": "天津市"}'}, {'id': 'call_7222cdcc3cd04c839f2427', 'name': 'get_current_weather', 'arguments': '{"location": "重庆市"}'}]
在得到 Function Calling 输出的工具信息后，您可以参考运行工具函数与大模型总结工具函数输出，使大模型能够根据工具运行的结果进行回答。

注意事项
不支持的功能与参数

不支持的功能

结构化输出、前缀续写、上下文缓存

不支持的参数

temperature、top_p、presence_penalty、frequency_penalty、logprobs、top_logprobs

设置这些参数都不会生效，即使没有输出错误提示。
为了达到模型的最佳推理效果，不建议设置 System Message。

我的应用：工作流应用已支持QwQ模型；智能体应用已支持QwQ模型（不包括插件、流程、音视频交互能力 ）。

模型在线体验：支持体验 QwQ 模型。

常见问题
Q：怎么关闭思考过程？
A：无法关闭，QwQ 模型的推理模式是先输出思考内容，再输出回复内容。

Q：免费额度用完后如何购买 Token？
A：您可以访问费用与成本中心进行充值，确保您的账户没有欠费即可调用 QwQ 模型。

超出免费额度后，调用 QwQ 模型会自动扣费，出账周期为一小时，消费明细请前往账单详情进行查看。
Q：如何接入Chatbox或Cherry Studio？
A：请根据您的使用情况参考以下步骤：

此处以使用较多的工具为例，其它大模型工具接入的方法较为类似。
Dify 云服务暂时不支持接入 QwQ 模型。
ChatboxCherry Studio
在设置界面的模型提供方选择添加自定义提供方。

image.png

进行 API 设置

名称输入“阿里云”（可自定义）；

API 域名输入https://dashscope.aliyuncs.com/compatible-mode/v1；

API 路径输入/chat/completions；

API 密钥输入您的 API Key，获取方法请参见：获取API Key；

模型输入您需要使用的 QwQ模型，此处以 qwq-plus 为例（请注意字母的大小写）；

单击保存，完成设置。

image.png

进行对话测试

在输入框输入“你是谁？”进行测试：

image.png

Q：可以上传图片或文档进行提问吗？
A：QwQ 模型仅支持文本输入，不支持输入图片或文档。通义千问VL模型支持图片输入，Qwen- Long模型支持文档输入。

Q：如何在使用 LangChain 时输出思考过程？
A：请参考以下步骤：

更新依赖库

确保 langchain_community 和 dashscope 为最新版本：

 
pip install -U langchain_community dashscope
调用 QwQ 模型

QwQ 模型目前仅支持流式输出，通过以下代码来分开打印“思考过程”与“回复内容”：

 
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage

chatLLM = ChatTongyi(
    model="qwq-plus",   # 此处以qwq-plus为例，您可按需更换模型名称。
)
completion = chatLLM.stream([HumanMessage(content="你是谁")])
is_answering = False
print("="*20+"思考过程 "+"="*20)
for chunk in completion:
    if chunk.additional_kwargs.get("reasoning_content"):
        print(chunk.additional_kwargs.get("reasoning_content"),end="",flush=True)
    else:   
        if not is_answering:
            print("\n"+"="*20+"回复内容"+"="*20)
            is_answering = True
        print(chunk.content,end="",flush=True)
可以获得如下输出：

 
====================思考过程 ====================
嗯，用户问我“你是谁”，我需要先确定他们想了解什么。可能他们刚接触我的时候，或者想确认我的身份。首先，我应该简要介绍自己是通义千问，阿里巴巴集团旗下的超大规模语言模型。然后说明我的功能，比如回答问题、创作文字、编程等，这样用户知道我能做什么。还要提到我支持多语言，这样用户知道语言不是障碍。接下来，可能需要解释我的应用场景，比如写故事、写公文、写邮件、写剧本等，这样用户能具体了解我的用途。还要提到我的训练数据截止时间，这样用户知道我的知识更新到什么时候。最后，邀请用户提问，保持友好和开放的态度。需要确保回答简洁明了，信息全面，同时口语化，避免使用专业术语。可能用户是普通用户，不需要太技术性的解释。还要注意不要遗漏关键点，比如我的研发公司、功能、多语言支持、应用场景和训练时间。检查有没有重复或冗余的信息，确保流畅自然。可能用户还想知道如何与我互动，所以最后的邀请提问很重要。总之，结构应该是先介绍身份，再功能，应用场景，训练数据，最后邀请提问。这样用户能快速获取所需信息，并知道下一步该怎么做。
====================回复内容====================
你好！我是通义千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。

我的训练数据截止时间是2024年12月，这意味着我对2024年之前的信息有较好的了解，但对之后发生的事情可能不了解。如果你有