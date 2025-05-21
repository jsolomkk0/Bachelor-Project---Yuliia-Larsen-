import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import pandas as pd
import re

# Parse the LaTeX table function
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

def create_separate_source_affinity_diagrams(df):
    """
    Create separate affinity diagrams for Interview and Survey sources.
    Each diagram maintains the same cluster organization but only shows items from one source.
    """
    # Get unique clusters
    unique_clusters = df['cluster'].unique()
    num_clusters = len(unique_clusters)
    
    # Create a color map for clusters
    colors = plt.cm.tab20(np.linspace(0, 1, num_clusters))
    cluster_colors = {cluster: colors[i] for i, cluster in enumerate(unique_clusters)}
    
    # Split data by source
    interview_df = df[df['source'] == "Interview"]
    survey_df = df[df['source'] == "Survey"]
    
    # Function to create an affinity diagram for a specific source
    def create_affinity_diagram(source_df, source_name):
        plt.figure(figsize=(36, 30))
        ax = plt.gca()
        ax.set_facecolor('#F5F5F5')
        
        # Setup cluster positions in a circular layout
        cluster_centers = {}
        angle_step = 2 * np.pi / num_clusters
        radius = 60  # Spread of clusters from center
        
        for i, cluster in enumerate(unique_clusters):
            angle = i * angle_step
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            cluster_centers[cluster] = (x, y)
        
        width, height = 3.5, 0.9  # Dimensions for pattern label boxes
        
        # Function to generate positions for items within a cluster
        def generate_cluster_positions(center_x, center_y, n):
            if n == 0:
                return []
                
            cols = max(1, int(np.ceil(np.sqrt(n * 1.5))))  # More columns than strictly needed for better spacing
            rows = int(np.ceil(n / cols))
            spacing_x = width * 2.2  # Horizontal spacing
            spacing_y = height * 3.0  # Vertical spacing
            
            start_x = center_x - (cols - 1) * spacing_x / 2
            start_y = center_y + (rows - 1) * spacing_y / 2
            
            positions = []
            for i in range(n):
                row = i // cols
                col = i % cols
                
                # Add staggered layout and jitter
                offset = spacing_x / 3 if row % 2 else 0
                jitter_x = random.uniform(-0.5, 0.5)
                jitter_y = random.uniform(-0.5, 0.5)
                
                x = start_x + col * spacing_x + jitter_x + offset
                y = start_y - row * spacing_y + jitter_y
                positions.append((x, y))
            return positions
        
        # Draw clusters and their items
        for cluster in unique_clusters:
            cluster_df = source_df[source_df['cluster'] == cluster]
            center_x, center_y = cluster_centers[cluster]
            color = cluster_colors[cluster]
            
            # Draw cluster label
            plt.text(center_x, center_y + 6, cluster, ha='center', va='center',
                     fontsize=16, fontweight='bold',
                     bbox=dict(facecolor='white', alpha=0.95, boxstyle='round,pad=1.2',
                               edgecolor=color, linewidth=2))
            
            # Skip empty clusters (for the current source)
            if len(cluster_df) == 0:
                continue
                
            # Generate positions for the items in this cluster
            positions = generate_cluster_positions(center_x, center_y, len(cluster_df))
            
            # Draw the item boxes
            for i, (_, row) in enumerate(cluster_df.iterrows()):
                x, y = positions[i]
                
                # Create rectangle for the pattern label
                rect_color = tuple(list(color[:3]) + [0.75])
                rect = patches.Rectangle((x - width / 2, y - height / 2), width, height,
                                         facecolor=rect_color, edgecolor='black',
                                         linewidth=1.0, alpha=0.9)
                ax.add_patch(rect)
                
                # Add the pattern label text
                label = row['pattern_label']
                short_text = (label[:40] + "...") if len(label) > 40 else label
                plt.text(x, y, short_text, fontsize=8,
                         ha='center', va='center', zorder=2)
        
        # Title and customization
        plt.title(f"Cybersecurity Pattern Labels - {source_name} Source", fontsize=24)
        plt.axis('off')
        plt.axis('equal')
        
        # Add a legend for clusters
        legend_elements = [patches.Patch(facecolor=cluster_colors[clust], label=clust)
                           for clust in unique_clusters]
        plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.02),
                   ncol=3, fontsize=12, frameon=True)
        
        plt.tight_layout()
        plt.savefig(f"{source_name.lower()}_affinity_diagram.png", dpi=300, bbox_inches="tight")
        plt.close()
    
    # Create separate diagrams for each source
    create_affinity_diagram(interview_df, "Interview")
    create_affinity_diagram(survey_df, "Survey")
    
    print(f"Created separate affinity diagrams for Interview ({len(interview_df)} items) and Survey ({len(survey_df)} items)")

def create_heatmap_comparison(df):
    """
    Create a heatmap visualization showing the distribution of pattern labels across
    sources and clusters.
    """
    # Get counts for each cluster-source combination
    cross_tab = pd.crosstab(df['cluster'], df['source'])
    
    # Sort clusters by total count (descending)
    cross_tab['Total'] = cross_tab.sum(axis=1)
    cross_tab = cross_tab.sort_values(by='Total', ascending=False)
    cross_tab = cross_tab.drop('Total', axis=1)
    
    plt.figure(figsize=(14, 12))
    
    # Create heatmap
    im = plt.imshow(cross_tab.values, cmap='YlOrRd')
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Number of Pattern Labels', rotation=270, labelpad=20)
    
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
    
    plt.title('Distribution of Cybersecurity Pattern Labels by Cluster and Source', fontsize=16)
    plt.tight_layout()
    plt.savefig('cluster_source_heatmap.png', dpi=300)
    plt.close()
    
    print("Created cluster-source heatmap visualization")

def create_network_visualization(df):
    """
    Create a network visualization showing relationships between
    clusters and sources, without displaying small count numbers.
    """
    plt.figure(figsize=(20, 16))
    ax = plt.gca()
    ax.set_facecolor('#f8f8f8')
    
    # Get unique clusters and count patterns in each
    unique_clusters = df['cluster'].unique()
    cluster_counts = df['cluster'].value_counts()
    
    # Position for sources
    source_pos = {'Interview': (-50, 0), 'Survey': (50, 0)}
    
    # Position clusters in a circular layout
    cluster_pos = {}
    num_clusters = len(unique_clusters)
    
    # Interview-heavy clusters on left side, Survey-heavy on right, balanced in middle
    cluster_source_bias = {}
    for cluster in unique_clusters:
        cluster_df = df[df['cluster'] == cluster]
        interview_count = len(cluster_df[cluster_df['source'] == 'Interview'])
        survey_count = len(cluster_df[cluster_df['source'] == 'Survey'])
        
        if interview_count > survey_count:
            cluster_source_bias[cluster] = -1  # Left side
        elif survey_count > interview_count:
            cluster_source_bias[cluster] = 1   # Right side
        else:
            cluster_source_bias[cluster] = 0   # Middle
    
    # Sort clusters by bias and then by total count
    sorted_clusters = sorted(
        cluster_source_bias.items(), 
        key=lambda x: (x[1], -cluster_counts[x[0]])
    )
    
    # Distribute clusters in an arc based on their bias
    left_clusters = [c for c, b in sorted_clusters if b == -1]
    middle_clusters = [c for c, b in sorted_clusters if b == 0]
    right_clusters = [c for c, b in sorted_clusters if b == 1]
    
    # Position the clusters
    def position_cluster_group(clusters, start_angle, end_angle, radius=40):
        positions = {}
        if not clusters:
            return positions
            
        angle_step = (end_angle - start_angle) / max(1, len(clusters) - 1) if len(clusters) > 1 else 0
        
        for i, cluster in enumerate(clusters):
            angle = start_angle + i * angle_step
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            positions[cluster] = (x, y)
        
        return positions
    
    # Position each group
    left_pos = position_cluster_group(left_clusters, 3*np.pi/4, 5*np.pi/4, radius=30)
    middle_pos = position_cluster_group(middle_clusters, np.pi/4, 3*np.pi/4, radius=40)
    right_pos = position_cluster_group(right_clusters, -np.pi/4, np.pi/4, radius=30)
    
    # Combine all positions
    cluster_pos = {**left_pos, **middle_pos, **right_pos}
    
    # Draw nodes for sources
    for source, (x, y) in source_pos.items():
        source_count = len(df[df['source'] == source])
        size = np.sqrt(source_count) * 50
        color = '#3498db' if source == 'Interview' else '#e74c3c'
        
        circle = plt.Circle((x, y), 6, color=color, alpha=0.9)
        ax.add_patch(circle)
        
        plt.text(x, y-10, f"{source}\n({source_count} patterns)", 
                 ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Draw nodes for clusters
    for cluster, (x, y) in cluster_pos.items():
        cluster_count = cluster_counts[cluster]
        size = np.sqrt(cluster_count) * 5
        
        circle = plt.Circle((x, y), size, color='#2ecc71', alpha=0.7)
        ax.add_patch(circle)
        
        # Add cluster name
        name_parts = cluster.split()
        if len(name_parts) > 3:
            # Split long names into multiple lines
            midpoint = len(name_parts) // 2
            name_text = ' '.join(name_parts[:midpoint]) + '\n' + ' '.join(name_parts[midpoint:])
        else:
            name_text = cluster
            
        plt.text(x, y, name_text, ha='center', va='center', 
                 fontsize=9, fontweight='bold')
        
        # Remove the count display below clusters
        # The following line is commented out to remove the small numbers
        # plt.text(x, y-size-3, f"({cluster_count})", ha='center', va='center', fontsize=8)
    
    # Draw edges between sources and clusters
    for _, row in df.iterrows():
        source = row['source']
        cluster = row['cluster']
        
        source_x, source_y = source_pos[source]
        cluster_x, cluster_y = cluster_pos[cluster]
        
        # Draw line with low alpha to avoid visual clutter
        color = '#3498db' if source == 'Interview' else '#e74c3c'
        plt.plot([source_x, cluster_x], [source_y, cluster_y], 
                 color=color, alpha=0.05, linewidth=0.5)
    
    # Add summary connections with width based on count
    for cluster in unique_clusters:
        cluster_x, cluster_y = cluster_pos[cluster]
        
        for source in ['Interview', 'Survey']:
            source_x, source_y = source_pos[source]
            count = len(df[(df['cluster'] == cluster) & (df['source'] == source)])
            
            if count > 0:
                color = '#3498db' if source == 'Interview' else '#e74c3c'
                width = np.sqrt(count) * 0.8
                
                plt.plot([source_x, cluster_x], [source_y, cluster_y], 
                         color=color, alpha=0.6, linewidth=width)
    
    plt.title('Network Visualization of Cybersecurity Pattern Sources and Clusters', fontsize=18)
    plt.xlim(-60, 60)
    plt.ylim(-50, 50)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('source_cluster_network.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created network visualization of sources and clusters")
# Main function that runs the visualizations
def main(latex_content):
    # Parse the data
    df = parse_latex_table(latex_content)
    
    # Create the visualizations
    create_network_visualization(df)
    create_heatmap_comparison(df)
    create_separate_source_affinity_diagrams(df)  # Added this to actually create all visualizations
    
    return df

# Sample LaTeX content (adding this as it was missing in the original)
sample_latex_content = r"""
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

\end{longtable}
"""

# Execute the main function with the sample content
if __name__ == "__main__":
    print("Processing cybersecurity pattern visualizations...")
    df = main(sample_latex_content)  # Pass the sample content to the main function
    print("\nVisualization process complete! The following files have been created:")
    print("1. source_cluster_network.png - Network diagram showing relationships between sources and clusters")
    print("2. cluster_source_heatmap.png - Heatmap showing the distribution of patterns across clusters and sources")
    print("3. interview_affinity_diagram.png - Affinity diagram showing Interview patterns")
    print("4. survey_affinity_diagram.png - Affinity diagram showing Survey patterns")
    
    print("\nData summary:")
    print(f"Total patterns: {len(df)}")
    print(f"Patterns by source: {df['source'].value_counts().to_dict()}")
    print(f"Number of unique clusters: {df['cluster'].nunique()}")
    
    # Sort clusters by count and display the top 5
    top_clusters = df['cluster'].value_counts().head(5)
    print("\nTop 5 clusters by pattern count:")
    for cluster, count in top_clusters.items():
        print(f"- {cluster}: {count} patterns")
