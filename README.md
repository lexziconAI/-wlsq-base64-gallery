# WLSQ Base64 Assets & Interactive Galleries

This repository contains:

- `convert_wlsq_assets.py` – Converts source PNG/JPG images in `images/` into an enriched Base64 JSON lookup.
- `search_images.py` – Search by tag, category, description, or keyword.
- `inject_base64_into_html_v2.py` – Injects Base64 data URIs into HTML templates using `{{PLACEHOLDER}}` syntax.
- `image_base64_lookup.json` – Enriched lookup (28 images) with metadata.
- `interactive_gallery_embedded.html` – Generated interactive character gallery (Base64 embedded).
- `template_floating_animation.html` – Sample animation template (original placeholders or already injected variant created separately).
- `index.html` – Copy of `interactive_gallery_embedded.html` for GitHub Pages.

## GitHub Pages Deployment

1. Create a new GitHub repository (e.g., `wlsq-base64-gallery`).
2. Push this code (instructions below).
3. In the GitHub repo settings, enable Pages:
   - Source: `main` branch
   - Folder: `/ (root)`
4. After a few minutes, your gallery will be available at:
   `https://<your-username>.github.io/wlsq-base64-gallery/`

## Push Instructions
(Replace `YOUR_USERNAME` and repo name as needed.)

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/wlsq-base64-gallery.git
# Push main branch
git push -u origin main
```

## Regenerating the Lookup

```bash
python convert_wlsq_assets.py --no-pause
```

## Injecting a Template

```bash
python inject_base64_into_html_v2.py template_floating_animation.html floating_animation_embedded.html
```

## Searching

```bash
python search_images.py --list-categories
python search_images.py --tag woman
python search_images.py --keyword logo
```

## Creating a New Template
1. Add placeholders: `{{Sitting2_NOPROCESS_}}` etc.
2. Run injector.
3. Open the output HTML or deploy.

## Notes
- All images are embedded as Base64 data URIs – no external asset hosting needed.
- Large file sizes in HTML are expected due to embedded image data.
- For production, keep only the HTML you need to reduce repo size.

---
Generated automatically to assist deployment.
