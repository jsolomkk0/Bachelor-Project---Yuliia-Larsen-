import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import re
import random
from collections import Counter

# Parse the LaTeX table for hybrid threats data
def parse_hybrid_threats_table(latex_content):
    # Pattern to match lines like "Digital Vulnerability & PV3 \\"
    single_participant_pattern = r'(.*?) & (PV\d+) \\\\'
    # Pattern to match lines that have multiple participants like "Security Trade-offs & PV1, PV3 \\"
    multi_participant_pattern = r'(.*?) & (PV\d+(?:, PV\d+)*) \\\\'
    
    matches = re.findall(multi_participant_pattern, latex_content)
    
    data = []
    for match in matches:
        code = match[0].strip()
        participants_str = match[1].strip()
        
        # Handle multiple participants
        participants = [p.strip() for p in participants_str.split(',')]
        
        for participant in participants:
            data.append({'code': code, 'participant': participant})
    
    return pd.DataFrame(data)

def parse_themed_codes_table(latex_content):
    # Pattern to match lines with theme assignments
    pattern = r'(.*?) & (PV\d+(?:, PV\d+)*) & (.*?) \\\\'
    
    matches = re.findall(pattern, latex_content)
    
    data = []
    for match in matches:
        code = match[0].strip()
        participants_str = match[1].strip()
        theme = match[2].strip()
        
        # Handle multiple participants
        participants = [p.strip() for p in participants_str.split(',')]
        
        for participant in participants:
            data.append({'code': code, 'participant': participant, 'theme': theme})
    
    return pd.DataFrame(data)

def create_theme_distribution_visualization(df):
    """
    Create a visualization showing the distribution of themes across participants.
    """
    # Count codes by theme and participant
    theme_participant_counts = df.groupby(['theme', 'participant']).size().unstack(fill_value=0)
    
    # Sort themes by total count
    theme_participant_counts['Total'] = theme_participant_counts.sum(axis=1)
    theme_participant_counts = theme_participant_counts.sort_values(by='Total', ascending=False)
    theme_participant_counts = theme_participant_counts.drop('Total', axis=1)
    
    plt.figure(figsize=(15, 10))
    
    # Create horizontal bar chart with participant breakdown
    ax = theme_participant_counts.plot(kind='barh', stacked=True, figsize=(15, 10), 
                                       color=['#3498db', '#e74c3c', '#2ecc71'])
    
    plt.title('Distribution of Hybrid Threat Themes by Participant', fontsize=18)
    plt.xlabel('Number of Codes', fontsize=14)
    plt.ylabel('Theme', fontsize=14)
    
    # Add total counts at the end of each bar
    for i, total in enumerate(theme_participant_counts.sum(axis=1)):
        plt.text(total + 0.3, i, f"{total}", va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.legend(title='Participant')
    plt.savefig('theme_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created theme distribution visualization")

def create_participant_theme_heatmap(df):
    """
    Create a heatmap showing the concentration of themes by participant.
    """
    # Count codes by theme and participant
    cross_tab = pd.crosstab(df['theme'], df['participant'])
    
    plt.figure(figsize=(12, 10))
    
    # Create heatmap
    im = plt.imshow(cross_tab.values, cmap='YlOrRd')
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Number of Codes', rotation=270, labelpad=20)
    
    # Configure axes
    plt.xticks(range(len(cross_tab.columns)), cross_tab.columns, rotation=0)
    plt.yticks(range(len(cross_tab.index)), cross_tab.index)
    
    # Add text annotations to cells
    for i in range(len(cross_tab.index)):
        for j in range(len(cross_tab.columns)):
            text = plt.text(j, i, cross_tab.values[i, j],
                           ha="center", va="center", 
                           color="black" if cross_tab.values[i, j] < 5 else "white",
                           fontweight='bold')
    
    plt.title('Heatmap of Hybrid Threat Themes by Participant', fontsize=16)
    plt.tight_layout()
    plt.savefig('participant_theme_heatmap.png', dpi=300)
    plt.close()
    
    print("Created participant-theme heatmap visualization")

def create_theme_network_visualization(df):
    """
    Create a network visualization showing relationships between
    themes and participants.
    """
    plt.figure(figsize=(20, 16))
    ax = plt.gca()
    ax.set_facecolor('#f8f8f8')
    
    # Get unique themes and participants
    unique_themes = df['theme'].unique()
    unique_participants = df['participant'].unique()
    
    # Count codes in each theme
    theme_counts = df['theme'].value_counts()
    
    # Position for participants in a triangular layout
    participant_pos = {}
    for i, participant in enumerate(unique_participants):
        angle = 2 * np.pi * i / len(unique_participants)
        x = 50 * np.cos(angle)
        y = 50 * np.sin(angle)
        participant_pos[participant] = (x, y)
    
    # Position themes in a circular layout
    theme_pos = {}
    
    # Calculate participant bias for each theme
    theme_participant_bias = {}
    for theme in unique_themes:
        theme_df = df[df['theme'] == theme]
        participant_counts = theme_df['participant'].value_counts()
        
        # Find the dominant participant (if any)
        if len(participant_counts) > 0:
            max_count = participant_counts.max()
            dominants = [p for p, c in participant_counts.items() if c == max_count]
            
            if len(dominants) == 1:
                theme_participant_bias[theme] = dominants[0]  # Dominated by one participant
            else:
                theme_participant_bias[theme] = "mixed"  # Mixed participation
        else:
            theme_participant_bias[theme] = "unknown"
    
    # Group themes by dominant participant
    themes_by_dominant = {}
    for theme, dominant in theme_participant_bias.items():
        if dominant not in themes_by_dominant:
            themes_by_dominant[dominant] = []
        themes_by_dominant[dominant].append(theme)
    
    # Position themes based on dominant participant and count
    for dominant, themes in themes_by_dominant.items():
        if dominant in participant_pos:  # If it's a specific participant
            center_x, center_y = participant_pos[dominant]
            radius = 25  # Distance from participant
        else:  # For "mixed" or "unknown"
            center_x, center_y = 0, 0
            radius = 20
        
        # Arrange themes around the participant in a circle
        for i, theme in enumerate(themes):
            angle = 2 * np.pi * i / len(themes)
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            theme_pos[theme] = (x, y)
    
    # Draw nodes for participants
    participant_colors = {'PV1': '#3498db', 'PV2': '#e74c3c', 'PV3': '#2ecc71'}
    
    for participant, (x, y) in participant_pos.items():
        participant_count = len(df[df['participant'] == participant])
        size = np.sqrt(participant_count) * 4
        color = participant_colors.get(participant, '#999999')
        
        circle = plt.Circle((x, y), size, color=color, alpha=0.9)
        ax.add_patch(circle)
        
        plt.text(x, y, f"{participant}\n({participant_count} codes)", 
                 ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # Draw nodes for themes
    for theme, (x, y) in theme_pos.items():
        theme_count = theme_counts[theme]
        size = np.sqrt(theme_count) * 2.5
        
        # Color based on dominant participant
        dominant = theme_participant_bias.get(theme, "mixed")
        if dominant in participant_colors:
            color = participant_colors[dominant]
            alpha = 0.7
        else:
            color = '#999999'  # Gray for mixed
            alpha = 0.5
        
        circle = plt.Circle((x, y), size, color=color, alpha=alpha)
        ax.add_patch(circle)
        
        # Split long theme names into multiple lines
        name_parts = theme.split()
        if len(name_parts) > 3:
            midpoint = len(name_parts) // 2
            name_text = ' '.join(name_parts[:midpoint]) + '\n' + ' '.join(name_parts[midpoint:])
        else:
            name_text = theme
            
        plt.text(x, y, name_text, ha='center', va='center', 
                 fontsize=9, fontweight='bold')
        
        # Add count
        plt.text(x, y-size-2, f"({theme_count})", ha='center', va='center', fontsize=8)
    
    # Draw edges between participants and themes
    for _, row in df.iterrows():
        participant = row['participant']
        theme = row['theme']
        
        if participant in participant_pos and theme in theme_pos:
            participant_x, participant_y = participant_pos[participant]
            theme_x, theme_y = theme_pos[theme]
            
            # Draw line with low alpha to avoid visual clutter
            color = participant_colors.get(participant, '#999999')
            plt.plot([participant_x, theme_x], [participant_y, theme_y], 
                     color=color, alpha=0.05, linewidth=0.5)
    
    # Add summary connections with width based on count
    for theme in unique_themes:
        if theme not in theme_pos:
            continue
            
        theme_x, theme_y = theme_pos[theme]
        
        for participant in unique_participants:
            if participant not in participant_pos:
                continue
                
            participant_x, participant_y = participant_pos[participant]
            count = len(df[(df['theme'] == theme) & (df['participant'] == participant)])
            
            if count > 0:
                color = participant_colors.get(participant, '#999999')
                width = np.sqrt(count) * 0.8
                
                plt.plot([participant_x, theme_x], [participant_y, theme_y], 
                         color=color, alpha=0.6, linewidth=width)
    
    plt.title('Network Visualization of Hybrid Threat Themes and Participants', fontsize=18)
    plt.xlim(-60, 60)
    plt.ylim(-60, 60)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('theme_participant_network.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created network visualization of themes and participants")

def create_participant_focus_visualization(df):
    """
    Create a visualization that highlights what each participant focuses on.
    """
    plt.figure(figsize=(15, 10))
    
    # Get top themes for each participant
    top_themes_by_participant = {}
    for participant in df['participant'].unique():
        participant_df = df[df['participant'] == participant]
        theme_counts = participant_df['theme'].value_counts().head(5)
        top_themes_by_participant[participant] = theme_counts
    
    # Create a grouped bar chart
    axes = []
    index = 0
    width = 0.8
    colors = {'PV1': '#3498db', 'PV2': '#e74c3c', 'PV3': '#2ecc71'}
    
    # Prepare x positions
    participant_count = len(top_themes_by_participant)
    all_themes = set()
    for themes in top_themes_by_participant.values():
        all_themes.update(themes.index)
    all_themes = sorted(all_themes)
    
    # Create positions for bars
    positions = list(range(len(all_themes)))
    
    # Plot bars for each participant
    for participant, theme_counts in top_themes_by_participant.items():
        # Create bars for this participant
        bars = [theme_counts.get(theme, 0) for theme in all_themes]
        ax = plt.bar([p + index*width/participant_count for p in positions], 
                     bars, width/participant_count, alpha=0.7,
                     color=colors.get(participant, '#999999'), label=participant)
        axes.append(ax)
        index += 1
    
    plt.xlabel('Theme', fontsize=14)
    plt.ylabel('Number of Codes', fontsize=14)
    plt.title('Top Themes by Participant', fontsize=18)
    plt.xticks([p + width/2 - width/participant_count/2 for p in positions], 
               [theme[:20] + '...' if len(theme) > 20 else theme for theme in all_themes], 
               rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig('participant_focus.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created participant focus visualization")

def create_radar_chart_by_participant(df):
    """
    Create a radar chart showing theme distribution for each participant.
    """
    from matplotlib.path import Path
    from matplotlib.projections.polar import PolarAxes
    from matplotlib.projections import register_projection
    from matplotlib.spines import Spine

    def radar_factory(num_vars, frame='circle'):
        """Create a radar chart with `num_vars` axes."""
        # Calculate angles for each axis
        theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

        class RadarAxes(PolarAxes):
            name = 'radar'

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_theta_zero_location('N')

            def fill(self, *args, closed=True, **kwargs):
                """Override fill to draw a closed polygon."""
                return super().fill(closed=closed, *args, **kwargs)

            def plot(self, *args, **kwargs):
                """Override plot to draw a line to the first point."""
                line = super().plot(*args, **kwargs)
                if 'color' in kwargs:
                    line[0].set_color(kwargs['color'])
                return line

        register_projection(RadarAxes)

        # Create the figure
        fig = plt.figure(figsize=(9, 9))
        
        # Add the radar axes to the figure
        rect = [0.1, 0.1, 0.8, 0.8]
        ax = fig.add_axes(rect, projection='radar')
        
        # Set the angular gridlines
        ax.set_thetagrids(np.degrees(theta), labels=[])
        
        # Return the figure and the radar axes
        return fig, ax, theta

    # Get top 10 themes by count
    top_themes = df['theme'].value_counts().head(10).index.tolist()
    theme_counts = df.groupby(['participant', 'theme']).size().unstack(fill_value=0)
    
    # Keep only the top themes
    theme_counts = theme_counts[top_themes]
    
    # Normalize to percentages for each participant
    for participant in theme_counts.index:
        total = theme_counts.loc[participant].sum()
        if total > 0:
            theme_counts.loc[participant] = theme_counts.loc[participant] / total * 100
    
    # Create the radar chart
    fig, ax, theta = radar_factory(len(top_themes), frame='polygon')
    
    colors = {'PV1': '#3498db', 'PV2': '#e74c3c', 'PV3': '#2ecc71'}
    
    for participant in theme_counts.index:
        values = theme_counts.loc[participant].values.tolist()
        # Complete the loop for the radar chart
        values.append(values[0])
        
        # Add angles
        angles = np.concatenate((theta, [theta[0]]))
        
        ax.plot(angles, values, color=colors.get(participant, '#999999'), 
                linewidth=2, label=participant)
        ax.fill(angles, values, color=colors.get(participant, '#999999'), alpha=0.25)
    
    # Add theme labels
    ax.set_thetagrids(np.degrees(theta), labels=top_themes)
    for label, angle in zip(ax.get_xticklabels(), theta):
        if np.degrees(angle) > 90 and np.degrees(angle) < 270:
            label.set_rotation(np.degrees(angle) + 180)
        else:
            label.set_rotation(np.degrees(angle))
        label.set_fontsize(8)
        label.set_horizontalalignment('center')
    
    ax.set_title('Theme Focus by Participant (Normalized %)', size=15)
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.tight_layout()
    plt.savefig('participant_radar.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created radar chart visualization by participant")

def create_code_occurrence_chart(df):
    """
    Create a visualization showing the most common codes across all participants.
    """
    # Count occurrences of each code
    code_counts = df['code'].value_counts().head(15)  # Top 15 codes
    
    plt.figure(figsize=(12, 8))
    
    # Create horizontal bar chart
    bars = plt.barh(code_counts.index, code_counts.values, color='#3498db')
    
    # Add count labels
    for i, (code, count) in enumerate(code_counts.items()):
        plt.text(count + 0.1, i, str(count), va='center')
    
    plt.title('Most Common Hybrid Threat Codes', fontsize=16)
    plt.xlabel('Occurrences', fontsize=12)
    plt.tight_layout()
    plt.savefig('code_occurrences.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created code occurrence chart")

def extract_theme_clustering(latex_content):
    """
    Extract the section of the LaTeX content that contains the themed codes table.
    """
    match = re.search(r'\\section\{Clustered Codes after Affinity Diagram\}(.*?)(\\section|\\end\{longtable\})', 
                      latex_content, re.DOTALL)
    if match:
        return match.group(1)
    return None

# Main function
def main(latex_content):
    # Extract the themed codes section
    themed_codes_section = extract_theme_clustering(latex_content)
    
    if not themed_codes_section:
        print("Could not find themed codes section in the LaTeX content.")
        return None
    
    # Parse the data
    df = parse_themed_codes_table(themed_codes_section)
    
    if df.empty:
        print("No data was parsed from the themed codes section.")
        return None
    
    print(f"Parsed {len(df)} coded entries across {df['participant'].nunique()} participants and {df['theme'].nunique()} themes")
    
    # Create the visualizations
    create_theme_distribution_visualization(df)
    create_participant_theme_heatmap(df)
    create_theme_network_visualization(df)
    create_participant_focus_visualization(df)
    create_radar_chart_by_participant(df)
    create_code_occurrence_chart(df)
    
    return df

if __name__ == "__main__":
    print("Processing hybrid threat visualizations...")
    
    # This would be the LaTeX content from the file
    # For this example, we'll use the content passed to the function
    with open('paste-2.txt', 'r') as file:
        latex_content = file.read()
    
    df = main(latex_content)
    
    if df is not None:
        print("\nVisualization process complete! The following files have been created:")
        print("1. theme_distribution.png - Bar chart showing theme distribution across participants")
        print("2. participant_theme_heatmap.png - Heatmap showing theme concentrations by participant")
        print("3. theme_participant_network.png - Network visualization of themes and participants")
        print("4. participant_focus.png - Bar chart showing top themes for each participant")
        print("5. participant_radar.png - Radar chart comparing theme focus across participants")
        print("6. code_occurrences.png - Bar chart of most frequent codes")
        
        print("\nData summary:")
        print(f"Total coded entries: {len(df)}")
        print(f"Participants: {', '.join(df['participant'].unique())}")
        print(f"Number of unique themes: {df['theme'].nunique()}")
        print(f"Number of unique codes: {df['code'].nunique()}")
        
        # Top themes by count
        top_themes = df['theme'].value_counts().head(5)
        print("\nTop 5 themes by code count:")
        for theme, count in top_themes.items():
            print(f"- {theme}: {count} codes")