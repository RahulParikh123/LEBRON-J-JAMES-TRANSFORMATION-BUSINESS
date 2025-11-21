# GitHub Setup - Step by Step (For Beginners)

Follow these steps exactly. I'll tell you where to paste each command.

---

## Step 1: Create GitHub Account (If You Don't Have One)

1. Go to: https://github.com
2. Click "Sign up" (top right)
3. Create your account (username, email, password)
4. Verify your email

**✅ Done? Move to Step 2**

---

## Step 2: Create the Repository on GitHub

1. **Go to GitHub.com** and log in
2. **Click the "+" icon** (top right corner)
3. **Click "New repository"**
4. **Fill in the form:**
   - **Repository name**: Type exactly: `LEBRON-J-JAMES-TRANSFORMATION-BUSINESS`
   - **Description** (optional): "Enterprise Data Transformation Platform"
   - **Visibility**: Choose "Private" (or "Public" if you want)
   - **DO NOT** check "Add a README file" (we already have one)
   - **DO NOT** check "Add .gitignore" (we already have one)
   - **DO NOT** choose a license (we already have one)
5. **Click the green "Create repository" button**

**✅ Done? You'll see a page with instructions. Move to Step 3**

---

## Step 3: Open Command Prompt (Windows)

**Where to run commands**: Windows Command Prompt or PowerShell

1. **Press Windows key + R**
2. **Type**: `cmd` and press Enter
   - OR type `powershell` and press Enter
3. **A black window opens** - this is where you'll paste commands

**✅ Done? Move to Step 4**

---

## Step 4: Navigate to Your Project Folder

**In the Command Prompt window**, type this and press Enter:

```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
```

**What this does**: Takes you to your project folder

**✅ Done? You should see the folder path in the prompt. Move to Step 5**

---

## Step 5: Configure Git Identity (REQUIRED FIRST!)

**⚠️ IMPORTANT**: You must do this BEFORE making a commit!

**In the Command Prompt**, paste these TWO commands (one at a time):

**Command 1** - Set your email (replace YOUR_EMAIL):
```bash
git config --global user.email "YOUR_EMAIL"
```

**Example**:
```bash
git config --global user.email "rahul@example.com"
```

**Press Enter**

**Command 2** - Set your name (replace YOUR_NAME):
```bash
git config --global user.name "YOUR_NAME"
```

**Example**:
```bash
git config --global user.name "Rahul Parikh"
```

**Press Enter**

**✅ Done? Move to Step 6**

---

## Step 6: Initialize Git

**In the Command Prompt**, paste this and press Enter:

```bash
git init
```

**What this does**: Sets up Git in your folder

**✅ You should see**: "Initialized empty Git repository..."

**✅ Done? Move to Step 7**

---

## Step 7: Add All Files to Git

**In the Command Prompt**, paste this and press Enter:

```bash
git add .
```

**What this does**: Tells Git to track all your files

**✅ Done? (No message is normal) Move to Step 7**

---

## Step 8: Create Your First Commit

**In the Command Prompt**, paste this and press Enter:

```bash
git commit -m "Initial commit: Enterprise Data Transformation Platform"
```

**What this does**: Saves all your files as the first version

**✅ You should see**: "X files changed, Y insertions..."

**✅ Done? Move to Step 8**

---

## Step 9: Connect to GitHub

**In the Command Prompt**, paste this and press Enter:

```bash
git remote add origin https://github.com/YOUR_USERNAME/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS.git
```

**⚠️ IMPORTANT**: Replace `YOUR_USERNAME` with your actual GitHub username!

**Example**: If your username is `rahul123`, it would be:
```bash
git remote add origin https://github.com/rahul123/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS.git
```

**What this does**: Connects your local folder to GitHub

**✅ Done? Move to Step 9**

---

## Step 10: Rename Branch to "main"

**In the Command Prompt**, paste this and press Enter:

```bash
git branch -M main
```

**What this does**: Names your branch "main" (GitHub's standard)

**✅ Done? Move to Step 10**

---

## Step 11: Push Everything to GitHub

**In the Command Prompt**, paste this and press Enter:

```bash
git push -u origin main
```

**What this does**: Uploads all your files to GitHub

**⚠️ FIRST TIME**: GitHub will ask you to log in:
- It might open a browser window
- OR ask for username/password in the command prompt
- Follow the prompts to authenticate

**✅ You should see**: "Enumerating objects...", "Writing objects...", "X objects pushed"

**✅ Done? Move to Step 11**

---

## Step 12: Verify It Worked!

1. **Go back to GitHub.com** in your browser
2. **Refresh the page** (F5 or click refresh)
3. **You should see all your files!**
   - README.md
   - src/ folder
   - docs/ folder
   - samples/ folder
   - Everything!

**✅ Success! Your code is on GitHub!**

---

## 🎉 You're Done!

Your repository is now live at:
```
https://github.com/YOUR_USERNAME/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS
```

**Share this link with your friend!**

---

## ❌ Troubleshooting

### Problem: "git is not recognized"
**Solution**: Git is not installed. Install it:
1. Go to: https://git-scm.com/download/win
2. Download and install Git for Windows
3. Restart Command Prompt
4. Try Step 5 again

### Problem: "Authentication failed"
**Solution**: 
1. GitHub might ask for a Personal Access Token instead of password
2. Go to: https://github.com/settings/tokens
3. Click "Generate new token (classic)"
4. Give it a name, check "repo" permission
5. Click "Generate token"
6. Copy the token and use it as your password when pushing

### Problem: "remote origin already exists"
**Solution**: 
```bash
git remote remove origin
```
Then do Step 8 again.

### Problem: "fatal: not a git repository"
**Solution**: You're in the wrong folder. Do Step 4 again.

---

## 📋 Quick Command Reference

Copy these in order (replace YOUR_USERNAME):

```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
git init
git add .
git commit -m "Initial commit: Enterprise Data Transformation Platform"
git remote add origin https://github.com/YOUR_USERNAME/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS.git
git branch -M main
git push -u origin main
```

---

**That's it! Follow these steps and you'll have your code on GitHub!** 🚀

