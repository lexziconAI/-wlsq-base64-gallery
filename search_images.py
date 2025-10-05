#!/usr/bin/env python3
"""
Search for images by tags, description, or category from enriched lookup file.

Usage:
    python search_images.py --tag woman --tag pointing
    python search_images.py --description "sitting on block"
    python search_images.py --category people
    python search_images.py --keyword woman
    
Examples:
    # Find all images tagged "woman"
    python search_images.py --tag woman
    
    # Find images with multiple tags (AND logic)
    python search_images.py --tag woman --tag sitting
    
    # Search in descriptions
    python search_images.py --description "woman pointing"
    
    # Search anywhere (tags, description, category, notes)
    python search_images.py --keyword travel
    
    # List all images in a category
    python search_images.py --category icons
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any


def load_lookup(lookup_file: str = "image_base64_lookup.json") -> Dict[str, Any]:
    """Load the enriched lookup JSON file."""
    
    lookup_path = Path(lookup_file)
    
    if not lookup_path.exists():
        print(f"ERROR: Lookup file not found: {lookup_file}")
        print("Run batch_images_to_base64_enhanced.py first.")
        sys.exit(1)
    
    with open(lookup_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def search_by_tags(lookup: Dict[str, Any], tags: List[str]) -> List[str]:
    """Find images that have ALL specified tags (AND logic)."""
    
    tags_lower = [tag.lower() for tag in tags]
    results = []
    
    for key, data in lookup.items():
        image_tags = [tag.lower() for tag in data.get('tags', [])]
        
        # Check if ALL search tags are present
        if all(tag in image_tags for tag in tags_lower):
            results.append(key)
    
    return results


def search_by_description(lookup: Dict[str, Any], search_term: str) -> List[str]:
    """Find images where description contains search term."""
    
    search_lower = search_term.lower()
    results = []
    
    for key, data in lookup.items():
        description = data.get('description', '').lower()
        
        if search_lower in description:
            results.append(key)
    
    return results


def search_by_category(lookup: Dict[str, Any], category: str) -> List[str]:
    """Find all images in specified category."""
    
    category_lower = category.lower()
    results = []
    
    for key, data in lookup.items():
        image_category = data.get('category', '').lower()
        
        if category_lower == image_category:
            results.append(key)
    
    return results


def search_by_keyword(lookup: Dict[str, Any], keyword: str) -> List[str]:
    """Search across all text fields (tags, description, category, notes)."""
    
    keyword_lower = keyword.lower()
    results = []
    
    for key, data in lookup.items():
        # Combine all searchable text
        searchable = ' '.join([
            data.get('description', ''),
            data.get('category', ''),
            data.get('notes', ''),
            ' '.join(data.get('tags', []))
        ]).lower()
        
        if keyword_lower in searchable:
            results.append(key)
    
    return results


def display_results(results: List[str], lookup: Dict[str, Any], show_details: bool = False):
    """Display search results."""
    
    if not results:
        print("No images found matching your search criteria.")
        return
    
    print(f"\nFound {len(results)} image(s):\n")
    
    for key in sorted(results):
        data = lookup[key]
        
        print(f"📷 {{{{{{key}}}}}}")
        
        if show_details:
            desc = data.get('description', 'No description')
            cat = data.get('category', 'uncategorized')
            tags = ', '.join(data.get('tags', [])) or 'No tags'
            
            print(f"   Description: {desc}")
            print(f"   Category: {cat}")
            print(f"   Tags: {tags}")
        
        print()
    
    print("="*60)
    print(f"Usage in HTML template:")
    for key in sorted(results):
        print(f'  <img src="{{{{{{key}}}}}}" alt="{lookup[key].get("description", key)}">')
    print("="*60)


def list_all_categories(lookup: Dict[str, Any]):
    """List all available categories with counts."""
    
    categories = {}
    
    for data in lookup.values():
        cat = data.get('category', 'uncategorized')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nAvailable categories:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} images")
    print()


def list_all_tags(lookup: Dict[str, Any]):
    """List all unique tags."""
    
    all_tags = set()
    
    for data in lookup.values():
        all_tags.update(data.get('tags', []))
    
    sorted_tags = sorted(all_tags)
    
    print(f"\nAvailable tags ({len(sorted_tags)}):")
    for tag in sorted_tags:
        print(f"  {tag}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Search for images in base64 lookup file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --tag woman --tag sitting
  %(prog)s --description "woman pointing"
  %(prog)s --category people
  %(prog)s --keyword travel
  %(prog)s --list-categories
  %(prog)s --list-tags
        """
    )
    
    parser.add_argument('--tag', action='append', help='Search by tag (can use multiple)')
    parser.add_argument('--description', help='Search in descriptions')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--keyword', help='Search across all fields')
    parser.add_argument('--list-categories', action='store_true', help='List all categories')
    parser.add_argument('--list-tags', action='store_true', help='List all tags')
    parser.add_argument('--details', action='store_true', help='Show detailed info')
    parser.add_argument('--lookup', default='image_base64_lookup.json', help='Lookup file path')
    
    args = parser.parse_args()
    
    # Load lookup
    lookup = load_lookup(args.lookup)
    
    # Handle list commands
    if args.list_categories:
        list_all_categories(lookup)
        sys.exit(0)
    
    if args.list_tags:
        list_all_tags(lookup)
        sys.exit(0)
    
    # Perform search
    results = None
    
    if args.tag:
        results = search_by_tags(lookup, args.tag)
        print(f"Searching for images with tags: {', '.join(args.tag)}")
    
    elif args.description:
        results = search_by_description(lookup, args.description)
        print(f"Searching descriptions for: {args.description}")
    
    elif args.category:
        results = search_by_category(lookup, args.category)
        print(f"Searching category: {args.category}")
    
    elif args.keyword:
        results = search_by_keyword(lookup, args.keyword)
        print(f"Searching all fields for: {args.keyword}")
    
    else:
        print("ERROR: No search criteria specified.")
        print("Use --help for usage examples")
        sys.exit(1)
    
    # Display results
    if results is not None:
        display_results(results, lookup, args.details)
