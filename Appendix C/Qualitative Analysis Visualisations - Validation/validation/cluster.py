import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import random
import matplotlib.patches as patches
import matplotlib.colors as mcolors

# Parse the LaTeX table
def parse_latex_table(latex_content):
    # Pattern to match rows in the LaTeX table
    pattern = r'(.*?) & (.*?) & (.*?) \\\\'
    matches = re.findall(pattern, latex_content)
    
    data = []
    for match in matches:
        code = match[0].strip()
        participants = match[1].strip()
        theme = match[2].strip()
        
        # Skip header rows
        if code != '\\textbf{Code}':
            data.append({'code': code, 'participants': participants, 'theme': theme})
    
    return pd.DataFrame(data)

# Read the LaTeX content from file
with open('paste.txt', 'r') as f:
    latex_content = f.read()

# Parse the data
df = parse_latex_table(latex_content)

# Print basic information about the data
print(f"Total entries: {len(df)}")
print(f"Unique participants: {df['participants'].nunique()}")
print(f"Unique themes: {df['theme'].nunique()}")

# Count occurrences of each participant
participant_counts = df['participants'].value_counts()
print("\nParticipant counts:")
print(participant_counts)

# Count occurrences of each theme
theme_counts = df['theme'].value_counts()
print("\nTheme counts:")
print(theme_counts)

# Calculate theme distribution per participant
theme_by_participant = pd.crosstab(df['participants'], df['theme'])
print("\nTheme distribution by participant:")
print(theme_by_participant)

# VISUALIZATION 1: Theme distribution
plt.figure(figsize=(14, 8))
theme_counts.plot(kind='bar', color=plt.cm.tab20.colors[:len(theme_counts)])
plt.title('Distribution of Themes', fontsize=16)
plt.xlabel('Theme', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('theme_distribution.png', dpi=300)
plt.close()

# VISUALIZATION 2: Participant distribution
plt.figure(figsize=(10, 6))
participant_counts.plot(kind='bar', color=plt.cm.Set2.colors[:len(participant_counts)])
plt.title('Distribution of Participants', fontsize=16)
plt.xlabel('Participant', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.tight_layout()
plt.savefig('participant_distribution.png', dpi=300)
plt.close()

# VISUALIZATION 3: Heatmap of themes by participants
plt.figure(figsize=(16, 8))
ax = plt.gca()
im = ax.imshow(theme_by_participant.values, cmap='YlOrRd')

# Set x and y labels
ax.set_xticks(np.arange(len(theme_by_participant.columns)))
ax.set_yticks(np.arange(len(theme_by_participant.index)))
ax.set_xticklabels(theme_by_participant.columns)
ax.set_yticklabels(theme_by_participant.index)

# Rotate x labels and set alignment
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add colorbar
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("Count", rotation=-90, va="bottom")

# Add text annotations on the heatmap
for i in range(len(theme_by_participant.index)):
    for j in range(len(theme_by_participant.columns)):
        text = ax.text(j, i, theme_by_participant.iloc[i, j],
                       ha="center", va="center", color="black")

plt.title('Theme Distribution by Participant', fontsize=16)
plt.tight_layout()
plt.savefig('theme_participant_heatmap.png', dpi=300)
plt.close()

# VISUALIZATION 4: Network diagram of codes and themes
from networkx import nx
import matplotlib.pyplot as plt

G = nx.Graph()

# Add nodes for codes and themes
for _, row in df.iterrows():
    G.add_node(row['code'], type='code')
    G.add_node(row['theme'], type='theme')
    G.add_edge(row['code'], row['theme'])

# Set positions using spring layout
pos = nx.spring_layout(G, k=0.3, iterations=50)

plt.figure(figsize=(20, 16))
# Draw nodes
code_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'code']
theme_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'theme']

nx.draw_networkx_nodes(G, pos, nodelist=code_nodes, node_color='skyblue', 
                      node_size=200, alpha=0.8)
nx.draw_networkx_nodes(G, pos, nodelist=theme_nodes, node_color='salmon', 
                      node_size=500, alpha=0.8)

# Draw edges
nx.draw_networkx_edges(G, pos, alpha=0.2)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=8)

plt.title('Network of Codes and Themes', fontsize=20)
plt.axis('off')
plt.tight_layout()
plt.savefig('code_theme_network.png', dpi=300)
plt.close()

# VISUALIZATION 5: Circular layout of themes
plt.figure(figsize=(16, 16))

# Create a circular layout for themes
unique_themes = df['theme'].unique()
theme_pos = {}
num_themes = len(unique_themes)
radius = 10

for i, theme in enumerate(unique_themes):
    angle = 2 * np.pi * i / num_themes
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    theme_pos[theme] = (x, y)

# Draw themes as larger nodes
for theme, (x, y) in theme_pos.items():
    color = plt.cm.tab20(hash(theme) % 20)
    plt.scatter(x, y, s=1000, color=color, alpha=0.7, edgecolors='black')
    plt.text(x, y, theme, fontsize=12, ha='center', va='center', fontweight='bold')
    
    # Get codes for this theme
    codes = df[df['theme'] == theme]['code'].tolist()
    
    # Position codes around the theme
    num_codes = len(codes)
    code_radius = 3
    
    for j, code in enumerate(codes):
        angle_offset = 2 * np.pi * j / num_codes
        code_x = x + code_radius * np.cos(angle_offset)
        code_y = y + code_radius * np.sin(angle_offset)
        
        # Draw a line from theme to code
        plt.plot([x, code_x], [y, code_y], color='gray', alpha=0.5)
        
        # Draw code node
        participant = df[df['code'] == code]['participants'].values[0]
        participant_color = 'blue' if participant == 'PV1' else 'green' if participant == 'PV2' else 'red'
        plt.scatter(code_x, code_y, s=300, color=participant_color, alpha=0.7, edgecolors='black')
        
        # Add code text with small offset
        text_offset_x = 0.3 * np.cos(angle_offset)
        text_offset_y = 0.3 * np.sin(angle_offset)
        plt.text(code_x + text_offset_x, code_y + text_offset_y, code, fontsize=8, ha='center', va='center')

# Add legend for participants
plt.scatter([], [], s=300, color='blue', label='PV1', alpha=0.7, edgecolors='black')
plt.scatter([], [], s=300, color='green', label='PV2', alpha=0.7, edgecolors='black')
plt.scatter([], [], s=300, color='red', label='PV3', alpha=0.7, edgecolors='black')
plt.legend(fontsize=12)

plt.title('Circular Layout of Themes and Codes', fontsize=20)
plt.axis('equal')
plt.axis('off')
plt.tight_layout()
plt.savefig('circular_themes.png', dpi=300)
plt.close()

# VISUALIZATION 6: Sunburst chart (hierarchical visualization)
try:
    import plotly.graph_objects as go
    
    # Create lists of data for the sunburst chart
    participants = []
    themes = []
    codes = []
    
    for _, row in df.iterrows():
        participants.append(row['participants'])
        themes.append(row['participants'] + ' - ' + row['theme'])
        codes.append(row['code'])
    
    # Create parents list - each code points to its theme, each theme points to its participant
    parents = themes + participants + [''] * len(participants)
    labels = codes + themes + participants
    
    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        branchvalues="total",
        insidetextorientation='radial',
        marker=dict(
            colors=np.random.rand(len(labels)),
            colorscale='Viridis',
            line=dict(width=0.5)
        ),
    ))
    
    fig.update_layout(
        title="Hierarchical View: Participants → Themes → Codes",
        width=800,
        height=800,
    )
    
    fig.write_html("sunburst_chart.html")
    print("Sunburst chart created as 'sunburst_chart.html'")
    
except ImportError:
    print("Plotly not installed. Skipping sunburst chart.")

# Create an interactive HTML visualization
def create_interactive_visualization(df):
    # Generate distinct colors for themes
    import colorsys
    
    def get_distinct_colors(n):
        colors = []
        for i in range(n):
            hue = i / n
            lightness = 0.5 + 0.2 * random.random()
            saturation = 0.6 + 0.2 * random.random()
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            hex_color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            colors.append(hex_color)
        return colors
    
    # Get unique themes and assign colors
    unique_themes = sorted(df['theme'].unique())
    theme_colors = {theme: color for theme, color in zip(unique_themes, get_distinct_colors(len(unique_themes)))}
    
    # Calculate positions for visualization
    nodes = []
    
    # Create theme nodes
    theme_positions = {}
    radius = 500
    for i, theme in enumerate(unique_themes):
        angle = 2 * np.pi * i / len(unique_themes)
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        theme_positions[theme] = (x, y)
        
        nodes.append({
            "id": f"theme_{i}",
            "label": theme,
            "x": x,
            "y": y,
            "color": theme_colors[theme],
            "isTheme": True
        })
    
    # Create code nodes around each theme
    for theme in unique_themes:
        theme_x, theme_y = theme_positions[theme]
        theme_df = df[df['theme'] == theme]
        
        # Calculate positions in a circle around the theme
        n_codes = len(theme_df)
        inner_radius = 150
        
        for i, (_, row) in enumerate(theme_df.iterrows()):
            angle = 2 * np.pi * i / n_codes
            
            # Add some jitter to prevent perfect alignment
            jitter_radius = inner_radius * (0.8 + 0.4 * random.random())
            jitter_angle = angle + random.uniform(-0.2, 0.2)
            
            x = theme_x + jitter_radius * np.cos(jitter_angle)
            y = theme_y + jitter_radius * np.sin(jitter_angle)
            
            participant_color = '#4285F4' if row['participants'] == 'PV1' else '#EA4335' if row['participants'] == 'PV2' else '#FBBC05'
            
            nodes.append({
                "id": f"code_{row['code']}",
                "label": row['code'],
                "x": x,
                "y": y,
                "theme": row['theme'],
                "participant": row['participants'],
                "color": participant_color,
                "borderColor": theme_colors[row['theme']]
            })
    
    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Cybersecurity Patterns Visualization</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }}
            .container {{ width: 100%; height: 100vh; position: relative; overflow: hidden; }}
            .node {{ position: absolute; border-radius: 5px; padding: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); 
                    transition: transform 0.3s, box-shadow 0.3s; overflow: hidden; cursor: pointer; }}
            .node:hover {{ transform: scale(1.1); z-index: 10; box-shadow: 0 4px 8px rgba(0,0,0,0.3); }}
            .theme-node {{ border-radius: 50%; text-align: center; display: flex; align-items: center; 
                       justify-content: center; font-weight: bold; z-index: 5; }}
            .edge {{ position: absolute; pointer-events: none; z-index: 1; }}
            .controls {{ position: fixed; top: 10px; left: 10px; z-index: 100; background: white; 
                      padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
            .legend {{ position: fixed; bottom: 10px; left: 10px; background: white; padding: 10px; 
                     border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
            .legend-item {{ display: flex; align-items: center; margin-bottom: 5px; }}
            .legend-color {{ width: 15px; height: 15px; margin-right: 5px; }}
        </style>
    </head>
    <body>
        <div class="controls">
            <button id="zoomIn">Zoom In</button>
            <button id="zoomOut">Zoom Out</button>
            <button id="reset">Reset View</button>
            <select id="filterParticipant">
                <option value="all">All Participants</option>
                <option value="PV1">PV1</option>
                <option value="PV2">PV2</option>
                <option value="PV3">PV3</option>
            </select>
            <select id="filterTheme">
                <option value="all">All Themes</option>
                {' '.join([f'<option value="{theme}">{theme}</option>' for theme in unique_themes])}
            </select>
        </div>
        
        <div class="container" id="visualization"></div>
        
        <div class="legend">
            <h3>Legend</h3>
            <div>
                <h4>Participants:</h4>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #4285F4;"></div>
                    <div>PV1</div>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #EA4335;"></div>
                    <div>PV2</div>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #FBBC05;"></div>
                    <div>PV3</div>
                </div>
            </div>
            <div>
                <h4>Themes:</h4>
                {' '.join([f'<div class="legend-item"><div class="legend-color" style="background-color: {color};"></div><div>{theme}</div></div>' for theme, color in theme_colors.items()])}
            </div>
        </div>
        
        <script>
            // Data from Python
            const nodes = {nodes};
            
            // Setup
            const container = document.getElementById('visualization');
            const width = container.clientWidth;
            const height = container.clientHeight;
            let scale = 1;
            let translateX = width / 2;
            let translateY = height / 2;
            
            // Create nodes and edges
            function createVisualization() {{
                // Clear container
                container.innerHTML = '';
                
                // Get filter values
                const filterParticipant = document.getElementById('filterParticipant').value;
                const filterTheme = document.getElementById('filterTheme').value;
                
                // Create theme nodes
                const themeNodes = nodes.filter(n => n.isTheme);
                const visibleThemes = filterTheme === 'all' ? 
                    themeNodes.map(n => n.label) : 
                    [filterTheme];
                
                // Create edges first (they should be behind nodes)
                nodes.forEach(node => {{
                    if (!node.isTheme) {{
                        // Check if this node should be visible based on filters
                        const themeVisible = visibleThemes.includes(node.theme);
                        const participantVisible = filterParticipant === 'all' || node.participant === filterParticipant;
                        
                        if (themeVisible && participantVisible) {{
                            // Find the associated theme node
                            const themeNode = themeNodes.find(t => t.label === node.theme);
                            
                            if (themeNode) {{
                                // Create an edge
                                const edge = document.createElement('div');
                                edge.className = 'edge';
                                
                                // Position and style the edge
                                const dx = node.x - themeNode.x;
                                const dy = node.y - themeNode.y;
                                const distance = Math.sqrt(dx*dx + dy*dy);
                                const angle = Math.atan2(dy, dx) * 180 / Math.PI;
                                
                                edge.style.width = `${{distance}}px`;
                                edge.style.height = '2px';
                                edge.style.backgroundColor = node.borderColor || '#888';
                                edge.style.opacity = '0.5';
                                edge.style.transformOrigin = '0 0';
                                edge.style.transform = `translate(${{width/2 + themeNode.x * scale}}px, ${{height/2 + themeNode.y * scale}}px) rotate(${{angle}}deg)`;
                                
                                container.appendChild(edge);
                            }}
                        }}
                    }}
                }});
                
                // Create all nodes
                nodes.forEach(node => {{
                    // For theme nodes
                    if (node.isTheme) {{
                        if (filterTheme === 'all' || node.label === filterTheme) {{
                            const themeElement = document.createElement('div');
                            themeElement.className = 'node theme-node';
                            themeElement.textContent = node.label;
                            
                            // Size and position
                            const size = 100;
                            themeElement.style.width = `${{size}}px`;
                            themeElement.style.height = `${{size}}px`;
                            themeElement.style.left = `${{width/2 + (node.x - size/2) * scale}}px`;
                            themeElement.style.top = `${{height/2 + (node.y - size/2) * scale}}px`;
                            
                            // Style
                            themeElement.style.backgroundColor = `${{node.color}}90`;
                            themeElement.style.border = `2px solid ${{node.color}}`;
                            
                            container.appendChild(themeElement);
                        }}
                    }} 
                    // For code nodes
                    else {{
                        // Check if this node should be visible based on filters
                        const themeVisible = visibleThemes.includes(node.theme);
                        const participantVisible = filterParticipant === 'all' || node.participant === filterParticipant;
                        
                        if (themeVisible && participantVisible) {{
                            const codeElement = document.createElement('div');
                            codeElement.className = 'node';
                            
                            // Create inner content
                            const codeText = document.createElement('div');
                            codeText.textContent = node.label;
                            
                            const participantBadge = document.createElement('div');
                            participantBadge.textContent = node.participant;
                            participantBadge.style.fontSize = '10px';
                            participantBadge.style.marginTop = '5px';
                            participantBadge.style.color = '#555';
                            
                            codeElement.appendChild(codeText);
                            codeElement.appendChild(participantBadge);
                            
                            // Size and position
                            codeElement.style.width = '120px';
                            codeElement.style.left = `${{width/2 + (node.x - 60) * scale}}px`;
                            codeElement.style.top = `${{height/2 + (node.y - 15) * scale}}px`;
                            
                            // Style
                            codeElement.style.backgroundColor = `${{node.color}}80`;
                            codeElement.style.border = `2px solid ${{node.borderColor || '#888'}}`;
                            
                            container.appendChild(codeElement);
                        }}
                    }}
                }});
            }}
            
            // Initial creation
            createVisualization();
            
            // Setup event listeners
            document.getElementById('zoomIn').addEventListener('click', () => {{
                scale *= 1.2;
                createVisualization();
            }});
            
            document.getElementById('zoomOut').addEventListener('click', () => {{
                scale /= 1.2;
                createVisualization();
            }});
            
            document.getElementById('reset').addEventListener('click', () => {{
                scale = 1;
                translateX = width / 2;
                translateY = height / 2;
                createVisualization();
            }});
            
            document.getElementById('filterParticipant').addEventListener('change', createVisualization);
            document.getElementById('filterTheme').addEventListener('change', createVisualization);
            
            // Make the visualization responsive
            window.addEventListener('resize', () => {{
                createVisualization();
            }});
            
            // Enable pan functionality
            let isDragging = false;
            let lastX, lastY;
            
            container.addEventListener('mousedown', (e) => {{
                if (e.target === container) {{
                    isDragging = true;
                    lastX = e.clientX;
                    lastY = e.clientY;
                    container.style.cursor = 'grabbing';
                }}
            }});
            
            window.addEventListener('mousemove', (e) => {{
                if (isDragging) {{
                    const dx = e.clientX - lastX;
                    const dy = e.clientY - lastY;
                    translateX += dx;
                    translateY += dy;
                    lastX = e.clientX;
                    lastY = e.clientY;
                    
                    // Update the transform
                    container.style.transform = `translate(${{translateX - width/2}}px, ${{translateY - height/2}}px)`;
                }}
            }});
            
            window.addEventListener('mouseup', () => {{
                isDragging = false;
                container.style.cursor = 'default';
            }});
        </script>
    </body>
    </html>
    """
    
    # Save the HTML file
    with open('interactive_visualization.html', 'w') as f:
        f.write(html_content)
    
    print("Interactive visualization saved as 'interactive_visualization.html'")

# Create the interactive visualization
create_interactive_visualization(df)

print("All visualizations have been created!")

# Export data summary to text file
with open('data_summary.txt', 'w') as f:
    f.write(f"Total entries: {len(df)}\n")
    f.write(f"Unique participants: {df['participants'].nunique()}\n")
    f.write(f"Unique themes: {df['theme'].nunique()}\n\n")
    
    f.write("Participant counts:\n")
    f.write(str(participant_counts) + "\n\n")
    
    f.write("Theme counts:\n")
    f.write(str(theme_counts) + "\n\n")
    
    f.write("Theme distribution by participant:\n")
    f.write(str(theme_by_participant) + "\n")

print("Data summary exported to 'data_summary.txt'")