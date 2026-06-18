@echo off
echo ================================
echo  KodeMerkezi Bot Kurulum Basliyor
echo ================================
echo.

echo [1/3] Python kuruluyor...
winget install -e --id Python.Python.3 --silent --accept-package-agreements --accept-source-agreements
echo.

echo [2/3] Git kuruluyor...
winget install -e --id Git.Git --silent --accept-package-agreements --accept-source-agreements
echo.

echo [3/3] Bot kutuphanesi kuruluyor...
pip install python-telegram-bot==20.7
echo.

echo ================================
echo  Kurulum tamamlandi!
echo  Simdi config.py dosyasini ac,
echo  token ve ID'ni gir, sonra:
echo  python bot.py
echo ================================
pause
