# Research-Network-Mapper
A Python-based tool that automates the identification of key influencers and collaborative clusters in scientific research.

## How it Works
1. **Data Acquisition:** Scrapes metadata based on user-defined keywords from the **arXiv API**.
2. **Graph Modeling:** Utilizes **NetworkX** to build a co-authorship graph where authors are treated as nodes and collaborations as edges.
3. **Mathematical Analysis:** Calculates **Normalized Degree Centrality** to quantify author influence:
   $$C_D(v) = \frac{deg(v)}{n-1}$$
4. **Visualization:**
Uses **Spring Layout** to reveal research "cliques" and bridge researchers.

## Tech Stack
* **Language:** Python
* **Libraries:** NetworkX, Matplotlib, Pandas, Feedparser

