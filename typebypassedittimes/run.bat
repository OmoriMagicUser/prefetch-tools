@echo off
TITLE crypto detector
color 4
for /f %%A in ('"prompt $H &echo on &for %%B in (1) do rem"') do set BS=%%A
echo.
echo.
echo.
echo.
echo                     enter path to winprefetchview
echo.
set /p choice=.%BS%         -^> 

cls

@echo off
echo.
echo.
echo.
echo.
echo                     enter path to run.bat folder
echo.
set /p choice2=.%BS%         -^> 
cd %choice%
WinPrefetchView.exe /scomma %choice2%\prefetch_data.csv

cd %choice2%
cls
python typebypassprefetch.py