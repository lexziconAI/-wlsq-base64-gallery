#!/usr/bin/env python3
"""
Inject base64 images from enriched lookup file into HTML templates.
Works with both simple and enriched JSON formats.

Usage:
    python inject_base64_into_html_v2.py template.html output.html
    
Supports:
    - Simple format: {"key": "data:image/png;base64,..."}
    - Enriched format: {"key": {"base64": "data:...", "description": "...", ...}}
"""

import json
import sys
import re
from pathlib import Path


def load_base64_lookup(lookup_file="image_base64_lookup.json"):
    """Load the base64 lookup JSON file (simple or enriched format)."""
    
    lookup_path = Path(lookup_file)
    
    if not lookup_path.exists():
        print(f"ERROR: Lookup file not found: {lookup_file}")
        print("Run batch_images_to_base64_enhanced.py first.")
        sys.exit(1)
    
    with open(lookup_path, 'r', encoding='utf-8') as f:
        raw_lookup = json.load(f)
    
    # Normalize to simple format {key: base64_string}
    normalized = {}
    
    for key, value in raw_lookup.items():
        if isinstance(value, dict):
            # Enriched format - extract base64
            normalized[key] = value.get('base64', '')
        else:
            # Simple format - use as-is
            normalized[key] = value
    
    return normalized, raw_lookup


def inject_base64_into_html(template_path, output_path, lookup, raw_lookup):
    """Replace {{IMAGE_NAME}} placeholders with base64 data URLs."""
    
    template_path = Path(template_path)
    
    if not template_path.exists():
        print(f"ERROR: Template file not found: {template_path}")
        sys.exit(1)
    
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find all placeholders
    placeholders = re.findall(r'\{\{([^}]+)\}\}', html_content)
    
    if not placeholders:
        print("WARNING: No {{placeholders}} found in template")
        print("Use format: <img src=\"{{image-name}}\" alt=\"...\">")
        return
    
    print(f"Found {len(placeholders)} placeholder(s): {', '.join(set(placeholders))}\n")
    
    # Replace each placeholder
    replacements = 0
    missing = []
    
    for placeholder in set(placeholders):
        if placeholder in lookup:
            html_content = html_content.replace(
                f"{{{{{placeholder}}}}}",
                lookup[placeholder]
            )
            replacements += 1
            
            # Show metadata if available
            if isinstance(raw_lookup.get(placeholder), dict):
                meta = raw_lookup[placeholder]
                desc = meta.get('description', 'No description')
                print(f"✓ {{{{{{placeholder}}}}}} - {desc}")
            else:
                print(f"✓ {{{{{{placeholder}}}}}}")
        else:
            missing.append(placeholder)
            print(f"✗ No base64 data for {{{{{{placeholder}}}}}}")
    
    # Report missing images
    if missing:
        print(f"\nWARNING: {len(missing)} image(s) not found in lookup:")
        for img in missing:
            print(f"  - {img}")
        print("\nAvailable images:")
        for img in sorted(lookup.keys())[:20]:
            if isinstance(raw_lookup.get(img), dict):
                desc = raw_lookup[img].get('description', '')
                print(f"  - {img} ({desc})")
            else:
                print(f"  - {img}")
        if len(lookup) > 20:
            print(f"  ... and {len(lookup) - 20} more")
        
        print("\nTIP: Use search_images.py to find images by tags/description")
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_size = Path(output_path).stat().st_size / 1024
    
    print(f"\n✓ Created: {output_path}")
    print(f"  Replacements: {replacements}")
    print(f"  File size: {output_size:.1f} KB")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python inject_base64_into_html_v2.py template.html output.html")
        sys.exit(1)
    
    template_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Load lookup (handles both formats)
    lookup, raw_lookup = load_base64_lookup()
    
    # Inject into template
    inject_base64_into_html(template_file, output_file, lookup, raw_lookup)
    
    print("\n" + "="*60)
    print("Done! Your HTML is ready to paste into RISE.")
    print("="*60)
