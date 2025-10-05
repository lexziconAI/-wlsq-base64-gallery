#!/usr/bin/env python3
"""
WLSQ Assets Base64 Converter
Converts PNG/JPG images to base64 with metadata enrichment

Usage:
    python convert_wlsq_assets.py

Files needed in same directory:
    - WLSQ_assets_catalogue.csv (metadata file)
    - images/ folder (containing your PNG/JPG files)

Output:
    - image_base64_lookup.json (enriched lookup file)
"""

import base64
import csv
import json
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional
import argparse


def debug_log(enabled: bool, msg: str):
    if enabled:
        print(f"[DEBUG] {msg}", flush=True)


def load_metadata(metadata_file: str = "WLSQ_assets_catalogue.csv", debug: bool = False) -> Dict[str, Dict[str, Any]]:
    """Load metadata from CSV file with debug instrumentation and error resilience."""
    start = time.time()
    if not os.path.exists(metadata_file):
        print(f"ERROR: Metadata file not found: {metadata_file}")
        print(f"Looking in: {os.path.abspath('.')}")
        return {}

    metadata: Dict[str, Dict[str, Any]] = {}
    try:
        with open(metadata_file, 'r', encoding='utf-8', newline='') as f:
            sample = f.read(4096)
            f.seek(0)
            debug_log(debug, f"First 120 chars of CSV: {sample[:120].replace(os.linesep, ' | ')} ...")
            reader = csv.DictReader(f)
            missing_cols = {c for c in ['filename'] if c not in reader.fieldnames}
            if missing_cols:
                print(f"ERROR: CSV missing required columns: {', '.join(missing_cols)}")
                return {}

            count = 0
            for row in reader:
                count += 1
                filename = row.get('filename', '').strip()
                if not filename:
                    debug_log(debug, f"Skipping row {count}: blank filename")
                    continue
                key = Path(filename).stem
                tags = [tag.strip() for tag in row.get('tags', '').split('|') if tag.strip()]
                metadata[key] = {
                    'description': row.get('description', ''),
                    'category': row.get('category', ''),
                    'tags': tags,
                    'notes': row.get('notes', ''),
                    'original_filename': filename
                }
            debug_log(debug, f"CSV rows processed: {count}")
    except Exception as e:
        print(f"ERROR: Failed reading CSV: {e}")
        if debug:
            traceback.print_exc()
        return {}

    elapsed = (time.time() - start) * 1000
    print(f"✓ Loaded metadata for {len(metadata)} images from {metadata_file} ({elapsed:.1f} ms)\n", flush=True)
    return metadata


def find_image_folder(explicit: Optional[str] = None, debug: bool = False) -> Optional[str]:
    """Find the images folder - try explicit path first, then common locations."""
    possible_folders: List[str] = []
    if explicit:
        possible_folders.append(explicit)
    possible_folders.extend([
        'images',
        'assets',
        'WLSQ_assets',
        '.',
    ])
    visited = set()
    for folder in possible_folders:
        if folder in visited:
            continue
        visited.add(folder)
        debug_log(debug, f"Inspecting folder candidate: {folder}")
        if os.path.isdir(folder):
            image_files: List[Path] = []
            try:
                for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']:
                    image_files.extend(Path(folder).glob(f'*{ext}'))
            except Exception as e:
                debug_log(debug, f"Error globbing in {folder}: {e}")
                continue
            if image_files:
                print(f"✓ Found images folder: {folder}")
                print(f"  Contains {len(image_files)} image files\n", flush=True)
                return folder
            else:
                debug_log(debug, f"No image files found in {folder}")
        else:
            debug_log(debug, f"Not a directory: {folder}")
    return None


def convert_images_with_metadata(image_folder: str, metadata: Dict[str, Dict[str, Any]], debug: bool = False, limit: Optional[int] = None) -> Dict[str, Any]:
    """Convert all PNG/JPG images to base64 and merge with metadata with diagnostics."""
    start_all = time.time()
    if not os.path.exists(image_folder):
        print(f"ERROR: Image folder not found: {image_folder}")
        return {}
    # Collect images once, avoiding duplicate case-insensitive matches (Windows)
    allowed_ext = {'.png', '.jpg', '.jpeg'}
    raw_list: List[Path] = [p for p in Path(image_folder).iterdir() if p.is_file() and p.suffix.lower() in allowed_ext]
    # Deduplicate by lowercase name (in case of accidental duplicates differing only by case)
    unique: Dict[str, Path] = {}
    for p in raw_list:
        key = p.name.lower()
        if key in unique:
            debug_log(debug, f"Duplicate filename encountered (case variation or duplicate): {p.name} -> keeping first {unique[key].name}")
            continue
        unique[key] = p
    image_files: List[Path] = sorted(unique.values(), key=lambda p: p.name.lower())
    if debug:
        debug_log(debug, f"Initial collected files: {len(raw_list)} | Unique after dedupe: {len(image_files)}")
    if limit:
        debug_log(debug, f"Limiting processing to first {limit} images of {len(image_files)} total")
        image_files = image_files[:limit]

    if not image_files:
        print(f"WARNING: No image files found in {image_folder}")
        return {}

    print(f"Found {len(image_files)} image files")
    print("Converting to base64...\n", flush=True)

    enriched_lookup: Dict[str, Any] = {}
    processed = 0
    skipped = 0
    last_print = time.time()

    for idx, img_file in enumerate(image_files, 1):
        loop_start = time.time()
        try:
            debug_log(debug, f"Opening {img_file} ({idx}/{len(image_files)})")
            with open(img_file, 'rb') as f:
                img_data = f.read()
            read_ms = (time.time() - loop_start) * 1000
            debug_log(debug, f"Read {len(img_data)} bytes in {read_ms:.2f} ms")

            b64_start = time.time()
            b64_string = base64.b64encode(img_data).decode('utf-8')
            b64_ms = (time.time() - b64_start) * 1000
            debug_log(debug, f"Encoded base64 in {b64_ms:.2f} ms (length {len(b64_string)})")

            ext = img_file.suffix.lower()
            mime_type = 'image/png' if ext == '.png' else 'image/jpeg'
            key = img_file.stem
            meta = metadata.get(key, {})

            enriched_lookup[key] = {
                'base64': f"data:{mime_type};base64,{b64_string}",
                'description': meta.get('description', ''),
                'category': meta.get('category', 'uncategorized'),
                'tags': meta.get('tags', []),
                'notes': meta.get('notes', ''),
                'filename': img_file.name
            }

            file_size = len(img_data) / 1024
            meta_status = "✓ with metadata" if key in metadata else "⚠ no metadata"
            print(f"{meta_status:20} | {img_file.name:40} | {file_size:6.1f} KB", flush=True)
            processed += 1
        except Exception as e:
            print(f"✗ ERROR | {img_file.name:40} | {e}")
            if debug:
                traceback.print_exc()
            skipped += 1
        finally:
            loop_total = (time.time() - loop_start) * 1000
            debug_log(debug, f"Loop total {loop_total:.2f} ms for {img_file.name}")
            if time.time() - last_print > 5:
                print("... still working ...", flush=True)
                last_print = time.time()

    total_ms = (time.time() - start_all) * 1000
    print(f"\n{'='*70}")
    print(f"Processed: {processed} images")
    print(f"Skipped: {skipped} images")
    print(f"Elapsed: {total_ms:.1f} ms ({total_ms/1000:.2f} s)")
    print(f"{'='*70}\n", flush=True)
    return enriched_lookup


def save_enriched_lookup(lookup: Dict[str, Any], output_path: str = "image_base64_lookup.json", debug: bool = False):
    """Save enriched lookup dictionary to JSON file with timing and debug."""
    start = time.time()
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(lookup, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write {output_path}: {e}")
        if debug:
            traceback.print_exc()
        return
    elapsed = (time.time() - start) * 1000
    total = len(lookup)
    with_metadata = sum(1 for v in lookup.values() if v.get('description'))
    file_size = os.path.getsize(output_path) / 1024
    print(f"✓ Saved enriched lookup: {output_path}")
    print(f"  Total images: {total}")
    print(f"  With metadata: {with_metadata}")
    print(f"  Without metadata: {total - with_metadata}")
    print(f"  File size: {file_size:.1f} KB (write {elapsed:.1f} ms)")


def display_summary(lookup: Dict[str, Any]):
    """Display category and tag summary."""
    
    if not lookup:
        return
    
    # Collect categories
    categories = {}
    all_tags = set()
    
    for key, data in lookup.items():
        cat = data.get('category', 'uncategorized')
        categories[cat] = categories.get(cat, 0) + 1
        all_tags.update(data.get('tags', []))
    
    print(f"\n{'='*70}")
    print("CATEGORIES:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat:20} : {count} images")
    
    print(f"\nUNIQUE TAGS: {len(all_tags)}")
    if all_tags:
        sorted_tags = sorted(all_tags)
        # Display in columns
        for i in range(0, min(30, len(sorted_tags)), 3):
            tags_row = sorted_tags[i:i+3]
            print(f"  {tags_row[0]:25} {tags_row[1] if len(tags_row) > 1 else '':25} {tags_row[2] if len(tags_row) > 2 else ''}")
        if len(sorted_tags) > 30:
            print(f"  ... and {len(sorted_tags) - 30} more tags")
    
    print(f"{'='*70}")


def suggest_onedrive_action():
    if 'OneDrive' in os.path.abspath('.'):
        print("⚠ Detected OneDrive path. If performance issues persist, try copying the entire folder to a non-synced path like C:\\Temp\\Base_64_images and run there.")


def parse_args():
    parser = argparse.ArgumentParser(description="WLSQ Assets Base64 Converter")
    parser.add_argument('--metadata', default='WLSQ_assets_catalogue.csv', help='Metadata CSV file')
    parser.add_argument('--images', default=None, help='Explicit images folder')
    parser.add_argument('--output', default='image_base64_lookup.json', help='Output JSON path')
    parser.add_argument('--debug', action='store_true', help='Enable verbose debug logging')
    parser.add_argument('--no-pause', action='store_true', help='Do not pause for Enter at end')
    parser.add_argument('--limit', type=int, default=None, help='Process only first N images (for testing)')
    parser.add_argument('--list-only', action='store_true', help='List images & metadata match status without converting')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    start_program = time.time()
    print("="*70)
    print("WLSQ Assets Base64 Converter")
    print("="*70)
    print(f"Python: {sys.version.split()[0]} | Platform: {sys.platform}")
    print(f"Working directory: {os.path.abspath('.')}")
    print(f"Started at: {time.strftime('%H:%M:%S')}\n", flush=True)
    suggest_onedrive_action()

    # Stage 1: Load metadata
    print("[Stage 1] Loading metadata...", flush=True)
    metadata = load_metadata(args.metadata, debug=args.debug)
    if not metadata:
        print("\nERROR: No metadata loaded. Cannot proceed.")
        print("Make sure the CSV file exists and has a 'filename' column.")
        if not args.no_pause:
            pass  # no input pause to avoid hang issues
        sys.exit(1)

    # Stage 2: Locate images folder
    print("[Stage 2] Locating images folder...", flush=True)
    image_folder = find_image_folder(args.images, debug=args.debug)
    if not image_folder:
        print("\nERROR: No image folder found.")
        print("Create an 'images' folder and place your PNG/JPG files there, or specify --images path.")
        if not args.no_pause:
            pass
        sys.exit(1)

    # Optional: list only
    if args.list_only:
        print("[Stage 3 - LIST ONLY] Previewing image/metadata alignment", flush=True)
        image_files: List[Path] = []
        for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']:
            image_files.extend(Path(image_folder).glob(f"*{ext}"))
        image_files = sorted(image_files, key=lambda p: p.name.lower())
        matches = 0
        for img in image_files:
            key = img.stem
            has_meta = key in metadata
            if has_meta:
                matches += 1
            print(f"{'META' if has_meta else '----'} | {img.name}")
        print(f"Total images: {len(image_files)} | With metadata: {matches} | Without: {len(image_files)-matches}")
        duration = (time.time() - start_program) * 1000
        print(f"Done (list-only) in {duration:.1f} ms")
        sys.exit(0)

    # Stage 3: Convert
    print("[Stage 3] Converting images...", flush=True)
    enriched_lookup = convert_images_with_metadata(image_folder, metadata, debug=args.debug, limit=args.limit)

    if enriched_lookup:
        # Stage 4: Save
        print("[Stage 4] Saving lookup...", flush=True)
        save_enriched_lookup(enriched_lookup, args.output, debug=args.debug)
        # Stage 5: Summary
        print("[Stage 5] Summary...", flush=True)
        display_summary(enriched_lookup)
        print("\n" + "="*70)
        print("SUCCESS! Next steps:")
        print("1. Use search_images.py to find images by tags/description")
        print("2. Use inject_base64_into_html_v2.py to apply to templates")
        print("="*70)
    else:
        print("\nERROR: No images were converted. Check that your image files are in the correct location.")

    total_duration = (time.time() - start_program) * 1000
    print(f"Total runtime: {total_duration:.1f} ms ({total_duration/1000:.2f} s)")
    if not args.no_pause:
        # Purposefully no blocking input() to avoid "hang" confusion if output window not scrolling.
        print("(Run with --no-pause to suppress this line.)")
