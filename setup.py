import networkx as nx
import networkx.algorithms.community as community
import pandas as pd
import matplotlib.pyplot as plt
import unidecode as uni
import math

# Import graph data from excel

excel_file_path = "class_dependency_data.xlsx"

dataframe = pd.read_excel(excel_file_path, sheet_name="graph_data")
dataframe.columns = ["Classes", "Dependencies", "Demand", "Ano"]
dataframe = dataframe.drop_duplicates(subset="Classes")
dataframe["Dependencies"] = dataframe['Dependencies'].str.upper();
dataframe["Classes"] = dataframe['Classes'].str.upper();
dataframe["Classes"] = dataframe['Classes'].str.strip();

dataframe["Dependencies"] = dataframe['Dependencies'].str.replace('\n', ' ')
dataframe["Classes"] = dataframe['Classes'].str.replace('\n', ' ')

def remove_accents(text):
    return uni.unidecode(str(text))

dataframe['Dependencies'] = dataframe['Dependencies'].apply(remove_accents)
dataframe['Classes'] = dataframe['Classes'].apply(remove_accents)

edgelist_dataframe = dataframe.assign(
    Dependencies=dataframe["Dependencies"].str.split("; ")
).explode("Dependencies")

edgelist_dataframe = dataframe.assign(
    Dependencies=dataframe["Dependencies"].str.split(";")
).explode("Dependencies")

edgelist_dataframe.Dependencies = edgelist_dataframe.Dependencies.str.strip()
edgelist_dataframe.Classes = edgelist_dataframe.Classes.str.strip()

edgelist_dataframe = edgelist_dataframe.reset_index(drop=True)

Graph = nx.from_pandas_edgelist(
    edgelist_dataframe, source="Dependencies", target="Classes", create_using=nx.DiGraph
)

def filter_nan_node(node):
    return node.startswith("nan")

Graph.remove_nodes_from(list(nx.subgraph_view(Graph, filter_node=filter_nan_node).nodes))


demands_dict = dataframe.set_index('Classes')['Demand'].to_dict()

demands_dict_aux = demands_dict.copy()

for node_demand in demands_dict:
    if math.isnan(demands_dict[node_demand]):
        demands_dict_aux.pop(node_demand)
        # print(node_demand + ' ' + str(demands_dict[node_demand]))

demands_dict = demands_dict_aux;

nx.set_node_attributes(Graph, demands_dict, name="demand")

communities = community.louvain_communities(Graph, seed=123)

node_colors = {}
color_map = plt.cm.get_cmap('viridis', len(communities))
for i, community in enumerate(communities):
    for node in community:
        node_colors[node] = color_map(i)


# Graph view

# pos = nx.forceatlas2_layout(Graph, seed=30, gravity=30)
# pos = nx.spring_layout(Graph, seed=30, k=0.7, iterations=50)
# plt.figure(figsize=(18, 10))

# plt.axis('off')
# plt.box(False)

# nx.draw_networkx_nodes(Graph, pos, node_size=80, node_color=[node_colors[node] for node in Graph.nodes()])
# nx.draw_networkx_nodes(Graph, pos, node_size=80)
# nx.draw_networkx_edges(Graph, pos, alpha=0.2, arrows=True, arrowsize=8, arrowstyle='-|>')
# nx.draw_networkx_labels(Graph, pos, font_size=4)

# plt.title("Disciplinas BC&T")
# plt.show()

# plt.savefig('graph_plot_1.png', dpi=400)





# Print data

print('Quantidade de nós: ' + str(Graph.number_of_nodes()))
print('Quantidade de arestas: ' + str(Graph.number_of_edges()))

degrees = nx.degree(G=Graph)
sum_degrees = 0

for degree in degrees:
    sum_degrees += degree[1]

avarage_degree = sum_degrees / len(degrees)

print('Grau Médio: ' + str(round(avarage_degree, 2)))

out_degree_node_list = Graph.out_degree()
out_degree_node_list = sorted(out_degree_node_list, key=lambda node: node[1], reverse=True)

# print(out_degree_node_list)

avarage_clustering_coefficient = nx.average_clustering(Graph)

print('Coeficiente de clustering: ' + str(avarage_clustering_coefficient))

node_betwenness_list = nx.betweenness_centrality(Graph, normalized=False)
node_betwenness_list = sorted(node_betwenness_list.items(), key=lambda node: node[1], reverse=True)

# print(node_betwenness_list)

node_closeness_list = nx.closeness_centrality(Graph)
node_closeness_list = sorted(node_closeness_list.items(), key=lambda node: node[1], reverse=True)

# print(node_closeness_list)

# node_eigenvector_list = nx.eigenvector_centrality(Graph)
# node_eigenvector_list = sorted(node_eigenvector_list.items(), key=lambda node: node[1], reverse=True)

# print(node_eigenvector_list)

graph_density = nx.density(Graph)

print('Densidade: ' + str(graph_density))

# print(edgelist_dataframe.to_string())

# df = nx.to_pandas_edgelist(Graph)

# print(df.to_string())
# df.to_excel('graph_edgelist.xlsx', index=False)

# print(dataframe.to_string())

# print("\nNodes:")

# nodes = sorted(Graph.nodes())

# for node in nodes:
#     print(node)

# print("\nNode demands:")

# node_demands = dict(sorted(demands_dict.items(), key=lambda item: item[1], reverse=True))

# print(node_demands)

# Community demands

# community_demands = {}

# for community in communities:
#     demands_sum = 0

#     for node in community:
#         demands_sum += demands_dict[node]

#     community_demands[next(iter(community))] = demands_sum / len(community)

# print(community_demands)

# print(demands_dict)

# especific_community = {}

# for node in communities[9]:
#     especific_community[node] = demands_dict[node]

# print(especific_community)

# print(communities)