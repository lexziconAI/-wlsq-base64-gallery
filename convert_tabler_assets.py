#!/usr/bin/env python3
"""
Batch convert Tabler assets to Base64 and organize by category.
Creates separate JSON files for each asset type.
"""

import base64
import json
import os
from pathlib import Path
from typing import Dict, Any, List
import argparse
import time


def convert_images_to_base64(source_folder: Path, output_name: str, limit: int = None) -> Dict[str, str]:
    """Convert images in a folder to base64 lookup."""
    if not source_folder.exists():
        print(f"⚠ Folder not found: {source_folder}")
        return {}
    
    # Find image files
    image_files = []
    for ext in ['.png', '.jpg', '.jpeg', '.svg', '.webp']:
        image_files.extend(source_folder.glob(f'**/*{ext}'))
    
    if limit:
        image_files = image_files[:limit]
    
    if not image_files:
        print(f"⚠ No images found in {source_folder}")
        return {}
    
    print(f"📁 {output_name}: Converting {len(image_files)} images...")
    
    lookup = {}
    processed = 0
    
    for img_path in image_files:
        try:
            # Create key from relative path (remove extension)
            rel_path = img_path.relative_to(source_folder)
            key = str(rel_path.with_suffix(''))
            
            # Read and encode
            with open(img_path, 'rb') as f:
                img_data = f.read()
            
            # Determine MIME type
            ext = img_path.suffix.lower()
            if ext == '.svg':
                mime_type = 'image/svg+xml'
            elif ext == '.webp':
                mime_type = 'image/webp'
            elif ext in ['.jpg', '.jpeg']:
                mime_type = 'image/jpeg'
            else:
                mime_type = 'image/png'
            
            # Create data URL
            b64_string = base64.b64encode(img_data).decode('utf-8')
            data_url = f"data:{mime_type};base64,{b64_string}"
            
            lookup[key] = data_url
            processed += 1
            
            if processed % 100 == 0:
                print(f"  Processed {processed}/{len(image_files)}...")
                
        except Exception as e:
            print(f"✗ Error processing {img_path}: {e}")
    
    print(f"✓ {output_name}: {processed} images converted")
    return lookup


def save_lookup(lookup: Dict[str, str], output_path: Path):
    """Save lookup to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(lookup, f, indent=2, ensure_ascii=False)
    
    file_size = output_path.stat().st_size / 1024 / 1024  # MB
    print(f"💾 Saved: {output_path.name} ({file_size:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Convert Tabler assets to Base64 collections")
    parser.add_argument('--limit', type=int, help='Limit images per collection (for testing)')
    parser.add_argument('--collections-only', action='store_true', help='Only process collections, skip existing WLSQ')
    args = parser.parse_args()
    
    start_time = time.time()
    base_path = Path("images to convert to base64")
    output_dir = Path("base64_collections")
    
    print("🎨 Tabler Assets to Base64 Converter")
    print("=" * 50)
    
    collections = []
    
    # Tabler Icons (outline)
    icons_outline = base_path / "tabler-icons" / "png" / "outline"
    if icons_outline.exists():
        lookup = convert_images_to_base64(icons_outline, "Tabler Icons (Outline)", args.limit)
        if lookup:
            output_path = output_dir / "tabler_icons_outline.json"
            save_lookup(lookup, output_path)
            collections.append({"name": "Tabler Icons Outline", "file": "tabler_icons_outline.json", "count": len(lookup)})
    
    # Tabler Icons (filled)
    icons_filled = base_path / "tabler-icons" / "png" / "filled"
    if icons_filled.exists():
        lookup = convert_images_to_base64(icons_filled, "Tabler Icons (Filled)", args.limit)
        if lookup:
            output_path = output_dir / "tabler_icons_filled.json"
            save_lookup(lookup, output_path)
            collections.append({"name": "Tabler Icons Filled", "file": "tabler_icons_filled.json", "count": len(lookup)})
    
    # Tabler Avatars (PNG)
    avatars_png = base_path / "tabler-avatars" / "png"
    if avatars_png.exists():
        lookup = convert_images_to_base64(avatars_png, "Tabler Avatars", args.limit)
        if lookup:
            output_path = output_dir / "tabler_avatars.json"
            save_lookup(lookup, output_path)
            collections.append({"name": "Tabler Avatars", "file": "tabler_avatars.json", "count": len(lookup)})
    
    # Tabler Illustrations (Light)
    illustrations_light = base_path / "tabler-illustrations" / "tabler-illustrations" / "png" / "light"
    if illustrations_light.exists():
        lookup = convert_images_to_base64(illustrations_light, "Tabler Illustrations (Light)", args.limit)
        if lookup:
            output_path = output_dir / "tabler_illustrations_light.json"
            save_lookup(lookup, output_path)
            collections.append({"name": "Tabler Illustrations Light", "file": "tabler_illustrations_light.json", "count": len(lookup)})
    
    # Tabler Illustrations (Dark)
    illustrations_dark = base_path / "tabler-illustrations" / "tabler-illustrations" / "png" / "dark"
    if illustrations_dark.exists():
        lookup = convert_images_to_base64(illustrations_dark, "Tabler Illustrations (Dark)", args.limit)
        if lookup:
            output_path = output_dir / "tabler_illustrations_dark.json"
            save_lookup(lookup, output_path)
            collections.append({"name": "Tabler Illustrations Dark", "file": "tabler_illustrations_dark.json", "count": len(lookup)})
    
    # Create master index
    index = {
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "collections": collections,
        "total_images": sum(c["count"] for c in collections)
    }
    
    index_path = output_dir / "collections_index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    duration = time.time() - start_time
    total_images = index["total_images"]
    
    print("\n" + "=" * 50)
    print(f"✅ COMPLETE!")
    print(f"📊 Total collections: {len(collections)}")
    print(f"🖼️  Total images: {total_images:,}")
    print(f"⏱️  Duration: {duration:.1f}s")
    print(f"📁 Output folder: {output_dir}")
    print("\n📋 Collections created:")
    for collection in collections:
        print(f"  • {collection['name']}: {collection['count']:,} images → {collection['file']}")


if __name__ == "__main__":
    main()