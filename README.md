# 社会学量化研究框架 Skill

[中文](README.md) · [English](README.en.md)

把一个社会学话题转化为可审查、可复现、适合期刊论文写作的**量化研究设计**。它不保存或复制原始论文；核心是方法、测量、数据选择、识别和诊断的规范库。

## 它会产出什么

- 明确的研究问题、理论机制、可证伪假设与竞争解释；
- 合适的结论强度：描述、关联、机制或因果，而不是把回归自动说成因果；
- 变量字典：构念、待核验题项、编码、缺失、参照组、替代测量；
- 中国数据建议：CGSS、CFPS、CLDS、CHARLS、CHFS、CEPS、CHIP、统计年鉴等；
- 主模型、识别假设、诊断、稳健性、异质性、可复现与伦理要求；
- 条件性的结论边界，而非虚构研究发现。

## 内置规范库

`data/quantitative-reference-catalog.json` 有 260 张可检索卡片：

- 116 张方法与诊断卡；
- 108 张变量测量与编码卡；
- 20 个数据集卡；
- 16 项质量控制卡。

## 使用

将整个目录放入 Codex 的 skills 目录，或安装后调用：

```text
$sociology-paper-framework
主题：平台劳动者的社会关系如何影响职业流动？
```

技能会先读取与话题相关的方法、测量和数据卡，再按 `references/quantitative-output-template.md` 生成框架。具体题项、字段和数据许可必须以所选数据集代码本为准。

## 文献资料库：增量、可追溯、不覆盖

`library/` 保存的是文章的公开**元数据与公开摘要**，不是论文全文。更新脚本遵循追加与 DOI 去重规则：旧记录永不被新扫描替换；新记录只会丰富同一资料库。

- `scripts/update_literature_library.py --mode current`：导入截至今天的近六个月资料；
- `--mode weekly`：扫描最新资料，并为每一种来源向更早历史推进一个六个月窗口；
- `--mode history --batches 12`：手动连续补 12 个窗口；
- 每个来源连续四个历史窗口为空后才被标记为“可自动获取的历史已暂时耗尽”。

覆盖中国社会研究相关英文期刊、ASR、*Social Problems*、*The British Journal of Sociology*，并增加 *American Economic Review*、*Econometrica*、*Journal of the American Statistical Association* 和 *Sociological Methods & Research* 以吸收计量与统计方法前沿。中文《社会学研究》和《社会》保留官方目录入口及人工核验队列，因为其元数据并不稳定地进入开放 API。

## 每周更新

GitHub Actions 会在每周一运行一次，并在有新增元数据或状态变更时提交到 `main`。也可以在 Actions 页面手动触发。工作流不会删除历史记录。

## 验证

```bash
python3 scripts/build_quant_catalog.py
python3 scripts/validate_quant_catalog.py
python3 scripts/query_quant_catalog.py --topic '社会关系与职业流动'
python3 scripts/update_literature_library.py --mode current
```

## 边界

本项目提供研究设计和资料发现支持，不替代代码本核对、研究伦理审查、数据使用协议或实证分析。
