# How to View Your Website in VS Code

## ✅ Background Image Added
The tech hand image has been added as a subtle watermark background on your intro cards with 8% opacity.

### To Use the Background Image:
1. Save your tech hand image as: `assets/images/background-tech.jpg`
2. The CSS is already configured to display it as a watermark

---

## 📺 Method 1: Live Server Extension (RECOMMENDED)

### Install Live Server:
1. Click the **Extensions** icon in VS Code sidebar (or press `Ctrl+Shift+X`)
2. Search for **"Live Server"** by Ritwick Dey
3. Click **Install**

### Use Live Server:
1. Right-click on `index.html` in the Explorer
2. Select **"Open with Live Server"**
3. Your website will open in your default browser at `http://localhost:5500`
4. Live reload: Any changes you make will automatically refresh!

---

## 📺 Method 2: VS Code Simple Browser

### Quick Open:
1. Press `Ctrl+Shift+P` to open Command Palette
2. Type: **"Simple Browser: Show"**
3. Enter this URL:
   ```
   file:///d:/Cyco%20Tab/Documents/Business/Websites/GitHub/App_Development/VSCode/Website/index.html
   ```

### Or Use Python Server:
1. Open terminal in VS Code: `Ctrl+` \`
2. Run this command:
   ```powershell
   python -m http.server 8000
   ```
3. Press `Ctrl+Shift+P` and type: **"Simple Browser: Show"**
4. Enter: `http://localhost:8000`

---

## 📺 Method 3: Default Browser

### Double-click:
Simply double-click `index.html` in File Explorer to open in your default browser.

### Or using terminal:
```powershell
cd "d:\Cyco Tab\Documents\Business\Websites\GitHub\App_Development\VSCode\Website"
start index.html
```

---

## 🎨 Background Image Setup

The background image styling is already added to `styles.css`:

```css
.intro-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background-image: url('assets/images/background-tech.jpg');
    background-size: contain;
    background-position: right center;
    background-repeat: no-repeat;
    opacity: 0.08;  /* Subtle watermark effect */
    pointer-events: none;
    z-index: 0;
}
```

### To adjust the watermark:
- **Make it more visible:** Change `opacity: 0.08;` to `opacity: 0.15;`
- **Make it less visible:** Change to `opacity: 0.05;`
- **Change position:** Modify `background-position` (options: `left`, `center`, `right`)
- **Change size:** Modify `background-size` (options: `contain`, `cover`, `50%`)

---

## 🔧 Troubleshooting

### Live Server not working?
- Make sure the extension is installed and enabled
- Try restarting VS Code
- Check if another server is using port 5500

### Python server not working?
- Verify Python is installed: `python --version`
- Try `python3 -m http.server 8000` instead
- Make sure you're in the Website folder

### Images not showing?
- Verify image path: `assets/images/background-tech.jpg`
- Check file exists in the correct folder
- Try hard refresh in browser: `Ctrl+F5`

---

## 📂 Your Website Structure

```
Website/
├── index.html              # Main homepage (new blog-style design)
├── index-old.html          # Backup of original design
├── archives.html           # Chronological project archive
├── resume.html             # Your full resume
├── case-study-signet.html  # Signet Jewelers case study
├── styles.css              # Main stylesheet (new clean design)
├── styles-old.css          # Backup of original styles
├── script.js               # JavaScript functionality
├── assets/
│   └── images/
│       └── background-tech.jpg  # Your watermark image
└── VIEW_WEBSITE_INSTRUCTIONS.md # This file

```

---

## 🌐 Current Website Features

✅ Clean sidebar layout (Tim Hopper-inspired)  
✅ Teal and tan color scheme  
✅ Blog-style project cards  
✅ Archives page with chronological listing  
✅ Interactive dashboard in case study  
✅ Mobile-responsive design  
✅ Background watermark image  
✅ Professional typography (Inter + Lora)

---

## 🚀 Next Steps

1. **Add your profile image:** Save as `assets/images/profile.jpg`
2. **Add background image:** Save as `assets/images/background-tech.jpg`
3. **Update email:** Replace `contact@pamelaaustin.com` with your real email
4. **Test all links:** Click through all navigation and project links
5. **Deploy:** Consider GitHub Pages, Netlify, or Vercel for hosting

Enjoy your new website! 🎉
