import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from pyvis.network import Network
import numpy as np
import os
import seaborn as sns
import json
import matplotlib.pyplot as plt
from pathlib import Path

# Create visualizations directory if it doesn't exist
vis_dir = Path("Visualizations")
vis_dir.mkdir(exist_ok=True)

# Read the dependencies CSV - enforce string type for story IDs
df = pd.read_csv('User Story Dependencies.csv', dtype={'Source Story': str, 'Target Story': str})

# Replace NaN values and ensure proper formatting
df['Source Story'] = df['Source Story'].fillna('Unknown').astype(str)
df['Target Story'] = df['Target Story'].fillna('NULL').astype(str)
df['Dependency Type'] = df['Dependency Type'].fillna('Unknown').astype(str)
df['Rationale'] = df['Rationale'].fillna('No rationale provided').astype(str)

# Filter out NULL values for certain visualizations
df_filtered = df[df['Target Story'] != 'NULL']

# Create a directed graph
G = nx.DiGraph()

# Define node groups by prefix
groups = {
    'CRM': '#8dd3c7',  # Collateral Record Management
    'RLM': '#ffffb3',  # Relationship Management
    'VRA': '#bebada',  # Valuation and Risk Assessment
    'WFN': '#fb8072',  # Workflow and Notifications
    'VIS': '#80b1d3',  # Visualization and Mapping
    'REP': '#fdb462',  # Reporting and Analytics
    'SCI': '#b3de69',  # System Configuration and Integration
    'SCD': '#fccde5',  # Security, Compliance, and Data Quality
}
DEFAULT_COLOR = '#d9d9d9'  # Default color for nodes without a recognized prefix

# Add all nodes first as string types with module information
for _, row in df.iterrows():
    source = str(row['Source Story'])
    if source not in G:
        prefix = source[:3] if len(source) >= 3 else source
        module = prefix if prefix in groups else "Other"
        G.add_node(source, prefix=prefix, module=module, 
                  color=groups.get(prefix, DEFAULT_COLOR))

    target = row['Target Story']
    if target != 'NULL' and target not in G:
        prefix = target[:3] if len(target) >= 3 else target
        module = prefix if prefix in groups else "Other"
        G.add_node(str(target), prefix=prefix, module=module, 
                  color=groups.get(prefix, DEFAULT_COLOR))

# Add all edges with type and rationale
for _, row in df.iterrows():
    source = str(row['Source Story'])
    target = row['Target Story']
    if target != 'NULL':
        G.add_edge(source, str(target), 
                  type=row['Dependency Type'], 
                  rationale=row['Rationale'])

# 1. PYVIS INTERACTIVE NETWORK VISUALIZATION
def create_interactive_network():
    # Create a Network object
    net = Network(height="800px", width="100%", directed=True, notebook=False, 
                 bgcolor="#ffffff", font_color="black")
    
    # Set physics layout options for better visualization
    net.barnes_hut(spring_length=200, spring_strength=0.001, damping=0.09, 
                  central_gravity=0.3, overlap=0)
    
    # Add nodes with proper attributes
    for node, attr in G.nodes(data=True):
        title = f"{node}<br>Module: {attr['module']}"
        net.add_node(node, label=node, title=title, color=attr['color'], 
                    size=20, borderWidth=2, borderWidthSelected=4,
                    font={'size': 14, 'face': 'Arial'})
    
    # Add edges with attributes
    for source, target, attr in G.edges(data=True):
        title = f"Type: {attr['type']}<br>Rationale: {attr['rationale']}"
        net.add_edge(source, target, title=title, 
                   arrows={'to': {'enabled': True, 'scaleFactor': 0.5}})
    
    # Save as HTML file
    net.save_graph(str(vis_dir / "interactive_network.html"))
    print(f"Interactive network saved as {vis_dir / 'interactive_network.html'}")

# 2. MODULE RELATIONSHIP SANKEY DIAGRAM
def create_module_sankey():
    # Count dependencies between modules
    module_edges = {}
    module_flow = []
    
    for _, row in df_filtered.iterrows():
        source = str(row['Source Story'])
        target = str(row['Target Story'])
        
        # Extract module prefixes
        source_prefix = source[:3] if len(source) >= 3 else source
        target_prefix = target[:3] if len(target) >= 3 else target
        
        # Only count edges between known modules
        if source_prefix in groups and target_prefix in groups and source_prefix != target_prefix:
            module_edges[(source_prefix, target_prefix)] = module_edges.get((source_prefix, target_prefix), 0) + 1
            module_flow.append({'source': source_prefix, 'target': target_prefix, 
                              'value': 1, 'type': row['Dependency Type']})
    
    # Create a DataFrame for the Sankey diagram
    flow_df = pd.DataFrame(module_flow)
    
    # Get unique modules
    all_modules = sorted(list(set(flow_df['source'].unique()) | set(flow_df['target'].unique())))
    module_indices = {module: i for i, module in enumerate(all_modules)}
    
    # Prepare Sankey data
    source_indices = [module_indices[source] for source in flow_df['source']]
    target_indices = [module_indices[target] for target in flow_df['target']]
    
    # Aggregate values by source-target pairs
    agg_df = flow_df.groupby(['source', 'target']).agg({'value': 'sum'}).reset_index()
    values = agg_df['value'].tolist()
    
    # Map to indices for the final Sankey
    final_sources = [module_indices[source] for source in agg_df['source']]
    final_targets = [module_indices[target] for target in agg_df['target']]
    
    # Create a color mapping for modules
    color_mapping = {module: groups.get(module, DEFAULT_COLOR) for module in all_modules}
    node_colors = [color_mapping[module] for module in all_modules]
    
    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_modules,
            color=node_colors
        ),
        link=dict(
            source=final_sources,
            target=final_targets,
            value=values,
            color='rgba(100, 100, 100, 0.4)'
        )
    )])
    
    fig.update_layout(
        title_text="Module Dependencies Flow",
        font_size=12,
        height=600,
        width=1000
    )
    
    # Save as HTML
    fig.write_html(str(vis_dir / "module_sankey.html"))
    print(f"Module Sankey diagram saved as {vis_dir / 'module_sankey.html'}")

# 3. INTERACTIVE DEPENDENCY MATRIX HEATMAP
def create_interactive_matrix():
    # Get all story IDs
    stories = sorted([str(node) for node in G.nodes()])
    
    # Group stories by module prefix
    story_to_module = {}
    for story in stories:
        story_str = str(story)
        prefix = story_str[:3] if len(story_str) >= 3 else story_str
        story_to_module[story] = prefix
    
    module_ordering = {module: i for i, module in enumerate(groups.keys())}
    
    # Create a sorting function that sorts by module then by ID
    def sort_key(story):
        story_str = str(story)
        module = story_str[:3] if len(story_str) >= 3 else "ZZZ"  # Default to end
        
        # Try to extract a numeric ID
        try:
            if '-' in story_str:
                story_num = int(story_str.split('-')[1])
            else:
                story_num = 0
        except (IndexError, ValueError):
            story_num = 0
            
        return (module_ordering.get(module, 999), story_num)
    
    # Sort stories by module and ID
    sorted_stories = sorted(stories, key=sort_key)
    
    # Create adjacency matrix
    adj_matrix = nx.to_numpy_array(G, nodelist=sorted_stories)
    
    # Find module boundaries
    module_boundaries = []
    current_module = None
    
    for i, story in enumerate(sorted_stories):
        module = story_to_module.get(story, "Other")
        if module != current_module:
            module_boundaries.append(i - 0.5)  # Offset by 0.5 to place line between cells
            current_module = module
    
    # Create heatmap with plotly
    fig = go.Figure(data=go.Heatmap(
        z=adj_matrix,
        x=sorted_stories,
        y=sorted_stories,
        colorscale='Blues',
        showscale=True,
        hoverongaps=False,
        hovertemplate='%{y} depends on %{x}<extra></extra>'
    ))
    
    # Add shapes for module boundaries
    for boundary in module_boundaries[1:]:  # Skip the first which is at -0.5
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=boundary,
            x1=len(sorted_stories) - 0.5,
            y1=boundary,
            line=dict(color="red", width=2)
        )
        fig.add_shape(
            type="line",
            x0=boundary,
            y0=-0.5,
            x1=boundary,
            y1=len(sorted_stories) - 0.5,
            line=dict(color="red", width=2)
        )
    
    fig.update_layout(
        title="User Story Dependency Matrix",
        height=800,
        width=900,
        xaxis=dict(
            tickangle=-90,
            side="bottom"
        )
    )
    
    # Save as HTML
    fig.write_html(str(vis_dir / "dependency_matrix.html"))
    print(f"Interactive dependency matrix saved as {vis_dir / 'dependency_matrix.html'}")

# 4. CRITICAL PATH ANALYSIS WITH HOVERABLE INFORMATION
def create_critical_path_analysis():
    # Count how many stories depend on each story (in-degree)
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())
    
    # Create data for critical stories
    critical_nodes = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:15]
    
    if not critical_nodes:
        print("No critical path data available")
        return
    
    stories, counts = zip(*critical_nodes)
    
    # Create colors based on module
    colors = []
    for story in stories:
        prefix = str(story)[:3] if len(str(story)) >= 3 else ""
        colors.append(groups.get(prefix, DEFAULT_COLOR))
    
    # Create hover text with additional information
    hover_texts = []
    for story in stories:
        deps_in = in_degree.get(story, 0)
        deps_out = out_degree.get(story, 0)
        
        # Get all stories that depend on this one
        dependent_stories = [n for n in G.predecessors(story)]
        dependent_str = ", ".join(dependent_stories[:5])
        if len(dependent_stories) > 5:
            dependent_str += f"... and {len(dependent_stories) - 5} more"
        
        hover_texts.append(
            f"<b>{story}</b><br>" +
            f"Module: {str(story)[:3] if len(str(story)) >= 3 else 'Unknown'}<br>" +
            f"Incoming dependencies: {deps_in}<br>" +
            f"Outgoing dependencies: {deps_out}<br>" +
            f"Dependent stories: {dependent_str if dependent_stories else 'None'}"
        )
    
    # Create interactive bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=list(stories),
            y=list(counts),
            marker_color=colors,
            hoverinfo="text",
            hovertext=hover_texts,
            text=list(counts),
            textposition="auto"
        )
    ])
    
    fig.update_layout(
        title="Critical Path Analysis: Most Depended-Upon User Stories",
        xaxis_title="User Story",
        yaxis_title="Number of Dependencies",
        height=600,
        width=1000,
        xaxis=dict(tickangle=-45)
    )
    
    # Save as HTML
    fig.write_html(str(vis_dir / "critical_path.html"))
    print(f"Critical path analysis saved as {vis_dir / 'critical_path.html'}")

# 5. DEPENDENCY TYPE DISTRIBUTION
def create_dependency_type_chart():
    if df_filtered.empty:
        print("No dependency type data available")
        return
    
    # Count dependency types
    dependency_types = df_filtered['Dependency Type'].value_counts().reset_index()
    dependency_types.columns = ['Type', 'Count']
    
    # Create a pie chart with plotly
    fig = px.pie(
        dependency_types, 
        values='Count', 
        names='Type',
        title='Distribution of Dependency Types',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hover_data=['Count']
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}'
    )
    
    fig.update_layout(
        height=600,
        width=800
    )
    
    # Save as HTML
    fig.write_html(str(vis_dir / "dependency_types.html"))
    print(f"Dependency type chart saved as {vis_dir / 'dependency_types.html'}")

# 6. CREATE A DASHBOARD HTML THAT LINKS TO ALL VISUALIZATIONS
def create_dashboard():
    # List of visualizations
    visualizations = [
        {
            "title": "Interactive Network Graph",
            "filename": "interactive_network.html",
            "description": "Explore the full dependency network with interactive nodes and edges. Hover for details and drag nodes to rearrange the view."
        },
        {
            "title": "Module Dependency Flow (Sankey)",
            "filename": "module_sankey.html",
            "description": "Visualize how dependencies flow between different modules using a Sankey diagram."
        },
        {
            "title": "Interactive Dependency Matrix",
            "filename": "dependency_matrix.html",
            "description": "View the dependency relationships in matrix form. Red lines separate different modules."
        },
        {
            "title": "Critical Path Analysis",
            "filename": "critical_path.html",
            "description": "Identify the most critical user stories based on how many other stories depend on them."
        },
        {
            "title": "Dependency Type Distribution",
            "filename": "dependency_types.html",
            "description": "See the distribution of different dependency types across all user stories."
        }
    ]
    
    # Create HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Story Dependency Analysis Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
                color: #333;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                border-radius: 5px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
                margin-top: 0;
            }
            h2 {
                color: #3498db;
                margin-top: 30px;
            }
            .card {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 20px;
                margin-bottom: 20px;
                background-color: #fff;
                transition: transform 0.3s ease;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .card h3 {
                margin-top: 0;
                color: #2c3e50;
            }
            .card p {
                color: #666;
            }
            .card a {
                display: inline-block;
                margin-top: 10px;
                padding: 8px 16px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                transition: background-color 0.3s;
            }
            .card a:hover {
                background-color: #2980b9;
            }
            .summary {
                background-color: #f1f8ff;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin-bottom: 30px;
            }
            .footer {
                margin-top: 50px;
                text-align: center;
                color: #7f8c8d;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>User Story Dependency Analysis Dashboard</h1>
            
            <div class="summary">
                <h2>Project Overview</h2>
                <p>This dashboard provides various interactive visualizations of the dependencies between user stories in the Collateral Management System. Use these visualizations to better understand the relationships, critical paths, and module interactions within the system.</p>
            </div>
            
            <h2>Available Visualizations</h2>
            <div class="visualizations">
    """
    
    # Add cards for each visualization
    for viz in visualizations:
        html_content += f"""
                <div class="card">
                    <h3>{viz['title']}</h3>
                    <p>{viz['description']}</p>
                    <a href="{viz['filename']}" target="_blank">Open Visualization</a>
                </div>
        """
    
    # Close HTML content
    html_content += """
            </div>
            
            <div class="footer">
                <p>Generated on """ + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Write to file
    with open(vis_dir / "index.html", "w") as f:
        f.write(html_content)
    
    print(f"Dashboard created at {vis_dir / 'index.html'}")

# Execute all visualization functions
if __name__ == "__main__":
    print("Generating HTML visualizations...")
    create_interactive_network()
    create_module_sankey()
    create_interactive_matrix()
    create_critical_path_analysis()
    create_dependency_type_chart()
    create_dashboard()
    print("All visualizations created in the 'Visualizations' folder!")
