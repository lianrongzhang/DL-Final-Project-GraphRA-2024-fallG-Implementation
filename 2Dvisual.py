import os
import pandas as pd
import networkx as nx
from pyvis.network import Network

def read_parquet_files(directory):
    dataframes = []
    for filename in os.listdir(directory):
        if filename.endswith('.parquet'):
            file_path = os.path.join(directory, filename)
            try:
                df = pd.read_parquet(file_path)
                dataframes.append(df)
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

directory = 'ragtest/output'

try:
    nodes_df = read_parquet_files(directory)
    edges_df = read_parquet_files(directory)
except Exception as e:
    print(f"Error reading Parquet files: {e}")
    exit(1)

required_node_columns = ['id', 'label']
required_edge_columns = ['source', 'target', 'relationship']

missing_node_columns = [col for col in required_node_columns if col not in nodes_df.columns]
for col in missing_node_columns:
    nodes_df[col] = 'default' if col == 'label' else None

missing_edge_columns = [col for col in required_edge_columns if col not in edges_df.columns]
for col in missing_edge_columns:
    edges_df[col] = None

nodes_df = nodes_df[(nodes_df['id'] != 'default') & (nodes_df['label'] != 'default')]

edges_df = edges_df[edges_df['source'] != 'default']
edges_df = edges_df[edges_df['target'] != 'default']


G = nx.Graph()

for _, row in nodes_df.iterrows():
    if pd.isna(row['id']):
        continue
    node_id = row['id']
    node_label = row['label']
    node_data = row.drop(['id', 'label'], errors='ignore').to_dict()
    G.add_node(node_id, label=node_label, **node_data)

for _, row in edges_df.iterrows():
    if pd.isna(row['source']) or pd.isna(row['target']):
        continue
    source = row['source']
    target = row['target']
    relationship = row.get('relationship', None)
    G.add_edge(source, target, relationship=relationship)

net = Network(height='100vh', width='100vw', notebook=True)
net.from_nx(G)

output_file = "graph_visualization.html"
net.show(output_file)
print(f"Graph visualization saved to {output_file}")