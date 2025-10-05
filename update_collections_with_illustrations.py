#!/usr/bin/env python3
"""
Update the collections index to include WLSQ illustrations
"""

import json
from pathlib import Path
from datetime import datetime

def update_collections_index():
    """Update the collections index with WLSQ illustrations"""
    collections_dir = Path("base64_collections")
    
    # Count images in each collection
    collections = {}
    total_images = 0
    
    collection_files = [
        ("tabler_icons_outline.json", "Tabler Icons Outline"),
        ("tabler_icons_filled.json", "Tabler Icons Filled"), 
        ("tabler_avatars.json", "Tabler Avatars"),
        ("tabler_illustrations_light.json", "Tabler Illustrations Light"),
        ("tabler_illustrations_dark.json", "Tabler Illustrations Dark"),
        ("wlsq_avatars.json", "WLSQ Brand Avatars"),
        ("wlsq_illustrations_light.json", "WLSQ Illustrations Light"),
        ("wlsq_illustrations_dark.json", "WLSQ Illustrations Dark"),
        ("image_base64_lookup.json", "WLSQ Original Images")
    ]
    
    for filename, display_name in collection_files:
        file_path = collections_dir / filename
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    count = len(data)
                    collections[filename] = {
                        "name": display_name,
                        "count": count
                    }
                    total_images += count
                    print(f"✅ {display_name}: {count:,} images")
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
    
    # Create collections index
    index = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_images": total_images,
        "collections": collections
    }
    
    # Save index
    index_file = collections_dir / "collections_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    print(f"\n📊 Collections Index Updated")
    print(f"Total images: {total_images:,}")
    print(f"Collections: {len(collections)}")
    print(f"Saved: {index_file}")
    
    return total_images, len(collections)

if __name__ == "__main__":
    print("🔄 Updating Collections Index...")
    print("=" * 40)
    update_collections_index()
    print("\n🎉 Index update completed!")