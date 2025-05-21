import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import re
import random
from collections import Counter

# LaTeX content included directly in the script
LATEX_CONTENT = r"""
\textbf{Thematic Code} & \textbf{Participants} \\
\hline
\endhead

Digital Vulnerability & PV3 \\
\hline
Security Awareness Gap & PV3 \\
\hline
Systemic Fragility & PV1 \\
\hline
Security Complexity & PV1 \\
\hline
Evolving Warfare & PV2 \\
\hline
Technology in Warfare & PV2 \\
\hline
Digital Economy & PV3 \\
\hline
Digital Efficiency & PV3 \\
\hline
Critical Infrastructure & PV3 \\
\hline
Infrastructure Governance & PV3 \\
\hline
Target Selection & PV2 \\
\hline
Defense Limitations & PV2 \\
\hline
Centralization Risk & PV1 \\
\hline
Centralization Dilemma & PV1 \\
\hline
Security Trade-offs & PV1, PV3 \\
\hline
Threat Escalation & PV3 \\
\hline
Attack Inevitability & PV3 \\
\hline
Cyber-First Strategy & PV2 \\
\hline
Hybrid Warfare Sequence & PV2 \\
\hline
System Redundancy & PV1 \\
\hline
Legacy System Loss & PV1 \\
\hline
Human Factor & PV3 \\
\hline
Security Behavior & PV3 \\
\hline
Awareness Deficit & PV3 \\
\hline
Civilian Involvement & PV2 \\
\hline
Preparedness Effect & PV2 \\
\hline
Trust Limitations & PV1 \\
\hline
Information Silos & PV1 \\
\hline
Crisis Trust & PV1 \\
\hline
Incident Planning & PV3 \\
\hline
Scenario Testing & PV3 \\
\hline
Emergency Preparation & PV3 \\
\hline
System Resilience & PV2 \\
\hline
Tactical Vulnerability & PV2 \\
\hline
System Redundancy & PV1 \\
\hline
Cost of Security & PV1 \\
\hline
Personal Resilience & PV1 \\
\hline
Security Framework & PV3 \\
\hline
Expertise Gap & PV3 \\
\hline
Response Framework & PV2 \\
\hline
Holistic Preparedness & PV2 \\
\hline
Information Access & PV1 \\
\hline
Security Innovation & PV1 \\
\hline
Data Sovereignty & PV3 \\
\hline
Foreign Dependency & PV3 \\
\hline
Trust Erosion & PV3 \\
\hline
Technological Dependency & PV2 \\
\hline
European Autonomy & PV2 \\
\hline
Technology Transition & PV1 \\
\hline
Shifting Trust & PV1 \\
\hline
Digital Sovereignty & PV1 \\
\hline
Transition Challenges & PV1 \\
\hline
Threat Actors & PV2 \\
\hline
Threat Prioritization & PV2 \\
\hline
Threat Assessment & PV1 \\
\hline
Russian Threat & PV1 \\
\hline
Primary Threats & PV3 \\
\hline
Knowledge Transfer & PV3 \\
\hline
Ukrainian Expertise & PV3, PV1 \\
\hline
European Security & PV2 \\
\hline
Security Realignment & PV2 \\
\hline
Cautious Cooperation & PV1 \\
\hline
Dependency Concerns & PV1 \\
\hline
Small Nation Strategy & PV1 \\
\hline
Attribution Challenge & PV2 \\
\hline
Undisclosed Attacks & PV2 \\
\hline
Cyber Countermeasures & PV2 \\
\hline
Russian Attribution & PV3 \\
\hline
Security Paradigm Shift & PV2 \\
\hline
Heightened Risk & PV2 \\
\hline
Future Uncertainty & PV2 \\
\hline
Continuous Threat & PV2 \\
\hline
Dynamic Landscape & PV3 \\
\hline
Security Arms Race & PV3 \\
\hline
Geopolitical Awareness & PV3 \\
\hline
Dependency Recognition & PV3 \\
\hline

\end{longtable}
\section{Clustered Codes after Affinity Diagram}

\begin{longtable}{|p{0.5\textwidth}|p{0.2\textwidth}|p{0.3\textwidth}|}
\hline
\textbf{Code} & \textbf{Participants} & \textbf{Theme} \\
\hline
\endhead

Digital Vulnerability & PV3 & Digital Security Challenges \\
\hline
Security Awareness Gap & PV3 & Human Factor in Security \\
\hline
Systemic Fragility & PV1 & System Vulnerabilities \\
\hline
Security Complexity & PV1 & Digital Security Challenges \\
\hline
Evolving Warfare & PV2 & Hybrid Warfare Dynamics \\
\hline
Technology in Warfare & PV2 & Hybrid Warfare Dynamics \\
\hline
Digital Economy & PV3 & Critical Infrastructure \\
\hline
Digital Efficiency & PV3 & Critical Infrastructure \\
\hline
Critical Infrastructure & PV3 & Critical Infrastructure \\
\hline
Infrastructure Governance & PV3 & Critical Infrastructure \\
\hline
Target Selection & PV2 & Hybrid Warfare Tactics \\
\hline
Defense Limitations & PV2 & Defensive Capabilities \\
\hline
Centralization Risk & PV1 & System Vulnerabilities \\
\hline
Centralization Dilemma & PV1 & System Vulnerabilities \\
\hline
Security Trade-offs & PV1, PV3 & Security Implementation \\
\hline
Threat Escalation & PV3 & Threat Evolution \\
\hline
Attack Inevitability & PV3 & Threat Evolution \\
\hline
Cyber-First Strategy & PV2 & Hybrid Warfare Tactics \\
\hline
Hybrid Warfare Sequence & PV2 & Hybrid Warfare Dynamics \\
\hline
System Redundancy & PV1 & Resilience Strategies \\
\hline
Legacy System Loss & PV1 & System Vulnerabilities \\
\hline
Human Factor & PV3 & Human Factor in Security \\
\hline
Security Behavior & PV3 & Human Factor in Security \\
\hline
Awareness Deficit & PV3 & Human Factor in Security \\
\hline
Civilian Involvement & PV2 & Societal Resilience \\
\hline
Preparedness Effect & PV2 & Societal Resilience \\
\hline
Trust Limitations & PV1 & Trust and Information Sharing \\
\hline
Information Silos & PV1 & Trust and Information Sharing \\
\hline
Crisis Trust & PV1 & Trust and Information Sharing \\
\hline
Incident Planning & PV3 & Preparedness and Response \\
\hline
Scenario Testing & PV3 & Preparedness and Response \\
\hline
Emergency Preparation & PV3 & Preparedness and Response \\
\hline
System Resilience & PV2 & Resilience Strategies \\
\hline
Tactical Vulnerability & PV2 & Defensive Capabilities \\
\hline
System Redundancy & PV1 & Resilience Strategies \\
\hline
Cost of Security & PV1 & Security Implementation \\
\hline
Personal Resilience & PV1 & Societal Resilience \\
\hline
Security Framework & PV3 & Security Implementation \\
\hline
Expertise Gap & PV3 & Knowledge and Expertise \\
\hline
Response Framework & PV2 & Preparedness and Response \\
\hline
Holistic Preparedness & PV2 & Preparedness and Response \\
\hline
Information Access & PV1 & Trust and Information Sharing \\
\hline
Security Innovation & PV1 & Security Implementation \\
\hline
Data Sovereignty & PV3 & Digital Sovereignty \\
\hline
Foreign Dependency & PV3 & Digital Sovereignty \\
\hline
Trust Erosion & PV3 & Trust and Information Sharing \\
\hline
Technological Dependency & PV2 & Digital Sovereignty \\
\hline
European Autonomy & PV2 & Digital Sovereignty \\
\hline
Technology Transition & PV1 & Digital Sovereignty \\
\hline
Shifting Trust & PV1 & Trust and Information Sharing \\
\hline
Digital Sovereignty & PV1 & Digital Sovereignty \\
\hline
Transition Challenges & PV1 & Digital Sovereignty \\
\hline
Threat Actors & PV2 & Threat Landscape \\
\hline
Threat Prioritization & PV2 & Threat Landscape \\
\hline
Threat Assessment & PV1 & Threat Landscape \\
\hline
Russian Threat & PV1 & Threat Landscape \\
\hline
Primary Threats & PV3 & Threat Landscape \\
\hline
Knowledge Transfer & PV3 & Knowledge and Expertise \\
\hline
Ukrainian Expertise & PV3, PV1 & Knowledge and Expertise \\
\hline
European Security & PV2 & International Cooperation \\
\hline
Security Realignment & PV2 & International Cooperation \\
\hline
Cautious Cooperation & PV1 & International Cooperation \\
\hline
Dependency Concerns & PV1 & International Cooperation \\
\hline
Small Nation Strategy & PV1 & International Cooperation \\
\hline
Attribution Challenge & PV2 & Attribution and Response \\
\hline
Undisclosed Attacks & PV2 & Attribution and Response \\
\hline
Cyber Countermeasures & PV2 & Attribution and Response \\
\hline
Russian Attribution & PV3 & Attribution and Response \\
\hline
Security Paradigm Shift & PV2 & Future Security Landscape \\
\hline
Heightened Risk & PV2 & Future Security Landscape \\
\hline
Future Uncertainty & PV2 & Future Security Landscape \\
\hline
Continuous Threat & PV2 & Future Security Landscape \\
\hline
Dynamic Landscape & PV3 & Future Security Landscape \\
\hline
Security Arms Race & PV3 & Future Security Landscape \\
\hline
Geopolitical Awareness & PV3 & International Cooperation \\
\hline
Dependency Recognition & PV3 & Digital Sovereignty \\
\hline
"""

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
    Create an improved network visualization showing relationships between
    themes and participants with larger canvas and better spacing.
    """
    plt.figure(figsize=(24, 20))  # Increased from (20, 16)
    ax = plt.gca()
    ax.set_facecolor('#f8f8f8')
    
    # Get unique themes and participants
    unique_themes = df['theme'].unique()
    unique_participants = df['participant'].unique()
    
    # Count codes in each theme
    theme_counts = df['theme'].value_counts()
    
    # Position for participants in a triangular layout with more space
    participant_pos = {}
    for i, participant in enumerate(unique_participants):
        angle = 2 * np.pi * i / len(unique_participants)
        x = 60 * np.cos(angle)  # Increased from 50
        y = 60 * np.sin(angle)  # Increased from 50
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
    
    # Position themes based on dominant participant and count with more space
    for dominant, themes in themes_by_dominant.items():
        if dominant in participant_pos:  # If it's a specific participant
            center_x, center_y = participant_pos[dominant]
            radius = 30  # Increased from 25
        else:  # For "mixed" or "unknown"
            center_x, center_y = 0, 0
            radius = 25  # Increased from 20
        
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
        size = np.sqrt(participant_count) * 4.5  # Slightly increased
        color = participant_colors.get(participant, '#999999')
        
        circle = plt.Circle((x, y), size, color=color, alpha=0.9)
        ax.add_patch(circle)
        
        plt.text(x, y, f"{participant}\n({participant_count} codes)", 
                 ha='center', va='center', fontsize=16, fontweight='bold', color='white')
    
    # Draw nodes for themes with improved spacing
    for theme, (x, y) in theme_pos.items():
        theme_count = theme_counts[theme]
        size = np.sqrt(theme_count) * 3  # Increased from 2.5
        
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
        
        # Split long theme names into multiple lines for better readability
        name_parts = theme.split()
        if len(name_parts) > 2:
            midpoint = len(name_parts) // 2
            name_text = ' '.join(name_parts[:midpoint]) + '\n' + ' '.join(name_parts[midpoint:])
        else:
            name_text = theme
            
        plt.text(x, y, name_text, ha='center', va='center', 
                 fontsize=11, fontweight='bold')
        
        # Add count with more space
        plt.text(x, y-size-3, f"({theme_count})", ha='center', va='center', fontsize=10)
    
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
    
    plt.title('Network Visualization of Hybrid Threat Themes and Participants', fontsize=22)
    
    # Increased canvas boundaries
    plt.xlim(-100, 100)
    plt.ylim(-100, 100)
    plt.axis('off')
    
    # Add a legend for participant colors
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label=f'PV1 - Blue',
                  markerfacecolor='#3498db', markersize=15),
        plt.Line2D([0], [0], marker='o', color='w', label=f'PV2 - Red',
                  markerfacecolor='#e74c3c', markersize=15),
        plt.Line2D([0], [0], marker='o', color='w', label=f'PV3 - Green',
                  markerfacecolor='#2ecc71', markersize=15)
    ]
    plt.legend(handles=legend_elements, loc='lower right', fontsize=12)
    
    # Ensure tight layout with extra padding
    plt.tight_layout(pad=3.0)
    plt.savefig('theme_participant_network.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created improved network visualization of themes and participants")

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
def main():
    print("Processing hybrid threat visualizations...")
    
    try:
        # Extract the themed codes section
        themed_codes_section = extract_theme_clustering(LATEX_CONTENT)
        
        if not themed_codes_section:
            print("Could not find themed codes section in the LaTeX content.")
            # Fall back to using the full content
            print("Using the full LaTeX content instead.")
            themed_codes_section = LATEX_CONTENT
        
        # Parse the data
        df = parse_themed_codes_table(themed_codes_section)
        
        if df.empty:
            print("No data was parsed from the themed codes section.")
            return
        
        print(f"Parsed {len(df)} coded entries across {df['participant'].nunique()} participants and {df['theme'].nunique()} themes")
        
        # Create the visualizations
        create_theme_distribution_visualization(df)
        create_participant_theme_heatmap(df)
        create_theme_network_visualization(df)
        create_participant_focus_visualization(df)
        create_radar_chart_by_participant(df)
        create_code_occurrence_chart(df)
        
        # Display summary information
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
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()