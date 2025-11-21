# ⚠️ IMPORTANT: Install Python First!

## The Problem

The BAT file didn't work because **Python is not installed** on your computer (or not in PATH).

## Solution: Install Python

### Step 1: Download Python

1. Go to: **https://www.python.org/downloads/**
2. Click the big yellow button: **"Download Python"**
3. Wait for the download to finish

### Step 2: Install Python

1. **Run the installer** (the file you just downloaded)
2. **IMPORTANT:** Check the box that says **"Add Python to PATH"** ✅
   - This is at the bottom of the installer window
   - It's VERY important - don't skip this!
3. Click **"Install Now"**
4. Wait for installation to finish (2-5 minutes)
5. Click **"Close"** when done

### Step 3: Restart Your Computer

- Close all windows
- Restart your computer
- This makes sure Python is available everywhere

### Step 4: Verify Python is Installed

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. Type:
   ```bash
   python --version
   ```
4. You should see something like: `Python 3.11.0`
5. If you see an error, Python isn't installed correctly

### Step 5: Install Dependencies

Now that Python is installed, you need to install the libraries:

1. **Open Command Prompt** (Windows Key + R, type `cmd`)
2. **Go to your project folder:**
   ```bash
   cd C:\Users\rahul\Downloads\data-transformation-platform
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Wait for it to finish** (this takes 5-10 minutes)
   - You'll see lots of text scrolling
   - Wait until it says "Successfully installed" or finishes

### Step 6: Install Language Model

```bash
python -m spacy download en_core_web_sm
```

Wait for this to finish (about 1 minute).

### Step 7: Now Try Again!

Now you can run the BAT file:

1. **Double-click** `RUN_YOUR_FILE.bat`
2. **OR** use Command Prompt:
   ```bash
   python main.py --input "HOME Model v4.xlsx" --output processed.jsonl
   ```

## Quick Checklist

- [ ] Downloaded Python from python.org
- [ ] Checked "Add Python to PATH" during installation
- [ ] Restarted computer
- [ ] Verified: `python --version` works
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Installed language model: `python -m spacy download en_core_web_sm`
- [ ] Ready to process files!

## Alternative: Use Microsoft Store Python

If the above doesn't work, try:

1. Open **Microsoft Store**
2. Search for **"Python 3.11"** or **"Python 3.12"**
3. Click **"Install"**
4. Wait for installation
5. Try again

## Still Having Issues?

If Python still doesn't work after installation:

1. **Check if Python is installed:**
   - Go to: `C:\Users\rahul\AppData\Local\Programs\Python\`
   - If you see a Python folder, it's installed

2. **Add Python to PATH manually:**
   - Search Windows for "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\Users\rahul\AppData\Local\Programs\Python\Python311\` (or your Python version)
   - Click OK on all windows
   - Restart Command Prompt

## Summary

**The issue:** Python isn't installed
**The fix:** Install Python from python.org
**Important:** Check "Add Python to PATH" ✅
**Then:** Install dependencies with `pip install -r requirements.txt`
**Finally:** Run your BAT file again!

Once Python is installed, everything will work! 🎉

