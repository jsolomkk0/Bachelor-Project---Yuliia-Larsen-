import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import to_rgba
import matplotlib as mpl

# Set high-quality rendering defaults
mpl.rcParams['figure.dpi'] = 100
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'Arial'  # Using a clean font
mpl.rcParams['font.weight'] = 'normal'
mpl.rcParams['axes.titleweight'] = 'bold'

# Create dataframe from the provided table data
data = [
    ["Digital Vulnerability", "PV3", "Digital Security Challenges"],
    ["Security Awareness Gap", "PV3", "Human Factor in Security"],
    ["Systemic Fragility", "PV1", "System Vulnerabilities"],
    ["Security Complexity", "PV1", "Digital Security Challenges"],
    ["Evolving Warfare", "PV2", "Hybrid Warfare Dynamics"],
    ["Technology in Warfare", "PV2", "Hybrid Warfare Dynamics"],
    ["Digital Economy", "PV3", "Critical Infrastructure"],
    ["Digital Efficiency", "PV3", "Critical Infrastructure"],
    ["Critical Infrastructure", "PV3", "Critical Infrastructure"],
    ["Infrastructure Governance", "PV3", "Critical Infrastructure"],
    ["Target Selection", "PV2", "Hybrid Warfare Tactics"],
    ["Defense Limitations", "PV2", "Defensive Capabilities"],
    ["Centralization Risk", "PV1", "System Vulnerabilities"],
    ["Centralization Dilemma", "PV1", "System Vulnerabilities"],
    ["Security Trade-offs", "PV1, PV3", "Security Implementation"],
    ["Threat Escalation", "PV3", "Threat Evolution"],
    ["Attack Inevitability", "PV3", "Threat Evolution"],
    ["Cyber-First Strategy", "PV2", "Hybrid Warfare Tactics"],
    ["Hybrid Warfare Sequence", "PV2", "Hybrid Warfare Dynamics"],
    ["System Redundancy", "PV1", "Resilience Strategies"],
    ["Legacy System Loss", "PV1", "System Vulnerabilities"],
    ["Human Factor", "PV3", "Human Factor in Security"],
    ["Security Behavior", "PV3", "Human Factor in Security"],
    ["Awareness Deficit", "PV3", "Human Factor in Security"],
    ["Civilian Involvement", "PV2", "Societal Resilience"],
    ["Preparedness Effect", "PV2", "Societal Resilience"],
    ["Trust Limitations", "PV1", "Trust and Information Sharing"],
    ["Information Silos", "PV1", "Trust and Information Sharing"],
    ["Crisis Trust", "PV1", "Trust and Information Sharing"],
    ["Incident Planning", "PV3", "Preparedness and Response"],
    ["Scenario Testing", "PV3", "Preparedness and Response"],
    ["Emergency Preparation", "PV3", "Preparedness and Response"],
    ["System Resilience", "PV2", "Resilience Strategies"],
    ["Tactical Vulnerability", "PV2", "Defensive Capabilities"],
    ["System Redundancy", "PV1", "Resilience Strategies"],
    ["Cost of Security", "PV1", "Security Implementation"],
    ["Personal Resilience", "PV1", "Societal Resilience"],
    ["Security Framework", "PV3", "Security Implementation"],
    ["Expertise Gap", "PV3", "Knowledge and Expertise"],
    ["Response Framework", "PV2", "Preparedness and Response"],
    ["Holistic Preparedness", "PV2", "Preparedness and Response"],
    ["Information Access", "PV1", "Trust and Information Sharing"],
    ["Security Innovation", "PV1", "Security Implementation"],
    ["Data Sovereignty", "PV3", "Digital Sovereignty"],
    ["Foreign Dependency", "PV3", "Digital Sovereignty"],
    ["Trust Erosion", "PV3", "Trust and Information Sharing"],
    ["Technological Dependency", "PV2", "Digital Sovereignty"],
    ["European Autonomy", "PV2", "Digital Sovereignty"],
    ["Technology Transition", "PV1", "Digital Sovereignty"],
    ["Shifting Trust", "PV1", "Trust and Information Sharing"],
    ["Digital Sovereignty", "PV1", "Digital Sovereignty"],
    ["Transition Challenges", "PV1", "Digital Sovereignty"],
    ["Threat Actors", "PV2", "Threat Landscape"],
    ["Threat Prioritization", "PV2", "Threat Landscape"],
    ["Threat Assessment", "PV1", "Threat Landscape"],
    ["Russian Threat", "PV1", "Threat Landscape"],
    ["Primary Threats", "PV3", "Threat Landscape"],
    ["Knowledge Transfer", "PV3", "Knowledge and Expertise"],
    ["Ukrainian Expertise", "PV3, PV1", "Knowledge and Expertise"],
    ["European Security", "PV2", "International Cooperation"],
    ["Security Realignment", "PV2", "International Cooperation"],
    ["Cautious Cooperation", "PV1", "International Cooperation"],
    ["Dependency Concerns", "PV1", "International Cooperation"],
    ["Small Nation Strategy", "PV1", "International Cooperation"],
    ["Attribution Challenge", "PV2", "Attribution and Response"],
    ["Undisclosed Attacks", "PV2", "Attribution and Response"],
    ["Cyber Countermeasures", "PV2", "Attribution and Response"],
    ["Russian Attribution", "PV3", "Attribution and Response"],
    ["Security Paradigm Shift", "PV2", "Future Security Landscape"],
    ["Heightened Risk", "PV2", "Future Security Landscape"],
    ["Future Uncertainty", "PV2", "Future Security Landscape"],
    ["Continuous Threat", "PV2", "Future Security Landscape"],
    ["Dynamic Landscape", "PV3", "Future Security Landscape"],
    ["Security Arms Race", "PV3", "Future Security Landscape"],
    ["Geopolitical Awareness", "PV3", "International Cooperation"],
    ["Dependency Recognition", "PV3", "Digital Sovereignty"]
]

df = pd.DataFrame(data, columns=["code", "participants", "theme"])

# Get unique themes
unique_themes = sorted(df['theme'].unique())

# Define a color mapping for each theme
# Using a colorful but professional palette
color_palette = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", 
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
]

# Ensure we have enough colors for all themes
while len(color_palette) < len(unique_themes):
    color_palette.extend(color_palette)

# Create theme-color mapping
theme_colors = {theme: color_palette[i] for i, theme in enumerate(unique_themes)}

def create_code_clustering(df, unique_themes, theme_colors):
    """
    Create visualization clustering codes by theme with a boxed layout.
    This improved version handles overlapping by increasing spacing.
    """
    """Create visualization clustering codes by theme with a boxed layout"""
    plt.figure(figsize=(40, 60))  # Further increased figure size
    ax = plt.gca()
    ax.set_facecolor('#F5F5F5')
    
    # Calculate layout dimensions - 4 themes per row
    num_cols = 4
    num_rows = (len(unique_themes) + num_cols - 1) // num_cols
    
    # Spacing parameters - significantly increased to prevent text overlapping
    horizontal_spacing = 60  # Space between themes horizontally (significantly increased)
    vertical_spacing = 50    # Space between themes vertically (significantly increased)
    
    # For placing the themes in a grid
    for theme_idx, theme in enumerate(unique_themes):
        # Calculate row and column position
        row = theme_idx // num_cols
        col = theme_idx % num_cols
        
        # Base position for this theme
        theme_x = col * horizontal_spacing
        theme_y = -row * vertical_spacing  # Negative to go downward
        
        # Create theme header box with rounded corners
        box_width = 18  # Increased width
        box_height = 3  # Increased height
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
                fontsize=14, fontweight='bold')  # Increased font size
        
        # Get codes for this theme
        theme_df = df[df['theme'] == theme]
        codes = theme_df['code'].tolist()
        n_codes = len(codes)
        
        if n_codes == 0:
            continue
            
        # Arrange codes in horizontal rows below the theme box
        max_codes_per_row = 3  # Reduced from 4 to 3 for less crowding
        num_code_rows = (n_codes + max_codes_per_row - 1) // max_codes_per_row
        
        # Start position for codes (below the theme box)
        start_y = theme_y - 6  # Further increased distance below the theme box
        
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
                code_x = theme_x + (j - offset) * 8.0  # Further increased horizontal spacing between codes
                code_y = start_y - row_idx * 5.0       # Further increased vertical spacing between rows of codes
                
                # Get participants for this code
                code_df = df[df['code'] == code]
                p_text = ', '.join(code_df['participants'].values)
                
                # Calculate color based on theme
                code_color = theme_colors[theme]
                
                # Draw code node (small horizontal rectangle)
                rect_width, rect_height = 7.0, 1.2  # Further increased width and height to fit text
                rect = patches.Rectangle(
                    (code_x - rect_width/2, code_y - rect_height/2),
                    rect_width, rect_height,
                    facecolor=code_color, alpha=0.6,
                    edgecolor='black', linewidth=1
                )
                ax.add_patch(rect)
                
                # Draw code label
                plt.text(code_x, code_y, code, fontsize=10, ha='center', va='center', weight='bold')  # Increased font size
                
                # Draw participant indicator below with more space
                plt.text(code_x, code_y - rect_height - 0.5, f"({p_text})", 
                       fontsize=8, ha='center', va='top', color='#555555')  # Increased font size and space
                
                # Draw dotted line connecting to theme box
                line = plt.Line2D(
                    [theme_x, code_x], 
                    [theme_y - box_height/2, code_y + rect_height/2],
                    color=code_color, alpha=0.5, linewidth=0.8, linestyle='--'
                )
                ax.add_line(line)
    
    plt.title('Cybersecurity Pattern Labels by Cluster (Boxed Layout)', fontsize=28)  # Increased title size
    plt.axis('off')
    plt.axis('equal')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('cybersecurity_code_clustering.png', dpi=300, bbox_inches='tight')
    
    plt.show()

# Execute the visualization function
create_code_clustering(df, unique_themes, theme_colors)