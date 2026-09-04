import json
import plotly.graph_objects as go

with open('research/notebooks/01_hotel_metadata_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

fig_json = nb['cells'][9]['outputs'][1]['data']['application/vnd.plotly.v1+json']
fig = go.Figure(fig_json)

# Shift map center to lon: 77.20 and zoom: 9.20 so East Delhi / Noida / Ghaziabad have balanced space
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    autosize=True,
    mapbox=dict(
        style='open-street-map',
        zoom=9.20,
        center=dict(lat=28.58, lon=77.20)  # Balanced center shifted to the right (East)
    ),
    title=None
)

html_content = fig.to_html(
    include_plotlyjs='cdn',
    full_html=True,
    config=dict(
        responsive=True,
        scrollZoom=True,
        displayModeBar=True,
        displaylogo=False,
        modeBarButtonsToRemove=['lasso2d', 'select2d']
    )
)

# Custom styling and JavaScript boundary lock
custom_script = """
<style>
  html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: transparent;
  }
  .plotly-graph-div {
    width: 100% !important;
    height: 100% !important;
  }
  .modebar-container {
    top: 8px !important;
    right: 8px !important;
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 6px !important;
    padding: 2px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.15) !important;
  }
</style>
<script>
  document.addEventListener('DOMContentLoaded', () => {
    let attempts = 0;
    const lockTimer = setInterval(() => {
      attempts++;
      const gd = document.querySelector('.plotly-graph-div');
      if (gd && gd._fullLayout && gd._fullLayout.mapbox && gd._fullLayout.mapbox._subplot && gd._fullLayout.mapbox._subplot.map) {
        const map = gd._fullLayout.mapbox._subplot.map;
        map.setMinZoom(8.7);
        map.setMaxZoom(17.0);
        map.setMaxBounds([
          [76.35, 28.00], // Southwest boundary
          [77.80, 29.20]  // Northeast boundary
        ]);
        clearInterval(lockTimer);
      }
      if (attempts > 50) clearInterval(lockTimer);
    }, 150);
  });
</script>
"""
html_content = html_content.replace('</head>', custom_script + '</head>')

with open('Report_Website/figs/01_hotel_map_interactive.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Regenerated Report_Website/figs/01_hotel_map_interactive.html with shifted center (lon: 77.20, zoom: 9.20)!")
