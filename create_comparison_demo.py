#!/usr/bin/env python3
"""
Create a comparison demo showing original vs WLSQ illustrations
"""

import json

def create_comparison_demo():
    # Load both collections
    with open('base64_collections/tabler_illustrations_light.json') as f:
        tabler = json.load(f)
    with open('base64_collections/wlsq_illustrations_light.json') as f:
        wlsq = json.load(f)

    # Get a sample illustration (error page)
    tabler_key = '403'
    wlsq_key = 'wlsq_403'

    if tabler_key in tabler and wlsq_key in wlsq:
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>WLSQ vs Tabler Illustration Comparison</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
        .comparison {{ display: flex; gap: 20px; margin: 20px 0; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #56477e; text-align: center; }}
        h3 {{ margin-top: 0; }}
        img {{ max-width: 300px; height: auto; }}
        .stats {{ text-align: center; margin-top: 30px; padding: 20px; background: white; border-radius: 8px; }}
    </style>
</head>
<body>
    <h1>🎨 WLSQ Brand Illustration Conversion</h1>
    <p style="text-align: center; color: #666;">Comparing original Tabler colors vs WLSQ brand colors</p>
    
    <div class="comparison">
        <div class="card">
            <h3>Original Tabler (Blue Theme)</h3>
            <img src="{tabler[tabler_key]}" alt="Original 403 illustration" />
            <p><strong>Colors:</strong> #066FD1 (blue), standard grays</p>
        </div>
        
        <div class="card">
            <h3>WLSQ Brand Version (Purple Theme)</h3>
            <img src="{wlsq[wlsq_key]}" alt="WLSQ 403 illustration" />
            <p><strong>Colors:</strong> #56477e (purple), #7e67a5 (secondary)</p>
        </div>
    </div>
    
    <div class="stats">
        <h3>✨ What Changed</h3>
        <p>✅ Preserved original shapes and designs</p>
        <p>🎨 Applied WLSQ brand color palette (#56477e primary purple)</p>
        <p>📈 Maintained visual consistency across {len(wlsq)} illustrations</p>
        <p>🚀 Ready for deployment in WLSQ branded applications</p>
    </div>
</body>
</html>"""
        
        with open('wlsq_illustration_comparison.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('✅ Created comparison demo: wlsq_illustration_comparison.html')
        return True
    else:
        print('❌ Sample illustrations not found')
        return False

if __name__ == "__main__":
    create_comparison_demo()