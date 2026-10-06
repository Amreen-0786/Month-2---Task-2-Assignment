from pathlib import Path
from level2.task_3_log_analyzer.log_analyzer import analyze_file

def test_log_analysis():
    log = Path(__file__).parents[1] / "level2" / "task_3_log_analyzer" / "sample.log"
    result = analyze_file(log)

    assert result["ip_counts"]["10.0.0.5"] == 3
    assert result["method_counts"]["GET"] == 5
    assert result["status_counts"]["200"] == 4
    assert len(result["error_lines"]) == 3
    assert result["login_attempts"] == 2
