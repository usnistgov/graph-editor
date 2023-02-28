import streamlit as st
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config
from layout import footer
import json


def get_type1():
    store = TripleStore()
    # TO IMPLEMENT
    # for result in results["results"]["bindings"]:
    #     node1 = result["name_pe1_en"]["value"]
    #     link = result["rel_en"]["value"]
    #     node2 = result["name_pe2_en"]["value"]
    #     store.add_triple(node1, link, node2)
    return store


def app():
    footer()
    st.title("Graph Demo")
    st.sidebar.title("Welcome")
    # could add more stuff here later on or add other endpoints in the sidebar.
    query_type = st.sidebar.selectbox(
        "Query Type: ", ["Type1", "Type2"])
    config = Config(height=600, width=700, nodeHighlightBehavior=True, highlightColor="#F7A7A6", directed=True,
                    collapsible=True)

    if query_type == "Type1":
        st.subheader("Type1")
        with st.spinner("Loading data"):
            store = get_type1()
            st.write("Nodes loaded: " + str(len(store.getNodes())))
        st.success("Done")
        agraph(list(store.getNodes()), (store.getEdges()), config)

    if query_type == "Type2":
        with open("./graph.json", encoding="utf8") as f:
            graph_file = json.loads(f.read())
            graph_store = TripleStore()
            for sub_graph in graph_file["children"]:
                graph_store.add_triple(
                    graph_file["name"], "has_subgroup", sub_graph["name"])
                for node in sub_graph["children"]:
                    node1 = node["name"]
                    link = "belong_to"
                    node2 = sub_graph["name"]
                    graph_store.add_triple(node1, link, node2)
            agraph(list(graph_store.getNodes()),
                   (graph_store.getEdges()), config)


if __name__ == '__main__':
    app()
