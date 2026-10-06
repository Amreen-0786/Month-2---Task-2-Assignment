from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
METHOD_RE = re.compile(r"\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b")
STATUS_RE = re.compile(r"\s(\d{3})\s")

def analyze_file(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)

    ip_counts = Counter()
    method_counts = Counter()
    status_counts = Counter()
    error_lines = []
    login_attempts = 0

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if m := IP_RE.search(line):
                ip_counts[m.group()] += 1
            if m := METHOD_RE.search(line):
                method_counts[m.group()] += 1
            if m := STATUS_RE.search(line):
                status = m.group(1)
                status_counts[status] += 1
                if status.startswith(("4", "5")):
                    error_lines.append(line.rstrip())
            if re.search(r"\b(login|signin|authentication)\b", line, re.I):
                login_attempts += 1

    return {
        "total_lines": sum(status_counts.values()),
        "ip_counts": ip_counts,
        "method_counts": method_counts,
        "status_counts": status_counts,
        "error_lines": error_lines,
        "login_attempts": login_attempts,
    }

def export_summary(result: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total parsed status lines", result["total_lines"]])
        writer.writerow(["Login/authentication attempts", result["login_attempts"]])
        writer.writerow(["Error lines (4xx/5xx)", len(result["error_lines"])])
        writer.writerow([])
        writer.writerow(["Top IP", "Count"])
        writer.writerows(result["ip_counts"].most_common(10))
        writer.writerow([])
        writer.writerow(["HTTP Method", "Count"])
        writer.writerows(result["method_counts"].most_common())
        writer.writerow([])
        writer.writerow(["HTTP Status", "Count"])
        writer.writerows(sorted(result["status_counts"].items()))

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze server/system logs.")
    parser.add_argument("--input", default="sample.log")
    parser.add_argument("--errors-only", action="store_true")
    parser.add_argument("--output", default="output/log_summary.csv")
    args = parser.parse_args()

    result = analyze_file(Path(args.input))

    print(f"Parsed lines with HTTP status: {result['total_lines']}")
    print(f"Login/authentication attempts: {result['login_attempts']}")
    print(f"Error lines (4xx/5xx): {len(result['error_lines'])}")

    print("\nTop IP addresses:")
    for ip, count in result["ip_counts"].most_common(5):
        print(f"  {ip}: {count}")

    print("\nRequest methods:")
    for method, count in result["method_counts"].most_common():
        print(f"  {method}: {count}")

    print("\nStatus codes:")
    for status, count in sorted(result["status_counts"].items()):
        print(f"  {status}: {count}")

    if args.errors_only:
        print("\nError lines:")
        for line in result["error_lines"]:
            print(line)

    export_summary(result, Path(args.output))
    print(f"\nSummary exported to: {Path(args.output).resolve()}")

if __name__ == "__main__":
    main()
