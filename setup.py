import networkx as nx
import pandas as pd

excel_file_path = "class_dependency_data.xlsx"

dataframe = pd.read_excel(excel_file_path, sheet_name="graph_data")
dataframe.columns = ["Classes", "Dependencies"]
dataframe = dataframe.drop_duplicates(subset="Classes")

edgelist_dataframe = dataframe.assign(
    Dependencies=dataframe["Dependencies"].str.split("; ")
).explode("Dependencies")

edgelist_dataframe = dataframe.assign(
    Dependencies=dataframe["Dependencies"].str.split(";")
).explode("Dependencies")

Graph = nx.from_pandas_edgelist(
    edgelist_dataframe, source="Dependencies", target="Classes", create_using=nx.DiGraph
)

for node, neighbors in Graph.adjacency():
    print(f"{node}: {list(neighbors)}")
