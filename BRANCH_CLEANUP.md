# 🌿 BRANCH CLEANUP GUIDE

## 🗑️ **Delete Unwanted Branch from GitHub**

### **Method 1: Command Line (Recommended)**

```bash
# Replace 'unwanted-branch-name' with the actual branch name
git push origin --delete unwanted-branch-name
```

### **Method 2: GitHub Web Interface**

1. Visit: https://github.com/doSwayamCode/internship-bpt
2. Click on "main" dropdown (branch selector)
3. You'll see all branches listed
4. Click the trash icon next to unwanted branch

### **Common Branch Names to Look For:**

- `development` or `dev`
- `feature/something`
- `gh-pages`
- `master` (if you switched to main)
- `old-main` or similar

### **After Deletion:**

```bash
# Clean up local references
git fetch --prune origin
```

### **Verify Only Main Branch Exists:**

```bash
git branch -a  # Should only show main
```

## 🎯 **Current Repository Status**

- Repository: https://github.com/doSwayamCode/internship-bpt
- Current Branch: main
- Local branches: main only
- Remote branches: main only (based on local fetch)

**If you can see the unwanted branch name on GitHub, just replace `unwanted-branch-name` in the delete command above!**
