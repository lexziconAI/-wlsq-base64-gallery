#!/usr/bin/env python3
"""
Convert Tabler illustrations to WLSQ brand colors
Processes both light and dark variants while preserving shapes and designs
"""

import os
import base64
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

class WLSQIllustrationConverter:
    def __init__(self):
        # WLSQ brand color palette from style guide
        self.wlsq_colors = {
            'primary': '#56477e',      # Main WLSQ purple
            'secondary': '#7e67a5',    # Lighter purple
            'accent': '#9f8cc7',       # Even lighter purple
            'dark': '#3d2f5a',         # Darker purple
            'light': '#b8a8d9',       # Very light purple
            'neutral_dark': '#2c2c2c', # Dark gray
            'neutral_light': '#f5f5f5', # Light gray
            'skin': '#FFCB9D'          # Keep skin tone natural
        }
        
        # Original Tabler colors to replace
        self.tabler_color_mappings = {
            # Primary blues to WLSQ purple
            '#066FD1': self.wlsq_colors['primary'],
            '#0054A3': self.wlsq_colors['dark'],
            '#3B82F6': self.wlsq_colors['secondary'],
            '#60A5FA': self.wlsq_colors['accent'],
            '#93C5FD': self.wlsq_colors['light'],
            
            # Grays remain similar but adjusted
            '#232B41': self.wlsq_colors['neutral_dark'],
            '#374151': '#4a4a4a',
            '#6B7280': '#666666',
            '#9CA3AF': '#888888',
            '#D1D5DB': '#cccccc',
            '#E5E7EB': self.wlsq_colors['neutral_light'],
            '#F3F4F6': '#fafafa',
            
            # Keep skin tones natural
            '#FFCB9D': self.wlsq_colors['skin'],
            '#FFB885': '#ffb885',
            '#FFA066': '#ffa066',
        }

    def convert_svg_colors(self, svg_content: str) -> str:
        """Convert SVG colors from Tabler to WLSQ brand colors"""
        modified_svg = svg_content
        
        # Replace direct color references
        for old_color, new_color in self.tabler_color_mappings.items():
            # Replace fill attributes
            modified_svg = re.sub(
                rf'fill="{re.escape(old_color)}"',
                f'fill="{new_color}"',
                modified_svg,
                flags=re.IGNORECASE
            )
            
            # Replace stroke attributes
            modified_svg = re.sub(
                rf'stroke="{re.escape(old_color)}"',
                f'stroke="{new_color}"',
                modified_svg,
                flags=re.IGNORECASE
            )
            
            # Replace style attributes
            modified_svg = re.sub(
                rf'fill:\s*{re.escape(old_color)}',
                f'fill: {new_color}',
                modified_svg,
                flags=re.IGNORECASE
            )
        
        # Update CSS variables to use WLSQ colors
        modified_svg = re.sub(
            r'--tblr-illustrations-primary,\s*var\(--tblr-primary,\s*#066FD1\)\)',
            f'--wlsq-primary, {self.wlsq_colors["primary"]})',
            modified_svg
        )
        
        modified_svg = re.sub(
            r'--tblr-illustrations-skin,\s*#FFCB9D\)',
            f'--wlsq-skin, {self.wlsq_colors["skin"]})',
            modified_svg
        )
        
        return modified_svg

    def process_illustration_directory(self, input_dir: str, output_dir: str, variant: str) -> Dict[str, str]:
        """Process all SVG files in a directory"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        illustrations = {}
        processed_count = 0
        
        print(f"🎨 Processing {variant} illustrations...")
        print(f"📂 Input: {input_path}")
        print(f"📁 Output: {output_path}")
        
        for svg_file in input_path.glob("*.svg"):
            try:
                # Read original SVG
                with open(svg_file, 'r', encoding='utf-8') as f:
                    original_svg = f.read()
                
                # Convert colors to WLSQ palette
                wlsq_svg = self.convert_svg_colors(original_svg)
                
                # Save WLSQ version
                output_file = output_path / f"wlsq_{svg_file.name}"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(wlsq_svg)
                
                # Convert to base64
                base64_string = base64.b64encode(wlsq_svg.encode('utf-8')).decode('utf-8')
                
                # Store in collection
                key = f"wlsq_{svg_file.stem}"
                illustrations[key] = f"data:image/svg+xml;base64,{base64_string}"
                
                processed_count += 1
                if processed_count % 10 == 0:
                    print(f"  ✅ Processed {processed_count} illustrations...")
                    
            except Exception as e:
                print(f"  ❌ Error processing {svg_file.name}: {e}")
                continue
        
        print(f"🎉 Completed {variant}: {processed_count} illustrations converted")
        return illustrations

    def create_collections(self):
        """Create WLSQ illustration collections"""
        base_path = Path("images to convert to base64/tabler-illustrations/tabler-illustrations/svg-css-variables")
        
        # Process light illustrations
        light_input = base_path / "light"
        light_output = Path("wlsq_illustrations_light")
        light_illustrations = self.process_illustration_directory(
            str(light_input), str(light_output), "light"
        )
        
        # Process dark illustrations  
        dark_input = base_path / "dark"
        dark_output = Path("wlsq_illustrations_dark")
        dark_illustrations = self.process_illustration_directory(
            str(dark_input), str(dark_output), "dark"
        )
        
        # Save collections as JSON
        collections_dir = Path("base64_collections")
        collections_dir.mkdir(exist_ok=True)
        
        # Save light collection
        light_json = collections_dir / "wlsq_illustrations_light.json"
        with open(light_json, 'w', encoding='utf-8') as f:
            json.dump(light_illustrations, f, indent=2)
        print(f"💾 Saved: {light_json} ({len(light_illustrations)} illustrations)")
        
        # Save dark collection
        dark_json = collections_dir / "wlsq_illustrations_dark.json"
        with open(dark_json, 'w', encoding='utf-8') as f:
            json.dump(dark_illustrations, f, indent=2)
        print(f"💾 Saved: {dark_json} ({len(dark_illustrations)} illustrations)")
        
        return len(light_illustrations), len(dark_illustrations)

def main():
    """Main execution function"""
    print("🚀 WLSQ Illustration Converter")
    print("=" * 50)
    print("Converting Tabler illustrations to WLSQ brand colors...")
    print("Preserving original shapes and designs ✨")
    print()
    
    converter = WLSQIllustrationConverter()
    
    try:
        light_count, dark_count = converter.create_collections()
        total_count = light_count + dark_count
        
        print()
        print("📊 Conversion Summary:")
        print("=" * 30)
        print(f"🌞 Light illustrations: {light_count}")
        print(f"🌙 Dark illustrations:  {dark_count}")
        print(f"📈 Total converted:     {total_count}")
        print()
        print("🎨 WLSQ Color Palette Applied:")
        print(f"  • Primary:   {converter.wlsq_colors['primary']}")
        print(f"  • Secondary: {converter.wlsq_colors['secondary']}")
        print(f"  • Accent:    {converter.wlsq_colors['accent']}")
        print(f"  • Dark:      {converter.wlsq_colors['dark']}")
        print(f"  • Light:     {converter.wlsq_colors['light']}")
        print()
        print("🎉 Conversion completed successfully!")
        print("Ready to update collections index and deploy! 🚀")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())