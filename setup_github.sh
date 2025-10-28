#!/bin/bash

# GitHub Repository Setup Script
# This script helps you set up the GitHub repository for the FHIR Imaging Report project

echo "🚀 Setting up GitHub repository for FHIR Imaging Report project"
echo "=============================================================="

# Repository details
REPO_NAME="sub-team-imaging-report-model"
REPO_DESCRIPTION="Xt-EHR T7.2 Sub-team analysis of imaging report elements for basic vs beyond basic classification"

echo ""
echo "📋 Repository Information:"
echo "Name: $REPO_NAME"
echo "Description: $REPO_DESCRIPTION"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository!"
    echo "Run 'git init' first."
    exit 1
fi

echo "✅ Git repository detected"

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Let's commit them first:"
    git status --short
    echo ""
    read -p "Commit these changes? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Add GitHub deployment configuration and documentation

- Add GitHub Actions workflow for testing and documentation deployment
- Create deployment guide for GitHub-friendly platforms (Railway, Render, Vercel)
- Add Procfile and railway.json for easy deployment
- Set up automatic GitHub Pages deployment for documentation
- Remove Heroku-specific files (organizational security requirements)"
        echo "✅ Changes committed"
    else
        echo "Please commit your changes before continuing."
        exit 1
    fi
else
    echo "✅ No uncommitted changes"
fi

echo ""
echo "🔧 Next Steps:"
echo "1. Create a GitHub repository manually:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: $REPO_NAME"
echo "   - Description: $REPO_DESCRIPTION"
echo "   - Set to Public (for GitHub Pages)"
echo "   - DO NOT initialize with README (we have one)"
echo ""

echo "2. Add the GitHub remote:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
echo ""

echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

echo "4. Enable GitHub Pages:"
echo "   - Go to repository Settings → Pages"
echo "   - Source: GitHub Actions"
echo "   - The workflow will automatically deploy documentation"
echo ""

echo "5. Optional - Deploy Flask app:"
echo "   - Railway: https://railway.app (connect GitHub repo)"
echo "   - Render: https://render.com (connect GitHub repo)"
echo "   - See DEPLOYMENT.md for detailed instructions"
echo ""

echo "📁 Files created for GitHub deployment:"
echo "   - .github/workflows/deploy.yml (GitHub Actions)"
echo "   - DEPLOYMENT.md (deployment guide)"
echo "   - Procfile (for Railway/Render)"
echo "   - railway.json (Railway configuration)"
echo ""

echo "🎉 Setup complete! Follow the next steps to push to GitHub."

# Optionally show the git commands to run
echo ""
echo "📋 Quick command reference:"
echo "git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
echo "git branch -M main"
echo "git push -u origin main"