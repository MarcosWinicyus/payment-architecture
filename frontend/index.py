import streamlit as st
from src.components.invetory import inventory

st.set_page_config(layout="wide")


buff, center, buff2 = st.sidebar.columns([0.3,2,0.3])

page_selected = center.radio(
     "Select your page",
     ('Inventory', 'Orders'))


if page_selected == 'Inventory':
    st.session_state["page"] = "inventory"
    st.session_state["formStatus"] = "new_product"

if page_selected == 'Orders':
    st.session_state["page"] = "orders"


if st.session_state["page"] == "inventory":
    inventory()
elif st.session_state["page"] == "orders":
    ...
    

