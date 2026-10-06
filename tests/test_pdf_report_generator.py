from level1.task_2_pdf_report_generator.pdf_report_generator import create_report

def test_pdf_report_is_created(tmp_path):
    csv_file = tmp_path / "data.csv"
    pdf_file = tmp_path / "report.pdf"
    csv_file.write_text("Name,Marks\nA,95\nB,88\n", encoding="utf-8")

    create_report(csv_file, pdf_file, "Test Report")

    assert pdf_file.exists()
    assert pdf_file.stat().st_size > 500
