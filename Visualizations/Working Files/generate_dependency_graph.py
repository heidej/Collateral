import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('Agg')  # Use non-interactive backend
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Set the style
plt.style.use('seaborn-v0_8-whitegrid')

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

# Add all nodes first as string types
for _, row in df.iterrows():
    source = str(row['Source Story'])
    if source not in G:
        # Extract prefix safely
        prefix = source[:3] if len(source) >= 3 else source
        G.add_node(source, prefix=prefix)

    target = row['Target Story']
    if target != 'NULL' and target not in G:
        # Extract prefix safely
        prefix = target[:3] if len(target) >= 3 else target
        G.add_node(str(target), prefix=prefix)

# Add all edges - ensure all values are strings
for _, row in df.iterrows():
    source = str(row['Source Story'])
    target = row['Target Story']
    if target != 'NULL':
        G.add_edge(source, str(target), 
                  type=row['Dependency Type'], 
                  rationale=row['Rationale'])

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

# Group nodes by their module prefix
module_nodes = {}
for node in G.nodes():
    node_str = str(node)
    prefix = node_str[:3] if len(node_str) >= 3 else node_str
    if prefix not in module_nodes:
        module_nodes[prefix] = []
    module_nodes[prefix].append(node)

# 1. IMPROVED MAIN VISUALIZATION - USER STORY DEPENDENCY GRAPH
plt.figure(figsize=(22, 18))

# Use a different layout algorithm that keeps related nodes closer together
# Try with stronger attraction between nodes
pos = nx.kamada_kawai_layout(G)

# Assign colors based on node prefixes
node_colors = []
for node in G.nodes():
    node_str = str(node)
    prefix = node_str[:3] if len(node_str) >= 3 else node_str
    node_colors.append(groups.get(prefix, DEFAULT_COLOR))

# Draw the graph with improved parameters
nx.draw(G, pos, with_labels=True, node_color=node_colors, 
        node_size=1000,  # Slightly larger nodes 
        font_size=9,     # Slightly larger font
        font_weight='bold', 
        arrowsize=15, 
        width=1.5,
        edge_color='gray', 
        alpha=0.9,       # More opaque
        connectionstyle='arc3,rad=0.1')  # Curved edges to reduce overlap

# Create a legend for module types
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                             markerfacecolor=color, markersize=15, label=prefix)
                  for prefix, color in groups.items()]

plt.legend(handles=legend_elements, title="Module Types", loc="upper right", fontsize=12)
plt.title("User Story Dependencies - Comprehensive View", fontsize=20)

# Add module labels to identify clusters
for module, nodes in module_nodes.items():
    if nodes and module in groups:  # Only for recognized modules with nodes
        # Calculate the centroid of this module's nodes
        x_coords = [pos[node][0] for node in nodes]
        y_coords = [pos[node][1] for node in nodes]
        if x_coords and y_coords:  # Ensure lists are not empty
            centroid_x = sum(x_coords) / len(x_coords)
            centroid_y = sum(y_coords) / len(y_coords)
            
            # Add a module label at the centroid
            plt.text(centroid_x, centroid_y, module, 
                    fontsize=18, fontweight='bold', 
                    ha='center', va='center',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor=groups[module]))

plt.savefig('User_Story_Dependencies.png', dpi=300, bbox_inches='tight')
print("Improved dependency graph saved as User_Story_Dependencies.png")

# Also create a hierarchical version that's easier to read
plt.figure(figsize=(24, 20))

# Create a hierarchically structured layout
hierarchy_pos = {}

# Calculate positions for each module - separate them clearly and make them larger
module_positions = {
    'CRM': (0.5, 0.9),   # Top center
    'RLM': (0.2, 0.7),   # Upper left
    'VRA': (0.8, 0.7),   # Upper right
    'WFN': (0.2, 0.4),   # Middle left
    'VIS': (0.8, 0.4),   # Middle right
    'REP': (0.5, 0.5),   # Center
    'SCI': (0.2, 0.1),   # Bottom left
    'SCD': (0.8, 0.1),   # Bottom right
}

# Create a strict mapping of nodes to their modules based on the prefix
node_to_module = {}
for node in G.nodes():
    node_str = str(node)
    # Extract the module prefix (first 3 characters if available)
    if len(node_str) >= 3:
        prefix = node_str[:3]
        if prefix in module_positions:
            node_to_module[node] = prefix
        else:
            # If we can't determine the module, place in center
            node_to_module[node] = 'REP'  # Default to center
    else:
        node_to_module[node] = 'REP'  # Default to center

# Process each module separately to ensure strict separation
for module, module_center in module_positions.items():
    # Get all nodes for this module
    module_nodes_list = [n for n in G.nodes() if node_to_module.get(n) == module]
    
    # Skip if no nodes for this module
    if not module_nodes_list:
        continue
    
    # Calculate module radius based on node count (min 0.15, max 0.3)
    module_radius = min(0.3, max(0.15, 0.05 * np.sqrt(len(module_nodes_list))))
    
    # Find foundation nodes (no incoming edges) within this module
    module_foundation_nodes = [n for n in module_nodes_list if G.in_degree(n) == 0]
    
    # First position foundation nodes at the top of the module area
    foundation_count = len(module_foundation_nodes)
    for i, node in enumerate(module_foundation_nodes):
        # Arrange in a row at the top of the module
        if foundation_count > 1:
            angle = np.pi * (0.25 + (i / (foundation_count - 1) * 0.5))  # Top arc
        else:
            angle = np.pi * 0.5  # Top
        
        # Position using polar coordinates
        x = module_center[0] + module_radius * 0.8 * np.cos(angle)
        y = module_center[1] + module_radius * 0.8 * np.sin(angle)
        hierarchy_pos[node] = (x, y)
    
    # Then position all other nodes in this module in a grid
    remaining_nodes = [n for n in module_nodes_list if n not in module_foundation_nodes]
    
    # Position in a grid pattern
    grid_radius = module_radius * 0.6  # Slightly smaller to keep within bounds
    rows = max(1, int(np.sqrt(len(remaining_nodes))))
    cols = max(1, int(np.ceil(len(remaining_nodes) / rows)))
    
    for i, node in enumerate(remaining_nodes):
        row = i // cols
        col = i % cols
        
        # Convert grid to polar-like coordinates for more natural placement
        angle = np.pi * (0.75 + (col / max(1, cols - 1) * 0.5))  # Bottom arc
        radius_factor = (row + 1) / (rows + 1)  # 0 to 1 based on row
        
        # Position node
        x = module_center[0] + grid_radius * radius_factor * np.cos(angle)
        y = module_center[1] + grid_radius * radius_factor * np.sin(angle)
        hierarchy_pos[node] = (x, y)

# Draw the hierarchical graph with curved edges
nx.draw(G, hierarchy_pos, with_labels=True, node_color=node_colors, 
        node_size=900, font_size=8, font_weight='bold', 
        arrowsize=12, width=1.2, edge_color='gray', alpha=0.9,
        connectionstyle='arc3,rad=0.1')

# Add a background circle for each module to visually group them
for module, center in module_positions.items():
    # Get all nodes for this module using our mapping
    module_nodes_list = [n for n in G.nodes() if node_to_module.get(n) == module]
    
    if module_nodes_list:
        # Calculate radius based on node count
        radius = min(0.3, max(0.15, 0.05 * np.sqrt(len(module_nodes_list))))
        
        # Create a boundary ellipse
        circle = plt.Circle(center, radius, color=groups.get(module, 'gray'), alpha=0.2)
        plt.gca().add_patch(circle)
        
        # Add a label with counter
        plt.text(center[0], center[1] + radius + 0.02, f"{module} ({len(module_nodes_list)})", 
                fontsize=14, fontweight='bold', ha='center', va='center',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='black'))

# Add a legend
plt.legend(handles=legend_elements, title="Module Types", loc="upper right", fontsize=12)
plt.title("User Story Dependencies - Hierarchical View", fontsize=20)
plt.savefig('User_Story_Dependencies_Hierarchical.png', dpi=300, bbox_inches='tight')
print("Hierarchical dependency graph saved as User_Story_Dependencies_Hierarchical.png")

# 2. MODULE-LEVEL DEPENDENCY VISUALIZATION
plt.figure(figsize=(14, 10))

# Create a module graph with known module prefixes only
module_graph = nx.DiGraph()
for prefix in groups.keys():
    module_graph.add_node(prefix)

# Count dependencies between modules
module_edges = {}
for _, row in df_filtered.iterrows():
    source = str(row['Source Story'])
    target = str(row['Target Story'])
    
    # Get prefixes safely
    source_prefix = source[:3] if len(source) >= 3 else source
    target_prefix = target[:3] if len(target) >= 3 else target
    
    # Only count edges between known modules
    if source_prefix in groups and target_prefix in groups and source_prefix != target_prefix:
        edge = (source_prefix, target_prefix)
        module_edges[edge] = module_edges.get(edge, 0) + 1

# Add weighted edges to the module graph
for edge, weight in module_edges.items():
    module_graph.add_edge(edge[0], edge[1], weight=weight)

# Position nodes for the module graph
module_pos = nx.spring_layout(module_graph, k=0.5, iterations=100, seed=42)

# Create edge labels showing the number of dependencies
edge_labels = {(u, v): f"{d['weight']}" for u, v, d in module_graph.edges(data=True)}

# Draw the module graph (safe version for colors)
node_colors_module = [groups.get(node, DEFAULT_COLOR) for node in module_graph.nodes()]
nx.draw(module_graph, module_pos, with_labels=True, 
        node_color=node_colors_module,
        node_size=2000, font_size=12, font_weight='bold', 
        arrowsize=20, width=2, edge_color='gray')

# Add edge labels
nx.draw_networkx_edge_labels(module_graph, module_pos, edge_labels=edge_labels, font_size=10)

# Add legend
plt.legend(handles=legend_elements, title="Module Types", loc="upper right", fontsize=12)
plt.title("Module Dependencies Overview", fontsize=20)
plt.savefig('Module_Dependencies.png', dpi=300, bbox_inches='tight')
print("Module dependency graph saved as Module_Dependencies.png")

# 3. DEPENDENCY MATRIX VISUALIZATION
stories = sorted([str(node) for node in G.nodes()])

# Create a dependency matrix
n = len(stories)
adj_matrix = nx.to_numpy_array(G, nodelist=stories)

# Create a DataFrame for better visualization
matrix_df = pd.DataFrame(adj_matrix, index=stories, columns=stories)

# Group stories by module prefix
story_to_module = {}
for story in stories:
    story_str = str(story)
    prefix = story_str[:3] if len(story_str) >= 3 else story_str
    story_to_module[story] = prefix

module_ordering = {module: i for i, module in enumerate(groups.keys())}

# Create a sorting key function that sorts first by module then by story ID
def sort_key(story):
    story_str = str(story)
    
    # Default module is unknown
    module = "UNK"
    if len(story_str) >= 3:
        module = story_str[:3]
    
    # Try to extract a numeric ID
    try:
        if '-' in story_str:
            story_num = int(story_str.split('-')[1])
        else:
            story_num = 0
    except (IndexError, ValueError):
        story_num = 0  # Default value if parsing fails
        
    return (module_ordering.get(module, 999), story_num)

# Sort stories by module and number
sorted_stories = sorted(stories, key=sort_key)

# Reindex the DataFrame with sorted stories
sorted_matrix_df = matrix_df.reindex(index=sorted_stories, columns=sorted_stories)

# Create the heatmap
plt.figure(figsize=(20, 18))

# Create a mask for the upper triangle to show only dependencies in one direction
mask = np.zeros_like(sorted_matrix_df.values, dtype=bool)
mask[np.triu_indices_from(mask, k=1)] = True  # Use k=1 to include the diagonal

# Define a custom colormap
cmap = sns.color_palette("Blues_r", as_cmap=True)

# Create boundaries for module sections
module_boundaries = []
current_module = None
for i, story in enumerate(sorted_stories):
    story_str = str(story)
    module = story_str[:3] if len(story_str) >= 3 else story_str
    if module != current_module:
        module_boundaries.append(i)
        current_module = module

# Create the heatmap
ax = plt.gca()
sns.heatmap(sorted_matrix_df, cmap=cmap, square=True, linewidths=0.5, 
           cbar_kws={"shrink": 0.8}, ax=ax, mask=mask)

# Add grid lines to separate modules
for boundary in module_boundaries[1:]:
    plt.axhline(y=boundary, color='red', linestyle='-', alpha=0.7, linewidth=2)
    plt.axvline(x=boundary, color='red', linestyle='-', alpha=0.7, linewidth=2)

# Customize labels
plt.xticks(np.arange(len(sorted_stories)) + 0.5, sorted_stories, rotation=90, fontsize=8)
plt.yticks(np.arange(len(sorted_stories)) + 0.5, sorted_stories, fontsize=8)

plt.title("User Story Dependency Matrix", fontsize=20)
plt.savefig('Dependency_Matrix.png', dpi=300, bbox_inches='tight')
print("Dependency matrix saved as Dependency_Matrix.png")

# 4. CRITICAL PATH ANALYSIS
# Count how many stories depend on each story (in-degree)
in_degree = dict(G.in_degree())

# Get top 15 most depended-upon stories
critical_nodes = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:15]

# Create a bar chart for critical path analysis
plt.figure(figsize=(14, 8))

# Check if there are any critical nodes before trying to unpack
if critical_nodes:
    stories, counts = zip(*critical_nodes)
    
    # Create the bar chart
    bars = plt.bar(stories, counts)
    
    # Color bars by module
    for i, story in enumerate(stories):
        story_str = str(story)
        prefix = story_str[:3] if len(story_str) >= 3 else ""
        bars[i].set_color(groups.get(prefix, DEFAULT_COLOR))
    
    plt.xticks(rotation=45, ha='right')
    plt.title('Critical Path Analysis: Most Depended-Upon User Stories', fontsize=16)
    plt.xlabel('User Story')
    plt.ylabel('Number of Dependencies')
else:
    plt.text(0.5, 0.5, "No dependencies found", ha='center', va='center', fontsize=14)
    plt.title('Critical Path Analysis: No Data Available', fontsize=16)

plt.tight_layout()
plt.savefig('Critical_Path_Analysis.png', dpi=300, bbox_inches='tight')
print("Critical path analysis saved as Critical_Path_Analysis.png")

# 5. DEPENDENCY TYPE ANALYSIS
if not df_filtered.empty:
    dependency_types = df_filtered['Dependency Type'].value_counts()
    
    plt.figure(figsize=(12, 8))
    
    # Only create pie chart if there are dependency types
    if not dependency_types.empty:
        colors = sns.color_palette("Set3", len(dependency_types))
        ax = dependency_types.plot(kind='pie', autopct='%1.1f%%', startangle=90, 
                                  fontsize=12, colors=colors)
        
        plt.title('Distribution of Dependency Types', fontsize=16)
        plt.axis('equal')
    else:
        plt.text(0.5, 0.5, "No dependency types found", ha='center', va='center', fontsize=14)
        plt.title('Dependency Types: No Data Available', fontsize=16)
else:
    plt.figure(figsize=(12, 8))
    plt.text(0.5, 0.5, "No filtered dependencies found", ha='center', va='center', fontsize=14)
    plt.title('Dependency Types: No Data Available', fontsize=16)

plt.tight_layout()
plt.savefig('Dependency_Types.png', dpi=300, bbox_inches='tight')
print("Dependency type analysis saved as Dependency_Types.png")

# Create a summary text report
with open('Dependency_Analysis_Summary.md', 'w') as f:
    f.write("# User Story Dependency Analysis Summary\n\n")
    
    # List foundation stories
    foundation_stories = df[df['Target Story'] == 'NULL']['Source Story'].tolist()
    if foundation_stories:
        f.write("## Foundation Stories\n")
        for story in sorted(foundation_stories, key=sort_key):
            story_str = str(story)
            # Find the row for this story
            story_rows = df[df['Source Story'] == story]
            if not story_rows.empty:
                row = story_rows.iloc[0]
                f.write(f"- **{story_str}**: {row['Dependency Type']} - {row['Rationale']}\n")
    else:
        f.write("## Foundation Stories\n")
        f.write("No foundation stories found.\n")
    
    # List critical path stories
    if critical_nodes:
        f.write("\n## Critical Path (Most Depended-Upon Stories)\n")
        for story, count in critical_nodes:
            f.write(f"- **{str(story)}**: {count} dependent stories\n")
    else:
        f.write("\n## Critical Path\n")
        f.write("No critical path stories identified.\n")
    
    # Module connectivity analysis
    f.write("\n## Module Connectivity\n")
    for source_module in sorted(groups.keys()):
        f.write(f"\n### {source_module} Dependencies\n")
        outgoing = []
        for (src, tgt), weight in module_edges.items():
            if src == source_module:
                outgoing.append((tgt, weight))
        if outgoing:
            for target, weight in sorted(outgoing, key=lambda x: x[1], reverse=True):
                f.write(f"- **{target}**: {weight} dependencies\n")
        else:
            f.write("- No outgoing dependencies to other modules\n")

print("Dependency analysis summary saved as Dependency_Analysis_Summary.md")
