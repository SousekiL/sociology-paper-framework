# 文献资料库维护

`library/article-metadata.jsonl` 保存期刊公开元数据与可获得摘要，不保存论文全文。它服务于两类任务：识别近期的理论/方法线索，以及为用户明确要求的文献阅读提供入口。

## 增量规则

- 记录以 DOI（无 DOI 时以来源、日期、题名）去重；新记录只能追加。
- 既有 JSONL 行永不被新扫描改写或删除；更新状态单独保存在 `library/state.json`。
- 每周任务扫描近 183 天的新记录，并为每个自动化来源新增一个更早的 183 天窗口。
- 连续四个历史窗口没有结果时，来源被标记为自动可获取历史暂时耗尽；这不是“期刊没有更早文献”的声明。

## 来源边界

Crossref 可自动收集 ASR、*Social Problems*、*The British Journal of Sociology*、*Chinese Sociological Review*、AER、*Econometrica*、JASA 与 *Sociological Methods & Research* 的元数据。

《社会学研究》《社会》和 *Chinese Journal of Sociology* 的官网目录被保留在 `library/manual-review-queue.md`。它们不稳定地暴露开放结构化元数据，因此需要人工核对再追加，不能伪装为自动抓取完成。

## 操作

```bash
python3 scripts/update_literature_library.py --mode current
python3 scripts/update_literature_library.py --mode weekly
python3 scripts/update_literature_library.py --mode history --batches 12
```

定时更新由 `.github/workflows/update-library.yml` 执行。它只提交 `library/` 下的新增资料和状态信息。
