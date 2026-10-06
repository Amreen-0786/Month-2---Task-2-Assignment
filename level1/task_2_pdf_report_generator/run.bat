@echo off
python "%~dp0pdf_report_generator.py" --input "%~dp0sample_data.csv" --output "%~dp0output\student_report.pdf"
pause
