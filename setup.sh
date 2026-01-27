#!/bin/bash

# =========================================================================
#        TERMOS ARCHITECT EDITION - GITHUB DEPLOYMENT SCRIPT
# =========================================================================

echo ">>> INITIALIZING TERMOS ARCHITECT DEPLOYMENT..."
echo " "

# 1. CREATE .NOJEKYLL FILE
# This tells GitHub to NOT run Jekyll (Ruby) and just serve the HTML/JS.
echo ">>> CREATING .NOJEKYLL FLAG..."
touch .nojekyll

# 2. GIT INITIALIZATION
# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo ">>> INITIALIZING GIT REPOSITORY..."
    git init
else
    echo ">>> GIT REPOSITORY ALREADY EXISTS."
fi

# 3. STAGE ALL FILES
echo ">>> STAGING FILES (index.html, style.css, script.js)..."
git add .

# 4. COMMIT
echo ">>> COMMITTING CHANGES..."
git commit -m "Deploy TermOS Architect Edition"

# 5. SET REMOTE (You will need to paste your URL here)
# IMPORTANT: Replace 'YOUR_REPO_URL_HERE' with your actual GitHub URL.
# Example: https://github.com/YOUR_USERNAME/termos.git

REPO_URL="YOUR_REPO_URL_HERE"

if [ "$REPO_URL" = "YOUR_REPO_URL_HERE" ]; then
    echo " "
    echo "⚠ WARNING: You need to edit this script first!"
    echo "   Open setup.sh and change 'YOUR_REPO_URL_HERE' to your actual GitHub URL."
    echo "   Then run: bash setup.sh"
else
    # Check if remote exists, if not add it. If yes, update it.
    git remote get-url origin > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        git remote set-url origin $REPO_URL
        echo ">>> UPDATING REMOTE ORIGIN..."
    else
        git remote add origin $REPO_URL
        echo ">>> ADDING REMOTE ORIGIN..."
    fi

    # 6. PUSH
    echo ">>> PUSHING TO GITHUB (MAIN BRANCH)..."
    git branch -M main
    git push -u origin main

    echo " "
    echo "✅ DEPLOYMENT COMPLETE!"
    echo "   Go to GitHub Settings > Pages to ensure your site is live."
fi
