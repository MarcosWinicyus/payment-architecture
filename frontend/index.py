import streamlit as st
from src.components.invetory import inventory
from src.components.orders import orders
st.set_page_config(layout="wide")

buff, center, buff2 = st.sidebar.columns([0.3, 2, 0.3])

with center.expander("Internal processes", expanded=True):

    page_selected = st.radio(
        "",
        ('Inventory', 'Orders List'))

with center.expander("Costumer page", expanded=True):

    page_selected = st.radio(
        "",
        ('Product Lidst', 'Sopphing Cart'))
        

if page_selected == 'Inventory':
    st.session_state["page"] = "inventory"
    st.session_state["formStatus"] = "new_product"

    if not "product_selected" in st.session_state:
        st.session_state["product_selected"] = {}

    if "layout" in st.session_state and st.session_state["layout"] == 'list_orders':
        st.session_state["layout"] = "new_product"
    
    inventory()

elif page_selected == 'Orders List':
    st.session_state["page"] = "orders"
    st.session_state["layout"] = 'list_orders'

    orders()
