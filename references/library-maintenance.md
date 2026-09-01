# Private Literature-Library Maintenance

`library/` is a private local directory ignored by Git. Never commit it, synchronize it to a public repository, or distribute it with the skill. It stores only local literature indexes and structured reading cards, never article PDFs or raw article text.

## Local update

```bash
python3 scripts/run_local_weekly_update.py
```

This command changes only the local `library/`. To enable open-access full-text review, set local `LLM_API_KEY` plus optional `LLM_BASE_URL` and `LLM_MODEL`. On macOS, the updater also checks the current user's Keychain items named `sociology-paper-framework-llm-api-key`, `sociology-paper-framework-llm-base-url`, and `sociology-paper-framework-llm-model`. Keep these values in an operating-system credential store or private environment configuration, never in Git.

The private library is append-only and deduplicated: new scans supplement existing records, state, and reading cards without replacing previous records.
