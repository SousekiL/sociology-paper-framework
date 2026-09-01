# 社会学量化研究框架 Skill

[中文](README.md) · [English](README.en.md)

把任意社会学话题转化为面向期刊论文的、可执行的**量化研究设计**。默认中文输出，也可要求英文。

## 你会得到什么

- 研究问题、理论机制、可证伪假设与竞争解释；
- 清楚区分描述、关联、机制与因果的结论边界；
- 变量字典：构念、编码、缺失处理、参照组和替代测量；
- 适合中国议题的数据建议，如 CGSS、CFPS、CLDS、CHARLS、CHFS、CEPS、CHIP 和统计年鉴；
- 主模型、识别假设、诊断、稳健性和异质性检验；
- 一份能直接扩展为论文大纲的研究设计，而不是虚构的实证结果。

## 使用

### 第一步：安装

打开并安装这个 skill：[Socpaper 安装页](https://github.com/SousekiL/sociology-paper-framework)。也可以直接下载：[ZIP 安装包](https://github.com/SousekiL/sociology-paper-framework/archive/refs/heads/main.zip)。

它适合支持自定义 Skill、Agent 或提示词包的工具。导入或复制**完整文件夹**，然后新开一个对话即可使用。不同工具的导入按钮或文件夹位置会不同，但不需要配置 API Key 才能生成研究框架。

常见选择包括：

- Codex、Claude Code、Hermes Agent 等支持本地 Skill 的 Agent 工具；
- [WorkBuddy](https://www.workbuddy.cn/work/)：可使用自定义 Skills；
- [扣子 Coze](https://docs.coze.cn/)：新建智能体后，将本 skill 的说明作为“人设与回复逻辑”，需要时再配置工作流；
- [Dify](https://docs.dify.ai/)：新建聊天助手或 Agent，把 `SKILL.md` 的说明放入系统提示词，并按需添加知识库；
- [FastGPT](https://doc.fastgpt.cn/)：新建对话 Agent 或工作流，将核心说明放入系统配置。

不同平台未必支持直接导入同一种 Skill 文件夹；遇到这种情况，请保留整个文件夹作为参考，并优先复制 `SKILL.md` 的内容到该平台的系统提示词或 Agent 指令区。

### 第二步：输入命令

只需记住一个命令：`/socpaper`。在命令后加入一个模式关键词，再写你的话题；不写关键词时默认 `paper`。

```text
/socpaper paper 社会关系如何影响平台劳动者的职业流动？
/socpaper method 社会关系与职业流动
/socpaper theory 数字平台中的社会关系发展
/socpaper review 中国青年就业中的社会资本
```

| 关键词 | 用途 | 最适合的输入 |
| --- | --- | --- |
| `paper` | 完整量化论文框架 | 话题或研究问题 |
| `method` | 方法选择、识别与诊断 | 问题或关键词 |
| `theory` | 理论背景、机制与命题 | 话题或现象 |
| `review` | 既有研究脉络、争论与缺口 | 研究领域或关键词 |

四种模式均以模型本身的社会科学与方法知识为主；本机私有资料库只在真实可用时补充线索。它不会把不确定的记忆伪装成具体文献事实。

也可以直接指定更具体的目标：

```text
/socpaper paper 请用英文设计一项关于户籍身份与职业流动的因果识别研究；优先推荐可获得的中国面板数据。
```

该 skill 内置方法、测量、数据与质量控制规范。具体题项、字段、样本限制和数据许可仍须以数据代码本与使用协议为准。

## 隐私

公开仓库不包含任何个人文献库、文章全文、阅读卡、API 密钥或自动更新产生的数据。你可在自己的设备上维护私有资料库；它不会随 skill 安装、fork 或下载而分发。

## 边界

本项目提供研究设计支持，不替代数据清洗、代码本核对、研究伦理审查、数据使用协议或实际实证分析。
