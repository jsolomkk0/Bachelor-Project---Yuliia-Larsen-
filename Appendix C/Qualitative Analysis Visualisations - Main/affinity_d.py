import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

# Load your data into a DataFrame
data = pd.read_csv("data.csv")  # Or parse your LaTeX into DataFrame

# Extract text features from Pattern Labels
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Pattern Label'])

# Reduce to 2D for plotting
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X.toarray())

data['x'] = X_reduced[:, 0]
data['y'] = X_reduced[:, 1]

# Plot using Plotly
fig = px.scatter(
    data,
    x='x',
    y='y',
    color='Cluster',
    text='Pattern Label',
    title='Clustered Codes after Affinity Diagram',
    hover_data=['Source']
)

fig.update_traces(textposition='top center')
fig.update_layout(legend_title_text='Cluster')
fig.show()
