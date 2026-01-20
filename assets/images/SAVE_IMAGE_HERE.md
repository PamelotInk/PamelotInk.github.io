# Save Your Tech Hand Image Here

## 📸 Instructions:

1. **Save the purple tech hand image from the attachment**
2. **Rename it to:** `tech-hand.jpg`
3. **Place it in this folder:** `assets/images/`

## ✅ What Will Happen:

The image will appear as a **subtle teal watermark** in the center background of your homepage with:
- 5% opacity (very subtle, won't interfere with text)
- Teal color (converted from purple using CSS filter)
- Fixed position in center of the page
- 600x600px size

## 🎨 Customization:

If you want to adjust the watermark in `styles.css`, look for `.main-content::before`:

- **More visible:** Change `opacity: 0.05;` to `0.10;`
- **Less visible:** Change to `0.03;`
- **Larger:** Change `width: 600px; height: 600px;` to `800px`
- **Different teal tone:** Adjust `hue-rotate(200deg)` value
- **Brighter:** Increase `brightness(1.2)` value
- **More saturated:** Increase `saturate(1.5)` value

## 🎨 Color Filter Explanation:

```css
filter: hue-rotate(200deg) saturate(1.5) brightness(1.2);
```

This converts the purple/violet image to teal/cyan:
- `hue-rotate(200deg)` - Shifts purple → teal
- `saturate(1.5)` - Makes the color more vibrant
- `brightness(1.2)` - Lightens it slightly

Save the image here and refresh your browser to see it! 🎉
