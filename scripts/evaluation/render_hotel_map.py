import math
import urllib.request
import io
import os
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def main():
    zoom = 11
    df = pd.read_csv('data/processed/cleaned/delhi_hotels_cleaned.csv').dropna(subset=['latitude', 'longitude', 'rating', 'review_count'])

    min_lat, max_lat = df['latitude'].min() - 0.02, df['latitude'].max() + 0.02
    min_lon, max_lon = df['longitude'].min() - 0.02, df['longitude'].max() + 0.02

    x0, y1 = deg2num(min_lat, min_lon, zoom)
    x1, y0 = deg2num(max_lat, max_lon, zoom)

    from PIL import Image
    width = (x1 - x0 + 1) * 256
    height = (y1 - y0 + 1) * 256
    map_img = Image.new('RGB', (width, height), (245, 245, 245))

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    # Use OpenStreetMap or CartoDB Positron tiles
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            url = f'https://tile.openstreetmap.org/{zoom}/{x}/{y}.png'
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=8) as resp:
                    tile = Image.open(io.BytesIO(resp.read()))
                    map_img.paste(tile, ((x - x0) * 256, (y - y0) * 256))
            except Exception as e:
                # Fallback to CartoDB Positron
                try:
                    fallback_url = f'https://basemaps.cartocdn.com/rastertiles/voyager/{zoom}/{x}/{y}.png'
                    req = urllib.request.Request(fallback_url, headers=headers)
                    with urllib.request.urlopen(req, timeout=8) as resp:
                        tile = Image.open(io.BytesIO(resp.read()))
                        map_img.paste(tile, ((x - x0) * 256, (y - y0) * 256))
                except Exception as ex2:
                    print(f'Error fetching tile {x},{y}: {e}, {ex2}')

    nw_lat, nw_lon = num2deg(x0, y0, zoom)
    se_lat, se_lon = num2deg(x1 + 1, y1 + 1, zoom)

    extent = [nw_lon, se_lon, se_lat, nw_lat]

    fig, ax = plt.subplots(figsize=(15, 10), dpi=200)
    ax.imshow(map_img, extent=extent, aspect='auto')

    # Plot hotels with size reflecting review count and color reflecting rating (matching Plotly IceFire/plasma styling)
    sizes = np.clip((df['review_count'] ** 0.55) * 8, 25, 450)
    sc = ax.scatter(
        df['longitude'],
        df['latitude'],
        c=df['rating'],
        s=sizes,
        cmap='turbo',
        alpha=0.75,
        edgecolors='#1e293b',
        linewidth=0.6,
        zorder=3
    )

    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    ax.set_title('Interactive Geographic Distribution of Delhi NCR Hotels', fontsize=18, fontweight='bold', pad=16, color='#0f172a')
    ax.set_xlabel('Longitude', fontsize=12, fontweight='bold', labelpad=8)
    ax.set_ylabel('Latitude', fontsize=12, fontweight='bold', labelpad=8)

    # Grid styling
    ax.grid(True, linestyle='--', alpha=0.4, color='#64748b')

    cbar = plt.colorbar(sc, ax=ax, fraction=0.035, pad=0.02)
    cbar.set_label('Rating (1.0 - 5.0 Stars)', fontsize=12, fontweight='bold', labelpad=10)
    cbar.ax.tick_params(labelsize=10)

    # Annotate key geographic hubs
    hubs = [
        ("Central Delhi\n(Paharganj / Connaught Place)", 77.2167, 28.6448),
        ("Gurugram Tech Corridor\n(Cyber City / Sector 29)", 77.0890, 28.4900),
        ("IGI Airport / Mahipalpur Hub", 77.1200, 28.5562),
        ("Noida Sector 18\n(Commercial Hub)", 77.3250, 28.5700)
    ]
    for label, lon, lat in hubs:
        ax.annotate(
            label,
            xy=(lon, lat),
            xytext=(lon + 0.03, lat + 0.035),
            bbox=dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#0f2043", lw=1.2, alpha=0.92),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2", color="#0f2043", lw=1.5),
            fontsize=9.5,
            fontweight='bold',
            color='#0f2043',
            zorder=5
        )

    plt.tight_layout()
    os.makedirs('Report_Website/figs', exist_ok=True)
    out_path = 'Report_Website/figs/01_hotel_map_interactive.png'
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == '__main__':
    main()
