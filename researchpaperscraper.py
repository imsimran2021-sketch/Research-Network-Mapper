import feedparser
import pandas as pd
import urllib.parse
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
def fetch_papers(query,max_results=10):
    s=urllib.parse.quote(query)
    url=f'https://export.arxiv.org/api/query?search_query=all:{s}&start=0&max_results={max_results}'
    feed=feedparser.parse(url)
    papers=[]
    for entry in feed.entries:
        papers.append({
       'title':entry.title,
        'authors':",".join(author.name for author in entry.authors),
        'published':entry.published,
        'summary':entry.summary,
        'link':entry.link})
    return pd.DataFrame(papers)
df = fetch_papers("reimann surface",max_results=5)
print(df[['title', 'authors']])



def build_authornet(df):
    G = nx.Graph()

    # 1. Add connections (Edges) for every paper
    for authors in df['authors']:
        if isinstance(authors,str):
            authorlist= [a.strip() for a in authors.split(',')]
        else:
                authorlist=authors
            # combinations(authors, 2) creates pairs: (Auth A, Auth B), (Auth A, Auth C), etc.
        if len(authorlist)>1:
            for pair in combinations(authorlist, 2):
                G.add_edge(pair[0], pair[1])
        else:
            # Handle single-author papers
            if authors:
                G.add_node(authors[0])

    # 2. Calculate Degree Centrality (The Math part!)
    cen= nx.degree_centrality(G)
    
    # 3. Sort authors by most connected
    sorted_authors = sorted(cen.items(), key=lambda x: x[1], reverse=True)
    
    nodesizes = [v * 5000 for v in cen.values()]
    nodecolors = list(cen.values())
    
    return G, sorted_authors, nodesizes, nodecolors
   
# --- EXECUTION ---
# (Assuming 'df' is the DataFrame you created yesterday)
G, top_authors, nsizes, ncolors = build_authornet(df)
print("Top 5 Most Connected Authors:")
for auth, score in top_authors[:5]:
    print(f"{auth}: {score:.4f}")


# 4. Simple Visualization
plt.figure(figsize=(15, 12))
pos = nx.spring_layout(G, k=3.0,iterations=200,seed=42) # k controls the spacing between nodes
nodes = nx.draw_networkx_nodes(G, pos,node_size=nsizes,node_color=ncolors, cmap=plt.cm.plasma,alpha=0.7,linewidths=1.5,edgecolors='white')
nx.draw(G, pos, with_labels=True, node_size=20, font_size=8, edge_color='gray', alpha=0.6)
nx.draw_networkx_edges(G, pos, alpha=0.05, edge_color='black')
top_5 = {auth: auth for auth, score in top_authors[:5]}
nx.draw_networkx_labels(G, pos, labels=top_5, font_size=10, font_weight="bold",verticalalignment="bottom")

plt.colorbar(nodes, label="Degree Centrality Score")
plt.title("Academic Collaboration Network\n(Clustered by Co-authorship)", fontsize=18, pad=25)
plt.axis('off')
plt.show()

plt.savefig("/sdcard/Download/research_network.png", dpi=300)
print("Graph saved to your Downloads folder!")
# Convert your 'top_authors' list to a DataFrame and save
top_df = pd.DataFrame(top_authors, columns=['Author', 'Centrality_Score'])
top_df.to_csv("/sdcard/Download/top_influencers.csv", index=False)
