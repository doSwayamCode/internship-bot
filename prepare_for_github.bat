@echo off
echo 🚀 PREPARING FOR GITHUB DEPLOYMENT
echo ==================================

REM Remove sensitive log files
echo 🧹 Cleaning up local files...
if exist *.log del *.log
if exist batch.json del batch.json
if exist scheduler_state.json del scheduler_state.json

REM Create clean seen.json if it doesn't exist
if not exist seen.json (
    echo {} > seen.json
    echo ✅ Created empty seen.json
)

echo.
echo ✅ Project ready for GitHub deployment!
echo.
echo 📋 Next steps:
echo 1. Create GitHub repository
echo 2. Upload all files to GitHub
echo 3. Set up GitHub Secrets (see GITHUB_DEPLOYMENT_GUIDE.md)
echo 4. Enable GitHub Actions
echo.
echo 📖 Full instructions in: GITHUB_DEPLOYMENT_GUIDE.md
echo.
pause
