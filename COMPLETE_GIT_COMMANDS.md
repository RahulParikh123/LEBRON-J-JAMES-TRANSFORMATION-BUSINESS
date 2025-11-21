# Complete Git Commands - Start to Finish

**Your Info:**
- Username: RahulParikh123
- Email: Rahul.Parikh.12345@gmail.com
- Project Folder: C:\Users\rahul\Downloads\data-transformation-platform

---

## Open Command Prompt

1. Press **Windows key + R**
2. Type: `cmd`
3. Press **Enter**

---

## Copy-Paste These Commands (One at a Time)

### Step 1: Go to Your Project Folder

```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
```

**Paste → Press Enter**

**✅ You should see**: The prompt changes to show the project folder path

---

### Step 2: Set Your Email

```bash
git config --global user.email "Rahul.Parikh.12345@gmail.com"
```

**Paste → Press Enter**

---

### Step 3: Set Your Name

```bash
git config --global user.name "RahulParikh123"
```

**Paste → Press Enter**

---

### Step 4: Initialize Git

```bash
git init
```

**Paste → Press Enter**

**✅ You should see**: "Initialized empty Git repository..."

---

### Step 5: Add Files (Excluding Setup Docs)

```bash
git add .
```

**Paste → Press Enter**

**Note**: The .gitignore file will exclude the setup docs automatically

---

### Step 6: Make the Commit

```bash
git commit -m "Initial commit: Enterprise Data Transformation Platform"
```

**Paste → Press Enter**

**✅ You should see**: "X files changed, Y insertions(+)"

---

### Step 7: Connect to GitHub

```bash
git remote add origin https://github.com/RahulParikh123/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS.git
```

**Paste → Press Enter**

---

### Step 8: Rename Branch

```bash
git branch -M main
```

**Paste → Press Enter**

---

### Step 9: Push to GitHub

```bash
git push -u origin main
```

**Paste → Press Enter**

**⚠️ If it asks for username**: Type `RahulParikh123`
**⚠️ If it asks for password**: Use Personal Access Token (see below)

---

## If It Asks for Password

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `Data Platform`
4. Check: `repo`
5. Click "Generate token"
6. **COPY THE TOKEN**
7. Paste token when Git asks for password

---

## ✅ Done!

Go to: https://github.com/RahulParikh123/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS

Refresh - your files should be there!

---

## All Commands in Order (Copy-Paste One at a Time)

```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
git config --global user.email "Rahul.Parikh.12345@gmail.com"
git config --global user.name "RahulParikh123"
git init
git add .
git commit -m "Initial commit: Enterprise Data Transformation Platform"
git remote add origin https://github.com/RahulParikh123/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS.git
git branch -M main
git push -u origin main
```

**That's it! 9 commands total!** 🚀

