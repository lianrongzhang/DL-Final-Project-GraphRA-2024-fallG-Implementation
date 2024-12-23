import os 
import pandas as pd 
import networkx as nx 
import plotly.graph_objects as go 

def read_parquet_files(directory):
    dataframes = []
    for filename in os.listdir(directory):
        if filename.endswith('.parquet'):
            file_path = os.path.join(directory, filename)
            df = pd.read_parquet(file_path)
            dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

def clean_dataframe(df):
    df = df.dropna(subset=['source', 'target'])
    df['source'] = df['source'].astype(str)
    df['target'] = df['target'].astype(str)
    return df

def create_knowledge_graph(df):
    G = nx.DiGraph()
    for _, row in df.iterrows():
        source = row['source']
        target = row['target']
        attributes = {k: v for k, v in row.items() if k not in ['source', 'target']}
        G.add_edge(source, target, **attributes)
    return G

def create_node_link_trace(G, pos):
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_z = [pos[node][2] for node in G.nodes()]

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='ylorrd',
            size=18,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            )
        )
    )

    node_adjacencies = []
    node_text = []
    for node, adjacencies in G.adjacency():
        node_adjacencies.append(len(adjacencies))
        node_text.append(f'Node: {node}<br># of connections: {len(adjacencies)}')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    return edge_trace, node_trace

def visualize_graph_plotly(G):
    if G.number_of_nodes() == 0:
        print("Graph is empty. Nothing to visualize.")
        return

    pos = nx.spring_layout(G, dim=3)  # 3D layout
    edge_trace, node_trace = create_node_link_trace(G, pos)

    fig = go.Figure()
    fig.add_trace(edge_trace)
    fig.add_trace(node_trace)

    fig.update_layout(
        scene=dict(
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            zaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            aspectmode='cube'
        ),
        scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
        title="3D Knowledge Graph",
        showlegend=False
    )

    fig.show()

def main():
    directory = './ragtest/output'  # Specify your directory
    df = read_parquet_files(directory)

    if df.empty:
        print("No data found in the specified directory.")
        return

    print("Original DataFrame shape:", df.shape)
    print("Original DataFrame columns:", df.columns.tolist())

    df = clean_dataframe(df)

    print("\nCleaned DataFrame shape:", df.shape)

    if df.empty:
        print("No valid data remaining after cleaning.")
        return

    G = create_knowledge_graph(df)

    print(f"\nGraph statistics:")
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")

    visualize_graph_plotly(G)

if __name__ == "__main__":
    main()