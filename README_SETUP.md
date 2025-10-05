# WLSQ Assets Base64 Conversion - Setup Instructions

## What You Need

1. **Python 3.7+** installed
2. **VS Code** (already have)
3. **Files in this folder:**
   - `convert_wlsq_assets.py` (main converter)
   - `search_images.py` (search tool)
   - `inject_base64_into_html_v2.py` (HTML generator)
   - `WLSQ_assets_catalogue.csv` (your metadata file)

## Folder Structure

Your folder should look like this:

```
Base_64_images/
├── convert_wlsq_assets.py
├── search_images.py
├── inject_base64_into_html_v2.py
├── WLSQ_assets_catalogue.csv
├── images/                          ← PUT YOUR PNG/JPG FILES HERE
│   ├── Sitting2_NOPROCESS_.png
│   ├── teal arrow.png
│   ├── Walking_NOPROCESS_.png
│   └── ... (all your image files)
└── README.md (this file)
```

## Step-by-Step Setup

### 1. Create Images Folder

Open your terminal in VS Code (Ctrl + `) and run:

```bash
mkdir images
```

### 2. Copy Your Image Files

Move all your PNG and JPG files into the `images/` folder.

**Important:** The filenames must match the names in `WLSQ_assets_catalogue.csv`

### 3. Verify Files Are Ready

Check you have:
- ✓ `WLSQ_assets_catalogue.csv` in the main folder
- ✓ All image files in `images/` subfolder
- ✓ All three Python scripts in the main folder

## Running the Conversion

### Open VS Code Terminal

Press `Ctrl + ~` or go to Terminal → New Terminal

### Run the Converter

```bash
python convert_wlsq_assets.py
```

### What Happens

1. Script loads metadata from CSV
2. Finds your images in the `images/` folder
3. Converts each to base64
4. Creates `image_base64_lookup.json`
5. Shows summary of categories and tags

### Expected Output

```
======================================================================
WLSQ Assets Base64 Converter
======================================================================
Working directory: C:\Users\regan\...\Base_64_images

✓ Loaded metadata for 29 images from WLSQ_assets_catalogue.csv

✓ Found images folder: images
  Contains 29 image files

Found 29 image files
Converting to base64...

✓ with metadata     | Sitting2_NOPROCESS_.png                 |   45.2 KB
✓ with metadata     | teal arrow.png                          |   12.3 KB
✓ with metadata     | Walking_NOPROCESS_.png                  |   52.1 KB
...

======================================================================
Processed: 29 images
Skipped: 0 images
======================================================================

✓ Saved enriched lookup: image_base64_lookup.json
  Total images: 29
  With metadata: 29
  Without metadata: 0
  File size: 4523.4 KB

======================================================================
CATEGORIES:
  arrows           : 2 images
  backgrounds      : 2 images
  dividers         : 8 images
  logos            : 3 images
  people           : 7 images
  transitions      : 7 images

UNIQUE TAGS: 65
  abstract-mark            beige                    branding
  centered                 character                chevron
  ...

======================================================================
SUCCESS! Next steps:
1. Use search_images.py to find images by tags/description
2. Use inject_base64_into_html_v2.py to apply to templates
======================================================================
```

## Using the Search Tool

After conversion, search your image library:

### Search by Tag

```bash
python search_images.py --tag woman --tag walking
```

### Search by Description

```bash
python search_images.py --description "chevron arrow"
```

### Search by Category

```bash
python search_images.py --category transitions
```

### List All Categories

```bash
python search_images.py --list-categories
```

### List All Tags

```bash
python search_images.py --list-tags
```

## Creating HTML with Embedded Images

### 1. Create Template

Create a file called `template_example.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .container { text-align: center; }
        .character { width: 300px; }
        .arrow { width: 100px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>WLSQ Example</h1>
        
        <!-- Placeholders will be replaced with base64 -->
        <img src="{{Sitting2_NOPROCESS_}}" class="character" alt="Woman sitting">
        
        <img src="{{teal arrow}}" class="arrow" alt="Arrow">
        
        <img src="{{Walking_NOPROCESS_}}" class="character" alt="Woman walking">
    </div>
</body>
</html>
```

**Important:** Use exact key names from the JSON (filename without extension)

### 2. Generate Final HTML

```bash
python inject_base64_into_html_v2.py template_example.html output_example.html
```

### 3. Result

`output_example.html` will have all `{{placeholders}}` replaced with base64 data URLs.

Open it in a browser to verify, then paste the HTML into RISE.

## Troubleshooting

### "ERROR: Metadata file not found"

Make sure `WLSQ_assets_catalogue.csv` is in the same folder as the Python script.

### "ERROR: No image folder found"

Create the `images/` folder and put your PNG/JPG files in it.

### "⚠ no metadata" warnings

The image filename doesn't match any entry in the CSV. Check:
- Exact filename match (case-sensitive)
- File extension included in CSV

### "No base64 data for {{placeholder}}"

The placeholder name doesn't match a key in the JSON. Check:
- Use filename WITHOUT extension: `{{teal arrow}}` not `{{teal arrow.png}}`
- Exact spelling and spacing

## File Sizes

Your `image_base64_lookup.json` will be approximately:
- 29 images × ~150 KB average = ~4.5 MB JSON file

This is perfectly fine for the system to handle.

## Next Steps

1. ✓ Convert images (you're doing this now)
2. Search and explore your image library
3. Create HTML templates with placeholders
4. Generate production HTML files
5. Paste into RISE HTML blocks
6. Export SCORM from RISE
7. Upload to Moodle

## Questions?

The scripts have built-in help:

```bash
python convert_wlsq_assets.py --help
python search_images.py --help
python inject_base64_into_html_v2.py --help
```

Happy converting! 🎨
