@echo off
echo Installing PyInstaller...
python -m pip install pyinstaller
if errorlevel 1 goto error

echo Building File Organizer...
pyinstaller --onefile --name FileOrganizer level1\task_1_file_organizer\file_organizer.py
if errorlevel 1 goto error

echo Building PDF Report Generator...
pyinstaller --onefile --name PDFReportGenerator level1\task_2_pdf_report_generator\pdf_report_generator.py
if errorlevel 1 goto error

echo Building Log Analyzer...
pyinstaller --onefile --name LogAnalyzer level2\task_3_log_analyzer\log_analyzer.py
if errorlevel 1 goto error

echo.
echo SUCCESS. Check the dist folder for the .exe files.
pause
exit /b 0

:error
echo.
echo BUILD FAILED. Check the error above.
pause
exit /b 1
