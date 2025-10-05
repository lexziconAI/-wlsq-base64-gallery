#!/usr/bin/env python3
"""
WLSQ Avatar Generator
Creates brand-compliant avatars following the WLSQ style guide
"""

import base64
import json
import random
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET


class WLSQAvatarGenerator:
    """Generate WLSQ brand-compliant avatars using SVG."""
    
    # WLSQ Brand Colors (from style guide)
    COLORS = {
        # Primary brand colors
        'purple_primary': '#56477e',
        'purple_secondary': '#7e67a5', 
        'teal_dark': '#07577a',
        'dark_grey': '#231f20',
        
        # Supporting colors
        'seafoam': '#69818b',
        'teal_light': '#bfcbcb',
        'wheat': '#dde0cd',
        'grey': '#c4c0b7',
        'light_grey': '#e4e3de',
        
        # Avatar-specific approved colors
        'avatar_purple_jacket': '#8b7ba8',
        'avatar_purple_dark': '#4a3a5c',
        'avatar_grey_light': '#c5cac9',
        'avatar_grey_medium': '#7a8b8f',
        'avatar_beige': '#b8af9d',
        'avatar_navy': '#2c3e4f',
        'avatar_teal': '#5a7d8a',
    }
    
    # Clothing color schemes following brand guidelines
    CLOTHING_SCHEMES = [
        # Professional purple (primary brand)
        {'top': 'avatar_purple_jacket', 'bottom': 'avatar_grey_light', 'accent': 'purple_primary'},
        {'top': 'purple_secondary', 'bottom': 'dark_grey', 'accent': 'avatar_teal'},
        
        # Neutral professional
        {'top': 'seafoam', 'bottom': 'avatar_grey_medium', 'accent': 'teal_dark'},
        {'top': 'grey', 'bottom': 'avatar_navy', 'accent': 'purple_primary'},
        
        # Light/approachable combinations
        {'top': 'teal_light', 'bottom': 'avatar_grey_light', 'accent': 'purple_secondary'},
        {'top': 'light_grey', 'bottom': 'avatar_grey_medium', 'accent': 'teal_dark'},
    ]
    
    # Hair styles (different path definitions)
    HAIR_STYLES = [
        # Short professional
        "M75,85 Q70,70 80,60 Q90,55 100,55 Q110,55 120,60 Q130,70 125,85 Q120,75 110,75 Q100,73 90,75 Q80,75 75,85 Z",
        
        # Medium length
        "M70,88 Q65,65 75,55 Q85,50 100,50 Q115,50 125,55 Q135,65 130,88 Q125,90 120,85 Q115,80 105,78 Q100,77 95,78 Q85,80 80,85 Q75,90 70,88 Z",
        
        # Longer style
        "M68,90 Q60,70 70,55 Q80,45 100,45 Q120,45 130,55 Q140,70 132,90 Q135,95 130,100 Q120,95 110,90 Q105,88 100,88 Q95,88 90,90 Q80,95 70,100 Q65,95 68,90 Z",
        
        # Bob cut
        "M72,87 Q68,72 78,58 Q88,52 100,52 Q112,52 122,58 Q132,72 128,87 Q128,92 125,90 Q118,85 110,83 Q100,82 90,83 Q82,85 75,90 Q72,92 72,87 Z",
        
        # Pixie cut
        "M78,82 Q75,70 82,62 Q88,58 100,58 Q112,58 118,62 Q125,70 122,82 Q118,78 112,76 Q106,75 100,75 Q94,75 88,76 Q82,78 78,82 Z",
    ]
    
    # Body poses (different arm positions)
    ARM_POSES = [
        # Arms at sides
        {
            'left': "M65,130 Q50,140 45,160 Q47,180 52,175",
            'right': "M135,130 Q150,140 155,160 Q153,180 148,175"
        },
        # Arms slightly raised
        {
            'left': "M68,128 Q52,125 48,145 Q50,165 55,160",
            'right': "M132,128 Q148,125 152,145 Q150,165 145,160"
        },
        # Crossed arms (professional)
        {
            'left': "M70,135 Q85,140 95,145 Q100,148 105,145",
            'right': "M130,135 Q115,140 105,145 Q100,148 95,145"
        },
        # One hand on hip
        {
            'left': "M65,130 Q55,135 58,155 Q62,170 68,165",
            'right': "M135,130 Q150,140 155,160 Q153,180 148,175"
        },
    ]

    def __init__(self):
        self.output_dir = Path("wlsq_avatars")
        self.output_dir.mkdir(exist_ok=True)

    def create_avatar_svg(self, 
                         clothing_scheme: Dict[str, str],
                         hair_style: str,
                         arm_pose: Dict[str, str],
                         avatar_id: str) -> str:
        """Create a single WLSQ-branded avatar SVG."""
        
        # Get colors
        top_color = self.COLORS[clothing_scheme['top']]
        bottom_color = self.COLORS[clothing_scheme['bottom']]
        accent_color = self.COLORS[clothing_scheme['accent']]
        hair_color = self.COLORS['avatar_navy']
        skin_color = self.COLORS['avatar_beige']
        
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300" style="background: transparent;">
  <!-- Drop shadow -->
  <ellipse cx="100" cy="285" rx="45" ry="6" fill="#000000" opacity="0.08"/>
  
  <!-- Body/Top -->
  <rect x="72" y="120" width="56" height="95" rx="8" fill="{top_color}"/>
  
  <!-- Arms -->
  <path d="{arm_pose['left']}" stroke="none" fill="{top_color}" stroke-width="0"/>
  <path d="{arm_pose['right']}" stroke="none" fill="{top_color}"/>
  
  <!-- Pants/Bottom -->
  <rect x="76" y="210" width="20" height="75" rx="4" fill="{bottom_color}"/>
  <rect x="104" y="210" width="20" height="75" rx="4" fill="{bottom_color}"/>
  
  <!-- Shoes -->
  <ellipse cx="86" cy="285" rx="10" ry="5" fill="{hair_color}"/>
  <ellipse cx="114" cy="285" rx="10" ry="5" fill="{hair_color}"/>
  
  <!-- Collar/Accent -->
  <rect x="90" y="120" width="20" height="8" rx="2" fill="{accent_color}"/>
  
  <!-- Head -->
  <circle cx="100" cy="85" r="28" fill="{skin_color}"/>
  
  <!-- Hair -->
  <path d="{hair_style}" fill="{hair_color}"/>
  
  <!-- Neck -->
  <rect x="92" y="108" width="16" height="12" rx="8" fill="{skin_color}"/>
</svg>'''
        
        return svg_content

    def generate_avatar_set(self, count: int = 25) -> Dict[str, str]:
        """Generate a set of diverse WLSQ avatars."""
        avatars = {}
        
        for i in range(count):
            # Create variations
            clothing = random.choice(self.CLOTHING_SCHEMES)
            hair = random.choice(self.HAIR_STYLES)
            pose = random.choice(self.ARM_POSES)
            
            avatar_id = f"wlsq_avatar_{i+1:02d}"
            
            # Generate SVG
            svg_content = self.create_avatar_svg(clothing, hair, pose, avatar_id)
            
            # Minify SVG
            svg_minified = self.minify_svg(svg_content)
            
            # Convert to base64
            base64_uri = self.svg_to_base64(svg_minified)
            
            avatars[avatar_id] = base64_uri
            
            # Save individual SVG file
            svg_path = self.output_dir / f"{avatar_id}.svg"
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_minified)
        
        return avatars

    def create_professional_variants(self) -> Dict[str, str]:
        """Create specific professional avatar variants."""
        variants = {}
        
        # Leadership avatar (primary purple)
        leadership_svg = self.create_avatar_svg(
            {'top': 'purple_primary', 'bottom': 'dark_grey', 'accent': 'avatar_teal'},
            self.HAIR_STYLES[1],  # Medium professional
            self.ARM_POSES[2],    # Crossed arms
            'wlsq_leadership'
        )
        variants['wlsq_leadership'] = self.svg_to_base64(self.minify_svg(leadership_svg))
        
        # Client services (approachable)
        client_svg = self.create_avatar_svg(
            {'top': 'teal_light', 'bottom': 'avatar_grey_light', 'accent': 'purple_secondary'},
            self.HAIR_STYLES[3],  # Bob cut
            self.ARM_POSES[1],    # Slightly raised
            'wlsq_client_services'
        )
        variants['wlsq_client_services'] = self.svg_to_base64(self.minify_svg(client_svg))
        
        # Legal advocate (professional)
        legal_svg = self.create_avatar_svg(
            {'top': 'avatar_purple_jacket', 'bottom': 'avatar_grey_medium', 'accent': 'teal_dark'},
            self.HAIR_STYLES[0],  # Short professional
            self.ARM_POSES[3],    # Hand on hip
            'wlsq_legal_advocate'
        )
        variants['wlsq_legal_advocate'] = self.svg_to_base64(self.minify_svg(legal_svg))
        
        return variants

    def minify_svg(self, svg_content: str) -> str:
        """Remove unnecessary whitespace from SVG."""
        import re
        # Remove comments
        svg_content = re.sub(r'<!--.*?-->', '', svg_content, flags=re.DOTALL)
        # Remove whitespace between tags
        svg_content = re.sub(r'>\s+<', '><', svg_content)
        # Remove leading/trailing whitespace
        return svg_content.strip()

    def svg_to_base64(self, svg_content: str) -> str:
        """Convert SVG to base64 data URI."""
        svg_bytes = svg_content.encode('utf-8')
        b64 = base64.b64encode(svg_bytes).decode('utf-8')
        return f"data:image/svg+xml;base64,{b64}"

    def save_collection(self, avatars: Dict[str, str], filename: str = "wlsq_avatars.json"):
        """Save avatar collection to JSON file."""
        output_path = Path("base64_collections") / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(avatars, f, indent=2, ensure_ascii=False)
        
        file_size = output_path.stat().st_size / 1024 / 1024  # MB
        print(f"💾 Saved WLSQ avatars: {filename} ({file_size:.1f} MB)")
        return output_path


def main():
    generator = WLSQAvatarGenerator()
    
    print("🎨 Generating WLSQ Brand-Compliant Avatars")
    print("=" * 50)
    
    # Generate diverse avatar set
    print("Creating diverse avatar collection...")
    diverse_avatars = generator.generate_avatar_set(30)
    
    # Generate professional variants
    print("Creating professional role variants...")
    professional_avatars = generator.create_professional_variants()
    
    # Combine collections
    all_avatars = {**diverse_avatars, **professional_avatars}
    
    # Save collection
    output_path = generator.save_collection(all_avatars)
    
    print(f"\n✅ Complete!")
    print(f"📊 Generated: {len(all_avatars)} WLSQ avatars")
    print(f"📁 SVG files: {generator.output_dir}/")
    print(f"📄 JSON collection: {output_path}")
    print(f"🎯 Brand compliance: Purple primary, rounded corners, minimal faces")
    
    # Show sample keys
    print(f"\n🔑 Sample avatar keys:")
    for key in list(all_avatars.keys())[:5]:
        print(f"  • {{{{ {key} }}}}")
    
    return all_avatars


if __name__ == "__main__":
    main()