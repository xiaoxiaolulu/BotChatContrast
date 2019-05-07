
### 项目简介
[![Build Status](https://travis-ci.org/xiaoxiaolulu/BotChatContrast.svg?branch=master)](https://travis-ci.org/xiaoxiaolulu/BotChatContrast)

BotChatContrast 是一款以Excel进行用例维护的聊天机器人文本回复对比小工具

#### 项目安装及使用
```text
1. 进入项目根目录执行 pip install -r requirements.txt 安装依赖库
2. 项目运行, 根目录执行python run.py 进行运行
3. 进行完程序进入report查看html报告, 测试报告根据运行的测试用例名生成对应名字的html文件
```


##### 报告详情修改
```text
如需改变报告详情内容 -》进入lib/templates修改index.html, 修改一下代码，源码如下
<table border="1" width="100%">
    <tr>
        <th>test_id</th>
        <th>test_question</th>
        <th>test_intent</th>
        <th>test_response</th>
        <th>test_diff</th>
        <th>test_result</th>
    </tr>
    {% for res in results %}
    <tr id="TestResultRep">
        <th>{{ loop.index }}</th>
        <th>{{ res.question}}</th>
        <th>{{res.indent}}</th>
        <th>{{res.response}}</th>
        <th>{{res.diff}}</th>
        <th class="Res">{{res.result}}</th>
    </tr>
    {% endfor %}
</table>
```

##### 需要对比API编写
使用Yaml文件管理，需要回答问题使用动态${question}$传参，其余根据下方模板编写具体入参信息
```text
# 聊天机器人对比的接口, yaml 管理，支持动态传参${val}$
method: post
url: https://192.168.1.104:10033/api/admin/channel/v2/webchat/getanswer
json:
  id: 8e0b6707-bcc6-4c4c-b072-80b169003804
  webtalkid: 4f0cd4fb1c1a4da9a0876ec0f5cd49ba
  question: ${question}$
  channels: WebChat
headers:
  Access-Token: A36141128D6466F1055AB47FC9E7A0E5A318B2B665A868A86D103E3D28BDDA88
  Content-Type: application/json
```
