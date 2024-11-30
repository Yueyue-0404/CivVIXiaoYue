@echo off

echo Installing lxml...
pip install lxml -i https://mirrors.aliyun.com/pypi/simple/
if %errorlevel% neq 0 (
    echo Failed to install lxml, exiting.
    exit /b 1
)

echo Installing pypinyin...
pip install pypinyin -i https://mirrors.aliyun.com/pypi/simple/
if %errorlevel% neq 0 (
    echo Failed to install pypinyin, exiting.
    exit /b 1
)

echo Installing fuzzywuzzy...
pip install fuzzywuzzy -i https://mirrors.cloud.tencent.com/pypi/simple
if %errorlevel% neq 0 (
    echo Failed to install fuzzywuzzy, exiting.
    exit /b 1
)

echo Installing python-Levenshtein...
pip install python-Levenshtein -i https://mirrors.cloud.tencent.com/pypi/simple
if %errorlevel% neq 0 (
    echo Failed to install python-Levenshtein, exiting.
    exit /b 1
)

echo Installing qq-botpy...
pip install qq-botpy -i https://mirrors.cloud.tencent.com/pypi/simple
if %errorlevel% neq 0 (
    echo Failed to install qq-botpy, exiting.
    exit /b 1
)

echo Installing ordered-set...
pip install ordered-set -i https://mirrors.cloud.tencent.com/pypi/simple
if %errorlevel% neq 0 (
    echo Failed to install qq-botpy, exiting.
    exit /b 1
)

echo "ordered-set installed successfully."




echo All packages installed successfully!
pause
exit /b 0