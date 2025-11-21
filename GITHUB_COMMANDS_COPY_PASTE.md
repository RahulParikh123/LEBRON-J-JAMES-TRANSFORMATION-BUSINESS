# Copy-Paste Commands for GitHub Setup

**Copy these commands one at a time and paste them into Command Prompt**

---

## Step 1: Go to Your Project Folder

```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
```

**Paste this in Command Prompt and press Enter**

---

## Step 2: Configure Git Identity (REQUIRED!)

**⚠️ DO THIS FIRST! Replace YOUR_EMAIL and YOUR_NAME**

**Command 1** - Set email:
```bash
git config --global user.email "YOUR_EMAIL"
```

**Command 2** - Set name:
```bash
git config --global user.name "YOUR_NAME"
```

**Paste each command and press Enter**

---

## Step 3: Initialize Git

```bash
git init
```

**Paste this in Command Prompt and press Enter**

---

## Step 4: Add All Files

```bash
git add .
```

**Paste this in Command Prompt and press Enter**

---

## Step 5: Create First Commit

```bash
git commit -m "Initial commit: Enterprise Data Transformation Platform"
```

**Paste this in Command Prompt and press Enter**

---

## Step 6: Connect to GitHub

**⚠️ REPLACE `YOUR_USERNAME` WITH YOUR ACTUAL GITHUB USERNAME!**

```bash
git remote add origin https://github.com/YOUR_USERNAME/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS.git
```

**Example** (if your username is `rahul123`):
```bash
git remote add origin https://github.com/rahul123/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS.git
```

**Paste this in Command Prompt and press Enter**

---

## Step 7: Rename Branch

```bash
git branch -M main
```

**Paste this in Command Prompt and press Enter**

---

## Step 8: Push to GitHub

```bash
git push -u origin main
```

**Paste this in Command Prompt and press Enter**

**Note**: First time will ask you to log in to GitHub

---

## ✅ Done!

Go to GitHub.com and refresh - you should see all your files!

---

**Need help? See GITHUB_SETUP_STEP_BY_STEP.md for detailed instructions**

