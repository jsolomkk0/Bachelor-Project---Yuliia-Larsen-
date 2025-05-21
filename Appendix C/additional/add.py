import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
import matplotlib as mpl
from matplotlib.patches import Wedge, ConnectionPatch, Circle
import matplotlib.patheffects as PathEffects

# Set high-quality rendering defaults
mpl.rcParams['figure.dpi'] = 100
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.weight'] = 'normal'
mpl.rcParams['axes.titleweight'] = 'bold'

# Create dataframe from the research question table data
data = [
    # RQ1 sections
    ["Digitization in Denmark", "RQ1", "Digital Infrastructure Challenges / Governance and Strategic Planning"],
    ["Strategic Targeting of Danish Infrastructure", "RQ1", "Critical Infrastructure Protection / Advanced Attack Strategies"],
    ["Multi-Vector Attacks", "RQ1", "Advanced Attack Strategies / State-Sponsored Threat Actors"],
    ["The Human Factor in Hybrid Defense", "RQ1", "Social Engineering and Human Vulnerabilities / Workforce and Expertise Challenges"],
    ["Incident Response and National Resilience", "RQ1", "Incident Response and Recovery / Governance and Strategic Planning"],
    ["Governance Fragmentation in Danish Infrastructure", "RQ1", "Governance and Strategic Planning / Regulatory and Compliance Matters"],
    
    # RQ2 sections
    ["Foreign Technology Dependencies", "RQ2", "Foreign Technology Considerations"],
    ["Asia's Advanced Persistent Threats", "RQ2", "State-Sponsored Threat Actors / Geopolitical Security Dimensions"],
    ["International Cooperation and Threat Intelligence", "RQ2", "International Collaboration / Information Operations"],
    ["Russia's Hybrid Warfare in Ukraine", "RQ2", "State-Sponsored Threat Actors / Advanced Attack Strategies / Information Operations"],
    ["Evolution of Threat Landscape", "RQ2", "Emerging Technology Threats / Geopolitical Security Dimensions / Information Operations"]
]

df = pd.DataFrame(data, columns=["section", "research_question", "clusters"])

# Split the clusters into separate rows
expanded_data = []
for _, row in df.iterrows():
    for cluster in row['clusters'].split(' / '):
        expanded_data.append([row['section'], row['research_question'], cluster])

# Create expanded dataframe
expanded_df = pd.DataFrame(expanded_data, columns=["section", "research_question", "cluster"])

# Get unique clusters
unique_clusters = sorted(expanded_df['cluster'].unique())

# Define a color mapping for each cluster
# Using a colorful but professional palette
color_palette = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5"
]

# Ensure we have enough colors for all clusters
while len(color_palette) < len(unique_clusters):
    color_palette.extend(color_palette)

# Create cluster-color mapping
cluster_colors = {cluster: color_palette[i] for i, cluster in enumerate(unique_clusters)}

# Function to wrap text to fit in pie wedges
def wrap_text(text, width=15):
    """Wrap text to fit in specified width"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        if len(' '.join(current_line + [word])) <= width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

def create_improved_visualization(df, expanded_df, unique_clusters, cluster_colors):
    """Create improved pie chart visualizations for each research question"""
    # Create figure with more space between subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(28, 14), gridspec_kw={'wspace': 0.3})
    fig.patch.set_facecolor('#F5F5F5')
    
    # Research questions
    research_questions = ["RQ1", "RQ2"]
    
    # RQ titles
    rq_titles = {
        "RQ1": "RQ1: How does digitization aid in hybrid warfare\ncampaigns, and how does this challenge Denmark's\ncybersecurity governance frameworks?",
        "RQ2": "RQ2: How do geopolitical tensions influence\nevolution of cyberwarfare against Denmark?"
    }
    
    # Function to create pie chart for a research question
    def create_rq_pie(ax, rq, title):
        # Get sections for this research question
        rq_df = df[df['research_question'] == rq]
        sections = rq_df['section'].tolist()
        n_sections = len(sections)

        # Calculate the optimal starting angle to distribute sections evenly
        if rq == "RQ1":
            start_angle = 90  # Start from top
        else:
            start_angle = 90  # Also start from top for RQ2
        
        # Equal sized wedges
        values = [1] * n_sections
        
        # Colors for sections
        section_colors = plt.cm.tab20(np.linspace(0, 1, n_sections))
        
        # Create pie chart for sections
        wedges, _ = ax.pie(values, radius=0.7, colors=section_colors, 
                          wedgeprops=dict(width=0.4, edgecolor='w', linewidth=2),
                          startangle=start_angle, counterclock=False)
        
        # Add center circle with RQ title
        circle = Circle((0, 0), 0.3, fc='white', ec='black', lw=2)
        ax.add_patch(circle)
        ax.text(0, 0, title, ha='center', va='center', fontsize=14, fontweight='bold', wrap=True)
        
        # Calculate positions for each section to avoid overlaps
        for i, section in enumerate(sections):
            # Calculate angle for center of wedge
            angle = (i * 360 / n_sections) + (360 / (2 * n_sections)) + start_angle
            # Convert to radians
            angle_rad = np.deg2rad(angle)
            
            # Calculate position for section label - moved further out
            x = 1.4 * np.cos(angle_rad)
            y = 1.4 * np.sin(angle_rad)
            
            # Add section text with background for better readability
            section_text = wrap_text(section, 15)
            text = ax.text(x, y, section_text, ha='center', va='center', fontsize=12, fontweight='bold',
                          bbox=dict(boxstyle="round,pad=0.4", fc='white', ec=section_colors[i], alpha=0.9, linewidth=2))
            
            # Add connecting lines from wedge to section label
            inner_x = 0.7 * np.cos(angle_rad)
            inner_y = 0.7 * np.sin(angle_rad)
            ax.plot([inner_x, x], [inner_y, y], '-', lw=1.5, color=section_colors[i], alpha=0.7)
            
            # Get clusters for this section
            section_clusters = expanded_df[(expanded_df['section'] == section) & 
                                           (expanded_df['research_question'] == rq)]['cluster'].unique()
            
            # Determine cluster placement strategy
            cluster_radius = 2.4  # Distance from center
            
            # Spread the clusters in an arc around the section
            cluster_span = np.pi / 6  # 30 degrees in radians
            
            # Number of clusters for this section
            n_clusters = len(section_clusters)
            
            # Create more spacing between clusters
            for j, cluster in enumerate(section_clusters):
                # Calculate arc position for cluster
                if n_clusters == 1:
                    # If only one cluster, place it directly in line with the section
                    cluster_angle = angle_rad
                else:
                    # Calculate spread for multiple clusters
                    offset = cluster_span * (j - (n_clusters - 1) / 2) / max(1, n_clusters - 1)
                    cluster_angle = angle_rad + offset
                
                # Calculate position for cluster bubble with increased distance
                cluster_x = cluster_radius * np.cos(cluster_angle)
                cluster_y = cluster_radius * np.sin(cluster_angle)
                
                # Draw cluster bubble - larger size
                cluster_circle = Circle((cluster_x, cluster_y), 0.25, 
                                        fc=cluster_colors[cluster], ec='black', alpha=0.8, linewidth=1)
                ax.add_patch(cluster_circle)
                
                # Format cluster text to fit in bubble
                cluster_words = cluster.split()
                if len(cluster_words) > 3:
                    # For long cluster names, break into multiple lines
                    formatted_cluster = '\n'.join([' '.join(cluster_words[:2]), ' '.join(cluster_words[2:])])
                else:
                    formatted_cluster = '\n'.join(cluster_words)
                
                # Add cluster label with better text wrapping
                ax.text(cluster_x, cluster_y, formatted_cluster, ha='center', va='center', 
                       fontsize=9, fontweight='bold', color='black')
                
                # Add connecting line from section label to cluster with curved path
                # Use bezier curve for smoother connection
                # Calculate control point
                control_x = (x + cluster_x) / 2 + np.sin(cluster_angle) * 0.2
                control_y = (y + cluster_y) / 2 - np.cos(cluster_angle) * 0.2
                
                # Create bezier curve points
                t = np.linspace(0, 1, 30)
                bezier_x = (1-t)**2 * x + 2*(1-t)*t * control_x + t**2 * cluster_x
                bezier_y = (1-t)**2 * y + 2*(1-t)*t * control_y + t**2 * cluster_y
                
                # Draw the curved path
                ax.plot(bezier_x, bezier_y, '-', lw=1.5, color=cluster_colors[cluster], alpha=0.7)
        
        ax.set_aspect('equal')
        ax.axis('off')
    
    # Create pie charts for each research question
    create_rq_pie(ax1, "RQ1", rq_titles["RQ1"])
    create_rq_pie(ax2, "RQ2", rq_titles["RQ2"])
    
    # Add legend for clusters in a more organized way
    # Create a separate axis for the legend
    legend_ax = fig.add_axes([0.1, 0.02, 0.8, 0.08])
    legend_ax.axis('off')
    
    # Create legend entries
    n_cols = 3
    n_rows = (len(unique_clusters) + n_cols - 1) // n_cols
    
    for i, cluster in enumerate(unique_clusters):
        row = i // n_cols
        col = i % n_cols
        
        x = 0.1 + col * 0.3
        y = 0.9 - row * 0.3
        
        # Add color box - larger
        legend_ax.add_patch(Circle((x, y), 0.04, fc=cluster_colors[cluster], ec='black'))
        
        # Add cluster name with better spacing
        legend_ax.text(x + 0.06, y, cluster, fontsize=11, va='center')
    
    # Add structural explanation text
    plt.figtext(0.5, 0.97, 'Research Questions and Their Matching Cybersecurity Clusters', 
                fontsize=22, ha='center', fontweight='bold')
    
    plt.figtext(0.5, 0.94, 'Each research question contains themes (inner pie sections) which connect to relevant cybersecurity clusters (outer bubbles)', 
                fontsize=14, ha='center', style='italic')
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12, top=0.9)
    
    # Save the figure
    plt.savefig('research_question_pie_charts.png', dpi=300, bbox_inches='tight')
    
    plt.show()

# Execute the visualization function
create_improved_visualization(df, expanded_df, unique_clusters, cluster_colors)