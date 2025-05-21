import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.patches import Circle

# Set rendering defaults
mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['savefig.dpi'] = 1000
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.weight'] = 'normal'
mpl.rcParams['axes.titleweight'] = 'bold'

# Create dataframe from table data
data = [
    ["Digitization in Denmark", "RQ1", "Digital Infrastructure Challenges / Governance and Strategic Planning"],
    ["Strategic Targeting of Danish Infrastructure", "RQ1", "Critical Infrastructure Protection / Advanced Attack Strategies"],
    ["Multi-Vector Attacks", "RQ1", "Advanced Attack Strategies / State-Sponsored Threat Actors"],
    ["The Human Factor in Hybrid Defense", "RQ1", "Social Engineering and Human Vulnerabilities / Workforce and Expertise Challenges"],
    ["Incident Response and National Resilience", "RQ1", "Incident Response and Recovery / Governance and Strategic Planning"],
    ["Governance Fragmentation in Danish Infrastructure", "RQ1", "Governance and Strategic Planning / Regulatory and Compliance Matters"],
    
    ["Foreign Technology Dependencies", "RQ2", "Foreign Technology Considerations"],
    ["Asia's Advanced Persistent Threats", "RQ2", "State-Sponsored Threat Actors / Geopolitical Security Dimensions"],
    ["International Cooperation and Threat Intelligence", "RQ2", "International Collaboration / Information Operations"],
    ["Russia's Hybrid Warfare in Ukraine", "RQ2", "State-Sponsored Threat Actors / Advanced Attack Strategies / Information Operations"],
    ["Evolution of Threat Landscape", "RQ2", "Emerging Technology Threats / Geopolitical Security Dimensions / Information Operations"]
]

df = pd.DataFrame(data, columns=["section", "research_question", "clusters"])

# Expand clusters into rows
expanded_data = []
for _, row in df.iterrows():
    for cluster in row['clusters'].split(' / '):
        expanded_data.append([row['section'], row['research_question'], cluster])
expanded_df = pd.DataFrame(expanded_data, columns=["section", "research_question", "cluster"])

# Unique clusters and color mapping
unique_clusters = sorted(expanded_df['cluster'].unique())
color_palette = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5"
]
while len(color_palette) < len(unique_clusters):
    color_palette *= 2
cluster_colors = {cluster: color_palette[i] for i, cluster in enumerate(unique_clusters)}

rq_titles = {
    "RQ1": "RQ1: How does digitization aid in hybrid warfare campaigns, and how does this challenge Denmark's cybersecurity governance frameworks?",
    "RQ2": "RQ2: How do geopolitical tensions influence evolution of cyberwarfare against Denmark?"
}

def wrap_text(text, width=20):
    words = text.split()
    lines, current_line = [], []
    for word in words:
        if len(' '.join(current_line + [word])) <= width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return '\n'.join(lines)

def create_single_rq_visualization(rq, rq_title, df, expanded_df, cluster_colors):
    fig = plt.figure(figsize=(16, 14), dpi=100)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor('#F5F5F5')

    rq_df = df[df['research_question'] == rq]
    sections = rq_df['section'].tolist()
    n_sections = len(sections)

    section_colors = plt.cm.tab20(np.linspace(0, 1, n_sections))
    section_color_map = {section: section_colors[i] for i, section in enumerate(sections)}

    center_x, center_y = 0.5, 0.48  # Moved slightly down
    rq_radius = 0.1
    ax.add_patch(plt.Circle((center_x, center_y), rq_radius, fc='royalblue', ec='black', lw=2))
    ax.text(center_x, center_y, rq.upper(), ha='center', va='center', fontsize=16, fontweight='bold', color='white')

    wrapped_title = wrap_text(rq_title, width=55)
    ax.text(center_x, 0.96, wrapped_title, ha='center', va='center',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", fc='white', ec='black', alpha=0.8))

    angles = np.linspace(0, 2 * np.pi, n_sections, endpoint=False) + np.pi / n_sections
    theme_radius, theme_distance = 0.18, 0.36  # Slightly adjusted spacing

    for i, (section, angle) in enumerate(zip(sections, angles)):
        theme_x = center_x + theme_distance * np.cos(angle)
        theme_y = center_y + theme_distance * np.sin(angle)

        ax.add_patch(plt.Circle((theme_x, theme_y), theme_radius,
                                fc=section_color_map[section], ec='black', lw=1.5, alpha=0.9))

        section_text = wrap_text(section, width=10)
        ax.text(theme_x, theme_y, section_text, ha='center', va='center',
                fontsize=9, fontweight='bold', color='black')
        ax.plot([center_x, theme_x], [center_y, theme_y], '-', lw=2,
                color=section_color_map[section], alpha=0.7)

        section_clusters = expanded_df[(expanded_df['section'] == section) &
                                       (expanded_df['research_question'] == rq)]['cluster'].unique()
        n_clusters = len(section_clusters)
        cluster_span = np.pi / 4

        cluster_angles = ([angle] if n_clusters == 1 else
                          np.linspace(angle - cluster_span / 2, angle + cluster_span / 2, n_clusters))

        cluster_radius, cluster_distance = 0.045, 0.19

        for cluster, cluster_angle in zip(section_clusters, cluster_angles):
            cluster_x = theme_x + cluster_distance * np.cos(cluster_angle)
            cluster_y = theme_y + cluster_distance * np.sin(cluster_angle)

            ax.add_patch(plt.Circle((cluster_x, cluster_y), cluster_radius,
                                    fc=cluster_colors[cluster], ec='black', lw=1, alpha=0.9))

            words = cluster.split()
            formatted_cluster = '\n'.join([' '.join(words[i:i + 2]) for i in range(0, len(words), 2)])

            ax.text(cluster_x, cluster_y, formatted_cluster, ha='center', va='center',
                    fontsize=7, fontweight='bold', color='black')

            # Bezier curve for aesthetic link
            control_x = (theme_x + cluster_x) / 2 + np.sin(cluster_angle) * 0.03
            control_y = (theme_y + cluster_y) / 2 - np.cos(cluster_angle) * 0.03
            t = np.linspace(0, 1, 30)
            bezier_x = (1 - t) ** 2 * theme_x + 2 * (1 - t) * t * control_x + t ** 2 * cluster_x
            bezier_y = (1 - t) ** 2 * theme_y + 2 * (1 - t) * t * control_y + t ** 2 * cluster_y
            ax.plot(bezier_x, bezier_y, '-', lw=1.5, color=cluster_colors[cluster], alpha=0.8)

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.05)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(top=0.97, bottom=0.03)
    return fig


def create_legend_figure(unique_clusters, cluster_colors):
    legend_fig = plt.figure(figsize=(10, 5), dpi=100)
    legend_ax = legend_fig.add_subplot(111)
    legend_ax.axis('off')

    n_cols = 3
    n_rows = (len(unique_clusters) + n_cols - 1) // n_cols

    for i, cluster in enumerate(unique_clusters):
        row = i // n_cols
        col = i % n_cols
        x = 0.1 + col * 0.3
        y = 0.9 - row * 0.15

        legend_ax.add_patch(Circle((x, y), 0.03, fc=cluster_colors[cluster], ec='black'))
        legend_ax.text(x + 0.05, y, cluster, fontsize=10, va='center')

    legend_ax.set_xlim(0, 1)
    legend_ax.set_ylim(0, 1)
    legend_ax.set_title('Cybersecurity Clusters Legend', fontsize=14, fontweight='bold')
    return legend_fig

def main():
    rq1_fig = create_single_rq_visualization("RQ1", rq_titles["RQ1"], df, expanded_df, cluster_colors)
    rq1_fig.savefig('rq1_visualization.png', dpi=700, bbox_inches='tight')

    rq2_fig = create_single_rq_visualization("RQ2", rq_titles["RQ2"], df, expanded_df, cluster_colors)
    rq2_fig.savefig('rq2_visualization.png', dpi=700, bbox_inches='tight')

    legend_fig = create_legend_figure(unique_clusters, cluster_colors)
    legend_fig.savefig('clusters_legend.png', dpi=700, bbox_inches='tight')

    plt.show()

if __name__ == "__main__":
    main()
