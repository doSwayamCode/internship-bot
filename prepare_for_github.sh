#!/bin/bash

echo "🚀 PREPARING FOR GITHUB DEPLOYMENT"
echo "=================================="

# Remove sensitive log files
echo "🧹 Cleaning up local files..."
rm -f *.log
rm -f batch.json
rm -f scheduler_state.json

# Create clean seen.json if it doesn't exist
if [ ! -f "seen.json" ]; then
    echo "{}" > seen.json
    echo "✅ Created empty seen.json"
fi

echo ""
echo "✅ Project ready for GitHub deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Create GitHub repository"
echo "2. Upload all files to GitHub"
echo "3. Set up GitHub Secrets (see GITHUB_DEPLOYMENT_GUIDE.md)"
echo "4. Enable GitHub Actions"
echo ""
echo "📖 Full instructions in: GITHUB_DEPLOYMENT_GUIDE.md"
