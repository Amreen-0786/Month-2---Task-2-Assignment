from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def create_report(input_csv: Path, output_pdf: Path, title: str) -> None:
    rows = read_csv(input_csv)
    if not rows:
        raise ValueError("The CSV file contains no data.")

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    story = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 5 * mm),
        Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"],
        ),
        Spacer(1, 4 * mm),
        Paragraph(f"Total records: {len(rows)}", styles["Heading2"]),
        Spacer(1, 4 * mm),
    ]

    headers = list(rows[0].keys())
    data = [headers] + [[str(row.get(h, "")) for h in headers] for row in rows]

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.whitesmoke, colors.lightgrey]),
    ]))

    story.append(table)
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "Summary: This report was generated automatically from structured CSV data.",
        styles["Normal"],
    ))
    doc.build(story)

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a PDF report from CSV.")
    parser.add_argument("--input", default="sample_data.csv")
    parser.add_argument("--output", default="output/student_report.pdf")
    parser.add_argument("--title", default="Code-A-Nova Data Report")
    args = parser.parse_args()

    create_report(Path(args.input), Path(args.output), args.title)
    print(f"PDF report created: {Path(args.output).resolve()}")

if __name__ == "__main__":
    main()
