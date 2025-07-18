import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import unidecode as uni

# Import graph data from excel

excel_file_path = "class_dependency_data.xlsx"

dataframe = pd.read_excel(excel_file_path, sheet_name="graph_data")
dataframe.columns = ["Classes", "Dependencies"]
dataframe = dataframe.drop_duplicates(subset="Classes")
dataframe = dataframe.dropna()
dataframe["Dependencies"] = dataframe['Dependencies'].str.upper();
dataframe["Classes"] = dataframe['Classes'].str.upper();

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
    edgelist_dataframe, source="Dependencies", target="Classes", create_using=nx.Graph
)






# Graph view

pos = nx.spring_layout(Graph, seed=30)
plt.figure(figsize=(18, 9))

nx.draw_networkx_nodes(Graph, pos, node_size=100, node_color='skyblue')
nx.draw_networkx_edges(Graph, pos, alpha=0.3)
nx.draw_networkx_labels(Graph, pos, font_size=6)

plt.title("Disciplinas BC&T")
plt.show()





# Print data

print('Quantidade de nós: ' + str(Graph.number_of_nodes()))
print('Quantidade de arestas: ' + str(Graph.number_of_edges()))

degrees = nx.degree(G=Graph)
sum_degrees = 0

for degree in degrees:
    sum_degrees += degree[1]

avarage_degree = sum_degrees / len(degrees)

print('Grau Médio: ' + str(round(avarage_degree, 2)))

# print(dataframe.to_string())

df = nx.to_pandas_edgelist(Graph)
df.to_excel('graph_edgelist.xlsx', index=False)
print(df)