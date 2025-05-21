import plotly.express as px

# Define the hierarchical structure
labels = []
parents = []
values = []

affinity_structure = {
    "Critical Infrastructure Vulnerabilities": {
        "Digital System Dependencies": [
            "P3: Denmark has moved to digital electoral rolls... The question becomes: what happens if the system goes down?",
            "P3: If power goes out and digital election lists fail, forcing a return to paper lists, it will be inconvenient and time-consuming.",
            "P13: Everything in healthcare is online... creates chaos.",
            "P2: Denmark is a highly digitalized country...",
            "P5: Our hospitals are becoming increasingly digitalized..."
        ],
        "Water and Energy Systems": [
            "P13: Threats against critical infrastructure... form the foundation of our society.",
            "P12: Last year there was a cyber attack on a water facility...",
            "P13: Center for Cybersecurity... water systems becoming attractive targets...",
            "P6: If they can take down hospitals, power supply, or water supply...",
            "P6: Russian attacks recently on water facilities...",
            "P6: No power means no hospitals, no water..."
        ],
        "Healthcare Sector Vulnerabilities": [
            "P7: The healthcare sector is an attractive target...",
            "P13: The most interesting target is communication between patients and providers.",
            "P15: Imagine a hospital gets hacked... moral effect is much greater.",
            "P9: Healthcare system in Denmark is dependent on IT...",
            "P6: Earlier hospitals were off-limits... That changed...",
            "P6: Main challenge is legacy software...",
            "P14: Biggest risks are attacks on older hospital equipment.",
            "P10: Budget constraints keep outdated medical systems in place."
        ],
        "Authentication System Vulnerabilities": [
            "P8: MitID and NemID are critical infrastructure...",
            "P8: You could enumerate usernames in MitID.",
            "P8: NemID's problem was social engineering."
        ]
    },
    "Technology Dependencies and Sovereignty": {
        "Foreign Technology Reliance": [
            "P3: Denmark is essentially a Microsoft country...",
            "P13: We're relying too much on foreign tools...",
            "P13: If a provider stops supporting us...",
            "P6: Limited supplier choice limits security requirements.",
            "P14: 80% of PCs and servers are Microsoft.",
            "P14: Microsoft releases security patches every Tuesday."
        ],
        "Chinese Technology Concerns": [
            "P6: Chinese AI systems... data goes to China.",
            "P6: Massive issue with Chinese surveillance cameras.",
            "P14: We block Chinese AI tools.",
            "P10: Some Chinese apps banned.",
            "P1: Blocked DeepSeek due to data leak risk."
        ],
        "US-Europe Relations and Platform Dependencies": [
            "P1: European companies need exit plans for US cloud.",
            "P1: Monitoring Trump and Greenland military discussions.",
            "P1: Considering blocking Musk's X AI."
        ],
        "Shifting Geopolitical Alignments": [
            "P7: US-Russia alignment raises questions.",
            "P13: Trust with US companies has changed.",
            "P9: No more cooperation with Chinese/Russian researchers.",
            "P9: Previously had exchange programs—now banned."
        ]
    },
    "Multi-Vector Attack Landscape": {
        "Coordinated Attack Strategies": [
            "P7: Attacks targeting multiple sectors simultaneously.",
            "P15: DDoS combined with hotline flooding.",
            "P15: Russia hacked a children's hospital before missile strike.",
            "P6: Phishing led to defense system compromise.",
            "P11: MITRE ATT&CK persistence techniques.",
            "P11: Multiple admin accounts as backup access."
        ],
        "Physical-Digital Combined Threats": [
            "P6: Baltic Sea ships without transponders.",
            "P6: Could disrupt communications or cause chaos.",
            "P14: We prepare for outages using old methods."
        ],
        "Ransomware and Phishing": [
            "P13: Akira ransomware is primary threat.",
            "P13: APT groups begin with phishing.",
            "P12: Legacy systems + employee entry point.",
            "P6: 95% of malware comes via email.",
            "P11: 85-90% attacks caused by human error.",
            "P1: Social engineering is the dominant attack method."
        ],
        "Emerging Threats": [
            "P13: Generative AI APIs are easily connected.",
            "P3: Zero days as cyber warfare ammunition.",
            "P6: Real-time deepfakes with Danish voice AI.",
            "P5: Unknown AI threats will dominate focus.",
            "P5: AI countermeasures will be our future challenge.",
            "P1: Generative AI enables tailored phishing."
        ]
    },
    "Human Factor and Cultural Challenges": {
        "Trust as Vulnerability": [
            "P3: Trust is a liability in Denmark.",
            "P3: Nobody expects a hacker from afar.",
            "P13: We don’t act until affected.",
            "P9: People trust tech they don’t understand."
        ],
        "Education and Awareness": [
            "P7: Biggest risk is lack of cyber competency.",
            "P12: Invest in people and training.",
            "P13: Young understand, old reluctant.",
            "P6: Users click everything.",
            "P6: 40 min/year awareness training allowed.",
            "P14: Internal threats are primary risk.",
            "P10: Security is human behavior.",
            "P5: Problem is people, not programs."
        ],
        "Social Engineering": [
            "P15: Malware and phishing are social engineering.",
            "P15: Russia excels at social engineering.",
            "P12: Maersk attack used employee access.",
            "P6: 34-45% plug in random USB sticks.",
            "P1: Emergency hospital staff more vulnerable."
        ]
    },
    "Data Protection and Encryption Challenges": {
        "Cryptographic Security": [
            "P2: Cryptography underpins communication.",
            "P2: Quantum computers threaten current crypto.",
            "P2: New crypto primitives needed.",
            "P2: Transition to post-quantum crypto is hard."
        ],
        "Regulatory Frameworks": [
            "P4: Everything governed by GDPR.",
            "P4: People overestimate privacy methods.",
            "P2: Strong data protection authority exists.",
            "P9: GDPR creates extra burdens."
        ],
        "Data as Strategic Asset": [
            "P9: Unknown data control can harm citizens.",
            "P9: Health data might go to insurers.",
            "P4: Eye movements reveal deep info.",
            "P6: Patient data leaks to foreign clouds."
        ]
    },
    "Governance and Response Coordination": {
        "Fragmented Responses": [
            "P3: Denmark lacks tabletop simulations.",
            "P13: No public outage awareness campaigns.",
            "P3: Scattered, disconnected infrastructure.",
            "P6: Security was neglected.",
            "P6: Departments installed systems freely.",
            "P8: No official contact for reporting incidents."
        ],
        "Incident Response Processes": [
            "P6: Response room with all stakeholders.",
            "P6: Two-track response system."
        ],
        "Consolidation Efforts": [
            "P7: Ministries now consolidating responsibilities."
        ]
    }
}

# Build labels and parents
for main_cat, subcats in affinity_structure.items():
    labels.append(main_cat)
    parents.append("")
    values.append(0)

    for subcat, quotes in subcats.items():
        labels.append(subcat)
        parents.append(main_cat)
        values.append(0)

        for quote in quotes:
            labels.append(quote)
            parents.append(subcat)
            values.append(1)

# Create Sunburst plot
fig = px.sunburst(
    names=labels,
    parents=parents,
    values=values,
    maxdepth=-1,
    title="Affinity Diagram: Danish Cybersecurity and Hybrid Warfare",
    width=1000,
    height=800
)

fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
fig.show()

