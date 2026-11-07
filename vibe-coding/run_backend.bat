@echo off
chcp 65001 > nul
echo ========================================================
echo        در حال اجرای سرور بک‌اند شعرخونه (Django DRF)
echo ========================================================
echo.
set PYTHONIOENCODING=utf-8
"..\SherKhane\.venv\Scripts\python.exe" backend\manage.py runserver 127.0.0.1:8000
pause
