import plotly.express as px

# Define the new hierarchical structure based on the table with RQ1 and RQ2
labels = []
parents = []
values = []

affinity_structure = {
    "RQ1": {
        "Digitization in Denmark": [
            "Digital Infrastructure Challenges / Governance and Strategic Planning"
        ],
        "Strategic Targeting of Danish Infrastructure": [
            "Critical Infrastructure Protection / Advanced Attack Strategies"
        ],
        "Multi-Vector Attacks": [
            "Advanced Attack Strategies / State-Sponsored Threat Actors"
        ],
        "The Human Factor in Hybrid Defense": [
            "Social Engineering and Human Vulnerabilities / Workforce and Expertise Challenges"
        ],
        "Incident Response and National Resilience": [
            "Incident Response and Recovery / Governance and Strategic Planning"
        ],
        "Governance Fragmentation in Danish Infrastructure": [
            "Governance and Strategic Planning / Regulatory and Compliance Matters"
        ]
    },
    "RQ2": {
        "Foreign Technology Dependencies": [
            "Foreign Technology Considerations"
        ],
        "Asia’s Advanced Persistent Threats": [
            "State-Sponsored Threat Actors / Geopolitical Security Dimensions"
        ],
        "International Cooperation and Threat Intelligence": [
            "International Collaboration / Information Operations"
        ],
        "Russia’s Hybrid Warfare in Ukraine": [
            "State-Sponsored Threat Actors / Advanced Attack Strategies / Information Operations"
        ],
        "Evolution of Threat Landscape": [
            "Emerging Technology Threats / Geopolitical Security Dimensions / Information Operations"
        ]
    }
}

# Build labels and parents
for main_cat, subcats in affinity_structure.items():
    labels.append(main_cat)
    parents.append("")
    values.append(0)

    for subcat, clusters in subcats.items():
        labels.append(subcat)
        parents.append(main_cat)
        values.append(0)

        for cluster in clusters:
            labels.append(cluster)
            parents.append(subcat)
            values.append(1)

# Create Sunburst plot
fig = px.sunburst(
    names=labels,
    parents=parents,
    values=values,
    maxdepth=-1,
    title="RQ1 and RQ2: Clusters Matching Sections",
    width=1000,
    height=800
)

fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
fig.show()
import plotly.express as px

# Define the new hierarchical structure based on the table
labels = []
parents = []
values = []

affinity_structure = {
    "RQ1: How does digitization aid in hybrid warfare campaigns, and how does this challenge Denmark’s cybersecurity governance frameworks?": {
        "Digitization in Denmark": [
            "Digital Infrastructure Challenges / Governance and Strategic Planning"
        ],
        "Strategic Targeting of Danish Infrastructure": [
            "Critical Infrastructure Protection / Advanced Attack Strategies"
        ],
        "Multi-Vector Attacks": [
            "Advanced Attack Strategies / State-Sponsored Threat Actors"
        ],
        "The Human Factor in Hybrid Defense": [
            "Social Engineering and Human Vulnerabilities / Workforce and Expertise Challenges"
        ],
        "Incident Response and National Resilience": [
            "Incident Response and Recovery / Governance and Strategic Planning"
        ],
        "Governance Fragmentation in Danish Infrastructure": [
            "Governance and Strategic Planning / Regulatory and Compliance Matters"
        ]
    },
    "RQ2: How do geopolitical tensions influence evolution of cyberwarfare against Denmark?": {
        "Foreign Technology Dependencies": [
            "Foreign Technology Considerations"
        ],
        "Asia’s Advanced Persistent Threats": [
            "State-Sponsored Threat Actors / Geopolitical Security Dimensions"
        ],
        "International Cooperation and Threat Intelligence": [
            "International Collaboration / Information Operations"
        ],
        "Russia’s Hybrid Warfare in Ukraine": [
            "State-Sponsored Threat Actors / Advanced Attack Strategies / Information Operations"
        ],
        "Evolution of Threat Landscape": [
            "Emerging Technology Threats / Geopolitical Security Dimensions / Information Operations"
        ]
    }
}

# Build labels and parents
for main_cat, subcats in affinity_structure.items():
    labels.append(main_cat)
    parents.append("")
    values.append(0)

    for subcat, clusters in subcats.items():
        labels.append(subcat)
        parents.append(main_cat)
        values.append(0)

        for cluster in clusters:
            labels.append(cluster)
            parents.append(subcat)
            values.append(1)

# Create Sunburst plot
fig = px.sunburst(
    names=labels,
    parents=parents,
    values=values,
    maxdepth=-1,
    title="RQ1 and RQ2: Clusters Matching Sections",
    width=1000,
    height=800
)

fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
fig.show()

