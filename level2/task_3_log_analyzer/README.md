# Log Analyzer Tool

The task sheet asks for a tool that reads system/server logs and extracts useful information such as error counts, frequent IP addresses, login attempts, and request patterns. It also suggests filters and exported summaries. fileciteturn0file0L95-L105

## Run

```powershell
python log_analyzer.py --input sample.log
```

Only errors:

```powershell
python log_analyzer.py --input sample.log --errors-only
```

A CSV summary is written to `output/log_summary.csv`.
