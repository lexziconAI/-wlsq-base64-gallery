#!/usr/bin/env python3
"""
Browse and search Tabler Base64 collections
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List


def load_collection(collection_file: Path) -> Dict:
    """Load a collection JSON file."""
    if not collection_file.exists():
        print(f"❌ Collection not found: {collection_file}")
        return {}
    
    with open(collection_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_collections():
    """List all available collections."""
    index_path = Path("base64_collections/collections_index.json")
    
    if not index_path.exists():
        print("❌ Collections index not found. Run convert_tabler_assets.py first.")
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    print("📚 Available Base64 Collections:")
    print("=" * 50)
    print(f"Generated: {index['generated']}")
    print(f"Total Images: {index['total_images']:,}")
    print()
    
    for i, collection in enumerate(index['collections'], 1):
        print(f"{i}. {collection['name']}")
        print(f"   📁 File: {collection['file']}")
        print(f"   🖼️  Images: {collection['count']:,}")
        print()


def search_collection(collection_name: str, search_term: str, limit: int = 20):
    """Search within a specific collection."""
    collections_map = {
        "icons": "tabler_icons_outline.json",
        "icons-outline": "tabler_icons_outline.json", 
        "icons-filled": "tabler_icons_filled.json",
        "avatars": "tabler_avatars.json",
        "wlsq-avatars": "wlsq_avatars.json",
        "wlsq": "wlsq_avatars.json",
        "illustrations": "tabler_illustrations_light.json",
        "illustrations-light": "tabler_illustrations_light.json",
        "illustrations-dark": "tabler_illustrations_dark.json",
        "wlsq-illustrations-light": "wlsq_illustrations_light.json",
        "wlsq-illustrations-dark": "wlsq_illustrations_dark.json"
    }
    
    if collection_name not in collections_map:
        print(f"❌ Unknown collection: {collection_name}")
        print(f"Available: {', '.join(collections_map.keys())}")
        return
    
    collection_file = Path("base64_collections") / collections_map[collection_name]
    collection = load_collection(collection_file)
    
    if not collection:
        return
    
    # Search for matching keys
    search_lower = search_term.lower()
    matches = [key for key in collection.keys() if search_lower in key.lower()]
    
    if not matches:
        print(f"❌ No matches found for '{search_term}' in {collection_name}")
        return
    
    print(f"🔍 Found {len(matches)} matches for '{search_term}' in {collection_name}:")
    print("=" * 50)
    
    for i, key in enumerate(matches[:limit], 1):
        base64_preview = collection[key][:60] + "..." if len(collection[key]) > 60 else collection[key]
        print(f"{i:2d}. {key}")
        print(f"    Key: {{{{ {key} }}}}")
        print(f"    Preview: {base64_preview}")
        print()
    
    if len(matches) > limit:
        print(f"... and {len(matches) - limit} more matches")


def show_random_samples(collection_name: str, count: int = 10):
    """Show random samples from a collection."""
    collections_map = {
        "icons": "tabler_icons_outline.json",
        "icons-outline": "tabler_icons_outline.json", 
        "icons-filled": "tabler_icons_filled.json",
        "avatars": "tabler_avatars.json",
        "wlsq-avatars": "wlsq_avatars.json",
        "wlsq": "wlsq_avatars.json",
        "illustrations": "tabler_illustrations_light.json",
        "illustrations-light": "tabler_illustrations_light.json",
        "illustrations-dark": "tabler_illustrations_dark.json",
        "wlsq-illustrations-light": "wlsq_illustrations_light.json",
        "wlsq-illustrations-dark": "wlsq_illustrations_dark.json"
    }
    
    if collection_name not in collections_map:
        print(f"❌ Unknown collection: {collection_name}")
        return
    
    collection_file = Path("base64_collections") / collections_map[collection_name]
    collection = load_collection(collection_file)
    
    if not collection:
        return
    
    import random
    keys = list(collection.keys())
    samples = random.sample(keys, min(count, len(keys)))
    
    print(f"🎲 Random {len(samples)} samples from {collection_name}:")
    print("=" * 50)
    
    for i, key in enumerate(samples, 1):
        print(f"{i:2d}. {key}")
        print(f"    Placeholder: {{{{ {key} }}}}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Browse Tabler Base64 collections")
    parser.add_argument('--list', action='store_true', help='List all collections')
    parser.add_argument('--search', help='Search term')
    parser.add_argument('--collection', help='Collection to search in')
    parser.add_argument('--random', type=int, help='Show N random samples')
    parser.add_argument('--limit', type=int, default=20, help='Limit search results')
    
    args = parser.parse_args()
    
    if args.list:
        list_collections()
    elif args.search and args.collection:
        search_collection(args.collection, args.search, args.limit)
    elif args.random and args.collection:
        show_random_samples(args.collection, args.random)
    else:
        print("Usage examples:")
        print("  python browse_collections.py --list")
        print("  python browse_collections.py --collection icons --search arrow")
        print("  python browse_collections.py --collection avatars --random 5")
        print("  python browse_collections.py --collection illustrations --search error")


if __name__ == "__main__":
    main()