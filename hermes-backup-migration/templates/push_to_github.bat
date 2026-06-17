@echo off
echo ========================================
echo Hermes Agent 配备份推送脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 推送 LFS 文件...
git lfs push origin %BRANCH_NAME% --all
if %errorlevel% neq 0 (
    echo LFS 推送失败！
    echo 可能原因: 网络问题、SSL错误、LFS配额不足
    pause
    exit /b 1
)

echo [2/3] 推送 Git 对象...
git push -u origin %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo Git 推送失败！
    pause
    exit /b 1
)

echo [3/3] 验证推送...
git ls-remote origin %BRANCH_NAME%

echo.
echo ========================================
echo 推送完成！
echo ========================================
pause
