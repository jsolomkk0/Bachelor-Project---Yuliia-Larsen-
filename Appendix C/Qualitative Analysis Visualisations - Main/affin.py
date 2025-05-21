import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import random
import matplotlib.patches as patches
import matplotlib.colors as mcolors

# Parse the LaTeX table
def parse_latex_table(latex_content):
    pattern = r'(.*?) & (.*?) & (.*?) \\\\'
    matches = re.findall(pattern, latex_content)
    
    data = []
    for match in matches:
        pattern_label = match[0].strip()
        source = match[1].strip()
        cluster = match[2].strip()
        
        if pattern_label != '\\textbf{Pattern Label}':  # Skip header row
            data.append({'pattern_label': pattern_label, 'source': source, 'cluster': cluster})
    
    return pd.DataFrame(data)

# Sample LaTeX content from the provided data
latex_content = r"""
\begin{longtable}{|p{0.45\textwidth}|p{0.15\textwidth}|p{0.4\textwidth}|}
\hline
\textbf{Pattern Label} & \textbf{Source} & \textbf{Cluster} \\
\hline
\endhead

% Cluster: Healthcare Security Vulnerabilities
Medical Data Vulnerability & Survey & Healthcare Security Vulnerabilities \\
\hline
Medical System Breach Example & Survey & Healthcare Security Vulnerabilities \\
\hline
Ransomware Response Strategy & Survey & Healthcare Security Vulnerabilities \\
\hline
Healthcare Data Breach & Interview & Healthcare Security Vulnerabilities \\
\hline
Healthcare Targeting Risk & Interview & Healthcare Security Vulnerabilities \\
\hline
Healthcare Impact Assessment & Survey & Healthcare Security Vulnerabilities \\
\hline

% Cluster: Digital Infrastructure Challenges
Digital Identity Infrastructure & Interview & Digital Infrastructure Challenges \\
\hline
Authentication System Weakness & Interview & Digital Infrastructure Challenges \\
\hline
Legacy System Dependence & Interview & Digital Infrastructure Challenges \\
\hline
Resource Limitation Impact & Interview & Digital Infrastructure Challenges \\
\hline
Digital Ecosystem Vulnerability & Interview & Digital Infrastructure Challenges \\
\hline

% Cluster: Critical Infrastructure Protection
Critical Infrastructure Targeting & Survey & Critical Infrastructure Protection \\
\hline
Utility Infrastructure Disruption & Interview & Critical Infrastructure Protection \\
\hline
Democratic Process Vulnerability & Interview & Critical Infrastructure Protection \\
\hline
Energy Sector Targeting & Survey & Critical Infrastructure Protection \\
\hline
Civilian Infrastructure Targeting & Interview & Critical Infrastructure Protection \\
\hline

% Cluster: Advanced Attack Strategies
Combined Attack Strategy & Survey & Advanced Attack Strategies \\
\hline
Tactics Evolution & Survey & Advanced Attack Strategies \\
\hline
Combined Disruption Strategy & Interview & Advanced Attack Strategies \\
\hline
Cyber-Physical Attack Coordination & Interview & Advanced Attack Strategies \\
\hline
Advanced Persistence Techniques & Interview & Advanced Attack Strategies \\
\hline
Combined Attack Approach & Survey & Advanced Attack Strategies \\
\hline
Attack Efficiency Characteristics & Survey & Advanced Attack Strategies \\
\hline
Common Attack Methods & Survey & Advanced Attack Strategies \\
\hline

% Cluster: Social Engineering and Human Vulnerabilities
Social Engineering Vulnerability & Interview & Social Engineering and Human Vulnerabilities \\
\hline
Email-Based Threat Dominance & Interview & Social Engineering and Human Vulnerabilities \\
\hline
AI-Enhanced Phishing Evolution & Interview & Social Engineering and Human Vulnerabilities \\
\hline
Cultural Trust Exploitation & Interview & Social Engineering and Human Vulnerabilities \\
\hline
Naive Security Mindset & Interview & Social Engineering and Human Vulnerabilities \\
\hline
Human Security Weakness & Interview & Social Engineering and Human Vulnerabilities \\
\hline
User Behavior Risk & Interview & Social Engineering and Human Vulnerabilities \\
\hline
Attack Vector Statistics & Survey & Social Engineering and Human Vulnerabilities \\
\hline
Social Engineering Prevalence & Interview & Social Engineering and Human Vulnerabilities \\
\hline

% Cluster: Workforce and Expertise Challenges
Generational Security Divide & Interview & Workforce and Expertise Challenges \\
\hline
Training Resource Constraint & Interview & Workforce and Expertise Challenges \\
\hline
Expertise Shortage Impact & Interview & Workforce and Expertise Challenges \\
\hline
Human Capital Investment Need & Interview & Workforce and Expertise Challenges \\
\hline
Workforce Challenge & Survey & Workforce and Expertise Challenges \\
\hline
Leadership Impact & Survey & Workforce and Expertise Challenges \\
\hline

% Cluster: Incident Response and Recovery
Incident Recovery Process & Interview & Incident Response and Recovery \\
\hline
Incident Response Coordination & Interview & Incident Response and Recovery \\
\hline
Parallel Response Methodology & Interview & Incident Response and Recovery \\
\hline
Low-Tech Contingency Planning & Interview & Incident Response and Recovery \\
\hline
Data Recovery Strategy & Survey & Incident Response and Recovery \\
\hline
Containment Strategy & Survey & Incident Response and Recovery \\
\hline
Resilience Mechanism & Survey & Incident Response and Recovery \\
\hline

% Cluster: Governance and Strategic Planning
Response Protocol Deficiency & Interview & Governance and Strategic Planning \\
\hline
Decentralized System Vulnerability & Interview & Governance and Strategic Planning \\
\hline
Historical Security Negligence & Interview & Governance and Strategic Planning \\
\hline
Uncontrolled Technology Acquisition & Interview & Governance and Strategic Planning \\
\hline
Governance Centralization Effort & Interview & Governance and Strategic Planning \\
\hline
Security Function Evolution & Interview & Governance and Strategic Planning \\
\hline
Governance Recommendation & Survey & Governance and Strategic Planning \\
\hline
Defense Strategy & Survey & Governance and Strategic Planning \\
\hline
Best Practice Recommendation & Survey & Governance and Strategic Planning \\
\hline
Security Strategy Effectiveness & Survey & Governance and Strategic Planning \\
\hline

% Cluster: Regulatory and Compliance Matters
Regulatory Compliance Emphasis & Interview & Regulatory and Compliance Matters \\
\hline
False Security Perception & Interview & Regulatory and Compliance Matters \\
\hline
Compliance-Efficiency Tradeoff & Interview & Regulatory and Compliance Matters \\
\hline
Legal Framework Challenges & Survey & Regulatory and Compliance Matters \\
\hline

% Cluster: International Collaboration
National Security Coordination & Interview & International Collaboration \\
\hline
Threat Intelligence Sharing & Interview & International Collaboration \\
\hline
Multi-Level Security Collaboration & Interview & International Collaboration \\
\hline
Regional Defense Coalition & Interview & International Collaboration \\
\hline
Public-Private Security Partnership & Interview & International Collaboration \\
\hline
Cross-Border Intelligence Sharing & Interview & International Collaboration \\
\hline
International Assistance Value & Survey & International Collaboration \\
\hline
Alliance Strengthening & Survey & International Collaboration \\
\hline
Real-time Intelligence Sharing & Survey & International Collaboration \\
\hline
Cross-border Healthcare Security & Survey & International Collaboration \\
\hline
Collaborative Defense & Survey & International Collaboration \\
\hline
Threat Intelligence Application & Survey & International Collaboration \\
\hline

% Cluster: Foreign Technology Considerations
Foreign Technology Reliance & Interview & Foreign Technology Considerations \\
\hline
Technology Sovereignty Need & Interview & Foreign Technology Considerations \\
\hline
Foreign Hardware Distrust & Interview & Foreign Technology Considerations \\
\hline
Foreign AI Restriction & Interview & Foreign Technology Considerations \\
\hline
Market Monopoly Vulnerability & Interview & Foreign Technology Considerations \\
\hline
Foreign Technology Restriction & Interview & Foreign Technology Considerations \\
\hline
Foreign AI Data Extraction & Interview & Foreign Technology Considerations \\
\hline

% Cluster: Geopolitical Security Dimensions
Geopolitical Trust Shift & Interview & Geopolitical Security Dimensions \\
\hline
Alliance Relationship Uncertainty & Interview & Geopolitical Security Dimensions \\
\hline
International Relationship Deterioration & Interview & Geopolitical Security Dimensions \\
\hline
International Collaboration Ban & Interview & Geopolitical Security Dimensions \\
\hline
Geopolitical Instability Exploitation & Interview & Geopolitical Security Dimensions \\
\hline
Cyber Warfare Definition & Interview & Geopolitical Security Dimensions \\
\hline

% Cluster: State-Sponsored Threat Actors
Threat Actor Hierarchy & Interview & State-Sponsored Threat Actors \\
\hline
Intellectual Property Targeting & Interview & State-Sponsored Threat Actors \\
\hline
Long-Term Trust Infiltration & Interview & State-Sponsored Threat Actors \\
\hline
Political Statement Retaliation & Interview & State-Sponsored Threat Actors \\
\hline
Economic Motivation Strategy & Interview & State-Sponsored Threat Actors \\
\hline
State-Sponsored Threat Actors & Interview & State-Sponsored Threat Actors \\
\hline
Russian Threat Primacy & Interview & State-Sponsored Threat Actors \\
\hline
Persistent State Aggression & Interview & State-Sponsored Threat Actors \\
\hline
Russian Cyber Capabilities & Interview & State-Sponsored Threat Actors \\
\hline

% Cluster: Information Operations
Public Opinion Manipulation & Interview & Information Operations \\
\hline
Disinformation Campaign Evidence & Interview & Information Operations \\
\hline
Geographic Access Restriction & Interview & Information Operations \\
\hline
Information Warfare Objectives & Survey & Information Operations \\
\hline
Societal Impact Concern & Interview & Information Operations \\
\hline

% Cluster: Emerging Technology Threats
AI Threat Anticipation & Interview & Emerging Technology Threats \\
\hline
Quantum Cryptography Threat & Interview & Emerging Technology Threats \\
\hline
Post-Quantum Transition Challenge & Interview & Emerging Technology Threats \\
\hline
Advanced Deepfake Capability & Interview & Emerging Technology Threats \\
\hline
AI Circumvention Potential & Interview & Emerging Technology Threats \\
\hline

% Cluster: Biometric Security Considerations
Biometric Defense Mechanism & Interview & Biometric Security Considerations \\
\hline
Behavioral Biometric Authentication & Interview & Biometric Security Considerations \\
\hline
Biometric Spoofing Vulnerability & Interview & Biometric Security Considerations \\
\hline
Neurobiological Identity Marker & Interview & Biometric Security Considerations \\
\hline
Multi-Factor Biometric Security & Interview & Biometric Security Considerations \\
\hline
"""

# Parse the data
df = parse_latex_table(latex_content)

# Count data sources
survey_count = len(df[df['source'] == 'Survey'])
interview_count = len(df[df['source'] == 'Interview'])
print(f"Survey entries: {survey_count}")
print(f"Interview entries: {interview_count}")
print(f"Total entries: {len(df)}")

# Get unique clusters
unique_clusters = df['cluster'].unique()
num_clusters = len(unique_clusters)
print(f"Number of unique clusters: {num_clusters}")

# Create a color map for clusters
colors = plt.cm.tab20(np.linspace(0, 1, num_clusters))
cluster_colors = {cluster: colors[i] for i, cluster in enumerate(unique_clusters)}

# VISUALIZATION 1: Separate by Source (Interview vs Survey)
# CLUSTER VISUALIZATION FIX
# Modify this function to prevent top/bottom congestion
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random

def create_cluster_visualization(df):
    plt.figure(figsize=(72, 60))  # Huge canvas for breathing room
    ax = plt.gca()
    ax.set_facecolor('#F5F5F5')

    num_clusters = len(unique_clusters)
    cluster_centers = {}
    angle_step = 2 * np.pi / num_clusters
    radius = 95  # Very wide spread of clusters from center

    for i, cluster in enumerate(unique_clusters):
        angle = i * angle_step
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        cluster_centers[cluster] = (x, y)

    width, height = 3.4, 0.85  # Wider boxes

    def generate_cluster_positions(center_x, center_y, n):
        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))
        spacing_x = width * 3.2  # More horizontal space
        spacing_y = height * 6.0  # More vertical space

        start_x = center_x - (cols - 1) * spacing_x / 2
        start_y = center_y + (rows - 1) * spacing_y / 2

        positions = []
        for i in range(n):
            row = i // cols
            col = i % cols

            offset = spacing_x / 2 if row % 2 else 0  # Staggered layout
            jitter_x = random.uniform(-1.0, 1.0)
            jitter_y = random.uniform(-1.0, 1.0)

            x = start_x + col * spacing_x + jitter_x + offset
            y = start_y - row * spacing_y + jitter_y
            positions.append((x, y))
        return positions

    for cluster in unique_clusters:
        cluster_df = df[df['cluster'] == cluster]
        center_x, center_y = cluster_centers[cluster]
        color = cluster_colors[cluster]

        # Cluster label
        plt.text(center_x, center_y + 9, cluster, ha='center', va='center',
                 fontsize=22, fontweight='bold',
                 bbox=dict(facecolor='white', alpha=0.95, boxstyle='round,pad=1.4',
                           edgecolor=color, linewidth=2))

        positions = generate_cluster_positions(center_x, center_y, len(cluster_df))

        for i, (_, row) in enumerate(cluster_df.iterrows()):
            x, y = positions[i]
            rect_color = tuple(list(color[:3]) + [0.75]) if row['source'] == 'Interview' else tuple(list(color[:3]) + [0.5])
            edge_color = 'black' if row['source'] == 'Interview' else 'gray'

            rect = patches.Rectangle((x - width / 2, y - height / 2), width, height,
                                     facecolor=rect_color, edgecolor=edge_color,
                                     linewidth=1.3, alpha=0.9)
            ax.add_patch(rect)

            label = row['pattern_label']
            source = "(I)" if row['source'] == "Interview" else "(S)"
            short_text = (label[:36] + "...") if len(label) > 40 else label
            plt.text(x, y, f"{short_text} {source}", fontsize=9,
                     ha='center', va='center', zorder=2)

    #plt.title("Cybersecurity Pattern Labels Grouped by Clusters", fontsize=28)
    plt.axis('off')
    plt.axis('equal')

    legend_elements = [
        patches.Patch(facecolor='lightgray', edgecolor='black', label='Interview (I)'),
        patches.Patch(facecolor='lightgray', edgecolor='gray', label='Survey (S)')
    ]
    plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.02),
               ncol=2, fontsize=16, frameon=True)

    plt.tight_layout()
    plt.savefig("cluster_visualization.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_source_visualization(df):
    plt.figure(figsize=(28, 22))
    ax = plt.gca()
    ax.set_facecolor('#F5F5F5')

    width, height = 2.5, 0.4
    h_spacing = width * 1.4
    v_spacing = height * 3.2
    columns = 8

    def draw_table(source_df, start_x, start_y, title):
        sorted_df = source_df.sort_values(by="cluster")
        rows = int(np.ceil(len(sorted_df) / columns))

        plt.text(start_x + (columns - 1) * h_spacing / 2, start_y + 2,
                 title, ha='center', fontsize=20, fontweight='bold')

        for i, (_, row) in enumerate(sorted_df.iterrows()):
            col = i % columns
            row_idx = i // columns
            jitter_x = random.uniform(-0.1, 0.1)
            jitter_y = random.uniform(-0.1, 0.1)
            x = start_x + col * h_spacing + jitter_x
            y = start_y - row_idx * v_spacing + jitter_y

            color = cluster_colors[row['cluster']]
            rect_color = tuple(list(color[:3]) + [0.7])
            rect = patches.Rectangle((x - width / 2, y - height / 2), width, height,
                                     facecolor=rect_color, edgecolor='black', alpha=0.9,
                                     linewidth=1.0)
            ax.add_patch(rect)

            label = row['pattern_label']
            text = label[:40] + ("..." if len(label) > 40 else "")
            plt.text(x, y, text, fontsize=7, ha='center', va='center')

    interview_df = df[df['source'] == "Interview"]
    survey_df = df[df['source'] == "Survey"]

    draw_table(interview_df, start_x=-20, start_y=10, title="INTERVIEW")
    draw_table(survey_df, start_x=10, start_y=10, title="SURVEY")

    plt.title("Cybersecurity Pattern Labels by Source", fontsize=24)
    plt.axis('off')
    plt.axis('equal')

    legend_elements = [patches.Patch(facecolor=tuple(list(c[:3]) + [0.7]), label=clust)
                       for clust, c in cluster_colors.items()]
    plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.04),
               ncol=4, fontsize=8, frameon=True)

    plt.tight_layout()
    plt.savefig("source_visualization.png", dpi=300, bbox_inches="tight")
    plt.close()

# Create an interactive HTML visualization that can be embedded in Miro
def create_miro_html_visualization(df):
    import json
    from colorsys import hls_to_rgb
    
    # Generate distinct colors for clusters
    def get_distinct_colors(n):
        colors = []
        for i in range(n):
            h = i / n
            l = 0.4 + 0.1 * random.random()
            s = 0.5 + 0.2 * random.random()
            rgb = hls_to_rgb(h, l, s)
            hex_color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            colors.append(hex_color)
        return colors
    
    # Get unique clusters and assign colors
    unique_clusters = sorted(df['cluster'].unique())
    cluster_colors = {cluster: color for cluster, color in zip(unique_clusters, get_distinct_colors(len(unique_clusters)))}
    
    # Calculate positions for the visualization in a more organized way
    # For source-based visualization
    source_nodes = []
    interview_x = -600
    survey_x = 600
    
    # Interview nodes - use a grid layout
    interview_df = df[df['source'] == 'Interview']
    num_interview = len(interview_df)
    grid_size = int(np.ceil(np.sqrt(num_interview * 1.5)))  # Slightly wider grid
    
    for idx, (_, row) in enumerate(interview_df.iterrows()):
        row_idx = idx // grid_size
        col_idx = idx % grid_size
        
        # Calculate position in a grid with some spacing
        base_x = interview_x + (col_idx - grid_size/2) * 100
        base_y = (row_idx - grid_size/2) * 60
        
        # Add small random jitter
        jitter_x = random.uniform(-5, 5)
        jitter_y = random.uniform(-5, 5)
        
        node = {
            "id": f"interview_{idx}",
            "label": row['pattern_label'],
            "cluster": row['cluster'],
            "source": row['source'],
            "x": base_x + jitter_x,
            "y": base_y + jitter_y,
            "color": cluster_colors[row['cluster']]
        }
        source_nodes.append(node)
    
    # Survey nodes - use a grid layout
    survey_df = df[df['source'] == 'Survey']
    num_survey = len(survey_df)
    grid_size = int(np.ceil(np.sqrt(num_survey * 1.5)))  # Slightly wider grid
    
    for idx, (_, row) in enumerate(survey_df.iterrows()):
        row_idx = idx // grid_size
        col_idx = idx % grid_size
        
        # Calculate position in a grid with some spacing
        base_x = survey_x + (col_idx - grid_size/2) * 100
        base_y = (row_idx - grid_size/2) * 60
        
        # Add small random jitter
        jitter_x = random.uniform(-5, 5)
        jitter_y = random.uniform(-5, 5)
        
        node = {
            "id": f"survey_{idx}",
            "label": row['pattern_label'],
            "cluster": row['cluster'],
            "source": row['source'],
            "x": base_x + jitter_x,
            "y": base_y + jitter_y,
            "color": cluster_colors[row['cluster']]
        }
        source_nodes.append(node)
    
    # For cluster-based visualization
    cluster_nodes = []
    radius = 800  # Increase radius to spread clusters
    cluster_centers = {}
    
    # Calculate cluster centers in a circular arrangement
    for i, cluster in enumerate(unique_clusters):
        angle = 2 * np.pi * i / len(unique_clusters)
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        cluster_centers[cluster] = (x, y)
    
    # Position nodes within each cluster with improved spacing
    for cluster in unique_clusters:
        cluster_df = df[df['cluster'] == cluster]
        center_x, center_y = cluster_centers[cluster]
        
        # Calculate positions around the cluster center
        num_items = len(cluster_df)
        
        if num_items <= 8:
            # Circle arrangement for small clusters
            item_radius = 200
            for i, (_, row) in enumerate(cluster_df.iterrows()):
                angle = 2 * np.pi * i / num_items
                x = center_x + item_radius * np.cos(angle)
                y = center_y + item_radius * np.sin(angle)
                
                # Add small jitter to prevent perfect alignment
                jitter_x = random.uniform(-10, 10)
                jitter_y = random.uniform(-10, 10)
                
                node = {
                    "id": f"{cluster}_{i}",
                    "label": row['pattern_label'],
                    "cluster": cluster,
                    "source": row['source'],
                    "x": x + jitter_x,
                    "y": y + jitter_y,
                    "color": cluster_colors[cluster]
                }
                cluster_nodes.append(node)
        else:
            # Grid arrangement for larger clusters with more spacing
            # Grid arrangement for larger clusters with more spacing
            grid_size = int(np.ceil(np.sqrt(num_items)))
            spacing_x = 120
            spacing_y = 80
            
            for i, (_, row) in enumerate(cluster_df.iterrows()):
                row_idx = i // grid_size
                col_idx = i % grid_size
                
                x = center_x + (col_idx - grid_size/2 + 0.5) * spacing_x
                y = center_y + (row_idx - grid_size/2 + 0.5) * spacing_y
                
                # Add small jitter to prevent perfect alignment
                jitter_x = random.uniform(-5, 5)
                jitter_y = random.uniform(-5, 5)
                
                node = {
                    "id": f"{cluster}_{i}",
                    "label": row['pattern_label'],
                    "cluster": cluster,
                    "source": row['source'],
                    "x": x + jitter_x,
                    "y": y + jitter_y,
                    "color": cluster_colors[cluster]
                }
                cluster_nodes.append(node)
    
    # Add cluster center labels
    cluster_labels = []
    for cluster, (x, y) in cluster_centers.items():
        label = {
            "id": f"label_{cluster}",
            "label": cluster,
            "x": x,
            "y": y,
            "color": cluster_colors[cluster],
            "isClusterLabel": True
        }
        cluster_labels.append(label)
    
    # Create HTML content with embedded JavaScript for visualization
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Cybersecurity Pattern Labels Visualization</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }}
            .container {{ width: 100%; height: 100vh; position: relative; }}
            .tab {{ overflow: hidden; background-color: #f1f1f1; position: fixed; top: 0; width: 100%; z-index: 10; }}
            .tab button {{ background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s; }}
            .tab button:hover {{ background-color: #ddd; }}
            .tab button.active {{ background-color: #ccc; }}
            .tabcontent {{ display: none; padding-top: 50px; height: calc(100vh - 50px); }}
            .note {{ position: absolute; width: 120px; min-height: 40px; background-color: white; border: 1px solid #ccc; border-radius: 3px; padding: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); overflow: hidden; font-size: 10px; transition: transform 0.3s; }}
            .note:hover {{ transform: scale(1.1); z-index: 5; }}
            .cluster-label {{ position: absolute; font-weight: bold; font-size: 14px; background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); }}
            .legend {{ position: fixed; bottom: 10px; left: 10px; background-color: white; padding: 10px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); }}
            .legend-item {{ display: flex; align-items: center; margin-bottom: 5px; }}
            .legend-color {{ width: 15px; height: 15px; margin-right: 5px; }}
            .instructions {{ position: fixed; top: 60px; right: 10px; background-color: rgba(255,255,255,0.9); padding: 10px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); max-width: 300px; }}
        </style>
    </head>
    <body>
        <div class="tab">
            <button class="tablinks active" onclick="openTab(event, 'bySource')">By Source</button>
            <button class="tablinks" onclick="openTab(event, 'byClusters')">By Clusters</button>
        </div>
        
        <div id="bySource" class="tabcontent" style="display: block;">
            <div class="instructions">
                <h3>By Source View</h3>
                <p>This view organizes pattern labels by their source (Interview or Survey).</p>
                <p>Each color represents a different cluster category.</p>
                <p>Hover over notes to see details and click to select.</p>
            </div>
        </div>
        
        <div id="byClusters" class="tabcontent">
            <div class="instructions">
                <h3>By Clusters View</h3>
                <p>This view organizes pattern labels by their cluster category.</p>
                <p>Each cluster is positioned around the visualization space.</p>
                <p>Interview (I) and Survey (S) sources are indicated in each note.</p>
            </div>
        </div>
        
        <script>
            // Data from Python
            const sourceNodes = {json.dumps(source_nodes)};
            const clusterNodes = {json.dumps(cluster_nodes)};
            const clusterLabels = {json.dumps(cluster_labels)};
            const clusterColors = {json.dumps(cluster_colors)};
            
            // Tab switching function
            function openTab(evt, tabName) {{
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {{
                    tabcontent[i].style.display = "none";
                }}
                tablinks = document.getElementsByClassName("tablinks");
                for (i = 0; i < tablinks.length; i++) {{
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }}
                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.className += " active";
                
                // Clear previous visualization
                document.getElementById(tabName).innerHTML = '';
                if (tabName === "bySource") {{
                    document.getElementById(tabName).appendChild(
                        document.querySelector(".instructions").cloneNode(true)
                    );
                    renderSourceView();
                }} else {{
                    document.getElementById(tabName).appendChild(
                        document.querySelector(".instructions").cloneNode(true)
                    );
                    renderClusterView();
                }}
            }}
            
            // Render source-based view
            function renderSourceView() {{
                const container = document.getElementById('bySource');
                
                // Add title headers
                const interviewHeader = document.createElement('div');
                interviewHeader.textContent = 'INTERVIEW';
                interviewHeader.style.position = 'absolute';
                interviewHeader.style.left = '25%';
                interviewHeader.style.top = '70px';
                interviewHeader.style.transform = 'translateX(-50%)';
                interviewHeader.style.fontSize = '24px';
                interviewHeader.style.fontWeight = 'bold';
                container.appendChild(interviewHeader);
                
                const surveyHeader = document.createElement('div');
                surveyHeader.textContent = 'SURVEY';
                surveyHeader.style.position = 'absolute';
                surveyHeader.style.left = '75%';
                surveyHeader.style.top = '70px';
                surveyHeader.style.transform = 'translateX(-50%)';
                surveyHeader.style.fontSize = '24px';
                surveyHeader.style.fontWeight = 'bold';
                container.appendChild(surveyHeader);
                
                // Create nodes
                sourceNodes.forEach(node => {{
                    const noteElement = document.createElement('div');
                    noteElement.className = 'note';
                    noteElement.style.left = `${{window.innerWidth/2 + node.x}}px`;
                    noteElement.style.top = `${{window.innerHeight/2 + node.y}}px`;
                    noteElement.style.backgroundColor = `${{node.color}}80`; // Add transparency
                    noteElement.style.borderColor = node.source === 'Interview' ? '#000' : '#555';
                    
                    const labelElement = document.createElement('div');
                    labelElement.textContent = node.label;
                    
                    const sourceElement = document.createElement('div');
                    sourceElement.textContent = node.source;
                    sourceElement.style.fontSize = '8px';
                    sourceElement.style.color = '#555';
                    sourceElement.style.marginTop = '5px';
                    
                    const clusterElement = document.createElement('div');
                    clusterElement.textContent = node.cluster;
                    clusterElement.style.fontSize = '8px';
                    clusterElement.style.color = '#555';
                    
                    noteElement.appendChild(labelElement);
                    noteElement.appendChild(sourceElement);
                    noteElement.appendChild(clusterElement);
                    
                    container.appendChild(noteElement);
                }});
                
                // Add legend
                addLegend(container);
            }}
            
            // Render cluster-based view
            function renderClusterView() {{
                const container = document.getElementById('byClusters');
                
                // Create cluster labels
                clusterLabels.forEach(label => {{
                    const labelElement = document.createElement('div');
                    labelElement.className = 'cluster-label';
                    labelElement.textContent = label.label;
                    labelElement.style.left = `${{window.innerWidth/2 + label.x}}px`;
                    labelElement.style.top = `${{window.innerHeight/2 + label.y}}px`;
                    labelElement.style.borderColor = label.color;
                    labelElement.style.backgroundColor = `${{label.color}}40`; // Very transparent
                    container.appendChild(labelElement);
                }});
                
                // Create nodes
                clusterNodes.forEach(node => {{
                    const noteElement = document.createElement('div');
                    noteElement.className = 'note';
                    noteElement.style.left = `${{window.innerWidth/2 + node.x}}px`;
                    noteElement.style.top = `${{window.innerHeight/2 + node.y}}px`;
                    noteElement.style.backgroundColor = `${{node.color}}80`; // Add transparency
                    noteElement.style.borderColor = node.source === 'Interview' ? '#000' : '#555';
                    
                    const labelElement = document.createElement('div');
                    labelElement.textContent = node.label;
                    
                    const sourceIndicator = document.createElement('div');
                    sourceIndicator.textContent = node.source === 'Interview' ? '(I)' : '(S)';
                    sourceIndicator.style.fontSize = '8px';
                    sourceIndicator.style.display = 'inline-block';
                    sourceIndicator.style.marginLeft = '3px';
                    
                    const wrapper = document.createElement('div');
                    wrapper.appendChild(labelElement);
                    wrapper.appendChild(sourceIndicator);
                    
                    noteElement.appendChild(wrapper);
                    container.appendChild(noteElement);
                }});
                
                // Add legend
                addLegend(container);
            }}
            
            // Add cluster legend
            function addLegend(container) {{
                const legend = document.createElement('div');
                legend.className = 'legend';
                
                const title = document.createElement('div');
                title.textContent = 'Clusters';
                title.style.fontWeight = 'bold';
                title.style.marginBottom = '5px';
                legend.appendChild(title);
                
                Object.entries(clusterColors).forEach(([cluster, color]) => {{
                    const item = document.createElement('div');
                    item.className = 'legend-item';
                    
                    const colorBox = document.createElement('div');
                    colorBox.className = 'legend-color';
                    colorBox.style.backgroundColor = color;
                    
                    const label = document.createElement('div');
                    label.textContent = cluster;
                    label.style.fontSize = '10px';
                    
                    item.appendChild(colorBox);
                    item.appendChild(label);
                    legend.appendChild(item);
                }});
                
                container.appendChild(legend);
            }}
            
            // Initialize the source view by default
            renderSourceView();
            
            // Make the visualization responsive
            window.addEventListener('resize', () => {{
                // Get active tab
                const activeTab = document.querySelector('.tablinks.active');
                if (activeTab) {{
                    activeTab.click(); // Rerender active view
                }}
            }});
            
            // Enable drag functionality for notes (optional enhancement)
            let draggedElement = null;
            let offsetX = 0;
            let offsetY = 0;
            
            document.addEventListener('mousedown', (e) => {{
                if (e.target.classList.contains('note') || e.target.parentElement.classList.contains('note')) {{
                    draggedElement = e.target.classList.contains('note') ? e.target : e.target.parentElement;
                    
                    // Calculate offset
                    const rect = draggedElement.getBoundingClientRect();
                    offsetX = e.clientX - rect.left;
                    offsetY = e.clientY - rect.top;
                    
                    // Bring to front
                    draggedElement.style.zIndex = 10;
                }}
            }});
            
            document.addEventListener('mousemove', (e) => {{
                if (draggedElement) {{
                    draggedElement.style.left = `${{e.clientX - offsetX}}px`;
                    draggedElement.style.top = `${{e.clientY - offsetY}}px`;
                }}
            }});
            
            document.addEventListener('mouseup', () => {{
                if (draggedElement) {{
                    draggedElement.style.zIndex = 1;
                    draggedElement = null;
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # Save the HTML file
    with open('miro_visualization.html', 'w') as f:
        f.write(html_content)
    
    print("HTML visualization saved as 'miro_visualization.html'")

# VISUALIZATION 3: Create a chord diagram showing relationships between clusters
def create_chord_diagram(df):
    # Count connections between clusters based on pattern labels
    pattern_to_cluster = dict(zip(df['pattern_label'], df['cluster']))
    clusters = sorted(df['cluster'].unique())
    
    # Create a mapping from cluster name to index
    cluster_to_idx = {cluster: idx for idx, cluster in enumerate(clusters)}
    
    # Create adjacency matrix
    n = len(clusters)
    matrix = np.zeros((n, n))
    
    # Identify related patterns based on common words
    pattern_words = {}
    for pattern in df['pattern_label']:
        words = set(re.findall(r'\b\w+\b', pattern.lower()))
        pattern_words[pattern] = words
    
    # Find related patterns
    for i, pattern1 in enumerate(df['pattern_label']):
        words1 = pattern_words[pattern1]
        cluster1 = pattern_to_cluster[pattern1]
        idx1 = cluster_to_idx[cluster1]  # Use the mapping instead of np.where
        
        for j, pattern2 in enumerate(df['pattern_label']):
            if i >= j:  # Avoid duplicate connections and self-connections
                continue
                
            words2 = pattern_words[pattern2]
            cluster2 = pattern_to_cluster[pattern2]
            idx2 = cluster_to_idx[cluster2]  # Use the mapping instead of np.where
            
            # If patterns share meaningful words, add connection
            common_words = words1.intersection(words2)
            # Exclude common stop words
            common_words = {w for w in common_words if len(w) > 3}
            
            if len(common_words) >= 2:
                matrix[idx1, idx2] += 1
                matrix[idx2, idx1] += 1  # Make the matrix symmetric
    
    # Enhance matrix by adding connections for clusters with similar names
    for i, cluster1 in enumerate(clusters):
        words1 = set(re.findall(r'\b\w+\b', cluster1.lower()))
        for j, cluster2 in enumerate(clusters):
            if i >= j:  # Avoid duplicate connections and self-connections
                continue
                
            words2 = set(re.findall(r'\b\w+\b', cluster2.lower()))
            common_words = words1.intersection(words2)
            
            if len(common_words) >= 1:
                matrix[i, j] += 2
                matrix[j, i] += 2
    
    # Rest of the function remains the same
    # Create the chord diagram
    plt.figure(figsize=(16, 16))
    
    # Custom function to create an enhanced chord diagram with D3-like appearance
    def plot_enhanced_chord(matrix, names):
        import matplotlib.patches as patches
        import matplotlib.path as path
        
        n = len(names)
        colors = plt.cm.tab20(np.linspace(0, 1, n))
        
        # Normalize matrix values
        row_sums = matrix.sum(axis=1)
        matrix_norm = np.zeros_like(matrix)
        for i in range(len(row_sums)):
            if row_sums[i] > 0:
                matrix_norm[i, :] = matrix[i, :] / row_sums[i]
            else:
                matrix_norm[i, :] = 0
        # Normalize matrix values while avoiding division by zero

        # Calculate angles for each segment
        angles = np.linspace(0, 2*np.pi, n+1)
        width = 0.1  # Width of the ring
        
        # Draw the outer ring segments
        ax = plt.subplot(111, polar=True)
        
        # Initialize dictionaries to store segment positions
        segment_mids = {}
        segment_colors = {}
        
        # Draw outer ring segments
        for i in range(n):
            start_angle = angles[i]
            end_angle = angles[i+1]
            mid_angle = (start_angle + end_angle) / 2
            segment_mids[i] = mid_angle
            segment_colors[i] = colors[i]
            
            # Create ring segment
            arc = patches.Wedge(
                (0, 0), 1.0, np.degrees(start_angle), np.degrees(end_angle),
                width=width, 
                color=colors[i],
                alpha=0.8,
                edgecolor='white',
                linewidth=1
            )
            ax.add_patch(arc)
            
            # Add text label outside the ring
            text_radius = 1.1
            ha = 'left' if -np.pi/2 <= mid_angle <= np.pi/2 else 'right'
            va = 'center'
            
            if mid_angle > np.pi/2 and mid_angle < 3*np.pi/2:
                ax.text(
                    mid_angle, text_radius, names[i], 
                    ha=ha, va=va, rotation=np.degrees(mid_angle) - 180,
                    fontsize=9, fontweight='bold', rotation_mode='anchor'
                )
            else:
                ax.text(
                    mid_angle, text_radius, names[i], 
                    ha=ha, va=va, rotation=np.degrees(mid_angle),
                    fontsize=9, fontweight='bold', rotation_mode='anchor'
                )
                
        # Draw edges (chords) between segments
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i, j] > 0:
                    start_angle_i = segment_mids[i]
                    start_angle_j = segment_mids[j]
                    
                    # Calculate edge width based on connection strength
                    edge_width = 0.03 * np.sqrt(matrix[i, j])
                    
                    # Create a cubic Bézier curve between segments
                    # Control point radius determined by connection strength
                    control_radius = 0.5  # Adjust as needed
                    
                    # Start point
                    x1 = (1.0 - width/2) * np.cos(start_angle_i)
                    y1 = (1.0 - width/2) * np.sin(start_angle_i)
                    
                    # End point
                    x4 = (1.0 - width/2) * np.cos(start_angle_j)
                    y4 = (1.0 - width/2) * np.sin(start_angle_j)
                    
                    # Control points
                    x2 = control_radius * np.cos(start_angle_i)
                    y2 = control_radius * np.sin(start_angle_i)
                    
                    x3 = control_radius * np.cos(start_angle_j)
                    y3 = control_radius * np.sin(start_angle_j)
                    
                    # Create the Bézier curve
                    verts = [
                        (x1, y1),
                        (x2, y2),
                        (x3, y3),
                        (x4, y4)
                    ]
                    
                    codes = [
                        path.Path.MOVETO,
                        path.Path.CURVE4,
                        path.Path.CURVE4,
                        path.Path.CURVE4
                    ]
                    
                    bezier_path = path.Path(verts, codes)
                    
                    # Mix colors from both segments
                    mix_color = ((colors[i][0] + colors[j][0])/2,
                                (colors[i][1] + colors[j][1])/2,
                                (colors[i][2] + colors[j][2])/2,
                                0.5)  # Semi-transparent
                    
                    # Draw the path
                    patch = patches.PathPatch(
                        bezier_path, 
                        facecolor='none',
                        edgecolor=mix_color,
                        lw=edge_width*10,
                        alpha=0.7
                    )
                    ax.add_patch(patch)
        
        # Configure the plot
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['polar'].set_visible(False)
        
        # Remove grid
        ax.grid(False)
        
        # Make sure all elements are visible
        plt.tight_layout()
    
    # Create the enhanced chord diagram
    plot_enhanced_chord(matrix, clusters)
    
    # Add title
    plt.title('Relationships Between Cybersecurity Pattern Clusters', fontsize=18, y=1.05)
    
    # Save the figure
    plt.savefig('chord_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
# Execute the visualizations
create_source_visualization(df)
create_cluster_visualization(df)
create_miro_html_visualization(df)
create_chord_diagram(df)

print("All visualizations have been created!")

# Additional analysis: Display statistics for clusters
cluster_stats = df.groupby('cluster').agg(
    num_patterns=('pattern_label', 'count'),
    survey_count=('source', lambda x: (x == 'Survey').sum()),
    interview_count=('source', lambda x: (x == 'Interview').sum())
).reset_index()

cluster_stats['survey_ratio'] = cluster_stats['survey_count'] / cluster_stats['num_patterns']
cluster_stats['interview_ratio'] = cluster_stats['interview_count'] / cluster_stats['num_patterns']

# Sort by number of patterns
cluster_stats = cluster_stats.sort_values('num_patterns', ascending=False)

print("\nCluster Statistics:")
print(cluster_stats)

# Plot cluster statistics
plt.figure(figsize=(14, 10))
bars = plt.barh(cluster_stats['cluster'], cluster_stats['num_patterns'], 
               color=[plt.cm.tab20(i) for i in range(len(cluster_stats))])

# Add source breakdown
for i, (_, row) in enumerate(cluster_stats.iterrows()):
    # Add text for survey and interview counts
    plt.text(row['num_patterns'] + 0.2, i, f"Survey: {row['survey_count']}, Interview: {row['interview_count']}")

plt.xlabel('Number of Pattern Labels')
plt.title('Number of Pattern Labels per Cluster')
plt.tight_layout()
plt.savefig('cluster_stats.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a word cloud for pattern labels
try:
    from wordcloud import WordCloud

    # Combine all pattern labels
    all_patterns = ' '.join(df['pattern_label'])
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, 
                          background_color='white',
                          colormap='viridis',
                          max_words=100,
                          contour_width=1,
                          contour_color='steelblue').generate(all_patterns)
    
    # Display the word cloud
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Cybersecurity Pattern Labels', fontsize=20)
    plt.tight_layout()
    plt.savefig('pattern_wordcloud.png', dpi=300)
    plt.close()
    
    print("Word cloud created successfully!")
except ImportError:
    print("WordCloud package not available. Skipping word cloud creation.")