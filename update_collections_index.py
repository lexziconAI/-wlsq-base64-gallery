#!/usr/bin/env python3
"""
Update collections index to include WLSQ avatars
"""

import json
import time
from pathlib import Path


def update_collections_index():
    """Add WLSQ avatars to the collections index."""
    
    index_path = Path("base64_collections/collections_index.json")
    wlsq_avatars_path = Path("base64_collections/wlsq_avatars.json")
    
    # Load existing index
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        index = {"collections": []}
    
    # Count WLSQ avatars
    if wlsq_avatars_path.exists():
        with open(wlsq_avatars_path, 'r', encoding='utf-8') as f:
            wlsq_avatars = json.load(f)
        wlsq_count = len(wlsq_avatars)
    else:
        wlsq_count = 0
    
    # Add or update WLSQ avatars entry
    wlsq_entry = {
        "name": "WLSQ Brand Avatars",
        "file": "wlsq_avatars.json",
        "count": wlsq_count
    }
    
    # Check if WLSQ avatars already in index
    existing_idx = None
    for i, collection in enumerate(index["collections"]):
        if collection["file"] == "wlsq_avatars.json":
            existing_idx = i
            break
    
    if existing_idx is not None:
        index["collections"][existing_idx] = wlsq_entry
        print(f"Updated existing WLSQ avatars entry: {wlsq_count} avatars")
    else:
        index["collections"].append(wlsq_entry)
        print(f"Added WLSQ avatars to index: {wlsq_count} avatars")
    
    # Update metadata
    index["generated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    index["total_images"] = sum(c["count"] for c in index["collections"])
    
    # Save updated index
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Collections index updated: {index['total_images']:,} total images")


if __name__ == "__main__":
    update_collections_index()