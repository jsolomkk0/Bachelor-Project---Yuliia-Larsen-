import matplotlib.pyplot as plt
import networkx as nx

# Define the themes, their corresponding codes, and associated quotes
themes = {
    "Critical Infrastructure Vulnerabilities": [
        ("BASELINE_SECURITY_DEFICIT", "First of all, the community recognized the fact that there was almost no proper cybersecurity in government agencies, enterprises, and institutions."),
        ("CRITICAL_INFRASTRUCTURE_IDENTIFICATION_GAP", "...it was not determined which enterprises, institutions, and systems are critical for ensuring the livelihood of the population of Ukraine."),
        ("RESOURCE_ALLOCATION_CHALLENGES", "The use of non-modern means and solutions to counter cyberattacks, the state cannot always allocate a budget for each medical institution."),
        ("GOVERNMENT_SECURITY_WEAKNESS", "...in government agencies, the protection of information systems is either absent or at a minimal level."),
        ("ENERGY_SECTOR_TARGETING", "Energy infrastructure facilities were among the main targets of cyberattacks from Russian cyber groups.")
    ],
    "Technology Dependencies and Sovereignty": [
        ("WESTERN_ALLIANCE_BENEFITS", "Ukraine's cybersecurity cooperation with Western countries has strengthened its hybrid defense, increased resilience to cyberattacks, and contributed to rapprochement with the EU and NATO."),
        ("INTERNATIONAL_CAPACITY_BUILDING", "Cooperation with international partners helps Ukraine receive material and technical assistance, free staff training, and exchange of indicators and information about cyber threats."),
        ("MILITARY_CYBER_INTEGRATION", "The conflict raised awareness of the need to integrate cybersecurity into the military strategies of NATO countries."),
        ("REAL_TIME_THREAT_INTELLIGENCE", "Ukraine actively cooperates with international partners, receiving data on new cyberattacks in real time.")
    ],
    "Multi-Vector Attack Landscape": [
        ("HYBRID_WARFARE_TACTICS", "Russia uses combined attacks on critical infrastructure, such attacks can serve as missile strikes in combination with a cyberattack on infrastructure."),
        ("ATTACK_METHODOLOGY_EVOLUTION", "Since the beginning of the full-scale invasion, 'cyberwar' has expanded the range of tactics and tools used in cyberattacks."),
        ("LOW_EFFORT_HIGH_IMPACT_THREATS", "The most likely threats to hospitals will be those that have a low entry threshold, quick effect, and maximum destructive impact. These are phishing campaigns, ransomware, DDoS attacks."),
        ("SOCIOPOLITICAL_MANIPULATION", "Cyber operations can be used to influence elections, manipulate public opinion, and conduct economic warfare.")
    ],
    "Human Factor and Cultural Challenges": [
        ("WARTIME_PERSONNEL_SHORTAGE", "Lack of qualified personnel (personnel shortage), as hostilities make their adjustments."),
        ("LEADERSHIP_COMPETENCY_ISSUES", "No less important, but also considered important is the presence of an incompetent head of an organization or institution, which in turn can lead to the 'decline' of cybersecurity issues in general."),
        ("PHISHING_VULNERABILITY", "80% of breaches start with phishing, a simple and effective way to penetrate a hospital's network, insufficient awareness of hospital staff about cyber hygiene."),
        ("HUMAN_ERROR_PREVALENCE", "It is also especially important to train personnel – 80% of attacks start with the human factor (phishing, weak passwords).")
    ],
    "Data Protection and Encryption Challenges": [
        ("MEDICAL_DATA_VULNERABILITY", "The importance of medical data access to medical histories, diagnoses, laboratory tests can be under threat or theft."),
        ("HEALTHCARE_OPERATIONAL_DISRUPTION", "In the medical field, such attacks pose a serious threat as they can block access to electronic medical records, stop the operation of vital equipment, and lead to the leakage of confidential data."),
        ("RANSOM_PAYMENT_TENDENCY", "Some private medical institutions are even ready to cooperate with cybercriminals (pay a ransom to quickly restore work and prevent the leakage of patients' personal data)."),
        ("REAL_MEDICAL_DATA_BREACH", "As an example, we can cite the recent attack on the HELSI medical information system, the essence of which was to use the vulnerabilities of the database systems, as a result of which a lot of patient data was sold on the DarkNet.")
    ],
    "Governance and Response Coordination": [
        ("INTELLIGENCE_QUALITY_ISSUES", "Incompleteness of collected information - which in turn can provide false information about the attack."),
        ("THREAT_PREDICTION_DEFICIT", "Lack of cyber intelligence and predictive risk assessment for cyberattacks on Ukraine's infrastructure."),
        ("CENTRALIZED_INCIDENT_RESPONSE", "Centralization of cybersecurity, use of technology for data preservation, rapid response to attacks."),
        ("CONTAINMENT_STRATEGY", "Limiting and localizing a resource that has been attacked to prevent spread by attackers."),
        ("LEGAL_FRAMEWORK_CONSTRAINTS", "Legal limitations and complexities in international law regarding cybercrimes.")
    ],
    "National Resilience and Strategic Awareness": [
        ("THREAT_AWARENESS_PROGRESS", "Today, government agencies, organizations, and institutions can be aware of certain cyber threats that have already occurred in the national resilience system and predict (prevent) similar cases in their own infrastructures."),
        ("CROSS_BORDER_SECURITY_RESPONSIBILITY", "Ukraine accepts citizens in medical institutions from other countries, and this is the security not only of Ukraine but also of international partners in general."),
        ("CLOUD_BACKUP_EFFICACY", "Backup and cloud technologies have proven their effectiveness – Ukraine transferred critical data to secure clouds, which allowed quick recovery of systems after attacks."),
        ("PROACTIVE_SECURITY_POSTURE", "Proactive monitoring and response to threats to quickly detect and neutralize attacks."),
        ("STRATEGIC_IMPLEMENTATION_BENEFITS", "If each medical institution follows Ukraine's cybersecurity strategy, then in general, one can achieve the best level of cybersecurity and minimize 75% of cyberattacks.")
    ]
}

# Create a graph
G = nx.Graph()

# Add nodes for each theme and code with quotes
for theme, quotes in themes.items():
    G.add_node(theme, type='theme')
    for code, quote in quotes:
        G.add_node(code, type='code', label=quote)
        G.add_edge(theme, code)

# Define the layout for the plot
pos = nx.spring_layout(G, seed=42)

# Plot the graph
plt.figure(figsize=(14, 10))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=8, font_weight='bold', edge_color='gray')

# Annotate the quotes
for node, (x, y) in pos.items():
    if G.nodes[node].get('type') == 'code':
        plt.text(x, y, G.nodes[node]['label'], fontsize=6, ha='left', va='bottom', color='black', alpha=0.7)

# Display the plot
plt.title('Cybersecurity Affinity Diagram with Quotes')
plt.axis('off')
plt.show()
import matplotlib.pyplot as plt
import networkx as nx

# Define the themes and their corresponding codes
themes = {
    "Critical Infrastructure Vulnerabilities": [
        "BASELINE_SECURITY_DEFICIT",
        "CRITICAL_INFRASTRUCTURE_IDENTIFICATION_GAP",
        "RESOURCE_ALLOCATION_CHALLENGES",
        "GOVERNMENT_SECURITY_WEAKNESS",
        "ENERGY_SECTOR_TARGETING"
    ],
    "Technology Dependencies and Sovereignty": [
        "WESTERN_ALLIANCE_BENEFITS",
        "INTERNATIONAL_CAPACITY_BUILDING",
        "MILITARY_CYBER_INTEGRATION",
        "REAL_TIME_THREAT_INTELLIGENCE"
    ],
    "Multi-Vector Attack Landscape": [
        "HYBRID_WARFARE_TACTICS",
        "ATTACK_METHODOLOGY_EVOLUTION",
        "LOW_EFFORT_HIGH_IMPACT_THREATS",
        "SOCIOPOLITICAL_MANIPULATION"
    ],
    "Human Factor and Cultural Challenges": [
        "WARTIME_PERSONNEL_SHORTAGE",
        "LEADERSHIP_COMPETENCY_ISSUES",
        "PHISHING_VULNERABILITY",
        "HUMAN_ERROR_PREVALENCE"
    ],
    "Data Protection and Encryption Challenges": [
        "MEDICAL_DATA_VULNERABILITY",
        "HEALTHCARE_OPERATIONAL_DISRUPTION",
        "RANSOM_PAYMENT_TENDENCY",
        "REAL_MEDICAL_DATA_BREACH"
    ],
    "Governance and Response Coordination": [
        "INTELLIGENCE_QUALITY_ISSUES",
        "THREAT_PREDICTION_DEFICIT",
        "CENTRALIZED_INCIDENT_RESPONSE",
        "CONTAINMENT_STRATEGY",
        "LEGAL_FRAMEWORK_CONSTRAINTS"
    ],
    "National Resilience and Strategic Awareness": [
        "THREAT_AWARENESS_PROGRESS",
        "CROSS_BORDER_SECURITY_RESPONSIBILITY",
        "CLOUD_BACKUP_EFFICACY",
        "PROACTIVE_SECURITY_POSTURE",
        "STRATEGIC_IMPLEMENTATION_BENEFITS"
    ]
}

# Create a graph
G = nx.Graph()

# Add nodes for each theme and code
for theme, codes in themes.items():
    G.add_node(theme, type='theme')
    for code in codes:
        G.add_node(code, type='code')
        G.add_edge(theme, code)

# Define the layout for the plot
pos = nx.spring_layout(G, seed=42)

# Plot the graph
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold', edge_color='gray')

# Display the plot
plt.title('Cybersecurity Affinity Diagram')
plt.show()

