from __future__ import annotations

import argparse
import csv
import shutil
from datetime import datetime
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Presentations": {".ppt", ".pptx"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".sql"},
}

def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Others"

def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1

def organize_directory(folder: Path, log_file: Path) -> int:
    folder = folder.expanduser().resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Directory not found: {folder}")

    log_file.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        if item.resolve() == log_file.resolve():
            continue

        category = category_for(item)
        target = folder / category
        target.mkdir(exist_ok=True)
        destination = unique_destination(target / item.name)
        shutil.move(str(item), str(destination))

        rows.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "source": str(item),
            "destination": str(destination),
            "category": category,
        })

    with log_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["timestamp", "source", "destination", "category"],
        )
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)

def main() -> None:
    parser = argparse.ArgumentParser(description="Organize files by type.")
    parser.add_argument("folder", nargs="?", help="Folder to organize")
    parser.add_argument("--log", default="organization_log.csv")
    args = parser.parse_args()

    folder = Path(args.folder) if args.folder else Path(
        input("Enter the folder path to organize: ").strip()
    )
    log = Path(args.log)
    if not log.is_absolute():
        log = folder / log

    try:
        count = organize_directory(folder, log)
        print(f"Done. Organized {count} file(s).")
        print(f"Log saved to: {log.resolve()}")
    except Exception as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
