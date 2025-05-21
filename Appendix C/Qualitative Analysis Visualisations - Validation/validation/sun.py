import plotly.express as px

# Define simplified structure from the LaTeX table: Research Question -> Themes
rq_themes = {
    "RQ1": [
        "Digital Security Challenges",
        "Human Factor in Security",
        "System Vulnerabilities",
        "Hybrid Warfare Dynamics",
        "Critical Infrastructure",
        "Hybrid Warfare Tactics",
        "Defensive Capabilities",
        "Security Implementation",
        "Threat Evolution",
        "Resilience Strategies",
        "Societal Resilience",
        "Trust and Information Sharing",
        "Preparedness and Response",
        "Knowledge and Expertise"
    ],
    "RQ2": [
        "Digital Sovereignty",
        "Trust and Information Sharing",
        "Threat Landscape",
        "Knowledge and Expertise",
        "International Cooperation",
        "Attribution and Response",
        "Future Security Landscape"
    ]
}

# Build sunburst chart data
labels = []
parents = []
values = []

for rq, themes in rq_themes.items():
    labels.append(rq)
    parents.append("")
    values.append(0)

    for theme in themes:
        labels.append(theme)
        parents.append(rq)
        values.append(1)

# Create sunburst chart
fig = px.sunburst(
    names=labels,
    parents=parents,
    values=values,
    title="Research Questions and Associated Themes",
    width=1000,
    height=800
)

fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
fig.show()
