import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import random
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.path as mpath  # Added this import for Path
import json
import os

def main():
    """
    Main function to run all visualizations for cybersecurity research data
    """
    print("Starting cybersecurity research visualization...")
    
    # Read the content from paste.txt
    try:
        with open('paste.txt', 'r') as file:
            latex_content = file.read()
    except FileNotFoundError:
        print("Error: paste.txt file not found. Please make sure the file exists in the current directory.")
        return
    
    # Parse the LaTeX table
    df = parse_latex_table(latex_content)
    
    # Display basic information about the dataset
    print("\nDataset Overview:")
    print(f"Total entries: {len(df)}")
    print(f"Unique themes: {len(df['theme'].unique())}")
    print(f"Unique codes: {len(df['code'].unique())}")
    print(f"Unique participants: {len(df['participants'].unique())}")
    
    # Count themes and participants
    theme_counts = df['theme'].value_counts()
    participant_counts = df['participants'].value_counts()
    
    print("\nTheme Distribution:")
    print(theme_counts)
    
    print("\nParticipant Distribution:")
    print(participant_counts)
    
    # Create a color map for themes
    unique_themes = df['theme'].unique()
    num_themes = len(unique_themes)
    colors = plt.cm.tab20(np.linspace(0, 1, num_themes))
    theme_colors = {theme: colors[i] for i, theme in enumerate(unique_themes)}
    
    # Add participant_list column to df
    df['participant_list'] = df['participants'].apply(lambda x: x.split(', '))
    
    # Create output directory if it doesn't exist
    os.makedirs('visualizations', exist_ok=True)
    
    # Generate all visualizations
    print("\nGenerating visualizations...")
    
    # Visualization 1: Theme Distribution Chart
    print("Creating theme distribution chart...")
    create_theme_distribution_chart(df, theme_counts, theme_colors)
    
    # Visualization 2: Participant-Theme Network
    print("Creating participant-theme network...")
    create_participant_theme_network(df, unique_themes, theme_counts, theme_colors)
    
    # Visualization 3: Theme Relationship Visualization
    print("Creating theme relationships visualization...")
    create_theme_relationship_viz(df, unique_themes, theme_counts, theme_colors)
    
    # Visualization 4: Code Clustering by Theme
    print("Creating code clustering visualization...")
    create_code_clustering(df, unique_themes, theme_colors)
    
    # Visualization 5: Interactive HTML Visualization
    print("Creating interactive D3.js visualization...")
    create_interactive_visualization(df, theme_counts, theme_colors)
    
    print("\nAll visualizations completed successfully!")
    print("Visualization files saved in the 'visualizations' directory:")
    print("  - theme_distribution.png")
    print("  - participant_theme_network.png")
    print("  - theme_relationships.png")
    print("  - code_clustering.png")
    print("  - interactive_visualization.html")

def parse_latex_table(latex_content):
    """Parse LaTeX table into a pandas DataFrame"""
    pattern = r'(.*?) & (.*?) & (.*?) \\\\'
    matches = re.findall(pattern, latex_content)
    
    data = []
    for match in matches:
        code = match[0].strip()
        participants = match[1].strip()
        theme = match[2].strip()
        
        if code != '\\textbf{Code}':  # Skip header row
            data.append({'code': code, 'participants': participants, 'theme': theme})
    
    return pd.DataFrame(data)

def create_theme_distribution_chart(df, theme_counts, theme_colors):
    """Create horizontal bar chart showing theme distribution"""
    plt.figure(figsize=(14, 10))
    bars = plt.barh(theme_counts.index, theme_counts.values, 
                  color=[theme_colors[theme] for theme in theme_counts.index])
    
    # Add value labels to the bars
    for i, v in enumerate(theme_counts.values):
        plt.text(v + 0.1, i, str(v), va='center')
    
    plt.xlabel('Number of Codes')
    plt.title('Distribution of Cybersecurity Themes')
    plt.tight_layout()
    plt.savefig('visualizations/theme_distribution.png', dpi=300)
    plt.close()

def create_participant_theme_network(df, unique_themes, theme_counts, theme_colors):
    """Create network visualization of participants and themes"""
    plt.figure(figsize=(16, 14))
    ax = plt.gca()
    ax.set_facecolor('#F5F5F5')
    
    # Create a clean version of participant data (some might have multiple)
    df['participant_list'] = df['participants'].apply(lambda x: x.split(', '))
    
    # Create participant positions (in a circle)
    unique_participants = list(set([p for sublist in df['participant_list'].tolist() for p in sublist]))
    num_participants = len(unique_participants)
    participant_angle = {p: 2 * np.pi * i / num_participants for i, p in enumerate(unique_participants)}
    participant_pos = {p: (np.cos(angle) * 8, np.sin(angle) * 8) for p, angle in participant_angle.items()}
    
    # Create theme positions (in a larger circle)
    num_themes = len(unique_themes)
    theme_angle = {t: 2 * np.pi * i / num_themes for i, t in enumerate(unique_themes)}
    theme_pos = {t: (np.cos(angle) * 16, np.sin(angle) * 16) for t, angle in theme_angle.items()}
    
    # Draw theme nodes
    for theme, (x, y) in theme_pos.items():
        count = theme_counts[theme]
        size = np.sqrt(count) * 1500
        color = theme_colors[theme]
        
        circle = plt.Circle((x, y), np.sqrt(size)/50, color=color, alpha=0.7)
        ax.add_patch(circle)
        
        # Theme label
        plt.text(x, y, theme, ha='center', va='center', fontsize=10, 
                 fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
    
    # Draw participant nodes
    for participant, (x, y) in participant_pos.items():
        circle = plt.Circle((x, y), 0.8, color='#3498db', alpha=0.8)
        ax.add_patch(circle)
        plt.text(x, y, participant, ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    
    # Draw connections
    for _, row in df.iterrows():
        theme = row['theme']
        theme_x, theme_y = theme_pos[theme]
        
        for participant in row['participant_list']:
            p_x, p_y = participant_pos[participant]
            
            # Calculate control points for curved line
            mid_x = (theme_x + p_x) / 2
            mid_y = (theme_y + p_y) / 2
            
            # Add some perpendicular offset to create curve
            dx = theme_x - p_x
            dy = theme_y - p_y
            dist = np.sqrt(dx*dx + dy*dy)
            nx = -dy / dist * dist * 0.1  # perpendicular direction
            ny = dx / dist * dist * 0.1
            
            ctrl_x = mid_x + nx
            ctrl_y = mid_y + ny
            
            # Draw curved connection using mpath.Path instead of plt.Path
            connection = mpath.Path([(p_x, p_y), 
                                 (ctrl_x, ctrl_y), 
                                 (theme_x, theme_y)],
                                [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3])
            
            patch = patches.PathPatch(connection, facecolor='none', 
                                     edgecolor=theme_colors[theme], alpha=0.3,
                                     lw=0.8)
            ax.add_patch(patch)
    
    plt.title('Participant-Theme Network in Cybersecurity Research', fontsize=20)
    plt.axis('off')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('visualizations/participant_theme_network.png', dpi=300)
    plt.close()

def create_theme_relationship_viz(df, unique_themes, theme_counts, theme_colors):
    """Create visualization showing relationships between themes"""
    # Create adjacency matrix between themes based on shared codes
    themes = list(unique_themes)
    n = len(themes)
    theme_matrix = np.zeros((n, n))
    
    # For each pair of themes, count how many participants they share
    theme_to_participants = {}
    for theme in themes:
        theme_df = df[df['theme'] == theme]
        participants = set()
        for p_list in theme_df['participant_list']:
            participants.update(p_list)
        theme_to_participants[theme] = participants
    
    # Fill the matrix
    for i, theme1 in enumerate(themes):
        for j, theme2 in enumerate(themes):
            if i != j:  # Avoid self-loops
                shared = len(theme_to_participants[theme1].intersection(theme_to_participants[theme2]))
                theme_matrix[i, j] = shared
    
    plt.figure(figsize=(14, 14))
    ax = plt.gca()
    ax.set_facecolor('#F5F5F5')
    
    # Position themes in a circle
    angle_step = 2 * np.pi / n
    radius = 9
    positions = {}
    
    for i, theme in enumerate(themes):
        angle = i * angle_step
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        positions[theme] = (x, y)
        
        # Create theme node
        color = theme_colors[theme]
        size = theme_counts[theme] * 60
        
        circle = plt.Circle((x, y), np.sqrt(size)/20, color=color, alpha=0.7)
        ax.add_patch(circle)
        
        # Add theme labels
        label_x = x * 1.1
        label_y = y * 1.1
        
        rotation_angle = np.degrees(angle)
        if rotation_angle > 90 and rotation_angle < 270:
            rotation_angle += 180
            ha = 'right'
        else:
            ha = 'left'
            
        plt.text(label_x, label_y, theme, 
                ha=ha, va='center', 
                fontsize=10, fontweight='bold',
                rotation=rotation_angle,
                rotation_mode='anchor',
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
    
    # Draw connections
    max_shared = np.max(theme_matrix)
    if max_shared > 0:  # Avoid division by zero
        for i, theme1 in enumerate(themes):
            x1, y1 = positions[theme1]
            for j, theme2 in enumerate(themes):
                if i < j and theme_matrix[i, j] > 0:  # Only lower triangle to avoid duplicates
                    x2, y2 = positions[theme2]
                    
                    # Calculate width based on relationship strength
                    width = 1 + 4 * (theme_matrix[i, j] / max_shared)
                    
                    # Draw curved connection
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    
                    # Add some perpendicular offset to create curve
                    dx = x2 - x1
                    dy = y2 - y1
                    dist = np.sqrt(dx*dx + dy*dy)
                    nx = -dy / dist * dist * 0.2  # perpendicular direction
                    ny = dx / dist * dist * 0.2
                    
                    ctrl_x = mid_x + nx
                    ctrl_y = mid_y + ny
                    
                    # Draw curved connection using mpath.Path
                    connection = mpath.Path([(x1, y1), 
                                         (ctrl_x, ctrl_y), 
                                         (x2, y2)],
                                        [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3])
                    
                    # Blend colors from both themes
                    conn_color = ((theme_colors[theme1][0] + theme_colors[theme2][0])/2,
                                (theme_colors[theme1][1] + theme_colors[theme2][1])/2,
                                (theme_colors[theme1][2] + theme_colors[theme2][2])/2,
                                0.5)
                    
                    patch = patches.PathPatch(connection, facecolor='none', 
                                             edgecolor=conn_color, alpha=0.5,
                                             lw=width)
                    ax.add_patch(patch)
                    
                    # Add text showing connection strength
                    if theme_matrix[i, j] >= max_shared * 0.5:  # Only label stronger connections
                        plt.text(ctrl_x, ctrl_y, f"{int(theme_matrix[i, j])}", 
                                fontsize=8, ha='center', va='center',
                                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.1'))
    
    plt.title('Theme Relationships in Cybersecurity Research', fontsize=20)
    plt.axis('off')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('visualizations/theme_relationships.png', dpi=300)
    plt.close()

def create_code_clustering(df, unique_themes, theme_colors):
    """Create visualization clustering codes by theme with a boxed layout"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np
    import random
    
    plt.figure(figsize=(24, 20))
    ax = plt.gca()
    ax.set_facecolor('#F5F5F5')
    
    # Calculate layout dimensions
    num_themes = len(unique_themes)
    num_cols = 4  # 4 themes per row as shown in the image
    num_rows = (num_themes + num_cols - 1) // num_cols  # Ceiling division
    
    # Spacing parameters
    horizontal_spacing = 24  # Space between themes horizontally
    vertical_spacing = 16    # Space between themes vertically
    
    # For placing the themes in a grid
    for theme_idx, theme in enumerate(unique_themes):
        # Calculate row and column position
        row = theme_idx // num_cols
        col = theme_idx % num_cols
        
        # Base position for this theme
        theme_x = col * horizontal_spacing
        theme_y = -row * vertical_spacing  # Negative to go downward
        
        # Create theme header box
        box_width = 12
        box_height = 2
        rect = patches.FancyBboxPatch(
            (theme_x - box_width/2, theme_y - box_height/2),
            box_width, box_height,
            boxstyle=patches.BoxStyle("Round", pad=0.6),
            facecolor='white',
            edgecolor=theme_colors[theme],
            linewidth=1.5
        )
        ax.add_patch(rect)
        
        # Add theme label
        plt.text(theme_x, theme_y, theme, ha='center', va='center', 
                fontsize=12, fontweight='bold')
        
        # Get codes for this theme
        theme_df = df[df['theme'] == theme]
        codes = theme_df['code'].tolist()
        n_codes = len(codes)
        
        if n_codes == 0:
            continue
            
        # Arrange codes in horizontal rows below the theme box
        max_codes_per_row = 4  # Maximum codes in a single row
        num_code_rows = (n_codes + max_codes_per_row - 1) // max_codes_per_row
        
        # Start position for codes (below the theme box)
        start_y = theme_y - 3  # Start below the theme box
        
        code_idx = 0
        for row_idx in range(num_code_rows):
            # How many codes in this row
            codes_this_row = min(max_codes_per_row, n_codes - code_idx)
            
            # Horizontal positioning of codes in this row
            for j in range(codes_this_row):
                if code_idx >= len(codes):
                    break
                
                code = codes[code_idx]
                code_idx += 1
                
                # Calculate position for this code
                # Center codes in this row
                offset = (codes_this_row - 1) / 2 if codes_this_row > 1 else 0
                code_x = theme_x + (j - offset) * 3.5  # Horizontal spacing between codes
                code_y = start_y - row_idx * 2.5       # Vertical spacing between rows of codes
                
                # Get participants for this code
                code_df = df[df['code'] == code]
                p_text = ', '.join(code_df['participants'].values)
                
                # Calculate color based on theme
                code_color = theme_colors[theme]
                
                # Draw code node (small horizontal rectangle)
                rect_width, rect_height = 3, 0.8
                rect = patches.Rectangle(
                    (code_x - rect_width/2, code_y - rect_height/2),
                    rect_width, rect_height,
                    facecolor=code_color, alpha=0.6,
                    edgecolor='black', linewidth=1
                )
                ax.add_patch(rect)
                
                # Draw code label
                plt.text(code_x, code_y, code, fontsize=8, ha='center', va='center', weight='bold')
                
                # Draw participant indicator below
                plt.text(code_x, code_y - rect_height - 0.2, f"({p_text})", 
                       fontsize=6, ha='center', va='top', color='#555555')
                
                # Draw dotted line connecting to theme box
                line = plt.Line2D(
                    [theme_x, code_x], 
                    [theme_y - box_height/2, code_y + rect_height/2],
                    color=code_color, alpha=0.5, linewidth=0.8, linestyle='--'
                )
                ax.add_line(line)
    
    plt.title('Cybersecurity Pattern Labels by Cluster (Boxed Layout)', fontsize=24)
    plt.axis('off')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('visualizations/code_clustering.png', dpi=300, bbox_inches='tight')
    plt.close()
    
def create_interactive_visualization(df, theme_counts, theme_colors):
    """Create interactive D3.js visualization"""
    # Prepare theme data for D3
    theme_data_json = []
    for theme, count in theme_counts.items():
        # Convert numpy array color to hex string
        color = theme_colors[theme]
        hex_color = mcolors.rgb2hex(color)
        
        theme_data_json.append({
            "name": theme,
            "count": int(count),
            "color": hex_color
        })
    
    # Prepare code data for D3
    code_data_json = []
    for _, row in df.iterrows():
        code_data_json.append({
            "name": row['code'],
            "theme": row['theme'],
            "participants": row['participant_list']
        })
    
    # Prepare participant data for D3
    participant_data_json = []
    for p, count in df['participants'].value_counts().items():
        participant_data_json.append({
            "name": p,
            "count": int(count)
        })
    
    # Generate the complete HTML content
    try:
        with open('paste.txt', 'r') as file:
            latex_content = file.read()
        # Parse the LaTeX table
        df = parse_latex_table(latex_content)
    except FileNotFoundError:
        # If paste-2.txt doesn't exist, use the data we already have
        pass
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Cybersecurity Research Visualization</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        #visualization { position: relative; width: 100%; height: 800px; background-color: white; border: 1px solid #ddd; border-radius: 5px; }
        .controls { margin-bottom: 20px; }
        button { padding: 8px 16px; margin-right: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .node { cursor: pointer; }
        .link { stroke-opacity: 0.6; }
        .label { font-size: 12px; pointer-events: none; }
        .theme-label { font-weight: bold; font-size: 14px; }
        .tooltip { position: absolute; background-color: white; padding: 8px; border: 1px solid #ddd; border-radius: 4px; pointer-events: none; opacity: 0; }
    </style>
</head>
<body>
    <h1>Cybersecurity Research Visualization</h1>
    <div class="controls">
        <button id="themeBtn" onclick="switchToThemeView()">Theme-centric View</button>
        <button id="participantBtn" onclick="switchToParticipantView()">Participant-centric View</button>
        <button id="resetBtn" onclick="resetVisualization()">Reset</button>
    </div>
    <div id="visualization"></div>
    <div class="tooltip" id="tooltip"></div>
    
    <script>
    // Data loading and visualization
    const width = document.getElementById('visualization').clientWidth;
    const height = document.getElementById('visualization').clientHeight;
    const svg = d3.select('#visualization')
        .append('svg')
        .attr('width', width)
        .attr('height', height);
        
    const tooltip = d3.select('#tooltip');
    
    // Load the data
    const data = {
        nodes: [],
        links: []
    };
    
    const themeData = THEME_DATA;
    const codeData = CODE_DATA;
    const participantData = PARTICIPANT_DATA;
    
    // Create nodes for themes
    themeData.forEach(theme => {
        data.nodes.push({
            id: 'theme-' + theme.name,
            name: theme.name,
            type: 'theme',
            count: theme.count,
            color: theme.color
        });
    });
    
    // Create nodes for codes
    codeData.forEach(code => {
        data.nodes.push({
            id: 'code-' + code.name,
            name: code.name,
            type: 'code',
            theme: code.theme,
            participants: code.participants
        });
    });
    
    // Create nodes for participants
    participantData.forEach(participant => {
        data.nodes.push({
            id: 'participant-' + participant.name,
            name: participant.name,
            type: 'participant',
            count: participant.count
        });
    });
    
    // Create links between themes and codes
    codeData.forEach(code => {
        data.links.push({
            source: 'code-' + code.name,
            target: 'theme-' + code.theme,
            type: 'code-theme'
        });
    });
    
    // Create links between codes and participants
    codeData.forEach(code => {
        code.participants.forEach(participant => {
            data.links.push({
                source: 'code-' + code.name,
                target: 'participant-' + participant,
                type: 'code-participant'
            });
        });
    });
    
    // Force simulation
    const simulation = d3.forceSimulation(data.nodes)
        .force('link', d3.forceLink(data.links).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(d => getNodeRadius(d) + 5));
    
    // Draw links
    const link = svg.append('g')
        .selectAll('line')
        .data(data.links)
        .enter()
        .append('line')
        .attr('class', 'link')
        .attr('stroke', d => getLinkColor(d))
        .attr('stroke-width', d => getLinkWidth(d));
    
    // Draw nodes
    const node = svg.append('g')
        .selectAll('.node')
        .data(data.nodes)
        .enter()
        .append('g')
        .attr('class', 'node')
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended))
        .on('mouseover', showTooltip)
        .on('mouseout', hideTooltip)
        .on('click', handleNodeClick);
    
    // Add circles to nodes
    node.append('circle')
        .attr('r', d => getNodeRadius(d))
        .attr('fill', d => getNodeColor(d))
        .attr('stroke', '#fff')
        .attr('stroke-width', 2);
    
    // Add labels to nodes
    node.append('text')
        .attr('class', d => d.type === 'theme' ? 'label theme-label' : 'label')
        .attr('dx', d => getNodeRadius(d) + 5)
        .attr('dy', '.35em')
        .text(d => d.name);
    
    // Update force simulation
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        
        node.attr('transform', d => `translate(${d.x},${d.y})`);
    });
    
    // Helper functions
    function getNodeRadius(d) {
        if (d.type === 'theme') return 15 + d.count * 2;
        if (d.type === 'participant') return 12 + d.count;
        return 8;
    }
    
    function getNodeColor(d) {
        if (d.type === 'theme') return d.color;
        if (d.type === 'code') {
            const theme = themeData.find(t => t.name === d.theme);
            return theme ? theme.color : '#999';
        }
        return '#3498db';
    }
    
    function getLinkColor(d) {
        if (d.type === 'code-theme') {
            const theme = themeData.find(t => t.name === d.target.name);
            return theme ? theme.color : '#999';
        }
        return '#999';
    }
    
    function getLinkWidth(d) {
        if (d.type === 'code-theme') return 2;
        return 1;
    }
    
    function showTooltip(event, d) {
        let content = '';
        
        if (d.type === 'theme') {
            content = `<strong>${d.name}</strong><br>Codes: ${d.count}`;
        } else if (d.type === 'code') {
            content = `<strong>${d.name}</strong><br>Theme: ${d.theme}<br>Participants: ${d.participants.join(', ')}`;
        } else if (d.type === 'participant') {
            content = `<strong>${d.name}</strong><br>Codes: ${d.count}`;
        }
        
        tooltip.html(content)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px')
            .style('opacity', 0.9);
    }
    
    function hideTooltip() {
        tooltip.style('opacity', 0);
    }
    
    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }
    
    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }
    
    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }
    
    function switchToThemeView() {
        simulation.stop();
        
        // Position themes in a circle
        const themeNodes = data.nodes.filter(d => d.type === 'theme');
        const numThemes = themeNodes.length;
        const themeRadius = Math.min(width, height) * 0.35;
        
        themeNodes.forEach((node, i) => {
            const angle = (i / numThemes) * 2 * Math.PI;
            node.fx = width/2 + themeRadius * Math.cos(angle);
            node.fy = height/2 + themeRadius * Math.sin(angle);
        });
        
        // Reset other node positions
        data.nodes.filter(d => d.type !== 'theme').forEach(node => {
            node.fx = null;
            node.fy = null;
        });
        
        simulation.alpha(1).restart();
    }
    
    function switchToParticipantView() {
    simulation.stop();
    
    // Position participants in a circle
    const participantNodes = data.nodes.filter(d => d.type === 'participant');
    const numParticipants = participantNodes.length;
    const participantRadius = Math.min(width, height) * 0.35;
    
    participantNodes.forEach((node, i) => {
        const angle = (i / numParticipants) * 2 * Math.PI;
        node.fx = width/2 + participantRadius * Math.cos(angle);
        node.fy = height/2 + participantRadius * Math.sin(angle);
    });
    
    // Reset other node positions
    data.nodes.filter(d => d.type !== 'participant').forEach(node => {
        node.fx = null;
        node.fy = null;
    });
    
    simulation.alpha(1).restart();
}

function resetVisualization() {
    // Clear fixed positions for all nodes
    data.nodes.forEach(node => {
        node.fx = null;
        node.fy = null;
    });
    
    // Restart simulation
    simulation.alpha(1).restart();
}

function handleNodeClick(event, d) {
    // Stop event propagation
    event.stopPropagation();
    
    // Highlight connections for clicked node
    if (d.type === 'theme') {
        highlightThemeConnections(d);
    } else if (d.type === 'participant') {
        highlightParticipantConnections(d);
    } else if (d.type === 'code') {
        highlightCodeConnections(d);
    }
}

function highlightThemeConnections(themeNode) {
    // Reset all opacities
    link.attr('stroke-opacity', 0.2);
    node.attr('opacity', 0.2);
    
    // Highlight the theme node
    node.filter(n => n.id === themeNode.id)
        .attr('opacity', 1);
    
    // Find all codes for this theme
    const connectedCodes = data.links
        .filter(l => l.target.id === themeNode.id)
        .map(l => l.source.id);
    
    // Highlight connected codes
    node.filter(n => connectedCodes.includes(n.id))
        .attr('opacity', 1);
    
    // Highlight theme-code links
    link.filter(l => l.target.id === themeNode.id)
        .attr('stroke-opacity', 0.8);
}

function highlightParticipantConnections(participantNode) {
    // Reset all opacities
    link.attr('stroke-opacity', 0.2);
    node.attr('opacity', 0.2);
    
    // Highlight the participant node
    node.filter(n => n.id === participantNode.id)
        .attr('opacity', 1);
    
    // Find all codes for this participant
    const connectedCodes = data.links
        .filter(l => l.target.id === participantNode.id)
        .map(l => l.source.id);
    
    // Highlight connected codes
    node.filter(n => connectedCodes.includes(n.id))
        .attr('opacity', 1);
    
    // Find themes for these codes
    const connectedThemes = data.links
        .filter(l => connectedCodes.includes(l.source.id) && l.type === 'code-theme')
        .map(l => l.target.id);
    
    // Highlight connected themes
    node.filter(n => connectedThemes.includes(n.id))
        .attr('opacity', 1);
    
    // Highlight participant-code links
    link.filter(l => l.target.id === participantNode.id)
        .attr('stroke-opacity', 0.8);
    
    // Highlight code-theme links for connected codes
    link.filter(l => connectedCodes.includes(l.source.id) && l.type === 'code-theme')
        .attr('stroke-opacity', 0.8);
}

function highlightCodeConnections(codeNode) {
    // Reset all opacities
    link.attr('stroke-opacity', 0.2);
    node.attr('opacity', 0.2);
    
    // Highlight the code node
    node.filter(n => n.id === codeNode.id)
        .attr('opacity', 1);
    
    // Find theme for this code
    const connectedTheme = data.links
        .filter(l => l.source.id === codeNode.id && l.type === 'code-theme')
        .map(l => l.target.id)[0];
    
    // Find participants for this code
    const connectedParticipants = data.links
        .filter(l => l.source.id === codeNode.id && l.type === 'code-participant')
        .map(l => l.target.id);
    
    // Highlight connected theme
    node.filter(n => n.id === connectedTheme)
        .attr('opacity', 1);
    
    // Highlight connected participants
    node.filter(n => connectedParticipants.includes(n.id))
        .attr('opacity', 1);
    
    // Highlight all links for this code
    link.filter(l => l.source.id === codeNode.id)
        .attr('stroke-opacity', 0.8);
}

// Initialize with theme-centric view
switchToThemeView();
</script>
</body>
</html>
"""

    # Replace placeholders with actual data
    html_content = html_content.replace('THEME_DATA', json.dumps(theme_data_json))
    html_content = html_content.replace('CODE_DATA', json.dumps(code_data_json))
    html_content = html_content.replace('PARTICIPANT_DATA', json.dumps(participant_data_json))
    
    # Write HTML to file
    with open('visualizations/interactive_visualization.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    main()