import streamlit as st
from search import search

st.title("Semantic Log Search")

query = st.text_input("Search logs")

if query:
    results = search(query)

    if not results:
     st.warning("No relevant logs found. Try another query.")

    for res in results:
        st.markdown(
            f"**[{res['source']}]** {res['text']}  \n"
            f"Similarity: `{res['score']:.3f}`"
        )
    